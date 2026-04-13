#pragma once

#include "types.h"

typedef struct {
    io_rw_32 CTLR;
    io_rw_32 CFGR;
    io_rw_32 STATR;
} WWDG_t;

#define WWDG ((WWDG_t *)0x40002C00)
