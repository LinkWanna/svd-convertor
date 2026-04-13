#pragma once

#include "types.h"

typedef struct {
    io_rw_32 CTLR[2];
    io_rw_32 STATR;
    io_rw_32 DATAR;
    io_rw_32 CRCR;
    io_ro_32 RCRCR;
    io_ro_32 TCRCR;
    io_rw_32 I2SCFGR;
    io_rw_32 I2SPR;
    io_rw_32 HSCR;
} SPI2_t;

typedef struct {
    io_rw_32 CTLR[2];
    io_rw_32 STATR;
    io_rw_32 DATAR;
    io_rw_32 CRCR;
    io_ro_32 RCRCR;
    io_ro_32 TCRCR;
    io_rw_32 SPI_I2S_CFGR;
    uint8_t _reserved_0[0x4];
    io_rw_32 HSCR;
} SPI1_t;

#define SPI2 ((SPI2_t *)0x40003800)
#define SPI3 ((SPI2_t *)0x40003C00)
#define SPI1 ((SPI1_t *)0x40013000)
