#pragma once

#include <stdint.h>

typedef volatile        uint8_t  io_rw_8;
typedef const volatile  uint8_t  io_ro_8;
typedef volatile        uint8_t  io_wo_8;
typedef volatile        uint16_t io_rw_16;
typedef const volatile  uint16_t io_ro_16;
typedef volatile        uint16_t io_wo_16;
typedef volatile        uint32_t io_rw_32;
typedef const volatile  uint32_t io_ro_32;
typedef volatile        uint32_t io_wo_32;
typedef volatile        uint64_t io_rw_64;
typedef const volatile  uint64_t io_ro_64;
typedef volatile        uint64_t io_wo_64;

typedef volatile uint8_t *const ioptr;
typedef ioptr const const_ioptr;
