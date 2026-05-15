#ifndef _WAKEUP_H
#define _WAKEUP_H

#include "main.h"
extern uint8_t Sleep_Flag ;

void SystemPower_Config(void);
void SystemClockConfig_STOP(void);
void RTC_Time_Config(uint32_t stoptime);
void reset_wake_up(void);


#endif


