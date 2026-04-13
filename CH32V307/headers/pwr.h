#pragma once

#include "types.h"

typedef struct {
    io_rw_32 CTLR;
    io_rw_32 CSR;
} PWR_t;

#define PWR ((PWR_t *)0x40007000)
