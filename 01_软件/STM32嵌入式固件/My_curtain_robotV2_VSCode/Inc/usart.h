/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    usart.h
  * @brief   This file contains all the function prototypes for
  *          the usart.c file
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2026 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __USART_H__
#define __USART_H__

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* USER CODE BEGIN Includes */
#include "stdio.h"
#include "string.h"
#include "wakeup.h"
/* USER CODE END Includes */

extern UART_HandleTypeDef huart1;

extern UART_HandleTypeDef huart2;

/* USER CODE BEGIN Private defines */
#define USART2_DMA_REC_SIE 256
#define USART2_REC_SIE 512
    typedef struct 
    {   
		uint8_t UsartRecFlag;   //���ݽ��յ���־λ
        uint16_t UsartDMARecLen; //DMA���ܳ���
        uint16_t UsartRecLen;    //�������ݳ���
        uint8_t  Usart2DMARecBuffer[USART2_DMA_REC_SIE];  //DMAbuffer
        uint8_t  Usart2RecBuffer[USART2_REC_SIE];         //���ݴ���buffer
    } teUsart2type;
extern teUsart2type Usart2type;  //�ṹ��ȫ�ֶ���



/* USER CODE END Private defines */

void MX_USART1_UART_Init(void);
void MX_USART2_UART_Init(void);

/* USER CODE BEGIN Prototypes */
void EnableUsart_IT(void);
/* USER CODE END Prototypes */

#ifdef __cplusplus
}
#endif

#endif /* __USART_H__ */

