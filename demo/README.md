# SANPO兴普智能 - 机器人集成开发板

## 通信协议说明 
- **[USB转CAN](#p1)**
- **[USB转RS485](#p2)**
- **[SPI转CAN](#p3)**
- **[SPI转RS485](#p4)**

## <span id="p1">USB转CAN</span>
|  模式   | 模式切换 |适用场景 | USB发送协议(USB->CAN) | USB接收协议(CAN->USB) |
| ---------- | --------- | --------- | --------- | --------- |
| 普通模式 | AT+ET |<div style="width: 150pt">使用CAN扩展帧</div> | <div style="width: 150pt">固定帧头2个字节(0x45 0x54) + CANID扩展帧4个字节 + 数据帧8个字节 + 固定帧尾2个字节(0x0D 0x0A)</div> | <div style="width: 150pt">固定帧头2个字节(0x45 0x54) + CANID扩展帧4个字节 + 数据帧8个字节 + 固定帧尾2个字节(0x0D 0x0A)</div> |
| 高级模式 | AT+AT | <div style="width: 150pt">使用CAN标准帧和扩展帧<br>使用小米电机原厂调试软件</div> | <div style="width: 150pt">固定帧头2个字节(0x41 0x54) + 帧标识符4个字节 + 帧数据长度1个字节 + 帧数据最大8个字节 + 固定帧尾2个字节(0x0D 0x0A)</div> | <div style="width: 150pt">固定帧头2个字节(0x41 0x54) + 帧标识符4个字节 + 帧数据长度1个字节 + 帧数据最大8个字节 + 固定帧尾2个字节(0x0D 0x0A)</div> |

### 说明
- 开发板上电后，默认切换为普通模式
- 启动小米电机调试软件，系统会自动进入高级模式，无需手动切换
- 手动切换普通模式，发送 AT+ET 串口指令
- 手动切换高级模式，发送 AT+AT 串口指令
- 在集成开发前，可以使用我们的[测试工具 test_usb2can](https://gitcode.com/sanpo/robot/blob/main/demo/test_usb2can.py)进行包括普通模式和高级模式的数据发送和接收测试

### 高级模式示例
发送数据前请先发送 AT+AT 切换到高级模式。
| 固定帧头(2字节) | 帧标识符(4字节) | 帧数据长度(1字节) | 帧数据(最大8字节) | 固定帧尾部(2字节) |  
| --------- | --------- | --------- | --------- | --------- |
| 0x41 0x54 | 0x00 0x00 0x00 0x00 | 0x08 | 0x48 0x45 0x4C 0x4F 0x01 0x02 0x03 0x04 | 0x0D 0x0A |

其中帧标识符总共4字节，也就是32位。下表表示帧标识符位的分段。
| Bit31-Bit21 | Bit20-Bit3 | Bit2 | Bit1 | Bit0 |  
| --------- | --------- | --------- | --------- | --------- |
| CAN标准帧ID<br>或者CAN扩展帧ID前11位 | CAN扩展帧ID后18位 | 1表示帧类型为扩展帧，0表示帧类型为标准帧 | 1表示远程帧，0表示数据帧 | 固定为0 |

高级模式样例程序请参考[测试工具 test_usb2can](https://gitcode.com/sanpo/robot/blob/main/demo/test_usb2can.py)

```
# CAN 标准帧 代码样例
# 先发送 AT+AT 切换到高级模式
# ======== 发送数据封装（标准帧）========
# 标准帧使用 11 位 CANID，IDE=0，RTR=0/1
std_can_id = 0x142  # 11-bit 标准帧 CANID, 需要替换为实际的CANID
rtr_bit = 0         # 0=数据帧，1=远程帧
# 标准帧帧标识符：Bit31-Bit21 放 CANID，Bit2=IDE，Bit1=RTR
frame_id_val = (std_can_id << 21) | (rtr_bit << 1) | (0 << 2)
frame_id_bytes = frame_id_val.to_bytes(4, "big")  # 4字节大端序
dlc = 8  # 数据长度 0~8
# 高级模式完整帧：帧头(0x41 0x54) + 标识符 + DLC + 数据 + 帧尾(0x0D 0x0A)
payload = b"\x41\x54" + frame_id_bytes + bytes([dlc]) + data_bytes[:dlc] + b"\x0D\x0A"

# ======== 接收数据的解析（标准帧）========
# 从返回帧中取到的标识符 4 字节，解析出 IDE/RTR 和标准帧 CANID
frame_id_val = int.from_bytes(frame_id_bytes, "big")
ide_bit = (frame_id_val >> 2) & 0x01
rtr_bit = (frame_id_val >> 1) & 0x01
std_can_id = (frame_id_val >> 21) & 0x7FF  # 11位标准帧ID


# CAN 扩展帧 代码样例
# 先发送 AT+AT 切换到高级模式
# ======== 发送封装（扩展帧）========
# 扩展帧使用 29 位 CANID，IDE=1，RTR=0/1
ext_can_id = 0x0000FD01  # 29-bit 扩展帧 CANID, 需要替换为实际的CANID
rtr_bit = 0              # 0=数据帧，1=远程帧
# 扩展帧帧标识符：CANID 左移 3 位，Bit2=IDE，Bit1=RTR
frame_id_val = (ext_can_id << 3) | (rtr_bit << 1) | (1 << 2)
frame_id_bytes = frame_id_val.to_bytes(4, "big")  # 4字节大端序
dlc = 8  # 数据长度 0~8
# 高级模式完整帧：帧头(0x41 0x54) + 标识符 + DLC + 数据 + 帧尾(0x0D 0x0A)
payload = b"\x41\x54" + frame_id_bytes + bytes([dlc]) + data_bytes[:dlc] + b"\x0D\x0A"

# ======== 接收解析（扩展帧）========
# 从返回帧中取到的标识符 4 字节，解析出 IDE/RTR 和扩展帧 CANID
frame_id_val = int.from_bytes(frame_id_bytes, "big")
ide_bit = (frame_id_val >> 2) & 0x01
rtr_bit = (frame_id_val >> 1) & 0x01
ext_can_id = (frame_id_val >> 3) & 0x1FFFFFFF  # 29位扩展帧ID

```

### 小米CyberGear电机官方调试软件  
**[下载地址](https://gitcode.com/sanpo/robot/blob/main/tools/CyberGear.zip)**  
注意：保存路径中不能有中文，否则软件无法启动  

## <span id="p2">USB串口转RS485</span>
|  适用场景 | 发送协议 | 接收协议 |
| --------- | --------- | --------- |
| <div style="width: 150pt">RS485协议电机，例如宇树<br>使用宇树电机原厂调试软件</div> | <div style="width: 150pt">透传<br></div> | <div style="width: 150pt">透传<br></div> |

### 说明
- 为了区分CAN协议，帧头0x45 0x54和0x41 0x54预留给CAN协议，RS485协议的前两个字节不可以使用0x45 0x54或者0x41 0x54，其他字节没有限制

### 示例代码
**[下载地址](https://gitcode.com/sanpo/robot/blob/main/demo/usb_demo)**

### 宇树电机官方调试软件  
**[下载地址](https://gitcode.com/sanpo/robot/blob/main/tools/UnitreeMotor.zip)**  
**[使用说明](https://support.unitree.com/home/zh/Motor_SDK_Dev_Guide/Motor_debugging_assistant)**  

## <span id="p3">SPI转CAN</span>
| 适用场景 |  接线规则 | 发送协议(SPI->CAN) | 接收协议(CAN->SPI) |
| --------- | --------- | --------- | --------- |
| 小米等CAN协议电机 | CS1片选通道控制CAN1,CAN2<br>CS2片选通道控制CAN3,CAN4 | <div style="width: 150pt">固定帧头2个字节(0x45 0x54) + CANID扩展帧 4个字节 + CAN数据帧8个字节 + 固定帧尾2个字节(0x0D 0x0A) + 预留4个字节(0x00 0x00 0x00 0x10) + CRC1个字节</div> | <div style="width: 150pt">固定帧头2个字节(0x45 0x54) + CANID扩展帧 4个字节 + 数据帧8个字节 + 固定帧尾2个字节(0x0D 0x0A) + 预留4个字节(0x00 0x00 0x00 0x10) + CRC1个字节</div> |
### 示例代码
**[下载地址](https://gitcode.com/sanpo/robot/blob/main/demo/spi_demo/cybergear)**

## <span id="p4">SPI转RS485</span>
| 适用场景 |  接线规则 | 发送协议(SPI->CAN) | 接收协议(CAN->SPI) |
| --------- | --------- | --------- | --------- |
| 宇树等RS485协议电机 | CS1片选通道控制RS485-1,RS485-2<br>CS2片选通道控制RS485-3,RS485-4 | <div style="width: 150pt">透传<br>固定长度21个字节，预留最后两个字节，最后一个字节为CRC的值，倒数第二个字节为实际有效数据长度</div> | <div style="width: 150pt">透传<br>固定长度21个字节，预留最后两个字节，最后一个字节为CRC的值，倒数第二个字节为实际有效数据长度</div> |
- 为了区分CAN协议，帧头0x45 0x54预留给CAN协议，RS485协议的前两个字节不可以使用0x45 0x54，其他字节没有限制
### 示例代码
**[下载地址](https://gitcode.com/sanpo/robot/blob/main/demo/spi_demo/unitree)**
