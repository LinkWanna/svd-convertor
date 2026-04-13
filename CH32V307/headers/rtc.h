#pragma once

#include "types.h"

typedef struct {
    io_rw_32 CTLRH;
    io_rw_32 CTLRL;
    io_wo_32 PSCRH;
    io_wo_32 PSCRL;
    io_ro_32 DIVH;
    io_ro_32 DIVL;
    io_rw_32 CNTH;
    io_rw_32 CNTL;
    io_wo_32 ALRMH;
    io_wo_32 ALRML;
} RTC_t;

#define RTC ((RTC_t *)0x40002800)
