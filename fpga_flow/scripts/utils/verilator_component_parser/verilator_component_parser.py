#----------------------------------------------------------------#
# Module:       Verilator Component Parser for TRISTAN eFPGA
# Company:      Yongatek Microelectronics
# Author:       Ugur Nezir
# Version:      0.2.1
# Description:  OpenFPGA generates several RTL files which
#               contain multiple modules within a single source
#               file. However, Verilator compiles designs that
#               have a singular component (module/class) only
#               which has the same filename with the component.
#
#               This module parses and dissects the components
#               Within Verilog/SystemVerilog source files, so
#               that we can compile and simulate the FPGA fabric
#               generated with OpenFPGA on Verilator.
#----------------------------------------------------------------#

import os
import argparse

INDEX_FILE = "processed_modules_index.txt"
PREFIX = "vmp_src_"
openfpga_comment_generation_override = False

def add_prefix_to_filenames(directory, prefix=PREFIX, file_types=None, debug=False):
    """
    Adds a prefix to all files in the directory that match the specified file types.
    
    Parameters:
    - directory (str): The directory containing the files to rename.
    - prefix (str): The prefix to add to the filenames.
    - file_types (list of str): List of file extensions to process. If None, all files are processed.
    - debug (bool): If True, prints detailed debug information.
    
    Returns:
    - None
    """
    # Check if any prefixed files already exist
    for filename in os.listdir(directory):
        if filename.startswith(prefix):
            print(f"Error: The directory '{directory}' is already processed. Prefixed file '{filename}' found.")
            exit(1)
    
    processed_modules = load_processed_modules()
    
    for filename in os.listdir(directory):
        if file_types and not any(filename.endswith(ext) for ext in file_types):
            continue
        if filename.startswith(prefix) or filename.replace(prefix, "") in processed_modules:
            if debug:
                print(f"Prefix already exists or file already processed: {filename}")
            continue
        old_path = os.path.join(directory, filename)
        if os.path.isfile(old_path):
            new_path = os.path.join(directory, prefix + filename)
            os.rename(old_path, new_path)
            if debug:
                print(f"Renamed {old_path} to {new_path}")

def load_processed_modules():
    """
    Loads the list of processed modules from the index file.
    
    Returns:
    - Set of processed module names.
    """
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r') as file:
            return set(line.strip() for line in file)
    return set()

def save_processed_module(module_name):
    """
    Saves a module name to the index file.
    
    Parameters:
    - module_name (str): The name of the module to save.
    
    Returns:
    - None
    """
    with open(INDEX_FILE, 'a') as file:
        file.write(f"{module_name}\n")

def process_files(directory, component_break, file_types=None, debug=False):
    """
    Processes files in the directory, splitting them into separate module/class files.
    
    Parameters:
    - directory (str): The directory containing the files to process.
    - component_break (str): The string that indicates the end of a component in the file.
    - file_types (list of str): List of file extensions to process. If None, all files are processed.
    - debug (bool): If True, prints detailed debug information.
    
    Returns:
    - None
    """
    processed_modules = load_processed_modules()
    
    for filename in os.listdir(directory):
        if not filename.startswith("vmp_src_"):
            continue
        if file_types and not any(filename.endswith(ext) for ext in file_types):
            continue
        if ("user_defined_templates" in filename):
            continue

        file_path = os.path.join(directory, filename)
        if not os.path.isfile(file_path):
            continue

        with open(file_path, 'r') as file:
            buffer = ""
            module_name = None
            for line in file:
                buffer += line
                if ("module " in line or "class " in line) and "(" in line:
                    module_name = line.split()[1].split("(")[0].strip()
                    if module_name in processed_modules:
                        if debug:
                            print(f"Module/Class {module_name} in {filename} has already been processed. Refer to {INDEX_FILE}.")
                        module_name = None  # Reset module_name to avoid processing
                        buffer = ""
                        continue
                if component_break in line:
                    if module_name:
                        new_filename = os.path.join(directory, f"{module_name}.v")
                        if os.path.exists(new_filename):
                            print(f"Error: File {new_filename} already exists.")
                        else:
                            with open(new_filename, 'w') as new_file:
                                new_file.write(buffer)
                            save_processed_module(module_name)
                            if debug:
                                print(f"Created file: {new_filename}")
                        buffer = ""
                        module_name = None
                    else:
                        if not openfpga_comment_generation_override:
                            print(f"Error: Module/Class name not found in file {filename}.\n(Can be ignored if no modules are inside as end of file comments cause this error. [to check, switch debug = True])")
                        else:
                            print(f"Warning: Module/Class name not found in file {filename}. Can be ignored in OpenFPGA flow.")
                        if debug:
                            print(f"Buffer content:\n{buffer}")
            if buffer.strip() and module_name:
                new_filename = os.path.join(directory, f"{module_name}.v")
                if os.path.exists(new_filename):
                    print(f"Error: File {new_filename} already exists.")
                else:
                    with open(new_filename, 'w') as new_file:
                        new_file.write(buffer)
                    save_processed_module(module_name)
                    if debug:
                        print(f"Created file: {new_filename}")
            elif buffer.strip():
                if not openfpga_comment_generation_override:
                    print(f"Error: Module/Class name not found in file {filename}.\n(Can be ignored if no modules are inside as end of file comments cause this error. [to check, switch debug = True])")
                elif debug:
                    print(f"Warning: Module/Class name not found in file {filename}. Can be ignored in OpenFPGA flow.")
                    print(f"Buffer content:\n{buffer}")

def cleanup_files(directory, prefix="vmp_src_", file_types=None, debug=False):
    """
    Deletes source files with the specified prefix in the directory.
    
    Parameters:
    - directory (str): The directory containing the files to delete.
    - prefix (str): The prefix of the filenames to delete.
    - file_types (list of str): List of file extensions to process. If None, all files are processed.
    - debug (bool): If True, prints detailed debug information.
    
    Returns:
    - None
    """
    for filename in os.listdir(directory):
        if filename.startswith(prefix):
            if file_types and not any(filename.endswith(ext) for ext in file_types):
                continue
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                if debug:
                    print(f"Deleted file: {file_path}")

def parse_as_module(directory, debug, openfpga_override = False):
    """
    Main function alternative to enable utilization from run_task.py in TRISTAN eFPGA flow.
    Parameters:
    - directory: The directory where the parsing and dissecting shall occur.
    - debug: Detailed debug print enable flag.
    
    Returns:
    - None
    """
    global openfpga_comment_generation_override
    openfpga_comment_generation_override = openfpga_override

    if os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)
        if debug:
            print(f"Cleared the index file: {INDEX_FILE}")

    add_prefix_to_filenames(directory, file_types=['.v', '.sv', '.vh', '.svh'], debug=debug)
    process_files(directory, 'endmodule', file_types=['.v', '.sv', '.vh', '.svh'], debug=debug)
    cleanup_files(directory, file_types=['.v', '.sv', '.vh', '.svh'], debug=debug)

def main():
    """
    Main function to parse command-line arguments and perform file processing and cleanup.
    
    Parameters:
    - None
    
    Returns:
    - None
    """
    parser = argparse.ArgumentParser(description='Process and cleanup Verilog and SystemVerilog files.')
    parser.add_argument('--directory', required=True, help='Directory containing the files to process.')
    parser.add_argument('--file_type', nargs='*', default=['.v', '.sv', '.vh', '.svh'], help='File extensions to process.')
    parser.add_argument('--component_break', default='endmodule', help='String that indicates the end of a component in the file.')
    parser.add_argument('--cleanup', action='store_true', help='Delete source files with "vmp_src_" prefix after processing.')
    parser.add_argument('--debug', action='store_true', help='Display detailed process information.')
    parser.add_argument('--clean_run', action='store_true', help='Remove the contents of the index file to run a fresh run.')

    args = parser.parse_args()
    directory = args.directory
    file_types = args.file_type
    component_break = args.component_break
    cleanup = args.cleanup
    debug = args.debug
    clean_run = args.clean_run

    if clean_run:
        if os.path.exists(INDEX_FILE):
            os.remove(INDEX_FILE)
            if debug:
                print(f"Cleared the index file: {INDEX_FILE}")

    add_prefix_to_filenames(directory, file_types=file_types, debug=debug)
    process_files(directory, component_break, file_types=file_types, debug=debug)
    if cleanup:
        cleanup_files(directory, file_types=file_types, debug=debug)

if __name__ == "__main__":
    main()
