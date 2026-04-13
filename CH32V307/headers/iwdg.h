#pragma once

#include "types.h"

typedef struct {
    io_wo_32 CTLR;
    io_rw_32 PSCR;
    io_rw_32 RLDR;
    io_ro_32 STATR;
} IWDG_t;

#define IWDG ((IWDG_t *)0x40003000)
