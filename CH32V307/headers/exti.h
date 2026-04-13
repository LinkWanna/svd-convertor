#pragma once

#include "types.h"

typedef struct {
    io_rw_32 INTENR;
    io_rw_32 EVENR;
    io_rw_32 RTENR;
    io_rw_32 FTENR;
    io_rw_32 SWIEVR;
    io_rw_32 INTFR;
} EXTI_t;

#define EXTI ((EXTI_t *)0x40010400)
