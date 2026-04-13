#pragma once

#include "types.h"

typedef struct {
    uint8_t _reserved_0[0x4];
    io_wo_32 KEYR;
    io_wo_32 OBKEYR;
    io_rw_32 STATR;
    io_rw_32 CTLR;
    io_wo_32 ADDR;
    uint8_t _reserved_1[0x4];
    io_ro_32 OBR;
    io_ro_32 WPR;
    io_wo_32 MODEKEYR;
} FLASH_t;

#define FLASH ((FLASH_t *)0x40022000)
