import os
from scripts.paths import get_fabric_path
from scripts.fix_tb import update_reset, remove_deposit

def extract_reslts(vpr_stdout, run_status):
    """
    This function is used to extract results from a the vpr (PnR tool) logs.
    """
    usage_flag = False
    count_flag = False
    tmp_flag   = False
    results_dict = {'Device':0, 'io':0, 'clb':0, 'mult_18':0, 'memory':0, 'Fmax':0, 'Critical path':0, 'L1':0, 'L2':0, 'L4':0}
    block_usage={}
    block_counts = {}
    io_count=0
    try:
        for i in range(len(vpr_stdout)):
            if("Resource usage..." in vpr_stdout[i] or tmp_flag):
                tmp_flag = True
                if("Netlist" in vpr_stdout[i]):
                    usage_flag = True
                    count_flag = False    
                elif("Architecture" in vpr_stdout[i]):
                    count_flag = True
                    usage_flag = False
                elif(vpr_stdout[i] != "\n"):
                    if(usage_flag):
                        block_usage[vpr_stdout[i].split()[4]]=vpr_stdout[i].split()[0]
                    elif(count_flag):
                        block_counts[vpr_stdout[i].split()[4]]=vpr_stdout[i].split()[0]
            if( "Device Utilization: " in vpr_stdout[i]):
                tmp_flag = False
            if("Failed to find device which satisifies resource requirements required:" in vpr_stdout[i]):
                print(vpr_stdout[i])
            if('Device Utilization:' in vpr_stdout[i] and 'Block Utilization' in vpr_stdout[i+1] and 'Block Utilization' in vpr_stdout[i+2]):
                results_dict['Device'] = float(vpr_stdout[i].split()[2]) # type: ignore
            if('Segment usage by length: length utilization' in vpr_stdout[i]):
                results_dict["L"+vpr_stdout[i+2].split()[0]] = float(vpr_stdout[i+2].split()[1]) # type: ignore
                if (len(vpr_stdout[i+3])>1):
                    results_dict["L"+vpr_stdout[i+3].split()[0]] = float(vpr_stdout[i+3].split()[1]) # type: ignore
                    if (len(vpr_stdout[i+4])>1):
                        results_dict["L"+vpr_stdout[i+4].split()[0]] = float(vpr_stdout[i+4].split()[1]) # type: ignore
                        if (len(vpr_stdout[i+5])>1):
                            results_dict["L"+vpr_stdout[i+5].split()[0]] = float(vpr_stdout[i+5].split()[1]) # type: ignore
                            if (len(vpr_stdout[i+6])>1):
                                results_dict["L"+vpr_stdout[i+6].split()[0]] = float(vpr_stdout[i+6].split()[1]) # type: ignore
                                if (len(vpr_stdout[i+7])>1):
                                    results_dict["L"+vpr_stdout[i+7].split()[0]] = float(vpr_stdout[i+7].split()[1]) # type: ignore
            if('Final critical path delay' in vpr_stdout[i] and 'Fmax:' in vpr_stdout[i]):
                    results_dict['Fmax'] = vpr_stdout[i].split()[9] + ' ' + vpr_stdout[i].split()[10]
                    results_dict['Critical path'] = vpr_stdout[i].split()[6] + ' ' + vpr_stdout[i].split()[7][:-1]
            if("Final intra-domain critical path delays (CPDs):" in vpr_stdout[i]):
                    for zz in range(2):
                        if( "CPD" in vpr_stdout[i+zz] and "MHz" in vpr_stdout[i+zz] and "virtual" not in vpr_stdout[i+zz]):
                            print( vpr_stdout[i+zz] )
                            results_dict[vpr_stdout[i+zz].split()[0] + " Fmax" ] =  vpr_stdout[i+zz].split()[6][1:] + vpr_stdout[i+zz].split()[7][:-1]
        
        io_count = 0
        for i in block_counts.keys():
            if("io" in i):
                io_count += int(block_counts[i])
        for i in block_usage.keys():
            if "io" in i:
                block_usage[i] = block_usage[i] + "/" + str(io_count)
            else:
                block_usage[i] = block_usage[i] + "/" + block_counts[i]
            results_dict[i] = block_usage[i] 
        return results_dict
    except Exception as e:
        print(e)
        return results_dict

def is_custom_tb_available(benchmark, tbs):
    #checks if a testbench matching the benchmark exists, e.g. counter.v and counter_tb.v, the naming is important here
    print(f"benchmark {benchmark}")
    print(tbs)
    for i in tbs:
        if(benchmark.get_name()+'_tb.v' in i):
            print('Using custom tb: ', i)
            return True
    return False

import os
from scripts.paths import get_fabric_path
from scripts.fix_tb import update_reset, remove_deposit

# xvlog SRC/counter_bram_dsp_automap_autocheck_top_tb.v SRC/fabric_netlists.v benchmark/counter_bram_dsp_automap.v
# xelab counter_bram_dsp_automap_autocheck_top_tb
# xsim work.counter_bram_dsp_automap_autocheck_top_tb -R

def generate_simulation_command(simulator, tb_type, benchmark, tbs, task_dir):
    """
    Generate simulation command based on simulator type, testbench type, and availability of custom testbench.
    """

    base_command = ''
    vlog_flags = '-suppress all +define+SIMULATION'
    vcs_flags = '-full64 +define+SIMULATION -hsopt=j -timescale=1ns/1ps'
    iverilog_flags = '-DSIMULATION'
    # xcelium_flags = ''
    fabric_netlists = 'SRC/fabric_netlists.v'
    # Define simulator-specific commands
    if simulator == "vlog":
        if tb_type == 4:  # full tb
            base_command = f'vlog {vlog_flags} SRC/{benchmark.get_name()}_autocheck_top_tb.v {fabric_netlists} benchmark/*.v ; vsim -do "run -all" -c {benchmark.get_name()}_autocheck_top_tb'
        elif tb_type == 3 and is_custom_tb_available(benchmark, tbs):  # custom preconfigured tb
            base_command = f'vlog {vlog_flags} ../../../../../benchmarks/{benchmark.get_name()}_tb.v SRC/{benchmark.get_name()}_top_formal_verification.v {fabric_netlists} ; vsim -do "run -all" -c {benchmark.get_name()}_tb'
        elif tb_type in [3, 2]:  # preconfigured tb
            base_command = f'vlog {vlog_flags} SRC/{benchmark.get_name()}_formal_random_top_tb.v SRC/{benchmark.get_name()}_top_formal_verification.v {fabric_netlists} benchmark/*.v ; vsim -do "run -all" -c {benchmark.get_name()}_top_formal_verification_random_tb'
        else:
            base_command = 'echo "Invalid testbench type"'
    elif simulator == "vcs":
        if tb_type == 4:  # full tb
            base_command = f'vcs {vcs_flags} SRC/{benchmark.get_name()}_autocheck_top_tb.v {fabric_netlists} benchmark/*.v ; ./simv'
        elif tb_type == 3 and is_custom_tb_available(benchmark, tbs):  # custom preconfigured tb
            base_command = f'vcs {vcs_flags} ../../../../../benchmarks/{benchmark.get_name()}_tb.v SRC/{benchmark.get_name()}_top_formal_verification.v {fabric_netlists} ; ./simv'
        elif tb_type in [3, 2]:  # preconfigured tb
            base_command = f'vcs {vcs_flags} SRC/{benchmark.get_name()}_formal_random_top_tb.v SRC/{benchmark.get_name()}_top_formal_verification.v {fabric_netlists} benchmark/*.v ; ./simv'
        else:
            base_command = 'echo "Invalid testbench type"'
    elif simulator == "iverilog":
        if tb_type == 4:  # full tb
            base_command = f'iverilog {iverilog_flags} SRC/{benchmark.get_name()}_autocheck_top_tb.v {fabric_netlists} benchmark/*.v ; ./simv'
        elif tb_type == 3 and is_custom_tb_available(benchmark, tbs):  # custom preconfigured tb
            base_command = f'iverilog {iverilog_flags} ../../../../../benchmarks/{benchmark.get_name()}_tb.v SRC/{benchmark.get_name()}_top_formal_verification.v {fabric_netlists} ; ./a.out'
        elif tb_type in [3, 2]:  # preconfigured tb
            base_command = f'iverilog {iverilog_flags} SRC/{benchmark.get_name()}_formal_random_top_tb.v SRC/{benchmark.get_name()}_top_formal_verification.v {fabric_netlists} benchmark/*.v ; ./a.out'
        else:
            base_command = 'echo "Invalid testbench type"'
    # elif simulator == "xvlog":
        # if tb_type == 4:  # full tb
            # base_command = f'xvlog {xcelium_flags} SRC/{benchmark.get_name()}_autocheck_top_tb.v {fabric_netlists} benchmark/*.v ; ./simv'
        # elif tb_type == 3 and is_custom_tb_available(benchmark, tbs):  # custom preconfigured tb
            # base_command = f'iverilog {xcelium_flags} ../../../../../benchmarks/{benchmark.get_name()}_tb.v SRC/{benchmark.get_name()}_top_formal_verification.v {fabric_netlists} ; ./a.out'
        # elif tb_type in [3, 2]:  # preconfigured tb
            # base_command = f'iverilog {xcelium_flags} SRC/{benchmark.get_name()}_formal_random_top_tb.v SRC/{benchmark.get_name()}_top_formal_verification.v {fabric_netlists} benchmark/*.v ; ./a.out'
        # else:
            # base_command = 'echo "Invalid testbench type"'
    else:
        base_command = 'echo "Simulator not supported"'

    return base_command


def is_custom_tb_available(benchmark, tbs):
    """
    Checks if a custom testbench is available for the given benchmark and testbenches list.
    """
    return benchmark.get_name()+"_tb.v" in tbs



def simulate(tb_type, benchmark, arch_name, simulator, tbs=['na'], run_status=True):
    task_dir = f"{os.getcwd()}/latest/{arch_name}/{benchmark.get_name()}/MIN_ROUTE_CHAN_WIDTH/"
    original_dir = os.getcwd()
    results_dict = {'Device': 0, 'io': 0, 'clb': 0, 'mult_18': 0, 'memory': 0, 'Fmax': 0, 'Critical path': 0, 'L1': 0, 'L2': 0, 'L4': 0}
    
    try:
        # Change directory to the task directory
        os.chdir(task_dir)
        if tb_type > 1 and tb_type != 5:
            os.system(f'cp -r {get_fabric_path()}/SRC/fabric_netlists.v ./SRC/')
    except Exception as e:
        print(e)
        print("Error: ", task_dir)
        os.chdir(original_dir)
        return False, results_dict
    
    if run_status:
        update_reset(tb_type, benchmark)
        if tb_type == 4:  # Full TB
            remove_deposit(benchmark.get_name())
        if(tb_type == 5):
            output = 'NO_TB'
        else:
            # Generate simulator command
            sim_command = generate_simulation_command(simulator, tb_type, benchmark, tbs, task_dir)
            print(f"Running simulation with command: {sim_command}")
            
            # Run the simulation
            stream = os.popen(sim_command)
            output = stream.read()
            print(output)
    else:
        print('Run failed')
        output = 'Run failed'
    
    try: 
        with open('vpr_stdout.log', 'r') as f:
            vpr_stdout = f.readlines()
    except Exception as e:
        print("Error reading vpr_stdout.log")
        print(e)
        os.chdir(original_dir)
        return False, results_dict

    results_dict = extract_reslts(vpr_stdout, run_status)
    os.chdir(original_dir)
    
    if 'Simulation Succeed' not in output and 'NO_TB' != output:
        print("Simulation Failed")
        print(f"Simulation Output: {output}")
        return False, results_dict
    else:
        return True, results_dict
