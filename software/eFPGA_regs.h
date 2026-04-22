// ----------------------------------------------------------------#
//  Module:       eFPGA Control Software Registers
//  Company:      Yongatek Microelectronics
//  Author:       Ahmad Houraniah
//  Version:      1.0.0
//  Description:  This file contains the register 
//                definitions for the eFPGA control software.
// ----------------------------------------------------------------#

#ifndef EFPGA_REGS_H
#define EFPGA_REGS_H

/* Revision number of the 'eFPGA' register map */
#define EFPGA_REVISION 206

/* Default base address of the 'eFPGA' register map */
#define EFPGA_DEFAULT_BASEADDR 0x48000000

/* Size of the 'eFPGA' register map, in bytes */
#define EFPGA_RANGE_BYTES 20

/* Register 'CSR' */
#define CSR_OFFSET 0x00000000 /* address offset of the 'CSR' register */

/* Field  'CSR.RESETN_CONFIG_CIRCUITRY' */
#define CSR_GLOBAL_RESETN_CONFIG_CIRCUITRY_BIT_OFFSET 0 /* bit offset of the 'GLOBAL_RESETN_CONFIG_CIRCUITRY' field */
#define CSR_GLOBAL_RESETN_CONFIG_CIRCUITRY_BIT_WIDTH 1 /* bit width of the 'GLOBAL_RESETN_CONFIG_CIRCUITRY' field */
#define CSR_GLOBAL_RESETN_CONFIG_CIRCUITRY_BIT_MASK 0x00000001 /* bit mask of the 'GLOBAL_RESETN_CONFIG_CIRCUITRY' field */
#define CSR_GLOBAL_RESETN_CONFIG_CIRCUITRY_RESET 0x1 /* reset value of the 'GLOBAL_RESETN_CONFIG_CIRCUITRY' field */

/* Field  'CSR.RESETN_USER_CIRCUITRY' */
#define CSR_GLOBAL_RESETN_USER_CIRCUITRY_BIT_OFFSET 1 /* bit offset of the 'GLOBAL_RESETN_USER_CIRCUITRY' field */
#define CSR_GLOBAL_RESETN_USER_CIRCUITRY_BIT_WIDTH 1 /* bit width of the 'GLOBAL_RESETN_USER_CIRCUITRY' field */
#define CSR_GLOBAL_RESETN_USER_CIRCUITRY_BIT_MASK 0x00000002 /* bit mask of the 'GLOBAL_RESETN_USER_CIRCUITRY' field */
#define CSR_GLOBAL_RESETN_USER_CIRCUITRY_RESET 0x1 /* reset value of the 'GLOBAL_RESETN_USER_CIRCUITRY' field */

/* Field  'CSR.RESET_USER_CIRCUITRY' */
#define CSR_LOGICAL_RESET_USER_CIRCUITRY_BIT_OFFSET 18 /* bit offset of the 'LOGICAL_RESET_USER_CIRCUITRY' field */
#define CSR_LOGICAL_RESET_USER_CIRCUITRY_BIT_WIDTH 1 /* bit width of the 'LOGICAL_RESET_USER_CIRCUITRY' field */
#define CSR_LOGICAL_RESET_USER_CIRCUITRY_BIT_MASK 0x0000040000 /* bit mask of the 'LOGICAL_RESET_USER_CIRCUITRY' field */
#define CSR_LOGICAL_RESET_USER_CIRCUITRY_RESET 0x0 /* reset value of the 'LOGICAL_RESET_USER_CIRCUITRY' field */

/* Field  'CSR.POWER_ENABLE' */
#define CSR_POWER_ENABLE_BIT_OFFSET 2 /* bit offset of the 'POWER_ENABLE' field */
#define CSR_POWER_ENABLE_BIT_WIDTH 1 /* bit width of the 'POWER_ENABLE' field */
#define CSR_POWER_ENABLE_BIT_MASK 0x00000004 /* bit mask of the 'POWER_ENABLE' field */
#define CSR_POWER_ENABLE_RESET 0x0 /* reset value of the 'POWER_ENABLE' field */

/* Field  'CSR.PACKER_MODE' */
#define CSR_PACKER_MODE_BIT_OFFSET 3 /* bit offset of the 'PACKER_MODE' field */
#define CSR_PACKER_MODE_BIT_WIDTH 2 /* bit width of the 'PACKER_MODE' field */
#define CSR_PACKER_MODE_BIT_MASK 0x00000018 /* bit mask of the 'PACKER_MODE' field */
#define CSR_PACKER_MODE_RESET 0x0 /* reset value of the 'PACKER_MODE' field */

/* Field  'CSR.UNPACKER_MODE' */
#define CSR_UNPACKER_MODE_BIT_OFFSET 5 /* bit offset of the 'UNPACKER_MODE' field */
#define CSR_UNPACKER_MODE_BIT_WIDTH 2 /* bit width of the 'UNPACKER_MODE' field */
#define CSR_UNPACKER_MODE_BIT_MASK 0x00000060 /* bit mask of the 'UNPACKER_MODE' field */
#define CSR_UNPACKER_MODE_RESET 0x0 /* reset value of the 'UNPACKER_MODE' field */

/* Field  'CSR.CLK_DIV' */
#define CSR_CLK_DIV_BIT_OFFSET 7 /* bit offset of the 'CLK_DIV' field */
#define CSR_CLK_DIV_BIT_WIDTH 5 /* bit width of the 'CLK_DIV' field */
#define CSR_CLK_DIV_BIT_MASK 0x00000F80 /* bit mask of the 'CLK_DIV' field */
#define CSR_CLK_DIV_RESET 0x00 /* reset value of the 'CLK_DIV' field */

/* Field  'CSR.INTERRUPT' */
#define CSR_INTERRUPT_BIT_OFFSET 12 /* bit offset of the 'INTERRUPT' field */
#define CSR_INTERRUPT_BIT_WIDTH 3 /* bit width of the 'INTERRUPT' field */
#define CSR_INTERRUPT_BIT_MASK 0x00007000 /* bit mask of the 'INTERRUPT' field */
#define CSR_INTERRUPT_RESET 0x0 /* reset value of the 'INTERRUPT' field */

/* Field  'CSR.INTERRUPT_MASK' */
#define CSR_INTERRUPT_MASK_BIT_OFFSET 15 /* bit offset of the 'INTERRUPT_MASK' field */
#define CSR_INTERRUPT_MASK_BIT_WIDTH 3 /* bit width of the 'INTERRUPT_MASK' field */
#define CSR_INTERRUPT_MASK_BIT_MASK 0x00038000 /* bit mask of the 'INTERRUPT_MASK' field */
#define CSR_INTERRUPT_MASK_RESET 0x0 /* reset value of the 'INTERRUPT_MASK' field */

/* Field  'CSR.SOC2FPGA_EMPTY' */
#define CSR_SOC2FPGA_EMPTY_BIT_OFFSET 28 /* bit offset of the 'SOC2FPGA_EMPTY' field */
#define CSR_SOC2FPGA_EMPTY_BIT_WIDTH 1 /* bit width of the 'SOC2FPGA_EMPTY' field */
#define CSR_SOC2FPGA_EMPTY_BIT_MASK 0x10000000 /* bit mask of the 'SOC2FPGA_EMPTY' field */
#define CSR_SOC2FPGA_EMPTY_RESET 0x0 /* reset value of the 'SOC2FPGA_EMPTY' field */

/* Field  'CSR.SOC2FPGA_FULL' */
#define CSR_SOC2FPGA_FULL_BIT_OFFSET 29 /* bit offset of the 'SOC2FPGA_FULL' field */
#define CSR_SOC2FPGA_FULL_BIT_WIDTH 1 /* bit width of the 'SOC2FPGA_FULL' field */
#define CSR_SOC2FPGA_FULL_BIT_MASK 0x20000000 /* bit mask of the 'SOC2FPGA_FULL' field */
#define CSR_SOC2FPGA_FULL_RESET 0x0 /* reset value of the 'SOC2FPGA_FULL' field */

/* Field  'CSR.FPGA2SOC_EMPTY' */
#define CSR_FPGA2SOC_EMPTY_BIT_OFFSET 30 /* bit offset of the 'FPGA2SOC_EMPTY' field */
#define CSR_FPGA2SOC_EMPTY_BIT_WIDTH 1 /* bit width of the 'FPGA2SOC_EMPTY' field */
#define CSR_FPGA2SOC_EMPTY_BIT_MASK 0x40000000 /* bit mask of the 'FPGA2SOC_EMPTY' field */
#define CSR_FPGA2SOC_EMPTY_RESET 0x0 /* reset value of the 'FPGA2SOC_EMPTY' field */

/* Field  'CSR.FPGA2SOC_FULL' */
#define CSR_FPGA2SOC_FULL_BIT_OFFSET 31 /* bit offset of the 'FPGA2SOC_FULL' field */
#define CSR_FPGA2SOC_FULL_BIT_WIDTH 1 /* bit width of the 'FPGA2SOC_FULL' field */
#define CSR_FPGA2SOC_FULL_BIT_MASK 0x80000000 /* bit mask of the 'FPGA2SOC_FULL' field */
#define CSR_FPGA2SOC_FULL_RESET 0x0 /* reset value of the 'FPGA2SOC_FULL' field */

/* Register 'DATA_CONFIG' */
#define DATA_CONFIG_OFFSET 0x00000004 /* address offset of the 'DATA_CONFIG' register */

/* Field  'DATA_CONFIG.DATA' */
#define DATA_CONFIG_DATA_BIT_OFFSET 0 /* bit offset of the 'DATA' field */
#define DATA_CONFIG_DATA_BIT_WIDTH 32 /* bit width of the 'DATA' field */
#define DATA_CONFIG_DATA_BIT_MASK 0xFFFFFFFF /* bit mask of the 'DATA' field */
#define DATA_CONFIG_DATA_RESET 0x0 /* reset value of the 'DATA' field */

/* Enumerated values for field 'DATA_CONFIG.DATA' */
#define DATA_CONFIG_DATA_DATA_CONFIG 0

/* Register 'DATA_IN' */
#define DATA_IN_OFFSET 0x00000008 /* address offset of the 'DATA_IN' register */

/* Field  'DATA_IN.DATA' */
#define DATA_IN_DATA_BIT_OFFSET 0 /* bit offset of the 'DATA' field */
#define DATA_IN_DATA_BIT_WIDTH 32 /* bit width of the 'DATA' field */
#define DATA_IN_DATA_BIT_MASK 0xFFFFFFFF /* bit mask of the 'DATA' field */
#define DATA_IN_DATA_RESET 0x0 /* reset value of the 'DATA' field */

/* Register 'DATA_OUT' */
#define DATA_OUT_OFFSET 0x0000000C /* address offset of the 'DATA_OUT_1' register */

/* Field  'DATA_OUT.DATA' */
#define DATA_OUT_DATA_BIT_OFFSET 0 /* bit offset of the 'DATA' field */
#define DATA_OUT_DATA_BIT_WIDTH 32 /* bit width of the 'DATA' field */
#define DATA_OUT_DATA_BIT_MASK 0xFFFFFFFF /* bit mask of the 'DATA' field */
#define DATA_OUT_DATA_RESET 0x0 /* reset value of the 'DATA' field */

/* Register 'CCFF_TAIL' */
#define CCFF_TAIL_OFFSET 0x00000010 /* address offset of the 'DATA_OUT_1' register */

/* Field  'DATA_OUT.DATA' */
#define CCFF_TAIL_DATA_BIT_OFFSET 0 /* bit offset of the 'DATA' field */
#define CCFF_TAIL_DATA_BIT_WIDTH 32 /* bit width of the 'DATA' field */
#define CCFF_TAIL_DATA_BIT_MASK 0xFFFFFFFF /* bit mask of the 'DATA' field */
#define CCFF_TAIL_DATA_RESET 0x0 /* reset value of the 'DATA' field */

#endif  /* EFPGA_REGS_H */
