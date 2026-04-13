#pragma once

#include "types.h"

typedef struct {
    io_rw_32 CR;
} OPA_t;

#define OPA ((OPA_t *)0x40023804)
