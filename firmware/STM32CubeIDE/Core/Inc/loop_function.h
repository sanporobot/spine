/*
 * loop_function.h
 *
 *  Created on: Aug 13, 2025
 *      Author: puwan
 */

#ifndef INC_LOOP_FUNCTION_H_
#define INC_LOOP_FUNCTION_H_

#include "stm32f4xx_hal.h"
#include <string.h>
#include <stdint.h>

void _init_cdcrx_queue(void);
uint8_t* _get_cdcrx_queue_buf(void);
uint8_t _is_full_cdcrx_queue(void);
void _push_cdcrx_queue(uint16_t len);
void _pop_cdcrx_queue(void);
void _set_cdc_mode(int mode);
uint8_t* _get_cdctx_queue_buf(void);
uint8_t _get_cdctx_queue_buf_size(void);
void _pop_cdctx_queue(void);

uint8_t* _get_spirx_queue_buf(void);
uint8_t _get_spirx_queue_buf_size(void);
uint8_t _push_spirx_queue(void);
void _reset_spirx_msglen(void);

uint8_t* _get_spitx_buf(void);
uint8_t _get_spitx_msg(void);

uint8_t* _get_rs485Arx_queue_buf(void);
uint8_t* _get_rs485Brx_queue_buf(void);
uint8_t _get_rs485rx_queue_buf_size(void);
uint8_t _push_rs485Arx_queue(uint16_t Size);
uint8_t _push_rs485Brx_queue(uint16_t Size);

CAN_RxHeaderTypeDef* _get_canrx_queue_header(void);
uint8_t* _get_canrx_queue_buf(void);
uint8_t _push_canrx_queue(void);

uint8_t* _get_cdc_cmd_atok();
uint32_t _get_cdc_cmd_atok_length();

void _set_rs485a_tx(void);
void _set_rs485b_tx(void);

int cdc_rx_loop();
int cdc_tx_loop();
int spi_rx_loop(CAN_HandleTypeDef* phcan1, CAN_HandleTypeDef* phcan2, UART_HandleTypeDef* phrs485A, UART_HandleTypeDef* phrs485B);
int cdc2can_tx_loop(CAN_HandleTypeDef* phcan1, CAN_HandleTypeDef* phcan2);
int spi2can_tx_loop(CAN_HandleTypeDef* phcan1, CAN_HandleTypeDef* phcan2);
int cdc2rs485a_tx_loop(UART_HandleTypeDef* phRS485A, GPIO_TypeDef* RS485A_Port, uint16_t RS485A_Pin);
int spi2rs485a_tx_loop(UART_HandleTypeDef* phRS485A, GPIO_TypeDef* RS485A_Port, uint16_t RS485A_Pin);
int cdc2rs485b_tx_loop(UART_HandleTypeDef* phRS485B, GPIO_TypeDef* RS485B_Port, uint16_t RS485B_Pin);
int spi2rs485b_tx_loop(UART_HandleTypeDef* phRS485B, GPIO_TypeDef* RS485B_Port, uint16_t RS485B_Pin);
int data_rx_loop();
int init_loop();
int init_task(SPI_HandleTypeDef *hspi,GPIO_TypeDef* RS485A_Port, uint16_t RS485A_Pin,UART_HandleTypeDef *huart_RS485A,DMA_HandleTypeDef *hdma_RS485A_rx,GPIO_TypeDef* RS485B_Port, uint16_t RS485B_Pin,UART_HandleTypeDef *huart_RS485B, DMA_HandleTypeDef *hdma_RS485B_rx);
int update_usart(UART_HandleTypeDef* phusart, uint32_t bitrate, uint8_t format, uint8_t paritytype, uint8_t datatype);
int update_can(CAN_HandleTypeDef* phcan, uint32_t bitrate, uint32_t ActiveITs);

#endif /* INC_LOOP_FUNCTION_H_ */
