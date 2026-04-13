#pragma once

#include "types.h"

typedef struct {
    io_rw_32 CTLR;
    io_rw_32 CFGR0;
    io_rw_32 INTR;
    io_rw_32 APB2PRSTR;
    io_rw_32 APB1PRSTR;
    io_rw_32 AHBPCENR;
    io_rw_32 APB2PCENR;
    io_rw_32 APB1PCENR;
    io_rw_32 BDCTLR;
    io_rw_32 RSTSCKR;
    io_rw_32 AHBRSTR;
    io_rw_32 CFGR2;
} RCC_t;

#define RCC ((RCC_t *)0x40021000)
