Get Started
===========

本页基于仓库内各目录的 README 内容整理，帮助你快速理解硬件架构、接线方式、软件工具和开发流程。

Introduction
------------

- 开发板集成 2 个 STM32F4 模块，每个模块负责 2 路 CAN，总计 4 路 CAN / 4 路 RS485。
- 支持 USB 和 SPI 作为上位机控制输入，同时支持 IIC、ADC、串口等传感器扩展。
- 提供 5V/3.3V 供电输出，可为树莓派、Nvidia Jetson 等上位机供电。
- 兼容 MIT Cheetash SPINE 硬件设计标准。

.. image:: ../images/taobao-github-architect-1.1.png
   :alt: 开发板设计架构

Hardware
--------

USB 接入（PC/上位机）
^^^^^^^^^^^^^^^^^^^^

- USB 作为控制输入时，可直接在 PC 上使用调试软件完成电机通信验证。
- USB 支持 CAN 与 RS485 协议，适合快速调试与验证。

SPI 接入（Jetson/树莓派）
^^^^^^^^^^^^^^^^^^^^^^^^

- SPI 作为控制输入时，CS1 对应 STM32F4(1) 模块，CS2 对应 STM32F4(2) 模块。
- 可参考仓库根目录的接口图进行连线。

.. image:: ../images/taobao-github-architect-1.2-2.png
   :alt: 开发板接口图

Software
--------

调试工具建议如下：

- USB 转 CAN 调试：小米 CyberGear 调试软件（示例电机）。
- USB 转 RS485 调试：宇树电机调试软件（示例电机）。
- 通用电机调试：Sanpo Studio（https://sanporobot.com/sanpo-studio）。

工具包位于仓库 `tools/` 目录：

- `tools/CyberGear.zip`（配套说明 `tools/CyberGear.pdf`）
- `tools/UnitreeMotor.zip`
- `tools/UartAssist.zip`（串口调试）

Build Your Program
------------------

协议定义与样例代码位于 `demo/` 目录，建议按以下顺序阅读：

- USB 转 CAN：`demo/README.md#p1`
- USB 转 RS485：`demo/README.md#p2`
- SPI 转 CAN：`demo/README.md#p3`
- SPI 转 RS485：`demo/README.md#p4`

推荐的编程样例与测试工具：

- USB 转 CAN 测试脚本：`demo/test_usb2can.py`
- SPI 转 CAN 样例：`demo/spi_demo/cybergear`
- SPI 转 RS485 样例：`demo/spi_demo/unitree`
- USB 转 RS485 样例：`demo/usb_demo`

Advanced
--------

自定义固件与协议开发建议从原厂固件开始：

- 原厂固件（可二次开发）：`firmware/STM32CubeIDE`
- MIT Cheetash SPINE 固件（学习用途）：`firmware/mit_cheetash_spine`

固件更新要点（详见 `firmware/README.md`）：

- 使用 STLINK 连接板载 STM32F407 芯片的 SWD 接口。
- 使用 STM32CubeProgrammer 刷写最新固件。
- 两颗 STM32F407 需要分别刷写对应固件。
