# Get Started

The SANPO integrated robot controller is designed for robots, robot dogs, and robotic arms. It integrates USB and SPI data inputs, CAN/RS485 motor interfaces, and sensor interfaces.

## Introduction

- The board integrates 2 STM32F4 modules. Each module controls 2 CAN and 2 RS485 channels, for a total of 4 CAN / 4 RS485.
- USB and SPI are supported as host control inputs, alongside IIC, ADC, and UART sensor expansion.
- 5V/3.3V power outputs are provided for Raspberry Pi, Nvidia Jetson, and similar hosts.
- Compatible with the MIT Cheetash SPINE hardware design standard.

![Board architecture](../../images/taobao-github-architect-1.1.png)

## Hardware

### USB connection (PC/host)

- With USB as the control input, you can verify motor communication using debugging tools on a PC.
- USB supports both CAN and RS485, suitable for quick validation.

### SPI connection (Jetson/Raspberry Pi)

- For SPI control, CS1 maps to STM32F4(1) and CS2 maps to STM32F4(2).
- Refer to the board interface diagram for wiring.

![Board interface diagram](../../images/taobao-github-architect-1.2-2.png)

## Software

Recommended tools:

- Xiaomi motor tool (USB to CAN): [Xiaomi CyberGear Tool](../../tools/CyberGear.zip). Note: avoid Chinese characters in the install path.
- Unitree motor tool (USB to RS485): [Unitree GOM8010 Tool](../../tools/UnitreeMotor.zip)
- SANPO motor tool (multiple motor types): <a href="https://sanporobot.com/sanpo-studio" target="_blank" rel="noopener">Sanpo Studio Motor Tools</a>

## Build Your Program

Protocol definitions and examples:

- [USB to CAN](usb_can)
- [USB to RS485](usb_rs485)
- [SPI to CAN](spi_can)
- [SPI to RS485](spi_rs485)

## Advanced

For custom firmware and protocol development, start from the official firmware:

- Official firmware (for customization): [STM32CubeIDE project](https://gitcode.com/sanpo/robot/tree/main/firmware/STM32CubeIDE)
- MIT Cheetash SPINE firmware (for study): [MBED STUDIO project](https://gitcode.com/sanpo/robot/tree/main/firmware/mit_cheetash_spine)

For firmware updates, see [Firmware Update](firmware_update):

- Connect STLINK to the SWD interface of each STM32F407.
- Flash the latest firmware using STM32CubeProgrammer.
- Each STM32F407 must be flashed separately.
