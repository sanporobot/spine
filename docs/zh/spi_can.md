# SPI 转 CAN

## 协议说明

| 适用场景 | 接线规则 | 发送协议（SPI->CAN） | 接收协议（CAN->SPI） |
| --- | --- | --- | --- |
| CAN 协议扩展帧电机 | CS1 片选通道控制 CAN1、CAN2；CS2 片选通道控制 CAN3、CAN4 | 固定帧头 2 字节（0x45 0x54）+ CANID 扩展帧 4 字节 + CAN 数据帧 8 字节 + 固定帧尾 2 字节（0x0D 0x0A）+ 预留 4 字节（0x00 0x00 0x00 0x10）+ CRC 1 字节 | 固定帧头 2 字节（0x45 0x54）+ CANID 扩展帧 4 字节 + 数据帧 8 字节 + 固定帧尾 2 字节（0x0D 0x0A）+ 预留 4 字节（0x00 0x00 0x00 0x10）+ CRC 1 字节 |
| CAN 协议标准帧电机（固件 V4.1+） | CS1 片选通道控制 CAN1、CAN2；CS2 片选通道控制 CAN3、CAN4 | 固定帧头 2 字节（0x53 0x54）+ 固定 2 字节（0x00 0x00）+ CANID 标准帧 2 字节 + CAN 数据帧 8 字节 + 固定帧尾 2 字节（0x0D 0x0A）+ 预留 4 字节（0x00 0x00 0x00 0x10）+ CRC 1 字节 | 固定帧头 2 字节（0x53 0x54）+ 固定 2 字节（0x00 0x00）+ CANID 标准帧 2 字节 + 数据帧 8 字节 + 固定帧尾 2 字节（0x0D 0x0A）+ 预留 4 字节（0x00 0x00 0x00 0x10）+ CRC 1 字节 |

## 示例代码

Python 样例程序（小米电机）：[spi_cybergear_demo.py](../../demo/spi_demo/cybergear/spi_cybergear_demo.py)
