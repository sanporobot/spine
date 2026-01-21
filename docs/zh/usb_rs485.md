# USB 转 RS485

## 协议说明

| 适用场景 | 发送协议 | 接收协议 |
| --- | --- | --- |
| RS485 协议电机（例如宇树，支持 64 字节报文长度） | 透传 | 透传 |

## 说明

- 为了区分 CAN 协议，帧头 `0x45 0x54`、`0x41 0x54`、`0x53 0x54` 预留给 CAN 协议。
- RS485 协议的前两个字节不可以使用上述值，其他字节没有限制。

## 示例代码

下载地址：[demo/usb_demo](../../demo/usb_demo)

## 宇树电机官方调试软件

- 下载地址：[tools/UnitreeMotor.zip](../../tools/UnitreeMotor.zip)
- 使用说明：https://support.unitree.com/home/zh/Motor_SDK_Dev_Guide/Motor_debugging_assistant
