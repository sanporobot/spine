### MIT Cheetash SPINE固件
#### 该项目工程，使用mbed studio开发。
该工程代码与SANPO开发板已经适配。
SANPO开发版与原MIT SPINE STM32芯片引脚定义的对应关系，如下表所示：  
|    功能     | SANPO开发板 | MIT SPINE |
| :---------- | :----------: | :---------: |
|   控制芯片   | STM32F407 | STM32F446 |
| 串口(TX)    | PD_8      | PC_2
| 串口(RX)    | PD_9      | PC_3
| CAN1(TX)   | PB_9      | PB_13
| CAN1(RX)   | PB_8      | PB_12
| CAN2(TX)   | PB_13      | PB_9
| CAN2(RX)   | PB_12     | PB_8
| SPI(MOSI)  | PC_12     | PA_7
| SPI(MISO)  | PC_11     | PA_6
| SPI(SCLK)  | PC_10     | PA_5
| SPI(CS)    | PA_15     | PA_4
| ESTOP      | PD_0      | PB_15