// ----------------------------------------------------------------------------#
//  Module:       eFPGA Control Software
//  Company:      Yongatek Microelectronics
//  Author:       Ahmad Houraniah
//  Version:      1.0.0
//  Description:  This module contains the implementation of the eFPGA 
// 				  control functions defined in efpga_ctrl.h. These
//                functions provide an interface for controlling various 
//                aspects of the eFPGA, such as resets, power, configuration, 
//                and data transfer. The functions interact with the eFPGA's 
// 				  control and status registers (CSRs) to perform the necessary 
//                operations. The implementation assumes that the eFPGA is 
//                memory-mapped and that the base address and register offsets 
//                are defined in eFPGA_regs.h.
// ----------------------------------------------------------------------------#

#include <stdint.h>
#include "efpga_ctrl.h"
#include "eFPGA_regs.h"
//Function prototypes
void enable_global_config_reset(){
	DEASSERT_BIT(CSR_REG_ADDR, CSR_GLOBAL_RESETN_CONFIG_CIRCUITRY_BIT_MASK);
}
void disable_global_config_reset(){
	ASSERT_BIT(CSR_REG_ADDR, CSR_GLOBAL_RESETN_CONFIG_CIRCUITRY_BIT_MASK);
}
void enable_global_user_reset(){
	DEASSERT_BIT(CSR_REG_ADDR, CSR_GLOBAL_RESETN_USER_CIRCUITRY_BIT_MASK);
}
void disable_global_user_reset(){
	ASSERT_BIT(CSR_REG_ADDR, CSR_GLOBAL_RESETN_USER_CIRCUITRY_BIT_MASK);
}
uint32_t get_csr_clk_div(void){
	uint32_t v = *CSR_REG_ADDR;
	v &= CSR_CLK_DIV_BIT_MASK;
	v >>= CSR_CLK_DIV_BIT_OFFSET;
	return v;
}
void set_logical_user_reset(uint32_t value){
	volatile uint32_t clk_div_ratio = get_csr_clk_div();
	if(value)
		ASSERT_BIT(CSR_REG_ADDR, CSR_LOGICAL_RESET_USER_CIRCUITRY_BIT_MASK);
	else
		DEASSERT_BIT(CSR_REG_ADDR, CSR_LOGICAL_RESET_USER_CIRCUITRY_BIT_MASK);
	volatile uint32_t dummy_counter = 0;
	for (dummy_counter=0; dummy_counter <= clk_div_ratio+1; dummy_counter = dummy_counter + 1);
}
void enable_power(){
	ASSERT_BIT(CSR_REG_ADDR,CSR_POWER_ENABLE_BIT_MASK);
}
void disable_power(){
	DEASSERT_BIT(CSR_REG_ADDR,CSR_POWER_ENABLE_BIT_MASK);
}
void set_csr_packer_mode(efpga_mode_t mode_value){
	uint32_t v = *CSR_REG_ADDR;
	v &= ~CSR_PACKER_MODE_BIT_MASK;
	v |= ((mode_value << CSR_PACKER_MODE_BIT_OFFSET) & CSR_PACKER_MODE_BIT_MASK);
	*CSR_REG_ADDR = v;
}
void set_csr_unpacker_mode(efpga_mode_t mode_value){
	uint32_t v = *CSR_REG_ADDR;
	v &= ~CSR_UNPACKER_MODE_BIT_MASK;
	v |= ((mode_value << CSR_UNPACKER_MODE_BIT_OFFSET) & CSR_UNPACKER_MODE_BIT_MASK);
	*CSR_REG_ADDR = v;
}
void set_csr_clk_div(uint32_t clk_div_ratio){
	uint32_t v = *CSR_REG_ADDR;
	v &= ~CSR_CLK_DIV_BIT_MASK;
	v |= ((clk_div_ratio << CSR_CLK_DIV_BIT_OFFSET) & CSR_CLK_DIV_BIT_MASK);
	*CSR_REG_ADDR = v;
}
void program_fpga(uint32_t * fabric_bitstream){
	volatile uint32_t *cfg = (volatile uint32_t*)(EFPGA_BASE_PTR + (DATA_CONFIG_OFFSET/4));
	int unpacked_counter = 0;
	for(uint32_t i = 0; i < EFPGA_BITSTREAM_PACKED_LENGTH; i += 2){
		if(unpacked_counter + 3 > EFPGA_BITSTREAM_LENGTH) {
			*cfg = fabric_bitstream[i] & 0x1FFFFF;
			unpacked_counter +=1;
			printf("Last Config written\n");
		} else {
			*cfg = fabric_bitstream[i] & 0x1FFFFF;
			*cfg = (fabric_bitstream[i] >> 21 ) | ((fabric_bitstream[i+1] & 0x3FF) << 11);
			*cfg = (fabric_bitstream[i+1] >> 10 ) & 0x1FFFFF;
			unpacked_counter +=3;
		}
	}
	printf("Config done\n");
}

void send_data(uint32_t data){
	*(EFPGA_BASE_PTR+(DATA_IN_OFFSET/4)) = data;
}
uint32_t get_soc2fpga_fifo_empty(void){
	return ((*(volatile uint32_t*)(CSR_REG_ADDR)) & CSR_SOC2FPGA_EMPTY_BIT_MASK ) >> CSR_SOC2FPGA_EMPTY_BIT_OFFSET;
}
uint32_t get_soc2fpga_fifo_full(void){
	return ((*(volatile uint32_t*)(CSR_REG_ADDR)) & CSR_SOC2FPGA_FULL_BIT_MASK) >> CSR_SOC2FPGA_FULL_BIT_OFFSET;
}
uint32_t get_fpga2soc_fifo_empty(void){
	return ((*(volatile uint32_t*)(CSR_REG_ADDR)) & CSR_FPGA2SOC_EMPTY_BIT_MASK) >> CSR_FPGA2SOC_EMPTY_BIT_OFFSET ;
}
uint32_t get_fpga2soc_fifo_full(void){
	return ((*(volatile uint32_t*)(CSR_REG_ADDR)) & CSR_FPGA2SOC_FULL_BIT_MASK) >> CSR_FPGA2SOC_FULL_BIT_OFFSET;
}
uint32_t read_data(){
	return (*(volatile uint32_t*)(EFPGA_BASE_PTR + (DATA_OUT_OFFSET/4))) ;
}
uint32_t read_ccff_tail(){
	return (*(volatile uint32_t*)(EFPGA_BASE_PTR + (CCFF_TAIL_OFFSET/4))) ;
}
uint32_t get_interrupts(void){
	return ((*(volatile uint32_t*)(CSR_REG_ADDR)) & CSR_INTERRUPT_BIT_MASK) >> CSR_INTERRUPT_BIT_OFFSET;
}
void set_interrupts(uint32_t inter){
	uint32_t v = *CSR_REG_ADDR;
	v &= ~CSR_INTERRUPT_BIT_MASK;
	v |= ((inter << CSR_INTERRUPT_BIT_OFFSET) & CSR_INTERRUPT_BIT_MASK);
	*CSR_REG_ADDR = v;
}
uint32_t get_interrupts_mask(void){
	return ((*(volatile uint32_t*)(CSR_REG_ADDR)) & CSR_INTERRUPT_MASK_BIT_MASK) >> CSR_INTERRUPT_MASK_BIT_OFFSET;
}
void set_interrupts_mask(uint32_t mask){
	uint32_t v = *CSR_REG_ADDR;
	v &= ~CSR_INTERRUPT_MASK_BIT_MASK;
	v |= ((mask << CSR_INTERRUPT_MASK_BIT_OFFSET) & CSR_INTERRUPT_MASK_BIT_MASK);
	*CSR_REG_ADDR = v;
}