#pragma once

#include "types.h"

typedef struct {
    io_rw_32 POWER;
    io_rw_32 CLKCR;
    io_rw_32 ARG;
    io_rw_32 CMD;
    io_ro_32 RESPCMD;
    io_ro_32 RESP[4];
    io_rw_32 DTIMER;
    io_rw_32 DLEN;
    io_rw_32 DCTRL;
    io_ro_32 DCOUNT;
    io_ro_32 STA;
    io_rw_32 ICR;
    io_rw_32 MASK;
    uint8_t _reserved_0[0x8];
    io_ro_32 FIFOCNT;
    uint8_t _reserved_1[0x34];
    io_rw_32 FIFO;
} SDIO_t;

#define SDIO ((SDIO_t *)0x40018000)
