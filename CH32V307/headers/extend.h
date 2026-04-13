#pragma once

#include "types.h"

typedef struct {
    io_rw_32 EXTEND_CTR;
} EXTEND_t;

#define EXTEND ((EXTEND_t *)0x40023800)
