#pragma once

#include "types.h"

typedef struct {
    io_rw_32 ECR;
    io_rw_32 PCFR;
    io_rw_32 EXTICR[4];
    uint8_t _reserved_0[0x4];
    io_rw_32 PCFR2;
} AFIO_t;

#define AFIO ((AFIO_t *)0x40010000)
