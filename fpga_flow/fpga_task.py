#----------------------------------------------------------------#
# Module:       eFPGA Flow script
# Company:      Yongatek Microelectronics
# Author:       Ahmad Houraniah
# Version:      0.2.0
# Description:  This script is used to generated FPGA fabrics (RTL and Timing Constraints),
#               generate bitstreams and testbenches, evaluate FPGA performance, 
#               and run simulations.
#----------------------------------------------------------------#

import os
import csv
import time
from scripts.utils.verilator_component_parser import verilator_component_parser as vcp
from scripts.utils.include_parser import include_parser as ip
from scripts.utils.include_parser import flist_parser as fp
from scripts.benchmark import Benchmark
from scripts.task_conf import TaskConf
from scripts.simulate import simulate
from scripts.fix_sdc import generate_tile_based_sdcs
from scripts.task_helper import generate_bus_group_file, set_pin_constraints

def use_docker() -> bool:
    """
    Checks if the script is running in a Docker environment.

    Returns:
        bool: True if running in Docker, False otherwise.
    """
    openfpga_path = os.getenv('OPENFPGA_PATH')
    return openfpga_path is None or openfpga_path.strip() == ""

def get_benchmarks_and_tbs():
    """
    Retrieves and sorts the list of benchmarks and testbenches.

    Returns:
        tuple: A tuple containing two lists - benchmarks and testbenches.
    """
    benchmarks_and_tbs = os.listdir('../benchmarks')
    benchmarks_and_tbs.sort()
    benchmarks = [item for item in benchmarks_and_tbs if 'tb' not in item]
    tbs = [item for item in benchmarks_and_tbs if 'tb' in item]
    return benchmarks, tbs

def select_benchmark(benchmarks, tb_type):
    """
    Selects a benchmark based on user input.

    Parameters:
        benchmarks (list[str]): List of available benchmarks.
        tb_type (int): Type of testbench.

    Returns:
        list[str]: List of selected benchmarks.
    """
    if tb_type < 2:
        selected_benchmark = benchmarks.index("or2.v")
    else:
        for i, benchmark in enumerate(benchmarks):
            print(i, benchmark)
        selected_benchmark = int(input("Select benchmark:\n99 for all\n"))

    if selected_benchmark != 99:
        return [benchmarks[selected_benchmark]]
    return benchmarks

def run_task_for_benchmark(task_conf_script: TaskConf, benchmark: Benchmark, tb_type: int, arch_name: str, simulator: str, tbs, autoset_pcf = False):
    """
    Runs the task for a given benchmark.

    Parameters:
        task_conf_script (TaskConf): Task configuration script.
        benchmark (Benchmark): The benchmark to run.
        tb_type (int): Type of testbench.
        arch_name (str): Architecture name.
        simulator (str): Simulator to use.
        tbs (list[str]): List of testbenches.

    Returns:
        tuple: A tuple containing the simulation result and area dictionary.
    """
    task_conf_script.set_benchmark(benchmark)
    generate_bus_group_file(benchmark)
    if(autoset_pcf):
        set_pin_constraints(benchmark)
    else:
        if input("Set PCF? (y/n): ") == "y":
            try:
                set_pin_constraints(benchmark)
            except Exception as e:
                print(e)
                print("set pcf failed")
        else:
            os.system("> config/constraints/constraints.pcf")

    task_conf_script.update_task_conf()
    run_status = task_conf_script.run_task()
    sim_res, area = simulate(tb_type, benchmark, arch_name, simulator, tbs, run_status)
    return sim_res, area


def set_simulator() -> str:
    """
    Sets the simulator to use for simulation.

    Returns:
        str: The simulator to use.
    """
    simulators = ["vcs", "vlog", "iverilog"] # Synopsys VCS, ModelSim/QuestaSim, Icarus Verilog
    for simulator in simulators:
        if os.system(f"command -v {simulator}") == 0:
            return simulator
    raise EnvironmentError("No suitable simulator found")

def main():
    pins_per_io = [2, 2, 2, 2]
    simulator = set_simulator()
    freq = (50, 10, 10)
    docker = use_docker()
    task_conf_script = TaskConf(docker, pins_per_io)
    arch_name = task_conf_script.get_arch_name()
    clocks = 0

    benchmarks, tbs = get_benchmarks_and_tbs()
    tb_type = int(input("0: Generate_fabric \n1: Generate_sdc \n2: Preconfigured testbench \n3: Custom preconfigured testbench (when available) \n4: Full testbench\n5: Generate Bitstream\n"))
    benchmarks = select_benchmark(benchmarks, tb_type)

    task_conf_script.set_openfpga_shell_script(tb_type)
    if tb_type > 1:
        results = []
        # Different headers based on tb_type
        headers = ["Benchmark", "Device Utilization", "IO Utilization", "CLB Utilization", 
                  "DSP Utilization", "BRAM Utilization", "Fmax", "Critical path", 
                  'L1 Utilization', 'L2 Utilization', 'L4 Utilization']
        if tb_type != 5:
            headers.insert(1, "Simulation Result")
        row_list = [headers]
        
        start_time = time.time()
        for benchmark_name in benchmarks:
            benchmark = Benchmark(benchmark_name)
            print(f'************************************************\nBENCHMARK : {benchmark.get_name()}\n************************************************')
            try:
                if len(benchmarks) > 1:
                    autoset_pcf = True
                else:  
                    autoset_pcf = False
                sim_res, area = run_task_for_benchmark(task_conf_script, benchmark, tb_type, arch_name, simulator, tbs, autoset_pcf)
                if tb_type == 5:
                    results.append(f'{area}')
                    row_data = [benchmark.get_name(), area["Device"], area['io'], area['clb'], 
                              area['mult_18'], area['memory'], area['Fmax'], area['Critical path'], 
                              area['L1'], area['L2'], area['L4']]
                else:
                    results.append(f'Simulation Result : {"Passed!" if sim_res else "Failed!"} || {area}')
                    row_data = [benchmark.get_name(), "Passed!" if sim_res else "Failed!"]
                    row_data.extend([area["Device"], area['io'], area['clb'], area['mult_18'], 
                                   area['memory'], area['Fmax'], area['Critical path'], 
                                   area['L1'], area['L2'], area['L4']])
                row_list.append(row_data)
            except Exception as e:
                print(e)
                if tb_type == 5:
                    results.append('na')
                    row_list.append([benchmark.get_name()] + ['na'] * (len(headers)-1))
                else:
                    results.append('Simulation Result : Failed! || na')
                    row_list.append([benchmark.get_name(), "Failed!"] + ['na'] * (len(headers)-2))
                print(f'{benchmark.get_name()} failed')
            if not sim_res and tb_type != 5:
                print('Failed sim !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('************************************************')

        for benchmark_name, result in zip(benchmarks, results):
            if tb_type == 5:
                print(f'Benchmark: {benchmark_name} || {result}')
            else:
                print(f'Benchmark: {benchmark_name} {result}')
        print(f"Total time: {round(time.time() - start_time, 2)} seconds")
        with open('results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(row_list)
    else:
        benchmark = Benchmark(benchmarks[0])
        task_conf_script.set_benchmark(benchmark)
        task_conf_script.update_task_conf()
        task_conf_script.run_task()
        if tb_type == 1:
            generate_tile_based_sdcs(freq)

if __name__ == "__main__":
    main()

