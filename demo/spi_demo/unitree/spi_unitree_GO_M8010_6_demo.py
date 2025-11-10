import time
import sys
import spidev
from unitree_GO_M8010_6_protocol_demo import *

class CRC8:
    def __init__(self, polynomial=10):
        self.polynomial = polynomial
        self.table = self._build_table()
    
    def _build_table(self):
        table = []
        for i in range(256):
            crc = i
            for _ in range(8):
                if crc & 0x80:
                    crc = ((crc << 1) ^ self.polynomial) & 0xFF
                else:
                    crc = (crc << 1) & 0xFF
            table.append(crc)
        return table
    
    def calculate(self, data):
        crc = 0
        for byte in data:
            crc = self.table[crc ^ byte] & 0xFF
        return crc

crc8_calculator = CRC8(polynomial=7)

#=========================设置RS485总线的波特率=====================
# SPI连接开发板，只需一条SPI总线，和两个CS片选通道，例如树莓派可以使用SPI通道0，片选通道0和1
# 发送和接收的数据结构：固定帧头6个字节(0x45 0x54 0x45 0x54 0xFF 0x02)+RS485总线的编号 2个字节+波特率4个字节+停止位1个字节+奇偶校验位1个字节+数据位1个字节+固定帧尾4个字节(0x0D 0x0A 0x0D 0x0A)+预留1个字节(0x00)+CRC1个字节
# spibus:                SPI总线
# cs:                    SPI片选通道
# rs485num:              RS485总线的编号，1，2，3，4
# baudrate:              RS485总线的波特率
# format:                停止位，1位停止位，2位停止位，默认为1
# paritytype:            奇偶校验位，0为无校验，1为奇校验，2为偶校验，默认为0
# datatype:              数据位，8位数据位，9位数据位，默认为8
#================================================================
def sys_set_rs485_baudrate(spibus, cs, rs485num, baudrate, format=1, paritytype=0, datatype=8):
    state = 0
    # 检查RS485总线编号是否有效
    if rs485num not in [1, 2, 3, 4]:
        raise ValueError("RS485总线编号必须为1、2、3或4")
    try:
        spi = spidev.SpiDev()
        # 打开SPI总线
        spi.open(int(spibus), int(cs))
        spi.max_speed_hz = 10000000  # 10 MHz（修正注释）
        spi.mode = 0                # SPI模式0 (CPOL=0, CPHA=0)

        # 固定帧头6个字节(0x45 0x54 0x45 0x54 0xFF 0x02)
        frame_header = [0x45, 0x54, 0x45, 0x54, 0xFF, 0x02]
        # RS485总线的编号 2个字节
        rs485id_bytes = [rs485num, 0x00]
        # 波特率4个字节
        baudrate_bytes = [
            (baudrate >> 24) & 0xFF,
            (baudrate >> 16) & 0xFF,
            (baudrate >> 8) & 0xFF,
            baudrate & 0xFF
        ]
        # 固定帧尾4个字节(0x0D 0x0A 0x0D 0x0A)
        frame_tail = [0x0D, 0x0A, 0x0D, 0x0A]
        # 预留1个字节(使用0x00填充)
        reserved_bytes = [0x00]
        # 合并所有数据
        full_data = frame_header + rs485id_bytes + baudrate_bytes + [format, paritytype, datatype] + frame_tail + reserved_bytes
        # 计算CRC值
        crc = crc8_calculator.calculate(full_data)
        # 添加CRC字节
        full_data.append(crc)
        print(f"[SPI发送]: {[f'0x{byte:02X}' for byte in full_data]}")

        # 使用xfer2发送数据并接收从设备的响应
        spi.xfer2(full_data)
        # 等待从设备准备数据
        time.sleep(0.01)
    except KeyboardInterrupt:
        state = -2
        spi.close()
        print("\nSPI连接已关闭")
    except Exception as e:
        state = -2
        print(f"发生错误: {e}")
        if spi is not None:
            spi.close()
    finally:
        if spi is not None:
            spi.close()
    return state

#=========================发送并接受宇树GO_M8010_6电机数据=====================
# SPI连接开发板，只需一条SPI总线，和两个CS片选通道，例如树莓派可以使用SPI通道0，片选通道0和1
# 发送和接收的数据结构：SANPO控制板的SPI数据总长度固定21个字节，最后一个字节为校验位，倒数第二个字节为实际有效数据长度
# 发送数据格式：宇树GO_M8010_6电机命令结构(17个字节)+预留3个字节(0x00 0x00 0x11)+CRC1个字节
# 接收数据时格式：宇树GO_M8010_6电机数据结构(16个字节)+预留4个字节(0x00 0x00 0x00 0x10)+CRC1个字节
# spibus:                SPI总线
# cs:                    SPI片选通道
# cmd:                   宇树GO_M8010_6电机发送命令结构(17个字节)
# data:                  宇树GO_M8010_6电机接收数据结构(16个字节)
#================================================================
def send_recv_main(spibus, cs, cmd):
    state = 0
    motor_data = 0
    try:
        spi = spidev.SpiDev()
        # 打开SPI总线, 默认（总线0，设备0）
        spi.open(int(spibus), int(cs))
        spi.max_speed_hz = 10000000  # 10 MHz（修正注释）
        spi.mode = 0                # SPI模式0 (CPOL=0, CPHA=0)

        # 预留3个字节(使用0x00, 0x00, 0x11填充)
        reserved_bytes = bytes([0x00, 0x00, 0x11])
        # 合并所有数据
        full_data = cmd + reserved_bytes
        #print(f"[SPI数据无校验值]: {[f'0x{byte:02X}' for byte in full_data]}")
        # 计算CRC值
        crc_value = crc8_calculator.calculate(full_data)
        # spi发送的固定数据长度为21个字节，最后一个字节为CRC值
        full_data = full_data + bytes([crc_value])
        #print(f"[SPI发送完整数据]: {[f'0x{byte:02X}' for byte in full_data]}")
        # 使用xfer2发送数据并接收从设备的响应
        # xfer2的特点是在同一时钟周期内完成发送和接收
        rx_data = spi.xfer2(full_data)

        # spi接收的固定数据长度为21个字节，最后一个字节为CRC值
        if len(rx_data) != 21:
            print("接收数据长度错误")
            state = -1
            return(state,motor_data)
        # 分离数据和CRC
        data_part = rx_data[:20]
        # 从接收到的数据中提取CRC值
        received_crc = rx_data[20]
        # 计算数据部分的CRC
        calculated_crc = crc8_calculator.calculate(data_part)
        # 验证CRC
        is_valid = (calculated_crc == received_crc)
        #print(f"[SPI接收]: {[f'0x{byte:02X}' for byte in rx_data]}")
        if is_valid:
            #print(f"CRC验证成功: 计算值=0x{calculated_crc:02X}, 接收值=0x{received_crc:02X}")
            data_len = rx_data[19] # 获取实际有效的数据，SPI 固定21个字节，最后一个字节为CRC值，倒数第二个字节为数据长度
            motor_data = data_part[:data_len]
            state = 1
        else:
            print(f"CRC验证失败: 计算值=0x{calculated_crc:02X}, 接收值=0x{received_crc:02X}")
            state = -1
    except KeyboardInterrupt:
        state = -2
        spi.close()
        print("\nSPI连接已关闭")
    except Exception as e:
        state = -2
        print(f"发生错误: {e}")
        if spi is not None:
            spi.close()
    finally:
        if spi is not None:
            spi.close()
    return(state,motor_data)

def set_motor_torque(spibus, cs, motorID, torque):
    # 创建一个电机指令实例
    motor_cmd = MotorCmd_t()
    motor_cmd.id = motorID
    motor_cmd.mode = 1 # 0:空闲 1:FOC控制 2:电机标定
    motor_cmd.T = torque # 期望关节的输出力矩(Nm)
    motor_cmd.W = 0 # 期望关节速度(rad/s)
    motor_cmd.Pos = 0 # 期望关节位置(rad)
    motor_cmd.K_P = 0 # 关节刚度系数
    motor_cmd.K_W = 0 # 关节速度系数

    # 转换为发送格式
    send_cmd = modify_data(motor_cmd)
    #print(f"[Motor CMD]: {[f'0x{byte:02X}' for byte in send_cmd]}")
    motor_data = MotorData_t()

    while True:
        try:
            state,recv_data = send_recv_main(spibus,cs,send_cmd)
            if state == 1:
                if(extract_data(motor_data, recv_data) == 0):
                    print(f"\n提取的数据:")
                    print(f"[Motor CMD]: {[f'0x{byte:02X}' for byte in send_cmd]}")
                    print(f"[Motor DATA]: {[f'0x{byte:02X}' for byte in recv_data]}")
                    print(f"电机ID: {motor_data.motor_id}")
                    print(f"模式: {motor_data.mode}")
                    print(f"温度: {motor_data.Temp}°C")
                    print(f"速度: {motor_data.W:.2f} rad/s")
                    print(f"力矩: {motor_data.T:.2f} Nm")
                    print(f"位置: {motor_data.Pos:.2f} rad")
                    print(f"足端力: {motor_data.footForce}")
                    print(f"数据是否完整: {motor_data.correct}")

                    is_show_motor_data = 0
            else:
                print("发送接收失败")
            time.sleep(0.0002) # 200 us
        # 当用户按下 Ctrl+C 时，会执行这里的代码
        except KeyboardInterrupt:
            print("按下 Ctrl+C,结束----")
            break

import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="这是一个示例脚本。")
    parser.add_argument("--cmd", help="1: 电机转动测试。 2: 电机停止。", default="1")
    parser.add_argument("--spibus", help="0 or 1", default="0")
    parser.add_argument("--cs", help="0 or 1", default="0")
    parser.add_argument("--motorid", help="motor id", default="1")
    parser.add_argument("--tor", help="set motor torque", default="0.05")
    args = parser.parse_args()
    spibus = int(args.spibus)
    cs = int(args.cs)
    torque = float(args.tor)
    motorID = int(args.motorid)
    
    # 宇树GM8010电机RS485总线要求4000000波特率，设置4个RS485通道的波特率为4000000
    sys_set_rs485_baudrate(0, 0, 1, 4000000)
    sys_set_rs485_baudrate(0, 0, 2, 4000000)
    sys_set_rs485_baudrate(0, 1, 3, 4000000)
    sys_set_rs485_baudrate(0, 1, 4, 4000000)

    if args.cmd == "1":
        set_motor_torque(spibus, cs, motorID, torque) #设置电机一定的扭矩
    else:
        print(f"未知命令: {args.cmd}")