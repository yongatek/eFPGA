import os
import shutil
import glob
from scripts.task_helper import write_clock_constraints, map_rst_and_clocks, generate_bus_group_file, set_pin_constraints, flatten_constraints
from scripts.benchmark import Benchmark
from scripts.paths import get_TRISTAN_EFPGA_PATH, get_fabric_path
from scripts.fix_netlist import replace_def_net_type, fix_fabric_netlist_path, generate_flist
from scripts.utils.verilator_component_parser import verilator_component_parser as vcp
from scripts.utils.include_parser import include_parser as ip
from scripts.utils.include_parser import flist_parser as fp
from scripts.generate_layout_csv import gen_layout_csv


class TaskConf:
    def __init__(self, is_docker, pins_per_io):
        """
        Initialize TaskConf with is_docker and pins_per_io.
        Reads configuration from 'config/task.conf' and sets FPGA layout and architecture.
        """
        self.pins_per_io = pins_per_io
        self.is_docker = is_docker
        self.width = None
        self.height = None
        self.arch_name = None

        # Read configuration file
        self._read_config()

    def _read_config(self):
        """Reads the task configuration file and sets up layout and architecture."""
        try:
            with open('config/task.conf', 'r') as f:
                config_lines = f.readlines()

            # Parse configuration lines
            for line in config_lines:
                if "openfpga_vpr_device_layout" in line:
                    self.width, self.height = map(int, line[27:].split('x'))
                if 'arch0=${PATH:TASK_DIR}/' in line:
                    clocks = 2 if '2clk' in line else 1
                    self.arch_name = line[line.rfind('/')+1:line.rfind('.xml')]
        except FileNotFoundError:
            print("Configuration file 'config/task.conf' not found.")
            raise

    def get_fpga_size(self):
        """Returns the FPGA size as a tuple (width, height)."""
        return self.width, self.height

    def get_arch_name(self):
        return self.arch_name

    def set_benchmark(self, benchmark):
        """Sets the benchmark object."""
        self.benchmark = benchmark

    def set_openfpga_shell_script(self, tb_type):
        """Sets the appropriate OpenFPGA shell script based on testbench type."""
        scripts = [
            "openfpga_shell_template=${PATH:TASK_DIR}/../yonga_openfpga_shell_scripts/generate_fabric.openfpga\n",
            "openfpga_shell_template=${PATH:TASK_DIR}/../yonga_openfpga_shell_scripts/generate_sdc.openfpga\n",
            "openfpga_shell_template=${PATH:TASK_DIR}/../yonga_openfpga_shell_scripts/preconfigured_tb_with_bitstream.openfpga\n",
            "openfpga_shell_template=${PATH:TASK_DIR}/../yonga_openfpga_shell_scripts/preconfigured_tb_with_bitstream.openfpga\n",
            "openfpga_shell_template=${PATH:TASK_DIR}/../yonga_openfpga_shell_scripts/full_tb_with_bitstream.openfpga\n",
            "openfpga_shell_template=${PATH:TASK_DIR}/../yonga_openfpga_shell_scripts/generate_bitstream.openfpga\n"
        ]
        self.openfpga_shell_script = scripts[tb_type]
        self.tb_type = tb_type

    def update_task_conf(self):
        """Updates the task configuration file with the benchmark's name/path and pin constraints."""
        map_rst_and_clocks(self.benchmark)

        try:
            with open('config/task.conf', 'r') as f:
                task_conf_lines = f.readlines()

            for i in range(len(task_conf_lines)):
                if "bench0=" in task_conf_lines[i]:
                    task_conf_lines[i] = f"bench0=${{PATH:TASK_DIR}}/../{self.benchmark.get_path()}\n"
                if "bench0_top=" in task_conf_lines[i]:
                    task_conf_lines[i] = f"bench0_top={self.benchmark.get_name()}\n"
                if "openfpga_shell_template" in task_conf_lines[i]:
                    task_conf_lines[i] = self.openfpga_shell_script

            with open('config/task.conf', 'w') as f:
                f.writelines(task_conf_lines)
        except FileNotFoundError:
            print("Configuration file 'config/task.conf' not found.")
            raise

    def run_task(self):
        """Runs the task based on the testbench type."""
        if self.tb_type > 1:
            self.generate_pin_map_csv()
        else:
            self._cleanup_old_sdc() 
            if self.tb_type == 0 :
                self._cleanup_old_rtl() 

        flatten_constraints()
        return self._execute_task_flow()

    def _cleanup_old_sdc(self):
        """Removes old SDC directories if they exist."""
        sdc_path = '../yonga_archs/Fabric/SDC'
        tile_sdc_path = '../yonga_archs/Fabric/tile_SDC'
        for path in [sdc_path, tile_sdc_path]:
            if os.path.isdir(path):
                print(f"Removing old SDC at {path}!")
                shutil.rmtree(path)

    def _cleanup_old_rtl(self):
        """Removes old RTL directories if they exist."""
        src_path = '../yonga_archs/Fabric/SRC'
        if os.path.isdir(src_path):
            print(f"Removing old SRC at {src_path}!")
            shutil.rmtree(src_path)

    def _execute_task_flow(self):
        """Executes the task flow based on the docker environment."""
        if self.is_docker:
            return self._run_docker_task()
        else:
            return self._run_local_task()

    def _run_docker_task(self):
        """Runs the task in a Docker container."""
        UID = os.popen("id -u").read().strip()
        command = f"docker run -it --rm --user {UID} -v {get_TRISTAN_EFPGA_PATH()[:-1]}:/home/openfpga_user/ ghcr.io/lnis-uofu/openfpga-master:latest /home/openfpga_user/docker_entrypoint.sh"
        return self._run_task(command)

    def _run_local_task(self):
        """Runs the task using a local installation."""
        command = "python3 $OPENFPGA_PATH/openfpga_flow/scripts/run_fpga_task.py ./ --show_thread"
        return self._run_task(command)

    def _run_task(self, command):
        """Executes a task and checks for errors in the output."""
        stream = os.popen(command)
        output = stream.read()
        if 'ERROR' in output:
            print("Task execution failed with error.")
            return False
        print(output)

        if self.tb_type == 0:
            self._process_task_post_execution()

        return True

    def _process_task_post_execution(self):
        """Handles post-execution steps for testbench type 0."""
        fix_fabric_netlist_path()
        generate_flist()
        replace_def_net_type()
        vcp.parse_as_module(get_fabric_path() + "SRC/sub_module/", False, True)
        ip.modify_include_file("../yonga_archs/Fabric/SRC/fabric_netlists.v", "processed_modules_index.txt")
        fp.do_convert_include_to_flist("../yonga_archs/Fabric/SRC/fabric_netlists.v", "sub_module", "../yonga_archs/Fabric/SRC/fabric_netlists.flist", "sub_module")
        
        fabric_dir = glob.glob(os.path.join(os.getcwd(), 'latest', self.arch_name, '*', 'MIN_ROUTE_CHAN_WIDTH', 'vpr_placement.pdf'))
        
        if fabric_dir and not self.is_docker:
            shutil.copy(fabric_dir[0], get_fabric_path())

        x, y = self.get_fpga_size()
        gen_layout_csv(max(x, y))

    def generate_pin_map_csv(self):
        """Generates a CSV file for pin mapping."""
        height, width = self.get_fpga_size()
        height -= 2
        width -= 2

        file_path = f"{get_TRISTAN_EFPGA_PATH()[:-1]}/yonga_archs/Fabric/pin_map.csv"
        try:
            with open(file_path, 'w') as f:
                f.write("orientation,row,col,pin_num_in_cell,port_name,mapped_pin,GPIO_type,Associated Clock,Clock Edge\n")
                self._generate_pin_mapping(f, width, height)
        except IOError:
            print(f"Could not open {file_path}")
            print("Fabric not found! Please generate fabric first.")
            return False

        return True

    def _generate_pin_mapping(self, file, width, height):
        """Helper function to generate pin mapping for each side of the FPGA."""
        start = 0
        end = width * self.pins_per_io[0]
        for i in range(start, end):
            file.write(f'TOP,,,,gfpga_pad_EMBEDDED_IO_SOC_IN[{i}],pad_fpga_io[{i}],in,,\n')
            file.write(f'TOP,,,,gfpga_pad_EMBEDDED_IO_SOC_OUT[{i}],pad_fpga_io[{i}],out,,\n')

        start = end
        end += height * self.pins_per_io[1]
        for i in range(start, end):
            file.write(f'RIGHT,,,,gfpga_pad_EMBEDDED_IO_SOC_IN[{i}],pad_fpga_io[{i}],in,,\n')
            file.write(f'RIGHT,,,,gfpga_pad_EMBEDDED_IO_SOC_OUT[{i}],pad_fpga_io[{i}],out,,\n')

        start = end
        end += (width - 2) * self.pins_per_io[2]
        for i in range(start, end):
            file.write(f'BOTTOM,,,,gfpga_pad_EMBEDDED_IO_SOC_IN[{i}],pad_fpga_io[{i}],in,,\n')
            file.write(f'BOTTOM,,,,gfpga_pad_EMBEDDED_IO_SOC_OUT[{i}],pad_fpga_io[{i}],out,,\n')

        start = end
        end += (height - 2) * self.pins_per_io[3]
        for i in range(start, end):
            file.write(f'LEFT,,,,gfpga_pad_EMBEDDED_IO_SOC_IN[{i}],pad_fpga_io[{i}],in,,\n')
            file.write(f'LEFT,,,,gfpga_pad_EMBEDDED_IO_SOC_OUT[{i}],pad_fpga_io[{i}],out,,\n')
