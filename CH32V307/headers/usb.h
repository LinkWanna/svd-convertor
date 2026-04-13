#pragma once

#include "types.h"

typedef struct {
    io_rw_16 EP0R;
    uint8_t _reserved_0[0x2];
    io_rw_16 EP1R;
    uint8_t _reserved_1[0x2];
    io_rw_16 EP2R;
    uint8_t _reserved_2[0x2];
    io_rw_16 EP3R;
    uint8_t _reserved_3[0x2];
    io_rw_16 EP4R;
    uint8_t _reserved_4[0x2];
    io_rw_16 EP5R;
    uint8_t _reserved_5[0x2];
    io_rw_16 EP6R;
    uint8_t _reserved_6[0x2];
    io_rw_16 EP7R;
    uint8_t _reserved_7[0x22];
    io_rw_16 CNTR;
    uint8_t _reserved_8[0x2];
    io_rw_16 ISTR;
    uint8_t _reserved_9[0x2];
    io_ro_16 FNR;
    uint8_t _reserved_10[0x2];
    io_rw_16 DADDR;
    uint8_t _reserved_11[0x2];
    io_rw_32 BTABLE;
} USB_t;

#define USB ((USB_t *)0x40005C00)
