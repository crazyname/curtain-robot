#ifndef __my_string_h
#define __my_string_h
#include "string.h"
#include <ctype.h>
#include <stdlib.h>
#include "usart.h"

int find_end(char * usart_buffer, int number);
int Find_string(char *pcBuf,char *left,char *right, char *pcRes);
void smart_array(unsigned char* addr,unsigned char *ip);
#endif

