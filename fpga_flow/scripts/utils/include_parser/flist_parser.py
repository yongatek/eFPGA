#----------------------------------------------------------------#
# Module:       Flist Parser for TRISTAN eFPGA
# Company:      Yongatek Microelectronics
# Author:       Ugur Nezir
# Version:      0.1.0
# Description:  A helper script to update OpenFPGA-generated
#               fabric flist based on the Verilator Component
#               Parser modifications.
#----------------------------------------------------------------#

def fetch_lines_with_substring(file_path, substring):
    lines = []

    with open(file_path, 'r') as file:
        for line in file:
            if substring in line:
                lines.append(line)
    
    return lines

def convert_include_to_flist_format(lines):
    converted_lines = []

    for line in lines:
        converted_line = line.replace('`include ', '').replace('"', '').strip()
        converted_lines.append(converted_line)

    return converted_lines

def replace_flist(file_path, substring, replacement_lines):

    replacement_done = False

    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if substring in line:
                if not replacement_done:
                    for replacement_line in replacement_lines:
                        file.write(replacement_line + '\n')

                    replacement_done = True

            else:
                file.write(line)

def do_convert_include_to_flist(include_file_path, include_substring, flist_file_path, flist_substring):
    replacement_lines = convert_include_to_flist_format(fetch_lines_with_substring(include_file_path, include_substring))
    replace_flist(flist_file_path, flist_substring, replacement_lines)
