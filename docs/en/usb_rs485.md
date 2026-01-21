# USB to RS485

## Protocol Overview

| Use Case | TX Protocol | RX Protocol |
| --- | --- | --- |
| RS485 motors (e.g., Unitree, up to 64-byte frames) | Transparent | Transparent |

- To avoid conflicts with CAN, headers `0x45 0x54`, `0x41 0x54`, and `0x53 0x54` are reserved for CAN.
- The first two bytes of RS485 frames must not use those values.

## Example Code

Download: Coming Soon
