#pragma once

#include "types.h"

typedef struct {
    io_rw_32 DATAR;
    io_rw_32 IDATAR;
    io_wo_32 CTLR;
} CRC_t;

#define CRC ((CRC_t *)0x40023000)
