import struct

# CRC-CCITT 表
crc_ccitt_table = [
	0x0000, 0x1189, 0x2312, 0x329b, 0x4624, 0x57ad, 0x6536, 0x74bf,
	0x8c48, 0x9dc1, 0xaf5a, 0xbed3, 0xca6c, 0xdbe5, 0xe97e, 0xf8f7,
	0x1081, 0x0108, 0x3393, 0x221a, 0x56a5, 0x472c, 0x75b7, 0x643e,
	0x9cc9, 0x8d40, 0xbfdb, 0xae52, 0xdaed, 0xcb64, 0xf9ff, 0xe876,
	0x2102, 0x308b, 0x0210, 0x1399, 0x6726, 0x76af, 0x4434, 0x55bd,
	0xad4a, 0xbcc3, 0x8e58, 0x9fd1, 0xeb6e, 0xfae7, 0xc87c, 0xd9f5,
	0x3183, 0x200a, 0x1291, 0x0318, 0x77a7, 0x662e, 0x54b5, 0x453c,
	0xbdcb, 0xac42, 0x9ed9, 0x8f50, 0xfbef, 0xea66, 0xd8fd, 0xc974,
	0x4204, 0x538d, 0x6116, 0x709f, 0x0420, 0x15a9, 0x2732, 0x36bb,
	0xce4c, 0xdfc5, 0xed5e, 0xfcd7, 0x8868, 0x99e1, 0xab7a, 0xbaf3,
	0x5285, 0x430c, 0x7197, 0x601e, 0x14a1, 0x0528, 0x37b3, 0x263a,
	0xdecd, 0xcf44, 0xfddf, 0xec56, 0x98e9, 0x8960, 0xbbfb, 0xaa72,
	0x6306, 0x728f, 0x4014, 0x519d, 0x2522, 0x34ab, 0x0630, 0x17b9,
	0xef4e, 0xfec7, 0xcc5c, 0xddd5, 0xa96a, 0xb8e3, 0x8a78, 0x9bf1,
	0x7387, 0x620e, 0x5095, 0x411c, 0x35a3, 0x242a, 0x16b1, 0x0738,
	0xffcf, 0xee46, 0xdcdd, 0xcd54, 0xb9eb, 0xa862, 0x9af9, 0x8b70,
	0x8408, 0x9581, 0xa71a, 0xb693, 0xc22c, 0xd3a5, 0xe13e, 0xf0b7,
	0x0840, 0x19c9, 0x2b52, 0x3adb, 0x4e64, 0x5fed, 0x6d76, 0x7cff,
	0x9489, 0x8500, 0xb79b, 0xa612, 0xd2ad, 0xc324, 0xf1bf, 0xe036,
	0x18c1, 0x0948, 0x3bd3, 0x2a5a, 0x5ee5, 0x4f6c, 0x7df7, 0x6c7e,
	0xa50a, 0xb483, 0x8618, 0x9791, 0xe32e, 0xf2a7, 0xc03c, 0xd1b5,
	0x2942, 0x38cb, 0x0a50, 0x1bd9, 0x6f66, 0x7eef, 0x4c74, 0x5dfd,
	0xb58b, 0xa402, 0x9699, 0x8710, 0xf3af, 0xe226, 0xd0bd, 0xc134,
	0x39c3, 0x284a, 0x1ad1, 0x0b58, 0x7fe7, 0x6e6e, 0x5cf5, 0x4d7c,
	0xc60c, 0xd785, 0xe51e, 0xf497, 0x8028, 0x91a1, 0xa33a, 0xb2b3,
	0x4a44, 0x5bcd, 0x6956, 0x78df, 0x0c60, 0x1de9, 0x2f72, 0x3efb,
	0xd68d, 0xc704, 0xf59f, 0xe416, 0x90a9, 0x8120, 0xb3bb, 0xa232,
	0x5ac5, 0x4b4c, 0x79d7, 0x685e, 0x1ce1, 0x0d68, 0x3ff3, 0x2e7a,
	0xe70e, 0xf687, 0xc41c, 0xd595, 0xa12a, 0xb0a3, 0x8238, 0x93b1,
	0x6b46, 0x7acf, 0x4854, 0x59dd, 0x2d62, 0x3ceb, 0x0e70, 0x1ff9,
	0xf78f, 0xe606, 0xd49d, 0xc514, 0xb1ab, 0xa022, 0x92b9, 0x8330,
	0x7bc7, 0x6a4e, 0x58d5, 0x495c, 0x3de3, 0x2c6a, 0x1ef1, 0x0f78
]

# CRC-CCITT 单字节处理
def crc_ccitt_byte(crc, c):
    return ((crc >> 8) & 0xFF) ^ crc_ccitt_table[(crc ^ c) & 0xFF]

# CRC-CCITT 计算函数
def crc_ccitt(crc, buffer, length):
    i = 0
    while i < length:
        crc = crc_ccitt_byte(crc, buffer[i])
        i += 1
    return crc

# 结构体定义 - 电机模式控制信息
class RIS_Mode_t:
    def __init__(self):
        self.id = 0      # 电机ID: 0-15
        self.status = 0  # 工作模式: 0-7
        self.reserve = 0 # 保留位
    
    # 打包为字节
    def pack(self):
        # 组合为一个字节
        combined = (self.id & 0x0F) | ((self.status & 0x07) << 4) | ((self.reserve & 0x01) << 7)
        return bytes([combined])
    
    # 从字节解包
    def unpack(self, data):
        combined = data[0]
        self.id = combined & 0x0F
        self.status = (combined >> 4) & 0x07
        self.reserve = (combined >> 7) & 0x01

# 结构体定义 - 电机状态控制信息
class RIS_Comd_t:
    def __init__(self):
        self.tor_des = 0  # 期望关节输出扭矩
        self.spd_des = 0  # 期望关节输出速度
        self.pos_des = 0  # 期望关节输出位置
        self.k_pos = 0    # 期望关节刚度系数
        self.k_spd = 0    # 期望关节阻尼系数
    
    # 打包为字节
    def pack(self):
        return struct.pack('<hhihh', self.tor_des, self.spd_des, self.pos_des, self.k_pos, self.k_spd)

# 结构体定义 - 电机状态反馈信息
class RIS_Fbk_t:
    def __init__(self):
        self.torque = 0      # 实际关节输出扭矩
        self.speed = 0       # 实际关节输出速度
        self.pos = 0         # 实际关节输出位置
        self.temp = 0        # 电机温度
        self.MError = 0      # 电机错误标识
        self.force = 0       # 足端气压传感器数据
        self.none = 0        # 保留位
    
    # 从字节解包
    def unpack(self, data):
        # 首先解析基本的字段
        self.torque, self.speed, self.pos, self.temp = struct.unpack('<hhih', data[:11])
        # 解析位字段
        error_force = data[11:14]
        error_force_int = struct.unpack('<H', error_force[:2])[0]
        self.MError = error_force_int & 0x07
        self.force = (error_force_int >> 3) & 0x0FFF
        if len(error_force) > 2:
            self.none = (error_force[2] >> 4) & 0x01

# 结构体定义 - 控制数据包格式
class RIS_ControlData_t:
    def __init__(self):
        self.head = [0xFE, 0xEE]  # 包头
        self.mode = RIS_Mode_t()  # 电机控制模式
        self.comd = RIS_Comd_t()  # 电机期望数据
        self.CRC16 = 0           # CRC校验
    
    # 打包为字节（不包括CRC）
    def pack_without_crc(self):
        data = bytes(self.head) + self.mode.pack() + self.comd.pack()
        return data

# 结构体定义 - 电机反馈数据包格式
class RIS_MotorData_t:
    def __init__(self):
        self.head = [0xFD, 0xEE]  # 包头
        self.mode = RIS_Mode_t()  # 电机控制模式
        self.fbk = RIS_Fbk_t()    # 电机反馈数据
        self.CRC16 = 0           # CRC校验
    
    # 从字节解包（不包括CRC）
    def unpack_without_crc(self, data):
        self.head = list(data[:2])
        self.mode.unpack(data[2:3])
        self.fbk.unpack(data[3:14])

# 结构体定义 - 电机指令结构体
class MotorCmd_t:
    def __init__(self):
        self.id = 0     # 电机ID，15代表广播数据包
        self.mode = 0   # 0:空闲 1:FOC控制 2:电机标定
        self.T = 0.0    # 期望关节的输出力矩(Nm)
        self.W = 0.0    # 期望关节速度(rad/s)
        self.Pos = 0.0  # 期望关节位置(rad)
        self.K_P = 0.0  # 关节刚度系数(0-25.599)
        self.K_W = 0.0  # 关节速度系数(0-25.599)
        self.motor_send_data = RIS_ControlData_t()

# 结构体定义 - 电机反馈结构体
class MotorData_t:
    def __init__(self):
        self.motor_id = 0    # 电机ID
        self.mode = 0        # 0:空闲 1:FOC控制 2:电机标定
        self.Temp = 0        # 温度
        self.MError = 0      # 错误码
        self.T = 0.0         # 当前实际电机输出力矩(Nm)
        self.W = 0.0         # 当前实际电机速度(rad/s)
        self.Pos = 0.0       # 当前电机位置(rad)
        self.correct = 0     # 接收数据是否完整(1完整，0不完整)
        self.footForce = 0   # 足端力传感器原始数值
        self.calc_crc = 0
        self.timeout = 0     # 通讯超时 数量
        self.bad_msg = 0     # CRC校验错误 数量
        self.motor_recv_data = RIS_MotorData_t()

# 限制函数（替代宏）
def saturate(value, min_val, max_val):
    if value <= min_val:
        return min_val
    elif value >= max_val:
        return max_val
    return value

# 将电机指令数据转换为发送格式
def modify_data(motor_s):
    # 设置包头
    motor_s.motor_send_data.head[0] = 0xFE
    motor_s.motor_send_data.head[1] = 0xEE

    # 限制参数范围
    motor_s.id = int(saturate(motor_s.id, 0, 15))
    motor_s.mode = int(saturate(motor_s.mode, 0, 7))
    motor_s.K_P = saturate(motor_s.K_P, 0.0, 25.599)
    motor_s.K_W = saturate(motor_s.K_W, 0.0, 25.599)
    motor_s.T = saturate(motor_s.T, -127.99, 127.99)
    motor_s.W = saturate(motor_s.W, -804.00, 804.00)
    motor_s.Pos = saturate(motor_s.Pos, -411774.0, 411774.0)

    # 设置发送数据
    motor_s.motor_send_data.mode.id = motor_s.id
    motor_s.motor_send_data.mode.status = motor_s.mode
    motor_s.motor_send_data.comd.k_pos = int(motor_s.K_P / 25.6 * 32768.0)
    motor_s.motor_send_data.comd.k_spd = int(motor_s.K_W / 25.6 * 32768.0)
    motor_s.motor_send_data.comd.pos_des = int(motor_s.Pos / 6.28318 * 32768.0)
    motor_s.motor_send_data.comd.spd_des = int(motor_s.W / 6.28318 * 256.0)
    motor_s.motor_send_data.comd.tor_des = int(motor_s.T * 256.0)
    
    # 计算CRC16校验
    data_without_crc = motor_s.motor_send_data.pack_without_crc()
    motor_s.motor_send_data.CRC16 = crc_ccitt(0, data_without_crc, len(data_without_crc))
    
    # 返回完整的发送数据(包括CRC)
    full_data = data_without_crc + struct.pack('<H', motor_s.motor_send_data.CRC16)
    return full_data

# 从接收的字节数据中提取电机反馈信息到MotorData_t结构体
def extract_data(motor_data, recv_bytes):
    """
    从字节数据解码到MotorData_t结构体
    motor_data: MotorData_t实例，用于存储解码后的数据
    recv_bytes: 接收到的字节数据
    """
    try:
        # 确保recv_bytes是bytes类型
        if isinstance(recv_bytes, list):
            recv_bytes = bytes(recv_bytes)
        elif not isinstance(recv_bytes, bytes):
            motor_data.correct = 0
            return -1
            
        # 首先检查数据长度是否有效
        if len(recv_bytes) < 14:  # 最小需要14字节（包头2+模式1+数据11）
            motor_data.correct = 0
            return -1
        
        # 检查包头
        if recv_bytes[0] != 0xFD or recv_bytes[1] != 0xEE:
            motor_data.correct = 0
            return -1
        
        # 解析模式字节（第3字节）
        mode_byte = recv_bytes[2]
        motor_data.motor_id = mode_byte & 0x0F  # 低4位是电机ID
        motor_data.mode = (mode_byte >> 4) & 0x07  # 第4-6位是模式
        
        # 解析电机数据（从第4字节开始）
        # 使用struct解包数据
        # torque(2字节), speed(2字节), pos(4字节), temp(1字节), error_force(2字节)
        if len(recv_bytes) >= 14:  # 确保有足够的数据
            # 解析基本数据字段
            torque, speed, pos, temp = struct.unpack('<hhib', recv_bytes[3:12])
            
            # 解析错误码和足端力数据
            error_force = struct.unpack('<H', recv_bytes[12:14])[0]
            
            # 填充结构体字段
            motor_data.Temp = temp
            motor_data.MError = error_force & 0x07  # 低3位是错误码
            motor_data.footForce = (error_force >> 3) & 0x0FFF  # 接下来的12位是足端力
            
            # 转换实际物理值
            motor_data.W = (float(speed) / 256.0) * 6.28318  # 速度转换为rad/s
            motor_data.T = float(torque) / 256.0  # 力矩转换为Nm
            motor_data.Pos = 6.28318 * float(pos) / 32768.0  # 位置转换为rad

            # 计算CRC16校验（如果数据长度足够）
            if len(recv_bytes) >= 16:  # 完整数据包应该有16字节（包括CRC）
                # 计算前14字节的CRC
                motor_data.calc_crc = crc_ccitt(0, recv_bytes[:14], 14)
                # 获取接收到的CRC
                received_crc = struct.unpack('<H', recv_bytes[14:16])[0]
                # 验证CRC
                if motor_data.calc_crc == received_crc:
                    motor_data.correct = 1
                else:
                    motor_data.correct = 0
                    return
            else:
                # 如果没有CRC部分，假设数据正确（仅用于调试）
                motor_data.correct = 1
        else:
            motor_data.correct = 0
            return -1
    
    except Exception as e:
        print(f"解析数据时出错: {e}")
        motor_data.correct = 0

    return 0