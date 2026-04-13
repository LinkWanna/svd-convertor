#pragma once

#include "types.h"

typedef struct {
    io_rw_32 CFGLR;
    io_rw_32 CFGHR;
    io_ro_32 INDR;
    io_rw_32 OUTDR;
    io_wo_32 BSHR;
    io_wo_32 BCR;
    io_rw_32 LCKR;
} GPIO_t;

#define GPIOA ((GPIO_t *)0x40010800)
#define GPIOB ((GPIO_t *)0x40010C00)
#define GPIOC ((GPIO_t *)0x40011000)
#define GPIOD ((GPIO_t *)0x40011400)
#define GPIOE ((GPIO_t *)0x40011800)
