#pragma once

#include "types.h"

typedef struct {
    io_rw_32 CR;
    io_rw_32 SR;
    io_ro_32 DR;
} RNG_t;

#define RNG ((RNG_t *)0x40023C00)
