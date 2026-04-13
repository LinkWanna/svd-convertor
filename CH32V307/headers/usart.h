#pragma once

#include "types.h"

typedef struct {
    io_rw_32 STATR;
    io_rw_32 DATAR;
    io_rw_32 BRR;
    io_rw_32 CTLR[3];
    io_rw_32 GPR;
} USART_t;

#define UART6 ((USART_t *)0x40001800)
#define UART7 ((USART_t *)0x40001C00)
#define UART8 ((USART_t *)0x40002000)
#define USART2 ((USART_t *)0x40004400)
#define USART3 ((USART_t *)0x40004800)
#define UART4 ((USART_t *)0x40004C00)
#define UART5 ((USART_t *)0x40005000)
#define USART1 ((USART_t *)0x40013800)
