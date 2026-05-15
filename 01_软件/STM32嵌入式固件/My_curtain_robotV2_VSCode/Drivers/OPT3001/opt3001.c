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
	HAL_StatusTypeDef status;
	uint8_t config_data[2] = {
		(uint8_t)(OPT3001_Config_Data >> 8),
		(uint8_t)(OPT3001_Config_Data & 0xFF)
	};
//	 I2C_OPT3001_WriteByte(Config_Address, OPT3001_Config_Data);
//  //下面两句设置OPT3001的上限和下限，超出之后会触发INT中断，如果是单片机主动查询，则不需要配置
//	I2C_OPT3001_WriteByte(Low_Limit_Address, OPT3001_Limit_10lx);
//	I2C_OPT3001_WriteByte(Hight_Limit_Address, OPT3001_Limit_150lx);
                             // I2C_MEMADD_SIZE_16BIT
	//HAL_StatusTypeDef HAL_I2C_Mem_Write(I2C_HandleTypeDef *hi2c, uint16_t DevAddress, uint16_t MemAddress, uint16_t MemAddSize, uint8_t *pData, uint16_t Size, uint32_t Timeout)
  //  uint8_t   test[2] = {}
	
	
	status = HAL_I2C_Mem_Write(&hi2c1, OPT3001_Address, Config_Address, I2C_MEMADD_SIZE_8BIT, config_data, sizeof(config_data), 0xFFFF);
	if(HAL_OK == status)
	{
	  printf("write ok\r\n");
	}
	else
	{
	  printf("Write Error\r\n");
	  return (uint8_t)status;
	}
	status = HAL_I2C_Mem_Read(&hi2c1, OPT3001_Address, Result_Address, I2C_MEMADD_SIZE_8BIT, dat, 2, 0xFFFF);
	if(HAL_OK == status)
	{
	  printf("Read ok\r\n");
	}
	else
	{
	  printf("Read Error\r\n");
	}
	return (uint8_t)status;
}