import time
from typing import Optional, Tuple

import serial


HEADER_NORMAL = bytes([0x45, 0x54])
HEADER_ADVANCED = bytes([0x41, 0x54])
TAIL = bytes([0x0D, 0x0A])


def format_hex(data: bytes) -> str:
    if not data:
        return "0x"
    return "0x" + " ".join(f"{b:02X}" for b in data)


def format_hex_no_prefix(data: bytes) -> str:
    return " ".join(f"{b:02X}" for b in data)


def parse_hex_bytes(
    prompt: str, expected_len: Optional[int], default: Optional[bytes] = None
) -> bytes:
    while True:
        raw = input(prompt).strip()
        if not raw:
            if default is not None:
                return default
            if expected_len == 0:
                return b""

        tokens = [t for t in raw.replace(",", " ").split() if t]
        try:
            if len(tokens) == 1 and len(tokens[0]) > 2:
                token = tokens[0]
                if token.startswith(("0x", "0X")):
                    token = token[2:]
                if len(token) % 2 != 0:
                    raise ValueError("hex string length must be even")
                values = [int(token[i : i + 2], 16) for i in range(0, len(token), 2)]
            else:
                values = []
                for token in tokens:
                    if token.startswith(("0x", "0X")):
                        token = token[2:]
                    if len(token) == 0 or len(token) > 2:
                        raise ValueError("each byte must be 1-2 hex digits")
                    values.append(int(token, 16))

            if expected_len is not None and len(values) != expected_len:
                raise ValueError(f"expected {expected_len} bytes, got {len(values)}")
            return bytes(values)
        except ValueError as exc:
            print(f"Invalid hex input: {exc}")


def bytes_to_int_be(data: bytes) -> int:
    return int.from_bytes(data, byteorder="big", signed=False)


def parse_frame_identifier(frame_id: bytes) -> Tuple[int, bool, bool]:
    value = int.from_bytes(frame_id, byteorder="big", signed=False)
    is_extended = bool((value >> 2) & 0x1)
    is_remote = bool((value >> 1) & 0x1)
    if is_extended:
        can_id = (value >> 3) & 0x1FFFFFFF
    else:
        can_id = (value >> 21) & 0x7FF
    return can_id, is_extended, is_remote


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


def send_and_receive(
    payload: bytes, handshake: Optional[bytes], port: str, baudrate: int
) -> bytes:
    with serial.Serial(port, baudrate=baudrate, timeout=0.1) as ser:
        ser.reset_input_buffer()
        if handshake:
            ser.write(handshake)
            ser.flush()
            if not wait_for_ok(ser):
                print("Handshake failed: no OK received.")
                return b""
        ser.write(payload)
        ser.flush()
        response = read_response(ser)

    print(f"TX: {format_hex(payload)}")
    print(f"RX: {format_hex(response)}")
    return response


def parse_advanced_response(response: bytes) -> Optional[Tuple[bytes, int, bytes]]:
    header = HEADER_ADVANCED
    tail = TAIL
    start = response.find(header)
    if start == -1:
        return None
    end = response.find(tail, start + len(header))
    if end == -1:
        return None

    body = response[start + len(header) : end]
    if len(body) < 5:
        return None
    frame_id = body[:4]
    dlc = body[4]
    data = body[5 : 5 + dlc]
    if len(data) != dlc:
        return None
    return frame_id, dlc, data


def build_frame_identifier(can_id: int, is_extended: bool, is_remote: bool) -> bytes:
    if is_extended:
        if not 0 <= can_id <= 0x1FFFFFFF:
            raise ValueError("extended CAN ID must be 0..0x1FFFFFFF (29 bits)")
        value = (can_id << 3) | (1 << 2)
    else:
        if not 0 <= can_id <= 0x7FF:
            raise ValueError("standard CAN ID must be 0..0x7FF (11 bits)")
        value = (can_id & 0x7FF) << 21

    if is_remote:
        value |= 1 << 1

    return value.to_bytes(4, byteorder="big", signed=False)


def run_normal_mode(port: str, baudrate: int) -> None:
    print(
        "Normal mode format: "
        "header(0x45 0x54) + CANID(4 bytes) + data(8 bytes) + tail(0x0D 0x0A). "
        "AT+ET to switch to normal mode."
    )
    can_id_bytes = parse_hex_bytes(
        "CANID 4 bytes (default 00 00 FD 01, Enter to use): ",
        4,
        default=bytes([0x00, 0x00, 0xFD, 0x01]),
    )
    data_bytes = parse_hex_bytes(
        "Data 8 bytes (default 00 00 00 00 00 00 00 00, Enter to use): ",
        8,
        default=bytes([0x00] * 8),
    )
    payload = HEADER_NORMAL + can_id_bytes + data_bytes + TAIL
    send_and_receive(payload, handshake=b"AT+ET", port=port, baudrate=baudrate)


def run_advanced_mode(port: str, baudrate: int) -> None:
    print(
        "Advanced mode format: "
        "header(0x41 0x54) + frame_id(4 bytes) + dlc(1 byte) + "
        "data(0-8 bytes) + tail(0x0D 0x0A). "
        "AT+AT to switch to advanced mode."
    )
    frame_type = input("Frame type: [1] standard [2] extended :").strip()
    if frame_type == "1":
        can_id_bytes = parse_hex_bytes(
            "Standard CANID (default 01 42, Enter to use): ",
            2,
            default=bytes([0x01, 0x42]),
        )
        can_id = bytes_to_int_be(can_id_bytes)
        frame_id = build_frame_identifier(can_id, is_extended=False, is_remote=False)
    elif frame_type == "2":
        can_id_bytes = parse_hex_bytes(
            "Extended CANID (default 00 00 FD 01, Enter to use): ",
            4,
            default=bytes([0x00, 0x00, 0xFD, 0x01]),
        )
        can_id = bytes_to_int_be(can_id_bytes)
        frame_id = build_frame_identifier(can_id, is_extended=True, is_remote=False)
    elif frame_type == "3":
        can_id_bytes = parse_hex_bytes(
            "Remote CANID (e.g. 01 42): ",
            2,
            default=bytes([0x01, 0x42]),
        )
        can_id = bytes_to_int_be(can_id_bytes)
        frame_id = build_frame_identifier(can_id, is_extended=False, is_remote=True)
    else:
        raise ValueError("invalid frame type selection")

    dlc_input = input("Data length (1-8, default 8, Enter to use): ").strip()
    dlc = 8 if not dlc_input else int(dlc_input)
    if not 0 <= dlc <= 8:
        raise ValueError("data length must be 0..8")
    data_bytes = parse_hex_bytes(
        "Data Bytes(default 00 00 00 00 00 00 00 00, Enter to use): ",
        dlc,
        default=bytes([0x00] * 8),
    )
    payload = HEADER_ADVANCED + frame_id + bytes([dlc]) + data_bytes + TAIL
    response = send_and_receive(payload, handshake=b"AT+AT", port=port, baudrate=baudrate)
    parsed = parse_advanced_response(response)
    if not parsed:
        print("RX frame parse failed.")
        return
    rx_frame_id, rx_dlc, _ = parsed
    parsed_can_id, parsed_is_extended, parsed_is_remote = parse_frame_identifier(rx_frame_id)
    frame_kind = "extended" if parsed_is_extended else "standard"
    if parsed_is_remote:
        frame_kind += " remote"
    can_id_bytes = parsed_can_id.to_bytes(4, byteorder="big", signed=False)
    print(f"RX CANID: {format_hex_no_prefix(can_id_bytes)} [{frame_kind}]")


def main() -> None:
    port_input = input(
        "Serial port (default /dev/ttyACM0, Enter to use). "
        "Linux e.g. /dev/ttyACM0, Windows e.g. COM3: "
    ).strip()
    port = port_input or "/dev/ttyACM0"
    baud_input = input("Baudrate (default 1000000, Enter to use): ").strip()
    baudrate = 1000000 if not baud_input else int(baud_input)
    mode = input("Mode: [1] normal [2] advanced: ").strip()
    if mode == "1":
        run_normal_mode(port, baudrate)
    elif mode == "2":
        run_advanced_mode(port, baudrate)
    else:
        raise ValueError("invalid mode selection")


if __name__ == "__main__":
    main()
