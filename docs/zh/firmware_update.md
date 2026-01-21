# 固件更新

## SANPO 原厂固件

源码地址：[STM32CubeIDE 项目工程](https://gitcode.com/sanpo/robot/tree/main/firmware/STM32CubeIDE)

1. 准备 STLINK 连接线，连接板载 STM32 芯片 STLINK 接口到 PC。
2. 板载有两个 STLINK 接口，分别对应两颗 STM32F407 芯片，请按丝印选择对应接口。
3. 安装 [STM32CubeProgrammer 工具](../../tools/STM32CubeProgrammer_win64.zip)。
4. 下载最新[原厂固件](https://gitcode.com/sanpo/robot/tree/main/firmware/STM32CubeIDE/Release)。
5. 用 STM32CubeProgrammer 将固件刷入开发板（两颗芯片需分别刷写）。

![STM32 固件更新流程](../../images/update_firmware_stm32.png)

## MIT Cheetash SPINE 固件

源码地址：[MBED STUDIO 项目工程](https://gitcode.com/sanpo/robot/tree/main/firmware/mit_cheetash_spine)

1. 安装 [MBED STUDIO](https://os.mbed.com/studio/)。
2. 打开 mbed studio，导入 MIT Cheetash SPINE 源代码。
3. 连接 STLINK，选择 Target->MCUs and custom targets->STM32F407VETx。
4. 构建并刷写固件。
