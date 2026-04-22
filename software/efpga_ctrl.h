// ----------------------------------------------------------------#
//  Module:       eFPGA Control Software Headers
//  Company:      Yongatek Microelectronics
//  Author:       Ahmad Houraniah
//  Version:      1.0.0
//  Description:  This file contains the function 
//                prototypes for the eFPGA control software.
// ----------------------------------------------------------------#

#ifndef EFPGA_CTRL_H
#define EFPGA_CTRL_H

#include <stdint.h>

#define EFPGA_BASE_PTR 	((volatile uint32_t *)EFPGA_DEFAULT_BASEADDR)
#define CSR_REG_ADDR 	((volatile uint32_t *)(EFPGA_DEFAULT_BASEADDR + CSR_OFFSET))

#define ASSERT_BIT(reg, mask)	(*(reg) |= (mask))	// Write 1
#define DEASSERT_BIT(reg, mask)	(*(reg) &= ~(mask)) // Write 0

#define EFPGA_BITSTREAM_LENGTH 9298
#define EFPGA_BITSTREAM_PACKED_LENGTH ((EFPGA_BITSTREAM_LENGTH + 2) / 3 * 2)

typedef enum {
	MODE_00 = 0, 
	MODE_01 = 1, 
	MODE_10 = 2,
	MODE_11 = 3
} efpga_mode_t;


void enable_global_config_reset(void);
void disable_global_config_reset(void);
void enable_global_user_reset(void);
void disable_global_user_reset(void);
void set_logical_user_reset(uint32_t value);
void enable_power(void);
void disable_power(void);
void set_csr_packer_mode(efpga_mode_t mode_value);
void set_csr_unpacker_mode(efpga_mode_t mode_value);
void set_csr_clk_div(uint32_t clk_div_ratio);
uint32_t get_interrupts(void);
void set_interrupts(uint32_t inter);
uint32_t get_interrupts_mask(void);
void set_interrupts_mask(uint32_t mask);
uint32_t get_soc2fpga_fifo_empty(void);
uint32_t get_soc2fpga_fifo_full(void);
uint32_t get_fpga2soc_fifo_empty(void);
uint32_t get_fpga2soc_fifo_full(void);
void program_fpga(uint32_t * fabric_bitstream);
void send_data(uint32_t data);
uint32_t read_data(void);
uint32_t read_ccff_tail(void);

#endif