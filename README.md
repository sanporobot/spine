# SANPO兴普智能 - 机器人集成开发板

## 功能描述 ##
- 支持**4**路**CAN**总线，**4**路**RS485**总线
- 支持**小米CyberGear**，**宇树GM**系列等常用关节电机
- 支持**USB**控制输入
- 支持**SPI**控制输入
- 支持外接**IIC，ADC，串口**传感器设备
- 支持**5V/3.3V**电源输出，提供**树莓派，Nvidia Jetson**等上位机供电
- 兼容**MIT Cheetash SPINE**硬件设计标准

**[淘宝店地址](https://e.tb.cn/h.SVimqfGYgPR7ARf?tk=oLuK4DG8Kgg)**

## 开发板设计架构 ##
- 开发板集成2个STM32F4模块。
- 一条腿（三个关节）为一路CAN/RS485，与STM32F4模块(Spine)进行通信，一个STM32F4(Spine)模块负责两条腿的CAN/RS485通信。
- 根据MIT Cheetash的设计标准，为了保证每路CAN的通信至少是1M。每个STM32F4有2路CAN，每一路负责三个电机的通讯可以达到1000Hz。
- 串口1，IIC接口1，ADC接口1与STM32F4(1)模块通信，串口2，IIC接口2，ADC接口2与STM32F4(2)通信。
- 二次开发时，可以通过SWD下载调试接口安装固件，SWD接口1对应STM32F4(1)模块，SWD接口2对应STM32F4(2)模块。([参考接口设计图](#p2))
- 原厂固件集成MPU050 IIC协议接入，FSR402 AD协议接入，可参考样例程序开发其他传感器协议接入。
- 上位机通过SPI与开发板通信时，CS1片选通道对应STM32F4(1)模块，CS2片选通道对应STM32F4(2)模块。
<img src="images/taobao-github-architect-1.1.png">

## 开发板接口图 ##
<span id="p2"><img src="images/taobao-github-architect-1.2.png"></span>

## 应用方案示例 ##
- [示例方案一：机器人关节电机控制(USB控制输入)](#s1)
- [示例方案二：机器人关节电机控制(SPI控制输入)](#s2)
- [示例方案三：外接传感器(姿态传感器，压力传感器等)](#s3)
- [示例方案四：MIT Cheetash SPINE固件](#s4)

### <span id="s1"> 示例方案一：机器人关节电机控制(USB控制输入) </span>
##### 接线示例图
<img src="images/taobao-github-usb-2.1.1.png">

### <span id="s2"> 示例方案二：机器人关节电机控制(SPI控制输入) </span>
##### 接线示例图
###### 1. Jetson Nano
<img src="images/taobao-github-spi-jetson-2.2.1.png">

###### 2. 树莓派4B
<img src="images/taobao-github-spi-pi-2.2.2.png">

### <span id="s3"> 示例方案三：外接传感器(姿态传感器，压力传感器等) </span>
##### 接线示例图
###### 1. IIC：MPU6050姿态传感器
###### 2. ADC：压力传感器

### <span id="s4"> 示例方案四：MIT Cheetash SPINE固件 </span>