import os
from scripts.paths import get_TRISTAN_EFPGA_PATH, get_fabric_path
from scripts.rtl_parser import extract_variables_info


def write_clock_constraints(clocks_names, reset_flag):
    with open("config/constraints/pin_constraints.xml", "w") as f:
        f.write("<pin_constraints>\n")
        if clocks_names:
            f.write(f"  <set_io pin=\"clk\" net=\"{clocks_names[0]}\"/>\n")
        else:
            f.write(f"  <set_io pin=\"clk\" net=\"clk\"/>\n")
        if reset_flag:
            f.write("  <set_io pin=\"Reset[0]\" net=\"Reset\"/>\n")
        f.write("</pin_constraints>\n")

    with open("config/constraints/repack_design_constraints.xml", "w") as f:
        f.write("<repack_design_constraints>\n")
        if clocks_names:
            f.write(f"  <pin_constraint pb_type=\"clb\" pin=\"clk\" net=\"{clocks_names[0]}\"/>\n")
            f.write(f"  <pin_constraint pb_type=\"memory\" pin=\"clk\" net=\"{clocks_names[0]}\"/>\n")
        else:
            f.write(f"  <pin_constraint pb_type=\"clb\" pin=\"clk\" net=\"clk\"/>\n")
            f.write(f"  <pin_constraint pb_type=\"memory\" pin=\"clk\" net=\"clk\"/>\n")
        f.write("</repack_design_constraints>\n")


import re

def map_rst_and_clocks(benchmark):
    """
    This function is responsible for mapping a benchmark's clock and reset signals to the global pins.
    It extracts the names of clock signals and checks if the global reset is used which must be called "Reset"
    """
    clocks_names=[]
    reset_flag=False
    top_module_flag = False
    for i in benchmark.get_top_module_code():
        # If multiple modules are defined in the same file, we should only consider the top module
        if("module" in i and benchmark.get_name() in i): 
            top_module_flag = True
        if(top_module_flag): 
            # If the global Reset pin is used  
            if("Reset" in i): 
                reset_flag=True
            # The loop below extracts the clock names
            if("clk" in i and "input" in i):
                list=i.split(",") #if multiple pins are defined in the same line
                for j in list: # 
                    clk_name=j.strip().strip("input").strip().strip(",").strip()
                    if("clk" in clk_name or "clock" in clk_name):
                        clocks_names.append(j.strip().strip("input").strip().strip("wire").strip().strip(",").strip().strip(';'))
            # Only consider the top module
            if("endmodule" in i):
                # Write the constraints and return
                write_clock_constraints(clocks_names, reset_flag)
                top_module_flag = False
                return 

def generate_bus_group_file(benchmark):
    bench_text = benchmark.get_top_module_code()
    bus_group = []
    top_module_flag = False
    var_names, size, big_endian = [], [], []
    in_block_comment = False

    for line in bench_text:
        # Handle block comments
        if in_block_comment:
            block_comment_end_pos = line.find("*/")
            if block_comment_end_pos != -1:
                line = line[block_comment_end_pos + 2:]
                in_block_comment = False
            else:
                continue

        # Handle single-line comments
        single_line_comment_pos = line.find("//")
        if single_line_comment_pos != -1:
            line = line[:single_line_comment_pos]

        # Handle block comment starts
        block_comment_start_pos = line.find("/*")
        if block_comment_start_pos != -1:
            line = line[:block_comment_start_pos]
            in_block_comment = True

        # Parse top module ports
        line = line.replace("\t", "    ")
        if benchmark.get_name() in line:
            top_module_flag = True
        if top_module_flag:
            if 'endmodule' in line:
                top_module_flag = False
                break
            elif ("input " in line or "output " in line) and "[" in line:
                try:
                    var_names_i, size_i, big_endian_i = extract_variables_info(line)
                    var_names.extend(var_names_i)
                    size.extend(size_i)
                    big_endian.extend(big_endian_i)
                except Exception as e:
                    print(f"{e} ERROR i= " + line)

    # Create bus group XML
    buses = "<bus_group>\n"
    for i in range(len(var_names)):
        bus_endian = "false" if big_endian[i] == "false" else "true"
        bus_range = f"{str(size[i] - 1)}:0" if big_endian[i] == "false" else f"0:{str(size[i] - 1)}"
        buses += f'  <bus name=\"{var_names[i]}[{bus_range}]\" big_endian=\"{bus_endian}\">\n'
        for j in range(size[i]):
            buses += f'    <pin id=\"{j}\" name=\"{var_names[i]}_{j}_\"/>\n'
        buses += '  </bus>\n'
    buses += '</bus_group>\n'

    with open('config/constraints/bus_group.xml', 'w') as f:
        f.write(buses)


def set_pin_constraints(benchmark):
    name = benchmark.get_name()
    pcf_list = os.listdir('../pin_constraints/')
    if f"{name}.pcf" in pcf_list:
        os.system(f"cp ../pin_constraints/{name}.pcf config/constraints/constraints.pcf")
        print("Copying PCF")
    else:
        bench_text = benchmark.get_top_module_code()
        var_names, size, port_types = [], [], []
        top_module_flag = False

        for line in bench_text:
            if name in line and 'module' in line:
                top_module_flag = True
            if top_module_flag:
                if "input " in line:
                    port_type = "input"
                else:
                    port_type = "output"
                if 'endmodule' in line:
                    top_module_flag = False
                elif ("input " in line or "output " in line) and "[" in line:
                    try:
                        var_names_i, size_i, big_endian_i = extract_variables_info(line)
                        var_names.extend(var_names_i)
                        size.extend(size_i)
                        port_types.extend([port_type] * len(var_names_i))
                    except:
                        print("ERROR i= " + line)
                elif "input " in line or "output " in line:
                    try:
                        tmp_list = line.split()
                        for m in tmp_list:
                            if not any(keyword in m for keyword in ["input", "signed", "inout", "output", "reg", "wire", "clk", "clock"]):
                                for n in m.split(","):
                                    if len(n.strip()) > 0:
                                        var_names.append(n.strip().strip(";"))
                                        size.append(1)
                                        port_types.append(port_type)
                    except:
                        print("ERROR i= " + line)

        # Write pin constraints to PCF
        with open("config/constraints/constraints.pcf", 'w') as f:
            kk = 0
            for i in range(len(var_names)):
                if port_types[i] == "input":
                    for j in range(size[i]):
                        if size[i] == 1:
                            f.write(f"set_io {var_names[i]} pad_fpga_io[{kk}]\n")
                        else:
                            f.write(f"set_io {var_names[i]}[{j}] pad_fpga_io[{kk}]\n")
                        kk += 1

            for i in range(len(var_names)):
                if port_types[i] == "output":
                    for j in range(size[i]):
                        if size[i] == 1:
                            f.write(f"set_io {var_names[i]} pad_fpga_io[{kk}]\n")
                        else:
                            f.write(f"set_io {var_names[i]}[{j}] pad_fpga_io[{kk}]\n")
                        kk += 1


def flatten_constraints():
    try:
        with open("config/constraints/constraints.pcf", 'r') as f:
            lines = f.readlines()

        flattened_lines = []
        for line in lines:
            if "set_io" in line and ":" in line:
                bench_m = int(line[line.find("[") + 1:line.find(":")].strip())
                bench_n = int(line[line.find(":") + 1:line.find("]")].strip())
                port_string = line[line.find("]") + 1:]
                port_m = int(port_string[port_string.find("[") + 1:port_string.find(":")].strip())
                port_n = int(port_string[port_string.find(":") + 1:port_string.find("]")].strip())

                for k in range(min(bench_n, bench_m), max(bench_n + 1, bench_m + 1)):
                    flattened_list = [["set_io", line.split()[1].split("[")[0] + f"[{k}]"]]
                    tmp_cnt = 0
                    for k in range(min(port_n, port_m), max(port_n + 1, port_m + 1)):
                        flattened_list.append([line.split()[1].split("[")[0] + f"[{k}]"])
                    flattened_lines.append(flattened_list)

        with open("config/constraints/constraints_flattened.pcf", 'w') as f:
            f.write("".join(flattened_lines))
    except:
        pass
