#pragma once

#include "types.h"

typedef struct {
    io_rw_8 CR[2];
    io_rw_8 IER;
    uint8_t _reserved_0[0x1];
    io_rw_16 ROW_NUM;
    io_rw_16 COL_NUM;
    io_rw_32 DMA_BUF[2];
    io_rw_8 IFR;
    io_ro_8 STATUS;
    uint8_t _reserved_1[0x2];
    io_ro_16 ROW_CNT;
    uint8_t _reserved_2[0x2];
    io_rw_16 HOFFCNT;
    io_rw_16 VST;
    io_rw_16 CAPCNT;
    io_rw_16 VLINE;
    io_ro_32 DR;
} DVP_t;

#define DVP ((DVP_t *)0x50050000)
