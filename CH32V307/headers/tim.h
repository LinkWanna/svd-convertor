#pragma once

#include "types.h"

typedef struct {
    io_rw_32 CTLR[2];
    io_rw_32 SMCFGR;
    io_rw_32 DMAINTENR;
    io_rw_32 INTFR;
    io_wo_32 SWEVGR;
    io_rw_32 CHCTLR1_Output;
    /* Alias registers at same offset: CHCTLR1_Input */
    io_rw_32 CHCTLR2_Output;
    /* Alias registers at same offset: CHCTLR2_Input */
    io_rw_32 CCER;
    io_rw_32 CNT;
    io_rw_32 PSC;
    io_rw_32 ATRLR;
    uint8_t _reserved_0[0x4];
    io_rw_32 CH1CVR;
    io_rw_32 CH2CVR;
    io_rw_32 CH3CVR;
    io_rw_32 CH4CVR;
    uint8_t _reserved_1[0x4];
    io_rw_32 DMACFGR;
    io_rw_32 DMAADR;
} TIM2_t;

typedef struct {
    io_rw_32 CTLR[2];
    uint8_t _reserved_0[0x4];
    io_rw_32 DMAINTENR;
    io_rw_32 INTFR;
    io_wo_32 SWEVGR;
    uint8_t _reserved_1[0xC];
    io_rw_32 CNT;
    io_rw_32 PSC;
    io_rw_32 ATRLR;
} TIM6_t;

typedef struct {
    io_rw_32 CTLR[2];
    io_rw_32 SMCFGR;
    io_rw_32 DMAINTENR;
    io_rw_32 INTFR;
    io_wo_32 SWEVGR;
    io_rw_32 CHCTLR1_Output;
    /* Alias registers at same offset: CHCTLR1_Input */
    io_rw_32 CHCTLR2_Output;
    /* Alias registers at same offset: CHCTLR2_Input */
    io_rw_32 CCER;
    io_rw_32 CNT;
    io_rw_32 PSC;
    io_rw_32 ATRLR;
    io_rw_32 RPTCR;
    io_rw_32 CH1CVR;
    io_rw_32 CH2CVR;
    io_rw_32 CH3CVR;
    io_rw_32 CH4CVR;
    io_rw_32 BDTR;
    io_rw_32 DMACFGR;
    io_rw_32 DMAADR;
} TIM1_t;

#define TIM2 ((TIM2_t *)0x40000000)
#define TIM3 ((TIM2_t *)0x40000400)
#define TIM4 ((TIM2_t *)0x40000800)
#define TIM5 ((TIM2_t *)0x40000C00)
#define TIM6 ((TIM6_t *)0x40001000)
#define TIM7 ((TIM6_t *)0x40001400)
#define TIM1 ((TIM1_t *)0x40012C00)
#define TIM8 ((TIM1_t *)0x40013400)
#define TIM9 ((TIM1_t *)0x40014C00)
#define TIM10 ((TIM1_t *)0x40015000)
