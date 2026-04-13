#pragma once

#include "types.h"

typedef struct {
    io_rw_32 CTLR;
    io_wo_32 SWTR;
    io_rw_32 R12BDHR1;
    io_rw_32 L12BDHR1;
    io_rw_32 R8BDHR1;
    io_rw_32 R12BDHR2;
    io_rw_32 L12BDHR2;
    io_rw_32 R8BDHR2;
    io_rw_32 RD12BDHR;
    io_rw_32 LD12BDHR;
    io_rw_32 RD8BDHR;
    io_ro_32 DOR[2];
} DAC_t;

#define DAC ((DAC_t *)0x40007400)
