#----------------------------------------------------------------#
# Module:       fix_netlist.py
# Company:      Yongatek Microelectronics
# Author:       Ahmad Houraniah
# Version:      1.0.0
# Description:  This script is used to fix the netlist files by 
#               fixing issues in the generated code.
#----------------------------------------------------------------#

import os
import re, sys
from scripts.paths import get_TRISTAN_EFPGA_PATH

def replace_include_paths(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()

    new_lines = []
    for line in lines:
        if "/yonga_archs/" in line:
            line = re.sub(r'\"/.*/yonga_archs/', '"', line)
        new_lines.append(line)    
    f = open(file_name, 'w')
    f.writelines(new_lines)
    f.close()


def remove_date(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()
    output_lines = [line for line in lines if "Date:" not in line]
    f = open(file_name, 'w')
    f.writelines(output_lines)
    f.close()

def fix_multiple_driver(file_name):
    ASSIGN_PATTERN = re.compile(r"^\s*assign\s+([a-zA-Z_0-9\[\]]+)\s*=")
    seen_nets = set()
    output_lines = []
    f = open(file_name, 'r')
    content = f.readlines()
    f.close()
    for line in content:
        match = ASSIGN_PATTERN.match(line)
        if match:
            net = match.group(1)
            if net in seen_nets:
                continue
            seen_nets.add(net)
        output_lines.append(line)

    f = open(file_name, 'w')
    f.writelines(output_lines)
    f.close()

def init_and_replace(m):
    if 'cout' in m.group(0) or '_out' in m.group(0):
        return m.group(0)
    w = abs(int(m.group(2)) - int(m.group(3))) +1
    init = "1'b0" if w==1 else f"{{{w}{{1'b0}}}}"
    return f"{m.group(1)} = {init};"

def initialize_undriven(file_name):
    f = open(file_name, 'r')
    content = f.read()
    f.close()
    content = re.sub(r'(wire\s+\[(\d+):(\d+)\]\s+\S*_undriven_\S*);', init_and_replace, content)
    # f = open(file_name+".test", 'w')
    # f.write(content)
    # f.close()

def fix_netlist():
    targets = [
        get_TRISTAN_EFPGA_PATH()[:-1] + "/yonga_archs/Fabric/SRC/tile/",
        get_TRISTAN_EFPGA_PATH()[:-1] + "/yonga_archs/Fabric/SRC/routing/",
        get_TRISTAN_EFPGA_PATH()[:-1] + "/yonga_archs/Fabric/SRC/fpga_top.v",
        get_TRISTAN_EFPGA_PATH()[:-1] + "/yonga_archs/Fabric/SRC/fpga_core.v"
    ]
    extra_targets = [
        get_TRISTAN_EFPGA_PATH()[:-1] + "/yonga_archs/Fabric/SRC/sub_module/",
        get_TRISTAN_EFPGA_PATH()[:-1] + "/yonga_archs/Fabric/SRC/lb/",
        get_TRISTAN_EFPGA_PATH()[:-1] + "/yonga_archs/Fabric/SRC/fpga_defines.v",
        get_TRISTAN_EFPGA_PATH()[:-1] + "/yonga_archs/Fabric/SRC/fabric_netlists.v"
    ]

    for path in targets:
        if os.path.isdir(path):
            for file in os.listdir(path):
                if file.endswith(".v"):
                    full_path = os.path.join(path, file)
                    initialize_undriven(full_path)
                    fix_multiple_driver(full_path)
                    remove_date(full_path)
        elif os.path.isfile(path):
            initialize_undriven(path)
            fix_multiple_driver(path)
            remove_date(path)
    for path in extra_targets:
        if os.path.isdir(path):
            for file in os.listdir(path):
                if file.endswith(".v"):
                    full_path = os.path.join(path, file)
                    remove_date(full_path)
        elif os.path.isfile(path):
            remove_date(path)

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
                line = line.strip()
                if not line or "//" in line:
                    continue
                line = line.replace("`include", "").strip()
                line = line[1:-1]
                flist.write(line+"\n")
    except FileNotFoundError:
        print(f"File not found: {netlist_path}")

