import os
from scripts.paths import get_fabric_path
from scripts.fix_tb import update_reset, remove_deposit
from scripts.task_helper import load_device_resources
from scripts.task_helper import generate_bitstream_c

def parse_required_resources(failure_message):
    """
    Parse the required resources from the failure message.
    Example: "Failed to find device which satisfies resource requirements required: io: 128, clb: 217, mult_16: 3, memory: 16"
    """
    required_resources = {}
    try:
        # Extract the part after "required:"
        if "required:" in failure_message:
            required_part = failure_message.split("required:")[1].split("(available")[0].strip()
            
            # Parse each resource type
            parts = required_part.split(',')
            for part in parts:
                part = part.strip()
                if ':' in part:
                    resource_type, value = part.split(':', 1)
                    resource_type = resource_type.strip()
                    value = value.strip()
                    try:
                        required_resources[resource_type] = int(value)
                    except ValueError:
                        pass
    except Exception as e:
        print(f"Error parsing required resources: {e}")
    
    return required_resources

def extract_reslts(vpr_stdout, run_status):
    """
    This function is used to extract results from a the vpr (PnR tool) logs.
    """
    usage_flag = False
    count_flag = False
    tmp_flag   = False
    results_dict = {'Device':0, 'io':0, 'clb':0, 'mult_16':0, 'memory':0, 'Fmax':0, 'Critical path':0, 'L1':0, 'L2':0, 'L4':0}
    block_usage={}
    block_counts = {}
    io_count=0
    design_doesnt_fit = False
    failure_message = ""
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
            if("Failed to find device which satisfies resource requirements required:" in vpr_stdout[i]):
                design_doesnt_fit = True
                failure_message = vpr_stdout[i].strip()
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
        
        # Always use device resources from JSON
        device_resources = load_device_resources()
        
        if design_doesnt_fit:
            # Parse required resources from failure message
            required_resources = parse_required_resources(failure_message)
            
            # Format as required/available
            results_dict['io'] = f"{required_resources.get('io', 0)}/{device_resources['io']}"
            results_dict['clb'] = f"{required_resources.get('clb', 0)}/{device_resources['clb']}"
            results_dict['mult_16'] = f"{required_resources.get('mult_16', 0)}/{device_resources['mult_16']}"
            results_dict['memory'] = f"{required_resources.get('memory', 0)}/{device_resources['memory']}"
            results_dict['Device'] = 0.95  # Indicate high utilization caused failure
        else:
            # For successful runs, still use JSON for available resources but parse usage from logs
            io_count = 0
            for i in block_counts.keys():
                if("io" in i):
                    io_count += int(block_counts[i])
            
            # Format using device resources from JSON for denominators
            for i in block_usage.keys():
                if "io" in i:
                    results_dict[i] = f"{block_usage[i]}/{device_resources['io']}"
                elif i == "clb":
                    results_dict[i] = f"{block_usage[i]}/{device_resources['clb']}"
                elif i == "mult_16":
                    results_dict[i] = f"{block_usage[i]}/{device_resources['mult_16']}"
                elif i == "memory":
                    results_dict[i] = f"{block_usage[i]}/{device_resources['memory']}"
                else:
                    # For other resources, use the old logic as fallback
                    results_dict[i] = block_usage[i] + "/" + block_counts.get(i, "0")
        
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


def generate_simulation_command(simulator, tb_type, benchmark, tbs, task_dir):
    """
    Generate simulation command based on simulator type, testbench type, and availability of custom testbench.
    """

    base_command = ''
    vlog_flags = '-suppress all +define+SIMULATION+UNIT_DELAY +incdir+../../../../../yonga_archs/'
    vcs_flags = '-full64 +define+SIMULATION+UNIT_DELAY -hsopt=j -timescale=1ns/1ps +incdir+../../../../../yonga_archs/'
    xrun_flags = '-delay_trigger +define+SIMULATION+UNIT_DELAY -gateloopwarn  +access+r \'-timescale\' \'1ns/1ps\' +incdir+../../../../../yonga_archs/'
    iverilog_flags = '-DSIMULATION -UNIT_DELAY'
    fabric_netlists = 'SRC/fabric_netlists.v'
    # Define simulator-specific commands
    if simulator == "vlog":
        if tb_type == 4:  # full tb
            base_command = f'vlog {vlog_flags} SRC/{benchmark.get_name()}_autocheck_top_tb.v {fabric_netlists} benchmark/*.v ; vsim -voptargs=+acc=npr -suppress 16154 -do "run -all" -c {benchmark.get_name()}_autocheck_top_tb'
        elif tb_type == 3 and is_custom_tb_available(benchmark, tbs):  # custom preconfigured tb
            base_command = f'vlog {vlog_flags} ../../../../../benchmarks/{benchmark.get_name()}_tb.v SRC/{benchmark.get_name()}_top_formal_verification.v {fabric_netlists} ; vsim -voptargs=+acc=npr -suppress 16154 -do "run -all" -c {benchmark.get_name()}_tb'
        elif tb_type in [3, 2]:  # preconfigured tb
            base_command = f'vlog {vlog_flags} SRC/{benchmark.get_name()}_formal_random_top_tb.v SRC/{benchmark.get_name()}_top_formal_verification.v {fabric_netlists} benchmark/*.v ; vsim -voptargs=+acc=npr -suppress 16154 -do "run -all" -c {benchmark.get_name()}_top_formal_verification_random_tb'
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
    elif simulator == "xrun":
        if tb_type == 4:  # full tb
            base_command = f'xrun {xrun_flags} SRC/{benchmark.get_name()}_autocheck_top_tb.v {fabric_netlists} benchmark/*.v '
        elif tb_type == 3 and is_custom_tb_available(benchmark, tbs):  # custom preconfigured tb
            base_command = f'xrun {xrun_flags} ../../../../../benchmarks/{benchmark.get_name()}_tb.v SRC/{benchmark.get_name()}_top_formal_verification.v {fabric_netlists} '
        elif tb_type in [3, 2]:  # preconfigured tb
            base_command = f'xrun {xrun_flags} SRC/{benchmark.get_name()}_formal_random_top_tb.v SRC/{benchmark.get_name()}_top_formal_verification.v {fabric_netlists} benchmark/*.v'
        else:
            base_command = 'echo "Invalid testbench type"'
    else:
        base_command = 'echo "Simulator not supported"'

    return base_command


def is_custom_tb_available(benchmark, tbs):
    """
    Checks if a custom testbench is available for the given benchmark and testbenches list.
    """
    return benchmark.get_name()+"_tb.v" in tbs



def simulate(tb_type, benchmark, arch_name, simulator, run_number, tbs=['na'], run_status=True):
    task_dir = f"{os.getcwd()}/run{run_number:03d}/{arch_name}/{benchmark.get_name()}/MIN_ROUTE_CHAN_WIDTH/"
    original_dir = os.getcwd()
    results_dict = {'Device': 0, 'io': 0, 'clb': 0, 'mult_16': 0, 'memory': 0, 'Fmax': 0, 'Critical path': 0, 'L1': 0, 'L2': 0, 'L4': 0}
    
    try:
        # Change directory to the task directory
        os.chdir(task_dir)
        if tb_type > 1 and tb_type != 5:
            os.system(f'mkdir -p ./SRC ; cp -r {get_fabric_path()}/SRC/fabric_netlists.v ./SRC/')
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
            generate_bitstream_c()
            output = 'NO_TB'
        else:
            generate_bitstream_c()
            # Generate simulator command
            sim_command = generate_simulation_command(simulator, tb_type, benchmark, tbs, task_dir)
            print(f"Running simulation with command: {sim_command}")
            
            # Run the simulation
            stream = os.popen(sim_command)
            output = stream.read()
            
            # Write simulation output to log file
            simulation_log_path = os.path.join(task_dir, 'simulation.log')
            try:
                with open('simulation.log', 'w') as log_file:
                    log_file.write(f"Simulation Command: {sim_command}\n")
                    log_file.write("=" * 50 + "\n")
                    log_file.write("Simulation Output:\n")
                    log_file.write("=" * 50 + "\n")
                    log_file.write(output)
                
                # Print status with log path
                if 'Simulation Succeed' in output:
                    print(f"Simulation PASSED - Log at: {simulation_log_path}")
                else:
                    print(f"Simulation FAILED - Log at: {simulation_log_path}")
                    
            except Exception as e:
                print(f"Error writing simulation log: {e}")
                print(output)  # Fallback to printing if log write fails
    else:
        output = 'Bitstream was not generated'
    
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
    
    if 'Simulation Succeed' not in output and 'NO_TB' != output and run_status:
        print("Simulation Failed")
        print(f"Simulation Output: {output}")
        return False, results_dict
    else:
        return run_status, results_dict
