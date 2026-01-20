import argparse
import math
import threading
import time
from dataclasses import dataclass
from typing import Iterable, List, Sequence

import serial


HEADER_NORMAL_EXT = bytes([0x45, 0x54])
TAIL = bytes([0x0D, 0x0A])

P_MIN = -12.5
P_MAX = 12.5
T_MIN = -12.0
T_MAX = 12.0
V_MIN = -30.0
V_MAX = 30.0
KP_MIN = 0.0
KP_MAX = 500.0
KD_MIN = 0.0
KD_MAX = 5.0


def float_to_uint16(float_data: float, float_data_min: float, float_data_max: float) -> int:
    if float_data > float_data_max:
        float_data = float_data_max
    elif float_data < float_data_min:
        float_data = float_data_min
    return int((float_data - float_data_min) / (float_data_max - float_data_min) * 65535)


def build_extended_frame(arbitration_id: int, data: Sequence[int]) -> bytes:
    can_id_bytes = arbitration_id.to_bytes(4, byteorder="big", signed=False)
    payload = bytearray(HEADER_NORMAL_EXT)
    payload.extend(can_id_bytes)
    data_bytes = bytearray(data[:8])
    if len(data_bytes) < 8:
        data_bytes.extend([0x00] * (8 - len(data_bytes)))
    payload.extend(data_bytes)
    payload.extend(TAIL)
    return bytes(payload)


def read_response(ser: serial.Serial, total_timeout_s: float = 1.0) -> bytes:
    deadline = time.monotonic() + total_timeout_s
    last_data_time = time.monotonic()
    chunks = []
    while time.monotonic() < deadline:
        waiting = ser.in_waiting
        data = ser.read(waiting or 1)
        if data:
            chunks.append(data)
            last_data_time = time.monotonic()
        elif time.monotonic() - last_data_time > 0.2:
            break
    return b"".join(chunks)


def wait_for_ok(ser: serial.Serial, total_timeout_s: float = 2.0) -> bool:
    data = read_response(ser, total_timeout_s=total_timeout_s)
    return b"OK" in data


def enter_passthrough_mode(ser: serial.Serial) -> None:
    ser.reset_input_buffer()
    ser.write(b"AT+ET")
    ser.flush()
    if not wait_for_ok(ser):
        raise RuntimeError("Failed to enter passthrough mode (AT+ET no OK).")


def send_extended_frame(ser: serial.Serial, arbitration_id: int, data: Sequence[int]) -> None:
    payload = build_extended_frame(arbitration_id, data)
    ser.write(payload)
    ser.flush()


def set_motor_angle_zero(ser: serial.Serial, motor_id: int) -> None:
    arbitration_id = 0x0600FD00 + motor_id
    data = [0x01] + [0x00] * 7
    send_extended_frame(ser, arbitration_id, data)


def set_motion_mode(ser: serial.Serial, motor_id: int) -> None:
    arbitration_id = 0x1200FD00 + motor_id
    data = [0x05, 0x70] + [0x00] * 6
    send_extended_frame(ser, arbitration_id, data)


def set_motion_enable(ser: serial.Serial, motor_id: int) -> None:
    arbitration_id = 0x0300FD00 + motor_id
    data = [0x00] * 8
    send_extended_frame(ser, arbitration_id, data)


def set_motion_stop(ser: serial.Serial, motor_id: int) -> None:
    arbitration_id = 0x0400FD00 + motor_id
    data = [0x00] * 8
    send_extended_frame(ser, arbitration_id, data)


def motor_set_motion_parameter(
    ser: serial.Serial,
    motor_id: int,
    torque: float,
    radian: float,
    speed: float,
    kp: float,
    kd: float,
) -> None:
    data = [0 for _ in range(8)]
    torque_u16 = float_to_uint16(torque, P_MIN, P_MAX)
    arbitration_id = 0x01000000 | (torque_u16 << 8) | motor_id

    rad_u16 = float_to_uint16(radian, T_MIN, T_MAX)
    data[0] = rad_u16 >> 8
    data[1] = rad_u16 & 0xFF

    speed_u16 = float_to_uint16(speed, V_MIN, V_MAX)
    data[2] = speed_u16 >> 8
    data[3] = speed_u16 & 0xFF

    kp_u16 = float_to_uint16(kp, KP_MIN, KP_MAX)
    data[4] = kp_u16 >> 8
    data[5] = kp_u16 & 0xFF

    kd_u16 = float_to_uint16(kd, KD_MIN, KD_MAX)
    data[6] = kd_u16 >> 8
    data[7] = kd_u16 & 0xFF

    send_extended_frame(ser, arbitration_id, data)


@dataclass
class PortConfig:
    name: str
    motors: List[int]


def parse_motor_list(raw: str) -> List[int]:
    if not raw:
        return []
    return [int(item.strip()) for item in raw.split(",") if item.strip()]


def setup_motors(ser: serial.Serial, motors: Iterable[int], do_zero: bool) -> None:
    for motor_id in motors:
        if do_zero:
            set_motor_angle_zero(ser, motor_id)
            time.sleep(0.01)
        set_motion_mode(ser, motor_id)
        time.sleep(0.01)
        set_motion_enable(ser, motor_id)
        time.sleep(0.01)


def stop_motors(ser: serial.Serial, motors: Iterable[int]) -> None:
    for motor_id in motors:
        set_motion_stop(ser, motor_id)
        time.sleep(0.005)


def run_port_loop(
    ser: serial.Serial,
    motors: Sequence[int],
    rate_hz: float,
    amp: float,
    freq_hz: float,
    phase_offset: float,
    ramp_time: float,
    kp: float,
    kd: float,
    speed: float,
    stop_event: threading.Event,
) -> None:
    if rate_hz <= 0:
        raise ValueError("rate_hz must be > 0")
    period = 1.0 / rate_hz
    start_time = time.perf_counter()
    next_tick = start_time
    while not stop_event.is_set():
        now = time.perf_counter()
        if now < next_tick:
            time.sleep(next_tick - now)
        cycle_time = time.perf_counter()
        t = cycle_time - start_time
        if ramp_time > 0:
            amp_scale = min(1.0, t / ramp_time)
        else:
            amp_scale = 1.0
        for idx, motor_id in enumerate(motors):
            phase = phase_offset + idx * 0.2
            rad = (amp * amp_scale) * math.sin(2 * math.pi * freq_hz * t + phase)
            motor_set_motion_parameter(ser, motor_id, 0.0, rad, speed, kp, kd)
        next_tick += period


def run_port_loop_sine_delay(
    ser: serial.Serial,
    motors: Sequence[int],
    amp: float,
    freq_hz: float,
    phase_offset: float,
    per_motor_delay: float,
    ramp_time: float,
    kp: float,
    kd: float,
    speed: float,
    stop_event: threading.Event,
) -> None:
    if per_motor_delay < 0:
        raise ValueError("per_motor_delay must be >= 0")
    start_time = time.perf_counter()
    while not stop_event.is_set():
        t = time.perf_counter() - start_time
        if ramp_time > 0:
            amp_scale = min(1.0, t / ramp_time)
        else:
            amp_scale = 1.0
        for idx, motor_id in enumerate(motors):
            phase = phase_offset + idx * 0.2
            rad = (amp * amp_scale) * math.sin(2 * math.pi * freq_hz * t + phase)
            motor_set_motion_parameter(ser, motor_id, 0.0, rad, speed, kp, kd)
            if per_motor_delay > 0:
                time.sleep(per_motor_delay)


def run_port_loop_sweep(
    ser: serial.Serial,
    motors: Sequence[int],
    rate_hz: float,
    rad_max: float,
    rad_step: float,
    kp: float,
    kd: float,
    speed: float,
    stop_event: threading.Event,
) -> None:
    if rate_hz <= 0:
        raise ValueError("rate_hz must be > 0")
    if rad_step <= 0:
        raise ValueError("rad_step must be > 0")
    period = 1.0 / rate_hz
    rad_values = [0.0 for _ in motors]
    directions = [1 for _ in motors]
    next_tick = time.perf_counter()
    while not stop_event.is_set():
        now = time.perf_counter()
        if now < next_tick:
            time.sleep(next_tick - now)
        for idx, motor_id in enumerate(motors):
            if directions[idx] == 1 and rad_values[idx] < rad_max:
                rad_values[idx] += rad_step
                if rad_values[idx] >= rad_max:
                    directions[idx] = -1
            elif directions[idx] == -1 and rad_values[idx] > 0.0:
                rad_values[idx] -= rad_step
                if rad_values[idx] <= 0.0:
                    directions[idx] = 1
            motor_set_motion_parameter(
                ser, motor_id, 0.0, rad_values[idx], speed, kp, kd
            )
        next_tick += period


def run_port_loop_sweep_delay(
    ser: serial.Serial,
    motors: Sequence[int],
    rad_max: float,
    rad_step: float,
    per_motor_delay: float,
    kp: float,
    kd: float,
    speed: float,
    stop_event: threading.Event,
) -> None:
    if rad_step <= 0:
        raise ValueError("rad_step must be > 0")
    if per_motor_delay < 0:
        raise ValueError("per_motor_delay must be >= 0")
    rad_values = [0.0 for _ in motors]
    directions = [1 for _ in motors]
    while not stop_event.is_set():
        for idx, motor_id in enumerate(motors):
            if directions[idx] == 1 and rad_values[idx] < rad_max:
                rad_values[idx] += rad_step
                if rad_values[idx] >= rad_max:
                    directions[idx] = -1
            elif directions[idx] == -1 and rad_values[idx] > 0.0:
                rad_values[idx] -= rad_step
                if rad_values[idx] <= 0.0:
                    directions[idx] = 1
            motor_set_motion_parameter(
                ser, motor_id, 0.0, rad_values[idx], speed, kp, kd
            )
            if per_motor_delay > 0:
                time.sleep(per_motor_delay)


def run_port_loop_delay(
    ser: serial.Serial,
    motors: Sequence[int],
    rad_max: float,
    rad_step: float,
    per_motor_delay: float,
    kp: float,
    kd: float,
    speed: float,
    stop_event: threading.Event,
) -> None:
    if rad_step <= 0:
        raise ValueError("rad_step must be > 0")
    if per_motor_delay < 0:
        raise ValueError("per_motor_delay must be >= 0")
    rad_values = [0.0 for _ in motors]
    directions = [1 for _ in motors]
    while not stop_event.is_set():
        for idx, motor_id in enumerate(motors):
            if directions[idx] == 1 and rad_values[idx] < rad_max:
                rad_values[idx] += rad_step
                if rad_values[idx] >= rad_max:
                    directions[idx] = -1
            elif directions[idx] == -1 and rad_values[idx] > 0.0:
                rad_values[idx] -= rad_step
                if rad_values[idx] <= 0.0:
                    directions[idx] = 1
            motor_set_motion_parameter(
                ser, motor_id, 0.0, rad_values[idx], speed, kp, kd
            )
            if per_motor_delay > 0:
                time.sleep(per_motor_delay)


def open_serial(port: str, baudrate: int) -> serial.Serial:
    ser = serial.Serial(port, baudrate=baudrate, timeout=0.1)
    enter_passthrough_mode(ser)
    return ser


def main() -> None:
    parser = argparse.ArgumentParser(
        description="USB2CAN demo for 12 Xiaomi CyberGear motors (6 per port)."
    )
    parser.add_argument("--port1", required=True, help="Serial port for motors 1-6.")
    parser.add_argument("--port2", required=True, help="Serial port for motors 7-12.")
    parser.add_argument("--baudrate", type=int, default=1000000)
    parser.add_argument("--motors1", default="4,5,6,7,8,9")
    parser.add_argument("--motors2", default="4,5,6,7,8,9")
    parser.add_argument("--rate", type=float, default=60.0)
    parser.add_argument("--amp", type=float, default=0.5)
    parser.add_argument("--freq", type=float, default=0.1)
    parser.add_argument(
        "--mode",
        choices=["sine", "sweep", "sine_delay", "sweep_delay", "delay_mode"],
        default="sine",
        help=(
            "sine/sweep: fixed rate; sine_delay/sweep_delay: per-motor delay; "
            "delay_mode: per-motor delay with sweep."
        ),
    )
    parser.add_argument("--rad-max", type=float, default=0.5)
    parser.add_argument("--rad-step", type=float, default=0.01)
    parser.add_argument("--per-motor-delay", type=float, default=0.01)
    parser.add_argument("--ramp-time", type=float, default=0.0)
    parser.add_argument("--kp", type=float, default=10.0)
    parser.add_argument("--kd", type=float, default=0.5)
    parser.add_argument("--speed", type=float, default=0.0)
    parser.add_argument("--no-zero", action="store_true")
    args = parser.parse_args()

    motors1 = parse_motor_list(args.motors1)
    motors2 = parse_motor_list(args.motors2)
    if len(motors1) != 6 or len(motors2) != 6:
        raise ValueError("Each port must have exactly 6 motors.")

    ser1 = open_serial(args.port1, args.baudrate)
    ser2 = open_serial(args.port2, args.baudrate)

    try:
        setup_motors(ser1, motors1, do_zero=not args.no_zero)
        setup_motors(ser2, motors2, do_zero=not args.no_zero)

        stop_event = threading.Event()
        if args.mode == "sine":
            thread1 = threading.Thread(
                target=run_port_loop,
                args=(
                    ser1,
                    motors1,
                    args.rate,
                    args.amp,
                    args.freq,
                    0.0,
                    args.ramp_time,
                    args.kp,
                    args.kd,
                    args.speed,
                    stop_event,
                ),
                daemon=True,
            )
            thread2 = threading.Thread(
                target=run_port_loop,
                args=(
                    ser2,
                    motors2,
                    args.rate,
                    args.amp,
                    args.freq,
                    1.0,
                    args.ramp_time,
                    args.kp,
                    args.kd,
                    args.speed,
                    stop_event,
                ),
                daemon=True,
            )
        elif args.mode == "sweep":
            thread1 = threading.Thread(
                target=run_port_loop_sweep,
                args=(
                    ser1,
                    motors1,
                    args.rate,
                    args.rad_max,
                    args.rad_step,
                    args.kp,
                    args.kd,
                    args.speed,
                    stop_event,
                ),
                daemon=True,
            )
            thread2 = threading.Thread(
                target=run_port_loop_sweep,
                args=(
                    ser2,
                    motors2,
                    args.rate,
                    args.rad_max,
                    args.rad_step,
                    args.kp,
                    args.kd,
                    args.speed,
                    stop_event,
                ),
                daemon=True,
            )
        elif args.mode == "sine_delay":
            thread1 = threading.Thread(
                target=run_port_loop_sine_delay,
                args=(
                    ser1,
                    motors1,
                    args.amp,
                    args.freq,
                    0.0,
                    args.per_motor_delay,
                    args.ramp_time,
                    args.kp,
                    args.kd,
                    args.speed,
                    stop_event,
                ),
                daemon=True,
            )
            thread2 = threading.Thread(
                target=run_port_loop_sine_delay,
                args=(
                    ser2,
                    motors2,
                    args.amp,
                    args.freq,
                    1.0,
                    args.per_motor_delay,
                    args.ramp_time,
                    args.kp,
                    args.kd,
                    args.speed,
                    stop_event,
                ),
                daemon=True,
            )
        elif args.mode == "sweep_delay":
            thread1 = threading.Thread(
                target=run_port_loop_sweep_delay,
                args=(
                    ser1,
                    motors1,
                    args.rad_max,
                    args.rad_step,
                    args.per_motor_delay,
                    args.kp,
                    args.kd,
                    args.speed,
                    stop_event,
                ),
                daemon=True,
            )
            thread2 = threading.Thread(
                target=run_port_loop_sweep_delay,
                args=(
                    ser2,
                    motors2,
                    args.rad_max,
                    args.rad_step,
                    args.per_motor_delay,
                    args.kp,
                    args.kd,
                    args.speed,
                    stop_event,
                ),
                daemon=True,
            )
        else:
            thread1 = threading.Thread(
                target=run_port_loop_delay,
                args=(
                    ser1,
                    motors1,
                    args.rad_max,
                    args.rad_step,
                    args.per_motor_delay,
                    args.kp,
                    args.kd,
                    args.speed,
                    stop_event,
                ),
                daemon=True,
            )
            thread2 = threading.Thread(
                target=run_port_loop_delay,
                args=(
                    ser2,
                    motors2,
                    args.rad_max,
                    args.rad_step,
                    args.per_motor_delay,
                    args.kp,
                    args.kd,
                    args.speed,
                    stop_event,
                ),
                daemon=True,
            )
        thread1.start()
        thread2.start()

        print("Sending 60 Hz commands per motor. Press Ctrl+C to stop.")
        while thread1.is_alive() and thread2.is_alive():
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            stop_motors(ser1, motors1)
        finally:
            ser1.close()
        try:
            stop_motors(ser2, motors2)
        finally:
            ser2.close()


if __name__ == "__main__":
    main()
