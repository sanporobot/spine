# SANPO兴普智能 - 机器人集成开发板

## 固件选择 ##
开发板支持如下两种固件
### SANPO原厂固件
[下载地址](https://gitcode.com/sanpo/robot/tree/main/firmware/STM32CubeIDE/Release)  

适用场景：
1. 提供STM32CubeIDE开发工程源码，方便用户进行二次开发。
2. 集成FreeRTOS框架，支持实时多任务并发执行。
3. 同时支持CAN总线和RS485总线通信。
4. 支持USB，IIC，SPI，串口，ADC等接口，方便用户进行扩展。
5. 支持小米CyberGear，宇树电机通信协议和官方调试工具。

### MIT Cheetash SPINE的固件
适用场景：
学习Cheetash运动控制原理。
提示：
开发调试难度高，因为源代码MIT团队已不再维护，mbedos框架也已经停止维护，并且不支持常用电机通信协议，不建议用于实际项目开发。