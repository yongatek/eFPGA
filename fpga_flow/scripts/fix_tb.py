#----------------------------------------------------------------#
# Module:       fix_tb.py
# Company:      Yongatek Microelectronics
# Author:       Ahmad Houraniah
# Version:      0.1.0
# Description:  This script is used to fix the issues from the 
#               autogenerated testbenches.
#----------------------------------------------------------------#

import os

def remove_deposit(benchmark_name):
    file_path = f"SRC/{benchmark_name}_autocheck_top_tb.v"
    
    with open(file_path, 'r') as f:
        tb_lines = f.readlines()
    
    with open(file_path, 'w') as f:
        skip_lines = False
        for line in tb_lines:
            if skip_lines:
                if "// ------ END driver initialization -----" in line:
                    skip_lines = False
                continue
            if "// ------ BEGIN driver initialization -----" in line:
                skip_lines = True
            if not skip_lines:
                f.write(line)

def update_reset(tb_type, benchmark):
    if tb_type not in [2, 3, 4]:
        return 0

    file_name = f"{benchmark.get_name()}_autocheck_top_tb.v" if tb_type == 4 else f"{benchmark.get_name()}_formal_random_top_tb.v"
    file_path = os.path.join(os.getcwd(), 'SRC', file_name)
    
    with open(file_path, 'r') as f:
        rtl_lines = f.readlines()

    reset_name = 'reset'
    input_stimulus_block = False
    input_initialization_block = False

    for i in range(len(rtl_lines)):
        line = rtl_lines[i]

        if 'Input Stimulus' in line:
            input_stimulus_block = True
        elif 'end' in line and input_stimulus_block:
            input_stimulus_block = False
        
        if 'Input Initialization' in line:
            input_initialization_block = True
        elif 'end' in line and input_initialization_block:
            input_initialization_block = False

        if input_initialization_block:
            if f"{reset_name} <= 1'b0;" in line:
                rtl_lines[i] = f'\t\t{reset_name} <= 1\'b1; \n\t\t#200;\n\t\t{reset_name} <= 1\'b0 ;'
            elif f"{reset_name}_shared_input <= 1'b0;" in line:
                rtl_lines[i] = '\n'

        if input_stimulus_block:
            if f"{reset_name}_shared_input <= $random;" in line:
                rtl_lines[i] = f'\t\t{reset_name}_shared_input <= ~Reset;\n'
            elif f"{reset_name} <= $random;" in line:
                rtl_lines[i] = '\n'
    
    with open(file_path, 'w') as f:
        f.writelines(rtl_lines)
