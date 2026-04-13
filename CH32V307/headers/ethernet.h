#pragma once

#include "types.h"

typedef struct {
    io_rw_32 MACCR;
    io_rw_32 MACFFR;
    io_rw_32 MACHTHR;
    io_rw_32 MACHTLR;
    io_rw_32 MACMIIAR;
    io_rw_32 MACMIIDR;
    io_rw_32 MACFCR;
    io_rw_32 MACVLANTR;
    uint8_t _reserved_0[0x8];
    io_rw_32 MACRWUFFR;
    io_rw_32 MACPMTCSR;
    uint8_t _reserved_1[0x8];
    io_rw_32 MACSR;
    io_rw_32 MACIMR;
    io_rw_32 MACA0HR;
    io_rw_32 MACA0LR;
    io_rw_32 MACA1HR;
    io_rw_32 MACA1LR;
    io_rw_32 MACA2HR;
    io_rw_32 MACA2LR;
    io_rw_32 MACA3HR;
    io_rw_32 MACA3LR;
} ETHERNET_MAC_t;

typedef struct {
    io_rw_32 MMCCR;
    io_rw_32 MMCRIR;
    io_rw_32 MMCTIR;
    io_rw_32 MMCRIMR;
    io_rw_32 MMCTIMR;
    uint8_t _reserved_0[0x38];
    io_ro_32 MMCTGFSCCR;
    io_ro_32 MMCTGFMSCCR;
    uint8_t _reserved_1[0x14];
    io_ro_32 MMCTGFCR;
    uint8_t _reserved_2[0x28];
    io_ro_32 MMCRFCECR;
    io_ro_32 MMCRFAECR;
    uint8_t _reserved_3[0x28];
    io_ro_32 MMCRGUFCR;
} ETHERNET_MMC_t;

typedef struct {
    io_rw_32 PTPTSCR;
    io_rw_32 PTPSSIR;
    io_ro_32 PTPTSHR;
    io_ro_32 PTPTSLR;
    io_rw_32 PTPTSHUR;
    io_rw_32 PTPTSLUR;
    io_rw_32 PTPTSAR;
    io_rw_32 PTPTTHR;
    io_rw_32 PTPTTLR;
} ETHERNET_PTP_t;

typedef struct {
    io_rw_32 DMABMR;
    io_rw_32 DMATPDR;
    io_rw_32 DMARPDR;
    io_rw_32 DMARDLAR;
    io_rw_32 DMATDLAR;
    io_rw_32 DMASR;
    io_rw_32 DMAOMR;
    io_rw_32 DMAIER;
    io_ro_32 DMAMFBOCR;
    uint8_t _reserved_0[0x24];
    io_ro_32 DMACHTDR;
    io_ro_32 DMACHRDR;
    io_ro_32 DMACHTBAR;
    io_ro_32 DMACHRBAR;
} ETHERNET_DMA_t;

#define ETHERNET_MAC ((ETHERNET_MAC_t *)0x40028000)
#define ETHERNET_MMC ((ETHERNET_MMC_t *)0x40028100)
#define ETHERNET_PTP ((ETHERNET_PTP_t *)0x40028700)
#define ETHERNET_DMA ((ETHERNET_DMA_t *)0x40029000)
