# Firmware Update

## SANPO Official Firmware

Source: [STM32CubeIDE project](https://gitcode.com/sanpo/robot/tree/main/firmware/STM32CubeIDE)

1. Prepare an STLINK cable and connect the board STLINK interface to your PC.
2. The board has two STLINK interfaces for the two STM32F407 chips. Use the silkscreen labels to choose the correct one.
3. Install [STM32CubeProgrammer](../../tools/STM32CubeProgrammer_win64.zip).
4. Download the latest [official firmware](https://gitcode.com/sanpo/robot/tree/main/firmware/STM32CubeIDE/Release).
5. Flash the firmware with STM32CubeProgrammer (flash both chips separately).

![STM32 firmware update flow](../../images/update_firmware_stm32.png)

## MIT Cheetash SPINE Firmware

Source: [MBED STUDIO project](https://gitcode.com/sanpo/robot/tree/main/firmware/mit_cheetash_spine)

1. Install [MBED STUDIO](https://os.mbed.com/studio/).
2. Open mbed studio and import the MIT Cheetash SPINE project.
3. Connect STLINK and select Target->MCUs and custom targets->STM32F407VETx.
4. Build and flash the firmware.
