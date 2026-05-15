#ifndef __OPT3001_H
#define __OPT3001_H

#include "i2c.h"
#include "usart.h"

#define OPT3001_Address              0x88
#define Result_Address      		 0x00
#define Config_Address        		 0x01
#define Low_Limit_Address     		 0x02
#define Hight_Limit_Address   		 0x03
#define MANUFACTURER_ID_Address    0x7E
#define DEVICE_ID_Address          0x7F

#define OPT3001_Config_Data        0xCE10  //每800ms采集一次数据
//#define OPT3001_Config_Data        0xC410  //每100ms采集一次数据
#define OPT3001_Limit_10lx         0x03E8
#define OPT3001_Limit_20lx         0x07D0
#define OPT3001_Limit_30lx         0x0BB8
#define OPT3001_Limit_40lx         0x0FA0
#define OPT3001_Limit_50lx         0x1338
#define OPT3001_Limit_60lx         0x1770
#define OPT3001_Limit_70lx         0x1B58
#define OPT3001_Limit_80lx         0x1F40
#define OPT3001_Limit_90lx         0x2328
#define OPT3001_Limit_100lx        0x2710
#define OPT3001_Limit_110lx        0x2AF8
#define OPT3001_Limit_120lx        0x2EE0
#define OPT3001_Limit_130lx        0x3C20
#define OPT3001_Limit_140lx        0x36B0
#define OPT3001_Limit_150lx        0x3A98
#define OPT3001_Limit_200lx        0x4E20
#define OPT3001_Limit_250lx        0x61A8

#define OPT3001_MANUFACTURER_ID    0x5449
#define OPT3001_DEVICE_ID          0x3001




uint8_t OPT_Read_ID(uint8_t* dat);



#endif

