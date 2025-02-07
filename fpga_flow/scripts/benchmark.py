#----------------------------------------------------------------#
# Module:       Benchmark class
# Company:      Yongatek Microelectronics
# Author:       Ahmad Houraniah
# Version:      0.1.0
# Description:  This class stores information about the current 
#               benchmark, including the benchmark name, path, and
#               top module code.
#----------------------------------------------------------------#

import os
import re
from scripts.paths import get_TRISTAN_EFPGA_PATH

class Benchmark:
    def __init__(self, name: str):
        """
        Initializes the Benchmark object.

        Parameters:
            name (str): The name of the benchmark file or directory.
        """
        self.name = name[:-2] if name.endswith(".v") else name
        self.is_dir = os.path.isdir(get_TRISTAN_EFPGA_PATH() + "benchmarks/" + self.name)
        self.path = self._get_benchmark_path()
        self.top_module_code = self._load_top_module_code()

    def _get_benchmark_path(self) -> str:
        """
        Determines the path of the benchmark.

        Returns:
            str: The path of the benchmark.
        """
        if self.is_dir:
            return f"benchmarks/{self.name}/*.v"
        return f"benchmarks/{self.name}.v"

    def _load_top_module_code(self):
        """
        Loads the top module code from the benchmark file.

        Returns:
            list[str]: The lines of the top module code.
        """
        try:
            file_path = get_TRISTAN_EFPGA_PATH() + self.path.replace("*.v", f"/{self.name}.v")
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Remove single-line comments
            lines = [re.sub(r'//.*', '', line) for line in lines]

            # Remove block comments
            code = ''.join(lines)
            code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
            lines = code.split('\n')

            # Find and replace parameters
            parameters = {}
            for line in lines:
                match = re.match(r'\s*parameter\s+(\w+)\s*=\s*(\d+)\s*;', line)
                if match:
                    parameters[match.group(1)] = match.group(2)

            # Handle parameterized module definitions
            param_match = re.search(r'#\((.*?)\)', ''.join(lines), re.DOTALL)
            if param_match:
                param_str = param_match.group(1)
                param_lines = param_str.split(',')
                for param_line in param_lines:
                    match = re.match(r'\s*parameter\s+(\w+)\s*=\s*(\d+)\s*', param_line)
                    if match:
                        parameters[match.group(1)] = match.group(2)

            def replace_parameters(line):
                for param, value in parameters.items():
                    line = re.sub(rf'\b{param}\b', value, line)
                return line

            lines = [replace_parameters(line) for line in lines]

            return lines
        except FileNotFoundError:
            print(f"Top level should be named {self.name}.v")
            return []

    def get_top_module_code(self) :
        """
        Retrieves the top module code.

        Returns:
            list[str]: The lines of the top module code.
        """
        return self.top_module_code

    def get_name(self) -> str:
        """
        Retrieves the name of the benchmark.

        Returns:
            str: The name of the benchmark.
        """
        return self.name

    def get_path(self) -> str:
        """
        Retrieves the path of the benchmark.

        Returns:
            str: The path of the benchmark.
        """
        return self.path
