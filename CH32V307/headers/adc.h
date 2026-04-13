#pragma once

#include "types.h"

typedef struct {
    io_rw_32 STATR;
    io_rw_32 CTLR[2];
    io_rw_32 SAMPTR1_CHARGE1;
    io_rw_32 SAMPTR2_CHARGE2;
    io_rw_32 IOFR[4];
    io_rw_32 WDHTR;
    io_rw_32 WDLTR;
    io_rw_32 RSQR[2];
    io_rw_32 RSQR3__CHANNEL;
    io_rw_32 ISQR;
    io_ro_32 IDATAR1_CHGOFFSET;
    io_ro_32 IDATAR2;
    io_ro_32 IDATAR3;
    io_ro_32 IDATAR4;
    io_rw_32 RDATAR_DR_ACT_DCG;
} ADC_t;

#define ADC2 ((ADC_t *)0x40012800)
