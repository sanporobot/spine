# SPI to CAN

## Protocol Overview

| Use Case | Wiring | TX Protocol (SPI->CAN) | RX Protocol (CAN->SPI) |
| --- | --- | --- | --- |
| CAN extended frame motors | CS1 controls CAN1/CAN2; CS2 controls CAN3/CAN4 | Header 2 bytes (0x45 0x54) + CANID ext 4 bytes + data 8 bytes + tail 2 bytes (0x0D 0x0A) + reserved 4 bytes (0x00 0x00 0x00 0x10) + CRC 1 byte | Header 2 bytes (0x45 0x54) + CANID ext 4 bytes + data 8 bytes + tail 2 bytes (0x0D 0x0A) + reserved 4 bytes (0x00 0x00 0x00 0x10) + CRC 1 byte |
| CAN standard frame motors (firmware V4.1+) | CS1 controls CAN1/CAN2; CS2 controls CAN3/CAN4 | Header 2 bytes (0x53 0x54) + fixed 2 bytes (0x00 0x00) + CANID std 2 bytes + data 8 bytes + tail 2 bytes (0x0D 0x0A) + reserved 4 bytes (0x00 0x00 0x00 0x10) + CRC 1 byte | Header 2 bytes (0x53 0x54) + fixed 2 bytes (0x00 0x00) + CANID std 2 bytes + data 8 bytes + tail 2 bytes (0x0D 0x0A) + reserved 4 bytes (0x00 0x00 0x00 0x10) + CRC 1 byte |

## Example Code

Python example (Xiaomi motor): [spi_cybergear_demo.py](../../demo/spi_demo/cybergear/spi_cybergear_demo.py)
