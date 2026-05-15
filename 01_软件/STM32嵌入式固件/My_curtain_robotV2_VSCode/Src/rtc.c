/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    rtc.c
  * @brief   This file provides code for the configuration
  *          of the RTC instances.
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
/* Includes ------------------------------------------------------------------*/
#include "rtc.h"

/* USER CODE BEGIN 0 */
#include "stdio.h"
#include "string.h"
RTC_DateTypeDef sdatestructure;
RTC_TimeTypeDef stimestructure;
/* USER CODE END 0 */

RTC_HandleTypeDef hrtc;

/* RTC init function */
void MX_RTC_Init(void)
{

  /* USER CODE BEGIN RTC_Init 0 */

  /* USER CODE END RTC_Init 0 */

  RTC_TimeTypeDef sTime = {0};
  RTC_DateTypeDef sDate = {0};

  /* USER CODE BEGIN RTC_Init 1 */

  /* USER CODE END RTC_Init 1 */

  /** Initialize RTC Only
  */
  hrtc.Instance = RTC;
  hrtc.Init.HourFormat = RTC_HOURFORMAT_24;
  hrtc.Init.AsynchPrediv = 127;
  hrtc.Init.SynchPrediv = 289;
  hrtc.Init.OutPut = RTC_OUTPUT_DISABLE;
  hrtc.Init.OutPutRemap = RTC_OUTPUT_REMAP_NONE;
  hrtc.Init.OutPutPolarity = RTC_OUTPUT_POLARITY_HIGH;
  hrtc.Init.OutPutType = RTC_OUTPUT_TYPE_OPENDRAIN;
  if (HAL_RTC_Init(&hrtc) != HAL_OK)
  {
    Error_Handler();
  }

  /* USER CODE BEGIN Check_RTC_BKUP */

  /* USER CODE END Check_RTC_BKUP */

  /** Initialize RTC and set the Time and Date
  */
  sTime.Hours = 0x0;
  sTime.Minutes = 0x0;
  sTime.Seconds = 0x0;
  sTime.DayLightSaving = RTC_DAYLIGHTSAVING_NONE;
  sTime.StoreOperation = RTC_STOREOPERATION_RESET;
  if (HAL_RTC_SetTime(&hrtc, &sTime, RTC_FORMAT_BCD) != HAL_OK)
  {
    Error_Handler();
  }
  sDate.WeekDay = RTC_WEEKDAY_MONDAY;
  sDate.Month = RTC_MONTH_JANUARY;
  sDate.Date = 0x1;
  sDate.Year = 0x0;

  if (HAL_RTC_SetDate(&hrtc, &sDate, RTC_FORMAT_BCD) != HAL_OK)
  {
    Error_Handler();
  }

  /** Enable the WakeUp
  */
  if (HAL_RTCEx_SetWakeUpTimer_IT(&hrtc, 0, RTC_WAKEUPCLOCK_CK_SPRE_16BITS) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN RTC_Init 2 */

  /* USER CODE END RTC_Init 2 */

}

void HAL_RTC_MspInit(RTC_HandleTypeDef* rtcHandle)
{

  if(rtcHandle->Instance==RTC)
  {
  /* USER CODE BEGIN RTC_MspInit 0 */

  /* USER CODE END RTC_MspInit 0 */
    /* RTC clock enable */
    __HAL_RCC_RTC_ENABLE();

    /* RTC interrupt Init */
    HAL_NVIC_SetPriority(RTC_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(RTC_IRQn);
  /* USER CODE BEGIN RTC_MspInit 1 */

  /* USER CODE END RTC_MspInit 1 */
  }
}

void HAL_RTC_MspDeInit(RTC_HandleTypeDef* rtcHandle)
{

  if(rtcHandle->Instance==RTC)
  {
  /* USER CODE BEGIN RTC_MspDeInit 0 */

  /* USER CODE END RTC_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_RTC_DISABLE();

    /* RTC interrupt Deinit */
    HAL_NVIC_DisableIRQ(RTC_IRQn);
  /* USER CODE BEGIN RTC_MspDeInit 1 */

  /* USER CODE END RTC_MspDeInit 1 */
  }
}

/* USER CODE BEGIN 1 */
uint32_t time2Stamp(void)    //����ʱ��תʱ���
{
    uint32_t result = 0;
    uint16_t Year = 0;
    //const uint8_t Days[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    const uint16_t monDays[12] = {0,31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334};
    /* Get the RTC current Time ,must get time first*/
    HAL_RTC_GetTime(&hrtc, &stimestructure, RTC_FORMAT_BIN);
    /* Get the RTC current Date */
    HAL_RTC_GetDate(&hrtc, &sdatestructure, RTC_FORMAT_BIN);
    /* Display date Format : yy/mm/dd */
    printf("%02d/%02d/%02d\r\n",2000 + sdatestructure.Year, sdatestructure.Month, sdatestructure.Date);
    /* Display time Format : hh:mm:ss */
    printf("%02d:%02d:%02d\r\n",stimestructure.Hours, stimestructure.Minutes, stimestructure.Seconds);

    Year=sdatestructure.Year+2000;
    result = (Year - 1970) * 365 * 24 * 3600 + (monDays[sdatestructure.Month-1] + sdatestructure.Date - 1) * 24 * 3600 + (stimestructure.Hours-8) * 3600 + stimestructure.Minutes * 60 + stimestructure.Seconds;
    printf("[%u]",result);
    result += (sdatestructure.Month>2 && (Year % 4 == 0) && (Year % 100 != 0 || Year % 400 == 0))*24*3600;	//����
    printf("[%u]",result);
    Year -= 1970;
    result += (Year/4 - Year/100 + Year/400)*24 * 3600;		  //����
    printf("[%u]",result);
    printf("ʱ���Success\r\n");
    return result;
}
void Calibration_Times(char * Time_buf)
{
    struct tm *gm_date;
    uint8_t RTC_Buf[6]= {0};
    RTC_TimeTypeDef sTime = {0};
    RTC_DateTypeDef sDate = {0};
    time_t time_buf = (time_t)atoll((char *)Time_buf);
    gm_date = localtime(&time_buf);
    RTC_Buf[0] = gm_date->tm_year-100;
    RTC_Buf[1] = gm_date->tm_mon+1;
    RTC_Buf[2] = gm_date->tm_mday;
    RTC_Buf[3] = gm_date->tm_hour+8;
    RTC_Buf[4] = gm_date->tm_min;
    RTC_Buf[5] = gm_date->tm_sec;
    HAL_PWR_EnableBkUpAccess();
    if(HAL_RTCEx_BKUPRead(&hrtc, RTC_BKP_DR1)!=0x3050) //�Ƿ��һ������
    {
        HAL_RTCEx_BKUPWrite(&hrtc, RTC_BKP_DR1, 0x5050);
        sTime.Hours = RTC_Buf[3];
        sTime.Minutes = RTC_Buf[4];
        sTime.Seconds = RTC_Buf[5];
        if (HAL_RTC_SetTime(&hrtc, &sTime, RTC_FORMAT_BIN) != HAL_OK)
        {
            printf("Calibration_Times error...\r\n");
            Error_Handler();
        }
        sDate.WeekDay = RTC_WEEKDAY_MONDAY;
        sDate.Month = RTC_Buf[1];
        sDate.Date = RTC_Buf[2];
        sDate.Year = RTC_Buf[0];
        if (HAL_RTC_SetDate(&hrtc, &sDate, RTC_FORMAT_BIN) != HAL_OK)
        {
            printf("Calibration_Times error...\r\n");
            Error_Handler();
        }
    }
    printf("Calibration_Times success...\r\n");
}

void RTC_Time_Config(uint32_t stoptime)
{
    printf("into_sleep_mode\r\nwill sleep %d s\r\n",stoptime);
    if(HAL_RTCEx_DeactivateWakeUpTimer(&hrtc) != HAL_OK)
    {
        /*Initialization Error*/
		 printf("RTC wakeUP error\r\n");
        Error_Handler();
    }
    /*## Setting the Wake up time ############################################*/
    HAL_RTCEx_SetWakeUpTimer_IT(&hrtc, stoptime, RTC_WAKEUPCLOCK_RTCCLK_DIV16);  //����Ϊ20S  RTC_WAKEUPCLOCK_RTCCLK_DIV16 RTC_WAKEUPCLOCK_CK_SPRE_16BITS
}

/* USER CODE END 1 */
