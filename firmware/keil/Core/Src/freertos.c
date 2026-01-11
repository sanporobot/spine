/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * File Name          : freertos.c
  * Description        : Code for freertos applications
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "FreeRTOS.h"
#include "task.h"
#include "main.h"
#include "cmsis_os.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "error.h"
#include "usbd_cdc.h"
#include "loop_function.h"
#include "spi.h"
#include "usart.h"
#include "i2c.h"
#include "adc.h"
#include "mpu6050.h"
#include "usart.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
/* USER CODE BEGIN Variables */
extern USBD_HandleTypeDef hUsbDeviceFS;
extern CAN_HandleTypeDef hcan1;
extern CAN_HandleTypeDef hcan2;
/* USER CODE END Variables */
/* Definitions for defaultTask */
osThreadId_t defaultTaskHandle;
const osThreadAttr_t defaultTask_attributes = {
  .name = "defaultTask",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for cdcRXTask */
osThreadId_t cdcRXTaskHandle;
const osThreadAttr_t cdcRXTask_attributes = {
  .name = "cdcRXTask",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for canTXTask */
osThreadId_t canTXTaskHandle;
const osThreadAttr_t canTXTask_attributes = {
  .name = "canTXTask",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for dataRXTask */
osThreadId_t dataRXTaskHandle;
const osThreadAttr_t dataRXTask_attributes = {
  .name = "dataRXTask",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for cdcTXTask */
osThreadId_t cdcTXTaskHandle;
const osThreadAttr_t cdcTXTask_attributes = {
  .name = "cdcTXTask",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for spiRXTask06 */
osThreadId_t spiRXTask06Handle;
const osThreadAttr_t spiRXTask06_attributes = {
  .name = "spiRXTask06",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for usartTXTask */
osThreadId_t usartTXTaskHandle;
const osThreadAttr_t usartTXTask_attributes = {
  .name = "usartTXTask",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for i2cRXTask */
osThreadId_t i2cRXTaskHandle;
const osThreadAttr_t i2cRXTask_attributes = {
  .name = "i2cRXTask",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for adcRXTask */
osThreadId_t adcRXTaskHandle;
const osThreadAttr_t adcRXTask_attributes = {
  .name = "adcRXTask",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for rs485ATXTask */
osThreadId_t rs485ATXTaskHandle;
const osThreadAttr_t rs485ATXTask_attributes = {
  .name = "rs485ATXTask",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for rs485BTXTask */
osThreadId_t rs485BTXTaskHandle;
const osThreadAttr_t rs485BTXTask_attributes = {
  .name = "rs485BTXTask",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};

/* Private function prototypes -----------------------------------------------*/
/* USER CODE BEGIN FunctionPrototypes */

/* USER CODE END FunctionPrototypes */

void StartDefaultTask(void *argument);
void StartCDCRXTask(void *argument);
void StartCANTXTask(void *argument);
void StartDataRXTask(void *argument);
void StartCDCTXTask(void *argument);
void StartSPIRXTask(void *argument);
void StartUSARTTXTask(void *argument);
void StartI2CRXTask(void *argument);
void StartADCRXTask(void *argument);
void StartRS485ATXTask(void *argument);
void StartRS485BTXTask(void *argument);

extern void MX_USB_DEVICE_Init(void);
void MX_FREERTOS_Init(void); /* (MISRA C 2004 rule 8.1) */

/**
  * @brief  FreeRTOS initialization
  * @param  None
  * @retval None
  */
void MX_FREERTOS_Init(void) {
  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* USER CODE BEGIN RTOS_MUTEX */
  /* add mutexes, ... */
  /* USER CODE END RTOS_MUTEX */

  /* USER CODE BEGIN RTOS_SEMAPHORES */
  /* add semaphores, ... */
  /* USER CODE END RTOS_SEMAPHORES */

  /* USER CODE BEGIN RTOS_TIMERS */
  /* start timers, add new ones, ... */
  /* USER CODE END RTOS_TIMERS */

  /* USER CODE BEGIN RTOS_QUEUES */
  /* add queues, ... */
  /* USER CODE END RTOS_QUEUES */

  /* Create the thread(s) */
  /* creation of defaultTask */
  defaultTaskHandle = osThreadNew(StartDefaultTask, NULL, &defaultTask_attributes);

  /* creation of cdcRXTask */
  cdcRXTaskHandle = osThreadNew(StartCDCRXTask, NULL, &cdcRXTask_attributes);

  /* creation of canTXTask */
  canTXTaskHandle = osThreadNew(StartCANTXTask, NULL, &canTXTask_attributes);

  /* creation of dataRXTask */
  dataRXTaskHandle = osThreadNew(StartDataRXTask, NULL, &dataRXTask_attributes);

  /* creation of cdcTXTask */
  cdcTXTaskHandle = osThreadNew(StartCDCTXTask, NULL, &cdcTXTask_attributes);

  /* creation of spiRXTask06 */
  spiRXTask06Handle = osThreadNew(StartSPIRXTask, NULL, &spiRXTask06_attributes);

  /* creation of usartTXTask */
  usartTXTaskHandle = osThreadNew(StartUSARTTXTask, NULL, &usartTXTask_attributes);

  /* creation of i2cRXTask */
  i2cRXTaskHandle = osThreadNew(StartI2CRXTask, NULL, &i2cRXTask_attributes);

  /* creation of adcRXTask */
  adcRXTaskHandle = osThreadNew(StartADCRXTask, NULL, &adcRXTask_attributes);

  /* creation of rs485ATXTask */
  rs485ATXTaskHandle = osThreadNew(StartRS485ATXTask, NULL, &rs485ATXTask_attributes);

  /* creation of rs485BTXTask */
  rs485BTXTaskHandle = osThreadNew(StartRS485BTXTask, NULL, &rs485BTXTask_attributes);

  /* USER CODE BEGIN RTOS_THREADS */
  /* add threads, ... */
  /* USER CODE END RTOS_THREADS */

  /* USER CODE BEGIN RTOS_EVENTS */
  /* add events, ... */
  /* USER CODE END RTOS_EVENTS */

}

/* USER CODE BEGIN Header_StartDefaultTask */
/**
  * @brief  Function implementing the defaultTask thread.
  * @param  argument: Not used
  * @retval None
  */
/* USER CODE END Header_StartDefaultTask */
void StartDefaultTask(void *argument)
{
  /* init code for USB_DEVICE */
  MX_USB_DEVICE_Init();
  /* USER CODE BEGIN StartDefaultTask */
  init_task(&hspi3,RS485A_RE_GPIO_Port,RS485A_RE_Pin,&huart1,&hdma_usart1_rx,RS485B_RE_GPIO_Port,RS485B_RE_Pin,&huart6,&hdma_usart6_rx);
  /* Infinite loop */
  for(;;)
  {
    osDelay(1);
  }
  /* USER CODE END StartDefaultTask */
}

/* USER CODE BEGIN Header_StartCDCRXTask */
/**
* @brief Function implementing the cdcRXTask thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartCDCRXTask */
void StartCDCRXTask(void *argument)
{
  /* USER CODE BEGIN StartCDCRXTask */
	int ret = 0;
  /* Infinite loop */
  for(;;)
  {
  	ret = cdc_rx_loop();
  	switch(ret)
  	{
  		case 1:
  			break;
  		case 2:
  			if(((USBD_CDC_HandleTypeDef*)(hUsbDeviceFS.pClassData))->TxState == 0)
  			{
  				USBD_CDC_SetTxBuffer(&hUsbDeviceFS, _get_cdc_cmd_atok(), _get_cdc_cmd_atok_length());
  				USBD_CDC_TransmitPacket(&hUsbDeviceFS);
  				_pop_cdcrx_queue();
  				_set_cdc_mode(2);
  			}
  			else
  			{
  				error_assert(ERR_CDCTX_BUSY);
  			}
  			break;
  		case 3:
  			if(((USBD_CDC_HandleTypeDef*)(hUsbDeviceFS.pClassData))->TxState == 0)
  			{
  				USBD_CDC_SetTxBuffer(&hUsbDeviceFS, _get_cdc_cmd_atok(), _get_cdc_cmd_atok_length());
  				USBD_CDC_TransmitPacket(&hUsbDeviceFS);
  				_pop_cdcrx_queue();
  				_set_cdc_mode(1);
  			}
  			else
  			{
  				error_assert(ERR_CDCTX_BUSY);
  			}
  			break;
  		default:
  			error_assert_int(ret);
  	}

    //osDelay(1);
  }
  /* USER CODE END StartCDCRXTask */
}

/* USER CODE BEGIN Header_StartCANTXTask */
/**
* @brief Function implementing the canTXTask thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartCANTXTask */
void StartCANTXTask(void *argument)
{
  /* USER CODE BEGIN StartCANTXTask */
  /* Infinite loop */
  for(;;)
  {
  	cdc2can_tx_loop(&hcan1, &hcan2);
  	spi2can_tx_loop(&hcan1, &hcan2);
  }
  /* USER CODE END StartCANTXTask */
}

/* USER CODE BEGIN Header_StartDataRXTask */
/**
* @brief Function implementing the dataRXTask thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartDataRXTask */
void StartDataRXTask(void *argument)
{
  /* USER CODE BEGIN StartDataRXTask */
  /* Infinite loop */
  for(;;)
  {
  	data_rx_loop();
  }
  /* USER CODE END StartDataRXTask */
}

/* USER CODE BEGIN Header_StartCDCTXTask */
/**
* @brief Function implementing the cdcTXTask thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartCDCTXTask */
void StartCDCTXTask(void *argument)
{
  /* USER CODE BEGIN StartCDCTXTask */
	int ret = 0;
  /* Infinite loop */
  for(;;)
  {
  	ret = cdc_tx_loop();
  	switch(ret)
  	{
  		case 1:
  		  if(((USBD_CDC_HandleTypeDef*)(hUsbDeviceFS.pClassData))->TxState == 0)
  		  {
  		    USBD_CDC_SetTxBuffer(&hUsbDeviceFS, _get_cdctx_queue_buf(), _get_cdctx_queue_buf_size());
  		    USBD_CDC_TransmitPacket(&hUsbDeviceFS);
  		    _pop_cdctx_queue();
  		  }
  		  else
  		  {
  		  	error_assert(ERR_CDCTX_BUSY);
  		  }
  			break;
  		default:
  			error_assert_int(ret);
  	}
  }
  /* USER CODE END StartCDCTXTask */
}

/* USER CODE BEGIN Header_StartSPIRXTask */
/**
* @brief Function implementing the spiRXTask06 thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartSPIRXTask */
void StartSPIRXTask(void *argument)
{
  /* USER CODE BEGIN StartSPIRXTask */
  /* Infinite loop */
  for(;;)
  {
  	spi_rx_loop(&hcan1, &hcan2, &huart1, &huart6);
  }
  /* USER CODE END StartSPIRXTask */
}

/* USER CODE BEGIN Header_StartUSARTTXTask */
/**
* @brief Function implementing the usartTXTask thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartUSARTTXTask */
void StartUSARTTXTask(void *argument)
{
  /* USER CODE BEGIN StartUSARTTXTask */
  /* Infinite loop */
  for(;;)
  {
  	//usart_tx_loop(&huart3);
    osDelay(1);
  }
  /* USER CODE END StartUSARTTXTask */
}

/* USER CODE BEGIN Header_StartI2CRXTask */
/**
* @brief Function implementing the i2cRxTask thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartI2CRXTask */
void StartI2CRXTask(void *argument)
{
  /* USER CODE BEGIN StartI2CRXTask */
	uint8_t mpu_len = 14;
	uint8_t mpu_data[14] = {0};
  /* Infinite loop */
  for(;;)
  {
  	if(MPU_Init(&hi2c2)==0)
  	{
  		MPU_Read_Len(&hi2c2, 0x3B, mpu_len, mpu_data);
  		HAL_UART_Transmit_DMA(&huart3, mpu_data, mpu_len);
  	}
		HAL_Delay(1000);
  }
  /* USER CODE END StartI2CRXTask */
}

/* USER CODE BEGIN Header_StartADCRXTask */
/**
* @brief Function implementing the adcRXTask thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartADCRXTask */
void StartADCRXTask(void *argument)
{
  /* USER CODE BEGIN StartADCRXTask */
  for(;;)
  {
  	HAL_ADC_Start(&hadc1);//开始ADC采集
  	HAL_ADC_PollForConversion(&hadc1,500);//等待采集结束
  	// ADC传感器数据处理

  	HAL_ADC_Start(&hadc2);//开始ADC采集
  	HAL_ADC_PollForConversion(&hadc2,500);//等待采集结束
  	// ADC传感器数据处理
  	// HAL_UART_Transmit_DMA(&huart3, (uint8_t*)&value_adc, value_len);

  	HAL_Delay(1000);
  }
  /* USER CODE END StartADCRXTask */
}

/* USER CODE BEGIN Header_StartRS485ATXTask */
/**
* @brief Function implementing the rs485ATXTask thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartRS485ATXTask */
void StartRS485ATXTask(void *argument)
{
  /* USER CODE BEGIN StartRS485ATXTask */
  /* Infinite loop */
  for(;;)
  {
  	cdc2rs485a_tx_loop(&huart1, RS485A_RE_GPIO_Port, RS485A_RE_Pin);
  	spi2rs485a_tx_loop(&huart1, RS485A_RE_GPIO_Port, RS485A_RE_Pin);
  }
  /* USER CODE END StartRS485ATXTask */
}

/* USER CODE BEGIN Header_StartRS485BTXTask */
/**
* @brief Function implementing the rs485BTXTask thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartRS485BTXTask */
void StartRS485BTXTask(void *argument)
{
  /* USER CODE BEGIN StartRS485BTXTask */
	/* Infinite loop */
  for(;;)
  {
  	cdc2rs485b_tx_loop(&huart6, RS485B_RE_GPIO_Port, RS485B_RE_Pin);
  	spi2rs485b_tx_loop(&huart6, RS485B_RE_GPIO_Port, RS485B_RE_Pin);
  }
  /* USER CODE END StartRS485BTXTask */
}

/* Private application code --------------------------------------------------*/
/* USER CODE BEGIN Application */

/* USER CODE END Application */

