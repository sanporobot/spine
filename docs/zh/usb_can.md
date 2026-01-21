# USB 转 CAN

## 协议说明

| 模式 | 模式切换 | 适用场景 | USB 发送协议（USB->CAN） | USB 接收协议（CAN->USB） |
| --- | --- | --- | --- | --- |
| 透传模式（CAN 扩展帧） | AT+ET | 使用 CAN 扩展帧 | 固定帧头 2 字节（0x45 0x54）+ CANID 扩展帧 4 字节 + 数据帧 8 字节 + 固定帧尾 2 字节（0x0D 0x0A） | 固定帧头 2 字节（0x45 0x54）+ CANID 扩展帧 4 字节 + 数据帧 8 字节 + 固定帧尾 2 字节（0x0D 0x0A） |
| 透传模式（CAN 标准帧，固件 V4.1+） | AT+ET | 使用 CAN 标准帧 | 固定帧头 2 字节（0x53 0x54）+ 固定 2 字节（0x00 0x00）+ CANID 标准帧 2 字节 + 数据帧 8 字节 + 固定帧尾 2 字节（0x0D 0x0A） | 固定帧头 2 字节（0x53 0x54）+ 固定 2 字节（0x00 0x00）+ CANID 标准帧 2 字节 + 数据帧 8 字节 + 固定帧尾 2 字节（0x0D 0x0A） |
| 高级模式 | AT+AT | 同时支持 CAN 标准帧、扩展帧，支持可变数据长度 | 固定帧头 2 字节（0x41 0x54）+ 帧标识符 4 字节 + 帧数据长度 1 字节 + 帧数据最大 8 字节 + 固定帧尾 2 字节（0x0D 0x0A） | 固定帧头 2 字节（0x41 0x54）+ 帧标识符 4 字节 + 帧数据长度 1 字节 + 帧数据最大 8 字节 + 固定帧尾 2 字节（0x0D 0x0A） |

- 查询固件版本：发送 `AT+VER`。
- 开发板每次上电后默认切换为透传模式。
- 手动切换透传模式：发送 `AT+ET`。
- 手动切换高级模式：发送 `AT+AT`。

## 示例代码

Python 样例代码，下载地址：[test_usb2can.py](../../demo/test_usb2can.py)

## 高级模式样例

发送数据前请先发送 `AT+AT` 切换到高级模式。

| 固定帧头（2 字节） | 帧标识符（4 字节） | 帧数据长度（1 字节） | 帧数据（最大 8 字节） | 固定帧尾部（2 字节） |
| --- | --- | --- | --- | --- |
| 0x41 0x54 | 0x00 0x00 0x00 0x00 | 0x08 | 0x48 0x45 0x4C 0x4F 0x01 0x02 0x03 0x04 | 0x0D 0x0A |

帧标识符总共 4 字节（32 位），位段如下：

| Bit31-Bit21 | Bit20-Bit3 | Bit2 | Bit1 | Bit0 |
| --- | --- | --- | --- | --- |
| CAN 标准帧 ID 或扩展帧 ID 前 11 位 | CAN 扩展帧 ID 后 18 位 | 1=扩展帧，0=标准帧 | 1=远程帧，0=数据帧 | 固定为 0 |

```python
# USB 转 CAN 测试工具使用方法
pip3 install pyserial
python3 test_usb2can.py
```

```python
# CAN 标准帧 代码样例
# 先发送 AT+AT 切换到高级模式
std_can_id = 0x142
rtr_bit = 0
frame_id_val = (std_can_id << 21) | (rtr_bit << 1) | (0 << 2)
frame_id_bytes = frame_id_val.to_bytes(4, "big")
dlc = 8
data_bytes = bytes([0x9C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
payload = b"\x41\x54" + frame_id_bytes + bytes([dlc]) + data_bytes[:dlc] + b"\x0D\x0A"

# 接收解析（标准帧）
frame_id_val = int.from_bytes(frame_id_bytes, "big")
ide_bit = (frame_id_val >> 2) & 0x01
rtr_bit = (frame_id_val >> 1) & 0x01
std_can_id = (frame_id_val >> 21) & 0x7FF

# CAN 扩展帧 代码样例
ext_can_id = 0x0000FD01
rtr_bit = 0
frame_id_val = (ext_can_id << 3) | (rtr_bit << 1) | (1 << 2)
frame_id_bytes = frame_id_val.to_bytes(4, "big")
dlc = 8
data_bytes = bytes([0x00] * 8)
payload = b"\x41\x54" + frame_id_bytes + bytes([dlc]) + data_bytes[:dlc] + b"\x0D\x0A"

# 接收解析（扩展帧）
frame_id_val = int.from_bytes(frame_id_bytes, "big")
ide_bit = (frame_id_val >> 2) & 0x01
rtr_bit = (frame_id_val >> 1) & 0x01
ext_can_id = (frame_id_val >> 3) & 0x1FFFFFFF
```
