#pragma once

#include "types.h"

typedef struct {
    io_rw_32 CFGR[2];
} DBG_t;

#define DBG ((DBG_t *)0xE000D000)
