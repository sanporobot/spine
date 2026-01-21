# SPI to RS485

## Protocol Overview

| Use Case | Wiring | TX Protocol (SPI->RS485) | RX Protocol (RS485->SPI) |
| --- | --- | --- | --- |
| RS485 motors (fixed 21-byte frames) | CS1 controls RS485-1/RS485-2; CS2 controls RS485-3/RS485-4 | Transparent, fixed length 21 bytes. Last two bytes reserved: last is CRC, second last is valid length. | Transparent, fixed length 21 bytes. Last two bytes reserved: last is CRC, second last is valid length. |

## Notes

- To avoid conflicts with CAN, headers `0x45 0x54` and `0x53 0x54` are reserved for CAN.
- The first two bytes of RS485 frames must not use those values.

## Example Code

Python example (Unitree GOM8010 motor): [spi_unitree_GO_M8010_6_demo.py](../../demo/spi_demo/unitree/spi_unitree_GO_M8010_6_demo.zip)
