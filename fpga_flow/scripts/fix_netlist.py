#----------------------------------------------------------------#
# Module:       fix_netlist.py
# Company:      Yongatek Microelectronics
# Author:       Ahmad Houraniah
# Version:      0.1.0
# Description:  This script is used to fix the netlist files by 
#               fixing issues in the generated code.
#----------------------------------------------------------------#

import os
from scripts.paths import get_TRISTAN_EFPGA_PATH

def replace_def_net_type():
    """
    Replaces `default_nettype none with `default_nettype wire in all Verilog files.
    """
    base_path = get_TRISTAN_EFPGA_PATH() + 'yonga_archs/Fabric/SRC/'
    os.system(f"sed -i 's/`default_nettype none/`default_nettype wire/g' {base_path}*.v")
    os.system(f"sed -i 's/`default_nettype none/`default_nettype wire/g' {base_path}**/*.v")

def fix_fabric_netlist_path():
    """
    Fixes the paths in the fabric netlist file.
    """
    netlist_path = get_TRISTAN_EFPGA_PATH()[:-1] + "/yonga_archs/Fabric/SRC/fabric_netlists.v"
    try:
        with open(netlist_path, 'r') as f:
            text = f.readlines()
        
        with open(netlist_path, 'w') as f:
            for line in text:
                new_line = line.replace("\"yonga_archs/", "\"" + get_TRISTAN_EFPGA_PATH()[:-1] + "/yonga_archs/")
                new_line = new_line.replace("/home/openfpga_user/fpga_flow/..", get_TRISTAN_EFPGA_PATH()[:-1])
                f.write(new_line)
    except FileNotFoundError:
        print(f"File not found: {netlist_path}")

def generate_flist():
    """
    Generates a file list from the fabric netlist file.
    """
    netlist_path = get_TRISTAN_EFPGA_PATH() + "yonga_archs/Fabric/SRC/fabric_netlists.v"
    flist_path = get_TRISTAN_EFPGA_PATH() + "yonga_archs/Fabric/SRC/fabric_netlists.flist"
    try:
        with open(netlist_path, 'r') as f:
            netlist = f.readlines()
        
        with open(flist_path, 'w') as flist:
            for line in netlist:
                if "//" not in line and line.strip():
                    flist.write(line.strip().strip("`include \"").replace("\"\n", "\n"))
    except FileNotFoundError:
        print(f"File not found: {netlist_path}")

