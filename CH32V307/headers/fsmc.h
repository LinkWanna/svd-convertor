#pragma once

#include "types.h"

typedef struct {
    io_rw_32 BCR1;
    io_rw_32 BTR1;
    uint8_t _reserved_0[0x58];
    io_rw_32 PCR2;
    io_rw_32 SR2;
    io_rw_32 PMEM2;
    io_rw_32 PATT2;
    uint8_t _reserved_1[0x4];
    io_ro_32 ECCR2;
    uint8_t _reserved_2[0x8C];
    io_rw_32 BWTR1;
} FSMC_t;

#define FSMC ((FSMC_t *)0xA0000000)
