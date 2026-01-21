# USB to CAN

## Protocol Overview

| Mode | Switch | Use Case | USB TX (USB->CAN) | USB RX (CAN->USB) |
| --- | --- | --- | --- | --- |
| Transparent (CAN extended frame) | AT+ET | CAN extended frames | Header 2 bytes (0x45 0x54) + CANID ext 4 bytes + data 8 bytes + tail 2 bytes (0x0D 0x0A) | Header 2 bytes (0x45 0x54) + CANID ext 4 bytes + data 8 bytes + tail 2 bytes (0x0D 0x0A) |
| Transparent (CAN standard frame, firmware V4.1+) | AT+ET | CAN standard frames | Header 2 bytes (0x53 0x54) + fixed 2 bytes (0x00 0x00) + CANID std 2 bytes + data 8 bytes + tail 2 bytes (0x0D 0x0A) | Header 2 bytes (0x53 0x54) + fixed 2 bytes (0x00 0x00) + CANID std 2 bytes + data 8 bytes + tail 2 bytes (0x0D 0x0A) |
| Advanced mode | AT+AT | Standard + extended, variable payload length | Header 2 bytes (0x41 0x54) + frame ID 4 bytes + DLC 1 byte + data up to 8 bytes + tail 2 bytes (0x0D 0x0A) | Header 2 bytes (0x41 0x54) + frame ID 4 bytes + DLC 1 byte + data up to 8 bytes + tail 2 bytes (0x0D 0x0A) |

- Query firmware version: `AT+VER`.
- Default mode after power-on is transparent mode.
- Switch to transparent mode: `AT+ET`.
- Switch to advanced mode: `AT+AT`.

## Example Code

Python example: [test_usb2can.py](../../demo/test_usb2can.py)

## Advanced Mode Example

Send `AT+AT` before transmitting data.

| Header (2 bytes) | Frame ID (4 bytes) | DLC (1 byte) | Data (max 8 bytes) | Tail (2 bytes) |
| --- | --- | --- | --- | --- |
| 0x41 0x54 | 0x00 0x00 0x00 0x00 | 0x08 | 0x48 0x45 0x4C 0x4F 0x01 0x02 0x03 0x04 | 0x0D 0x0A |

Frame ID is 4 bytes (32-bit):

| Bit31-Bit21 | Bit20-Bit3 | Bit2 | Bit1 | Bit0 |
| --- | --- | --- | --- | --- |
| Standard CAN ID or first 11 bits of extended ID | Last 18 bits of extended ID | 1=extended, 0=standard | 1=remote, 0=data | Fixed 0 |

```python
# USB to CAN test tool
pip3 install pyserial
python3 test_usb2can.py
```

```python
# CAN standard frame example
# Send AT+AT first
std_can_id = 0x142
rtr_bit = 0
frame_id_val = (std_can_id << 21) | (rtr_bit << 1) | (0 << 2)
frame_id_bytes = frame_id_val.to_bytes(4, "big")
dlc = 8
data_bytes = bytes([0x9C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
payload = b"\x41\x54" + frame_id_bytes + bytes([dlc]) + data_bytes[:dlc] + b"\x0D\x0A"

# Parse return (standard frame)
frame_id_val = int.from_bytes(frame_id_bytes, "big")
ide_bit = (frame_id_val >> 2) & 0x01
rtr_bit = (frame_id_val >> 1) & 0x01
std_can_id = (frame_id_val >> 21) & 0x7FF

# CAN extended frame example
ext_can_id = 0x0000FD01
rtr_bit = 0
frame_id_val = (ext_can_id << 3) | (rtr_bit << 1) | (1 << 2)
frame_id_bytes = frame_id_val.to_bytes(4, "big")
dlc = 8
data_bytes = bytes([0x00] * 8)
payload = b"\x41\x54" + frame_id_bytes + bytes([dlc]) + data_bytes[:dlc] + b"\x0D\x0A"

# Parse return (extended frame)
frame_id_val = int.from_bytes(frame_id_bytes, "big")
ide_bit = (frame_id_val >> 2) & 0x01
rtr_bit = (frame_id_val >> 1) & 0x01
ext_can_id = (frame_id_val >> 3) & 0x1FFFFFFF
```
