#pragma once

#include "types.h"

typedef struct {
    io_ro_32 ISR[4];
    uint8_t _reserved_0[0x10];
    io_ro_32 IPR[4];
    uint8_t _reserved_1[0x10];
    io_rw_32 ITHRESDR;
    uint8_t _reserved_2[0x4];
    io_rw_32 CFGR;
    io_ro_32 GISR;
    io_rw_32 VTFIDR;
    uint8_t _reserved_3[0xC];
    io_rw_32 VTFADDRR[4];
    uint8_t _reserved_4[0x90];
    io_wo_32 IENR[4];
    uint8_t _reserved_5[0x70];
    io_wo_32 IRER[4];
    uint8_t _reserved_6[0x70];
    io_wo_32 IPSR[4];
    uint8_t _reserved_7[0x70];
    io_wo_32 IPRR[4];
    uint8_t _reserved_8[0x70];
    io_wo_32 IACTR[4];
    uint8_t _reserved_9[0xF0];
    io_rw_8 IPRIOR[256];
    uint8_t _reserved_10[0x810];
    io_rw_32 SCTLR;
    uint8_t _reserved_11[0x2EC];
    io_rw_32 STK_CTLR;
    io_rw_32 STK_SR;
    io_rw_32 STK_CNTL;
    io_rw_32 STK_CNTH;
    io_rw_32 STK_CMPLR;
    io_rw_32 STK_CMPHR;
} PFIC_t;

#define PFIC ((PFIC_t *)0xE000E000)
