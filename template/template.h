#pragma once

#include "common.h"

typedef struct {
    io_rw_8 a;
    io_ro_8 b;
    io_wo_8 c;
    io_rw_16 d;
    io_ro_16 e;
    io_wo_16 f;
    io_rw_32 g;
    io_ro_32 h;
    io_wo_32 i;
    io_rw_64 j;
    io_ro_64 k;
    io_wo_64 l;

    ioptr m;
    const_ioptr n;
} template_t;

#define template1 ((template_t *)0x40000000)
#define template2 ((template_t *)0x40000000)
