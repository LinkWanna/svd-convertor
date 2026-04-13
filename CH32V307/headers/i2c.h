#pragma once

#include "types.h"

typedef struct {
    io_rw_32 CTLR[2];
    io_rw_32 OADDR[2];
    io_rw_32 DATAR;
    io_rw_32 STAR1;
    io_ro_32 STAR2;
    io_rw_32 CKCFGR;
    io_rw_32 RTR;
} I2C_t;

#define I2C1 ((I2C_t *)0x40005400)
#define I2C2 ((I2C_t *)0x40005800)
