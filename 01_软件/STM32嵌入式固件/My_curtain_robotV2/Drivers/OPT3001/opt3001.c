#include "opt3001.h"




//void OPT3001_Config(void)
//{
//  I2C_OPT3001_WriteByte(Config_Address, OPT3001_Config_Data);
//  //下面两句设置OPT3001的上限和下限，超出之后会触发INT中断，如果是单片机主动查询，则不需要配置
//	I2C_OPT3001_WriteByte(Low_Limit_Address, OPT3001_Limit_10lx);
//	I2C_OPT3001_WriteByte(Hight_Limit_Address, OPT3001_Limit_150lx);
//}



//static uint8_t   SHT30_Send_Cmd(uint16_t cmd)
//{
//    uint8_t cmd_buffer[2];
//    cmd_buffer[0] = cmd >> 8;
//    cmd_buffer[1] = cmd;
//    return HAL_I2C_Master_Transmit(&hi2c1, SHT30_ADDR_WRITE, (uint8_t*)cmd_buffer, 2, 0xFFFF);
//}


/**
 * @brief    从SHT30读取一次数据
 * @param    dat —— 存储读取数据的地址（6个字节数组）
 * @retval    成功 —— 返回HAL_OK
*/
uint8_t OPT_Read_ID(uint8_t* dat)
{
//	 I2C_OPT3001_WriteByte(Config_Address, OPT3001_Config_Data);
//  //下面两句设置OPT3001的上限和下限，超出之后会触发INT中断，如果是单片机主动查询，则不需要配置
//	I2C_OPT3001_WriteByte(Low_Limit_Address, OPT3001_Limit_10lx);
//	I2C_OPT3001_WriteByte(Hight_Limit_Address, OPT3001_Limit_150lx);
                             // I2C_MEMADD_SIZE_16BIT
	//HAL_StatusTypeDef HAL_I2C_Mem_Write(I2C_HandleTypeDef *hi2c, uint16_t DevAddress, uint16_t MemAddress, uint16_t MemAddSize, uint8_t *pData, uint16_t Size, uint32_t Timeout)
  //  uint8_t   test[2] = {}
	
	
	if(HAL_OK ==  HAL_I2C_Mem_Write(&hi2c1,0x88,0x01,I2C_MEMADD_SIZE_8BIT,(uint8_t *)OPT3001_Config_Data,2,0xFFFF))
	{
	  printf("write ok\r\n");
	}
	if(HAL_OK ==  HAL_I2C_Mem_Read(&hi2c1,0x88,0x00,I2C_MEMADD_SIZE_16BIT,dat,2,0xFFFF))
	{
	  printf("Read ok\r\n");
	}else printf("Read Error\r\n");
}