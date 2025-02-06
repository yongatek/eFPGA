#----------------------------------------------------------------#
# Module:       Include Parser for TRISTAN eFPGA
# Company:      Yongatek Microelectronics
# Author:       Ugur Nezir
# Version:      0.2.1
# Description:  A helper script to update OpenFPGA-generated
#               fabric netlist based on the Verilator Component
#               Parser modifications.
#----------------------------------------------------------------#

import argparse

def modify_filenames(input_file, output_file, prefix, suffix):
    """
    Modifies the filenames obtained from an input file to have specific prefix and suffix to turn it
    into an include statement.

    Parameters:
    - input_file: Input file name which is the custom string section.
    - output_file: Output file name which shall have the modified include statements.
    - prefix: Substring to append in front of the filenames (e.g. `include "../../)
    - suffix: Substring to append in end of the filenames (e.g. .v/")
    
    Returns:
    - None
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            filename = line.strip()
            modified_filename = f"{prefix}{filename}{suffix}"
            outfile.write(modified_filename + '\n')

def modify_include_file(target_file_path, module_list_path):
    """
    A variation of modify_filenames() function to be called from run_task.py script in TRISTAN eFPGA flow.

    Parameters:
    - target_file_path: Output file name which shall have the modified include statements replacing the original OpenFPGA generation.
    - module_list_path: Input file name which includes the module name list.

    Returns:
    - None
    """
    # Define markers and substrings for identification
    start_comment = "// ------ Include primitive module netlists -----"
    end_comment = "// ------ Include logic block netlists -----"
    include_path_marker = "/sub_module/"

    # Read the target file
    with open(target_file_path, "r") as file:
        lines = file.readlines()

    # Find target commands and do the extraction
    start_index = None
    end_index = None
    include_paths = None

    for i, line in enumerate(lines):
        if start_comment in line:
            start_index = i

        elif end_comment in line:
            end_index = i
            break

        elif include_path_marker in line:
            start_pos = line.find('`include') + len ('`include')
            end_pos = line.find(include_path_marker) + len(include_path_marker)
            include_paths = line[start_pos:end_pos]

    # Ensure both comments are found and include paths are extracted
    if ((start_index is None) or (end_index is None) or (include_paths is None) or (start_index >= end_index)):
        print("start_index: " + str(start_index))
        print("end_index: " + str(end_index))
        raise ValueError("Could not find valid comment markers or include paths")

    # Read the module filenames
    with open(module_list_path, "r") as file:
        filenames = [line.strip() for line in file.readlines()]

    # Prefix and suffix the individual module filenames for include statements
    suffix = '.v"'
    modified_filenames = [f'`include{include_paths}{filename}{suffix}' for filename in filenames]

    # Replace the content between the comments with the new lines
    new_lines = lines[:start_index + 1] + [line + "\n" for line in modified_filenames] + lines[end_index:]

    # Write the updated content back to the target file:
    with open(target_file_path, "w") as file:
        file.writelines(new_lines)
        file.writelines("\n")

def main():
    parser = argparse.ArgumentParser(description = 'Modify filenames by adding prefix and suffixes for include statements.')
    parser.add_argument('--input_file', required = True, help = 'Path to the input file containing filenames.')
    parser.add_argument('--output_file', required = True, help = 'Path to the output file containing modified filenames.')
    parser.add_argument('--prefix', default = '', help = 'String to append to the start of each filename.')
    parser.add_argument('--suffix', default = '', help = 'String to append to the end of each filename.')

    args = parser.parse_args()

    modify_filenames(args.input_file, args.output_file, args.prefix, args.suffix)

if __name__ == "__main__":
    main()

