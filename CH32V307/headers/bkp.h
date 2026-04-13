#pragma once

#include "types.h"

typedef struct {
    uint8_t _reserved_0[0x4];
    io_rw_32 DATAR[10];
    io_rw_32 OCTLR;
    io_rw_32 TPCTLR;
    io_rw_32 TPCSR;
    uint8_t _reserved_1[0x8];
    io_rw_32 DATAR11;
    io_rw_32 DATAR12;
    io_rw_32 DATAR13;
    io_rw_32 DATAR14;
    io_rw_32 DATAR15;
    io_rw_32 DATAR16;
    io_rw_32 DATAR17;
    io_rw_32 DATAR18;
    io_rw_32 DATAR19;
    io_rw_32 DATAR20;
    io_rw_32 DATAR21;
    io_rw_32 DATAR22;
    io_rw_32 DATAR23;
    io_rw_32 DATAR24;
    io_rw_32 DATAR25;
    io_rw_32 DATAR26;
    io_rw_32 DATAR27;
    io_rw_32 DATAR28;
    io_rw_32 DATAR29;
    io_rw_32 DATAR30;
    io_rw_32 DATAR31;
    io_rw_32 DATAR32;
    io_rw_32 DATAR33;
    io_rw_32 DATAR34;
    io_rw_32 DATAR35;
    io_rw_32 DATAR36;
    io_rw_32 DATAR37;
    io_rw_32 DATAR38;
    io_rw_32 DATAR39;
    io_rw_32 DATAR40;
    io_rw_32 DATAR41;
    io_rw_32 DATAR42;
} BKP_t;

#define BKP ((BKP_t *)0x40006C00)
