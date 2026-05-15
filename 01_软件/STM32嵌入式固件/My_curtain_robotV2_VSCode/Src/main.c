/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "adc.h"
#include "dma.h"
#include "i2c.h"
#include "rtc.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "opt3001.h"
#include "wakeup.h"
#include "my_string.h"
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

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */
    uint8_t Find_flag =0;
    uint8_t Time_buf[20];
    uint32_t start_time = 0;
    uint32_t end_time = 0;
    uint32_t worktime = 0;
  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_USART1_UART_Init();
  MX_USART2_UART_Init();
  MX_I2C1_Init();
  MX_RTC_Init();
  MX_ADC_Init();
  /* USER CODE BEGIN 2 */
    printf("################\r\n");
    EnableUsart_IT();
//	OPT_Read_ID(recv_dat);

//��������״̬
    HAL_GPIO_WritePin(BT_EN_GPIO_Port, BT_EN_Pin, GPIO_PIN_SET);         //�½��ػ��� 1-->0
    HAL_Delay(1000);
    HAL_GPIO_WritePin(BT_EN_GPIO_Port, BT_EN_Pin, GPIO_PIN_RESET);
    HAL_Delay(1000);   //10��ʱ�� �ֻ�APP����������������������������
    printf("will deep sleep\r\n");
    time2Stamp();
//��������״̬      �ֻ�APP������������������������
    HAL_GPIO_WritePin(BT_EN_GPIO_Port, BT_EN_Pin, GPIO_PIN_RESET);       //����������  0-->1
    HAL_Delay(1000);
    HAL_GPIO_WritePin(BT_EN_GPIO_Port, BT_EN_Pin, GPIO_PIN_SET);
    HAL_Delay(1000);
//  ���Ե͹��ģ�
    //RTC_Time_Config(10000); //�Ȼ����ⲿ�����ٲ��Զ�ʱ�⹦�ܰ�
    SystemPower_Config();   //���õ͹���ģʽ��GPIO��أ�
    HAL_PWR_EnterSTOPMode(PWR_LOWPOWERREGULATOR_ON, PWR_STOPENTRY_WFI); //����STOP�͹���ģʽ
    SystemClockConfig_STOP(); //�ָ�����ʱ��
    printf("WearkUP------>\r\n");
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
    while (1)
    {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
//        printf("SEND------>\r\n");
        if(Usart2type.UsartRecFlag ==1)
        {
            Usart2type.UsartRecFlag = 0;
            if( strstr((char *)Usart2type.Usart2RecBuffer,"ON") != NULL ) //����ָ��
            {
                memset(Usart2type.Usart2RecBuffer, 0x00, sizeof(Usart2type.Usart2RecBuffer)); //����ջ�����
                printf("@@@@@@@@@@@@@@@@@\r\n");
                if(worktime != 0)  //������ʱ��
                {
                    HAL_GPIO_WritePin(GPIOB, NSLEEP_Pin, GPIO_PIN_SET);  //�ر���������
                    HAL_GPIO_WritePin(GPIOB, N_IN1_Pin, GPIO_PIN_SET);   //����
                    HAL_GPIO_WritePin(GPIOB, N_IN2_Pin, GPIO_PIN_RESET);
					HAL_Delay(worktime); //����ʱ��
					HAL_GPIO_WritePin(GPIOB, N_IN1_Pin, GPIO_PIN_SET);   //ɲ��
                    HAL_GPIO_WritePin(GPIOB, N_IN2_Pin, GPIO_PIN_SET);
                    HAL_GPIO_WritePin(GPIOB, NSLEEP_Pin, GPIO_PIN_RESET);  //������������
                    HAL_GPIO_WritePin(GPIOB, N_IN2_Pin, GPIO_PIN_RESET);   //�ر���� ���͹���
                    HAL_GPIO_WritePin(GPIOB, N_IN1_Pin, GPIO_PIN_RESET);   //�ر���� ���͹���
                }
            }
            if( strstr((char *)Usart2type.Usart2RecBuffer,"OFF") != NULL ) //�ر�ָ��
            {
                printf("&&&&&&&&&&&&&&&&&&\r\n");
                memset(Usart2type.Usart2RecBuffer, 0x00, sizeof(Usart2type.Usart2RecBuffer)); //����ջ�����
                if(worktime != 0)  //������ʱ��
                {
                   HAL_GPIO_WritePin(GPIOB, NSLEEP_Pin, GPIO_PIN_SET);   //�ر���������
                    HAL_GPIO_WritePin(GPIOB, N_IN1_Pin, GPIO_PIN_RESET);   //������
                    HAL_GPIO_WritePin(GPIOB, N_IN2_Pin, GPIO_PIN_SET);
					HAL_Delay(worktime); //����ʱ��
					HAL_GPIO_WritePin(GPIOB, N_IN1_Pin, GPIO_PIN_SET);   //ɲ��
                    HAL_GPIO_WritePin(GPIOB, N_IN2_Pin, GPIO_PIN_SET);
                    HAL_GPIO_WritePin(GPIOB, NSLEEP_Pin, GPIO_PIN_RESET);  //������������
                    HAL_GPIO_WritePin(GPIOB, N_IN2_Pin, GPIO_PIN_RESET);   //�ر���� ���͹���
                    HAL_GPIO_WritePin(GPIOB, N_IN1_Pin, GPIO_PIN_RESET);   //�ر���� ���͹���
                    //MCU ��������
                    time2Stamp();
                    SystemPower_Config();   //���õ͹���ģʽ��GPIO��أ�
                    HAL_PWR_EnterSTOPMode(PWR_LOWPOWERREGULATOR_ON, PWR_STOPENTRY_WFI); //����STOP�͹���ģʽ
                }
            }
            if( strstr((char *)Usart2type.Usart2RecBuffer,"S") != NULL ) //��ʼ��ʱ��ָ��
            {
                if( strstr((char *)Usart2type.Usart2RecBuffer,"T") != NULL )
                {
                    memset(Time_buf, 0x00, sizeof(Time_buf)); //����ջ�����
                    Find_flag =  Find_string((char *)Usart2type.Usart2RecBuffer,"S","T",(char *)Time_buf);
                    printf("time: %s,%lu",Time_buf,(unsigned long)atoi((char *)Time_buf));
                    if(Find_flag) {
                        Calibration_Times((char *)Time_buf);
                    }
                }
                memset(Usart2type.Usart2RecBuffer, 0x00, sizeof(Usart2type.Usart2RecBuffer)); //����ջ�����
            }
            // HAL_GetTick();    //��ȡϵͳ����ʱ��   uint32_t
            if( strstr((char *)Usart2type.Usart2RecBuffer,"C") != NULL ) //��ʼ��ʱ��ָ��
            {
                if(start_time == 0) //��һ�γ�ʼ��
                {
                    start_time = HAL_GetTick();
                    HAL_GPIO_WritePin(GPIOB, NSLEEP_Pin, GPIO_PIN_SET);  //�ر���������
//                HAL_Delay(500);
                    HAL_GPIO_WritePin(GPIOB, N_IN1_Pin, GPIO_PIN_SET);   //����
                    HAL_GPIO_WritePin(GPIOB, N_IN2_Pin, GPIO_PIN_RESET);
                } else
                {
                    HAL_GPIO_WritePin(GPIOB, N_IN1_Pin, GPIO_PIN_SET);   //ɲ��
                    HAL_GPIO_WritePin(GPIOB, N_IN2_Pin, GPIO_PIN_SET);

                    HAL_GPIO_WritePin(GPIOB, NSLEEP_Pin, GPIO_PIN_RESET);  //������������
                    HAL_GPIO_WritePin(GPIOB, N_IN2_Pin, GPIO_PIN_RESET);   //�ر���� ���͹���
                    HAL_GPIO_WritePin(GPIOB, N_IN1_Pin, GPIO_PIN_RESET);   //�ر���� ���͹���
                    end_time = HAL_GetTick();
                    worktime = end_time-start_time;
                    start_time = 0;
                    end_time = 0;
                    printf("worktime:%lu\r\n",(unsigned long)worktime);
                }
                memset(Usart2type.Usart2RecBuffer, 0x00, sizeof(Usart2type.Usart2RecBuffer)); //����ջ�����
            }


        }
        HAL_Delay(50);
    }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI|RCC_OSCILLATORTYPE_LSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.LSIState = RCC_LSI_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_USART1|RCC_PERIPHCLK_USART2
                              |RCC_PERIPHCLK_I2C1|RCC_PERIPHCLK_RTC;
  PeriphClkInit.Usart1ClockSelection = RCC_USART1CLKSOURCE_PCLK2;
  PeriphClkInit.Usart2ClockSelection = RCC_USART2CLKSOURCE_PCLK1;
  PeriphClkInit.I2c1ClockSelection = RCC_I2C1CLKSOURCE_PCLK1;
  PeriphClkInit.RTCClockSelection = RCC_RTCCLKSOURCE_LSI;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */





/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
    /* User can add his own implementation to report the HAL error return state */

  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
    /* User can add his own implementation to report the file name and line number,
       tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
