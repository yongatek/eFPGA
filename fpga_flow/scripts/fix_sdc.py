#----------------------------------------------------------------#
# Module:       SDC File Generation and Fixer
# Company:      Yongatek Microelectronics
# Author:       Ahmad Houraniah
# Version:      0.1.0
# Description:  This module handles the generation and modification 
#               of Synopsys Design Constraints (SDC) files for FPGA
#               fabric timing analysis. It processes tile-based designs 
#               and extracts timing constraints from various sub-modules
#               like switch boxes (sb) and connection boxes (cbx).
#----------------------------------------------------------------#


import os
import re
from typing import Dict, List, Tuple, Optional
from pathlib import Path


# Constants
FABRIC_PATH = '../yonga_archs/Fabric'
TILE_PATH = f'{FABRIC_PATH}/SRC/tile'
SDC_DIR = Path("../yonga_archs/Fabric/tile_SDC")
FPGA_TOP_PREFIX = 'fpga_top/'
CREATE_CLOCK_KEYWORD = 'create_clock'

def extract_module_instances(text: str, pattern: str) :
    """
    Extracts module instances from text using regex pattern.
    
    Args:
        text (str): Verilog source text
        pattern (str): Regex pattern for matching module instances
    
    Returns:
        List[str]: List of extracted module instance names
    """
    matches = re.findall(pattern, text)
    return [f"{pattern.split('_')[0]}_{X}__{Y}_" for X, Y in matches]

def read_tile_file(tile_path: str) -> Optional[str]:
    """
    Reads content of a tile file.
    
    Args:
        tile_path (str): Path to the tile file
    
    Returns:
        Optional[str]: File contents or None if file cannot be read
    """
    try:
        with open(tile_path, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"Failed to read tile file {tile_path}: {e}")
        return None

import os
import re


def get_submodules():
    sub_modules = {}
    sub_module_instances = {}

    # Define all patterns to search for in the file
    patterns = [
        (r"sb_(?P<X>\d+)__(?P<Y>\d+)_ sb", lambda x, y: f"sb_{x}__{y}_"),
        (r"cbx_(?P<X>\d+)__(?P<Y>\d+)_ cbx", lambda x, y: f"cbx_{x}__{y}_"),
        (r"cby_(?P<X>\d+)__(?P<Y>\d+)_ cby", lambda x, y: f"cby_{x}__{y}_"),
        (r"grid_io_side_t ", lambda *_: "grid_io_side_t"),
        (r"grid_io_side_r ", lambda *_: "grid_io_side_r"),
        (r"grid_io_side_l ", lambda *_: "grid_io_side_l"),
        (r"grid_io_side_b ", lambda *_: "grid_io_side_b"),
        (r"grid_mult_18 ", lambda *_: "grid_mult_18"),
        (r"grid_memory ", lambda *_: "grid_memory"),
        (r"grid_clb ", lambda *_: "grid_clb"),
    ]

    try:
        tile_files = os.listdir('../yonga_archs/Fabric/SRC/tile/')
    except FileNotFoundError:
        print(f"Current Directory: {os.getcwd()}")
        print("**************************************************************************************")
        print("Fabric netlist not found! Please generate the fabric before running this script.")
        print("**************************************************************************************")
        return {}, {}

    # Process each tile file
    for tile_file in tile_files:
        tile_name = tile_file[:-2]  # Remove file extension
        sub_modules[tile_name] = []
        sub_module_instances[tile_name] = []

        tile_path = f'../yonga_archs/Fabric/SRC/tile/{tile_file}'
        with open(tile_path, 'r') as file:
            content = file.read()

        # Match all patterns in the content
        for pattern, formatter in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    sub_modules[tile_name].append(formatter(*match))
                else:
                    sub_modules[tile_name].append(formatter())

        # Extract submodule instances
        with open(tile_path, 'r') as file:
            lines = file.readlines()
        for submodule in sub_modules[tile_name]:
            for line in lines:
                if f"\t{submodule} " in line:
                    sub_module_instances[tile_name].append(line.split()[1])
                    break

    return sub_modules, sub_module_instances

def create_sdc(tile_name, submodules, freq):
    sdc_dir = '../yonga_archs/Fabric/SDC'
    tile_sdc_dir = '../yonga_archs/Fabric/tile_SDC'

    # Categorize SDC files
    sdc_files = {
        'io': [],
        'mult': [],
        'clb': [],
        'memory': []
    }

    for filename in os.listdir(sdc_dir):
        for key in sdc_files:
            if key in filename:
                sdc_files[key].append(filename)
                break
    # Ensure the tile_SDC directory exists
    os.makedirs(tile_sdc_dir, exist_ok=True)
    temp_sdc_path = os.path.join(tile_sdc_dir, f'{tile_name}_temp.sdc')

    with open(temp_sdc_path, 'w') as temp_sdc:
        for module in submodules:
            if 'io' in module:
                _write_sdc_files(temp_sdc, sdc_dir, sdc_files['io'])

            elif 'mult' in module:
                _write_sdc_files(temp_sdc, sdc_dir, sdc_files['mult'])

            elif 'clb' in module:
                _write_clock_constraints(temp_sdc, 'clb', freq[0])
                _write_sdc_files(temp_sdc, sdc_dir, sdc_files['clb'])

            elif 'memory' in module:
                _write_clock_constraints(temp_sdc, 'memory', freq[0])
                _write_sdc_files(temp_sdc, sdc_dir, sdc_files['memory'])

            else:
                custom_sdc_path = os.path.join(sdc_dir, f'{module}.sdc')
                _write_file_contents(temp_sdc, custom_sdc_path)

    # Fix paths and write the final SDC
    final_sdc_path = os.path.join(tile_sdc_dir, f'{tile_name}.sdc')
    _fix_sdc_paths(temp_sdc_path, final_sdc_path)

    # Remove the temporary file
    os.remove(temp_sdc_path)

def _write_sdc_files(output_file, sdc_dir, file_list):
    """Write contents of a list of SDC files to the output file."""
    for filename in file_list:
        file_path = os.path.join(sdc_dir, filename)
        _write_file_contents(output_file, file_path)

def _write_file_contents(output_file, file_path):
    """Write the contents of a single file to the output file."""
    with open(file_path, 'r') as file:
        output_file.writelines(file.readlines())

def _write_clock_constraints(output_file, module_type, period):
    """Write clock constraints for a specific module type."""
    output_file.write("################################### Operation Clocks constraints ###################################\n")
    output_file.write(f"create_clock -name {module_type}_left_width_0_height_0_subtile_0__pin_clk_0_ -period {period} \
                        [get_ports {module_type}_left_width_0_height_0_subtile_0__pin_clk_0_]\n")
    output_file.write("####################################################################################################\n")

def _fix_sdc_paths(temp_path, final_path):
    """Fix incorrect paths in the temporary SDC file and write to the final SDC file."""
    path_replacements = [
        (r"logical_tile_clb_mode_default__fle_mode_physical__fabric_mode_default__frac_logic_mode_default__carry_follower_1/"
         r"logical_tile_clb_mode_default__fle_mode_physical__fabric_mode_default__frac_logic_mode_default__carry_follower",
         "logical_tile_clb_mode_default__fle_mode_physical__fabric_mode_default__frac_logic_mode_default__carry_follower_0"),

        (r"logical_tile_mult_18_mode_mult_8x8__mult_8x8_slice_mode_default__mult_8x8/"
         r"logical_tile_mult_18_mode_mult_8x8__mult_8x8_slice_mode_default__mult_8x8/",
         "logical_tile_mult_18_mode_mult_8x8__mult_8x8_slice_mode_default__mult_8x8_0/"),

        (r"logical_tile_mult_18_mode_mult_8x8__mult_8x8_slice_mode_default__mult_8x8_0/"
         r"logical_tile_mult_18_mode_mult_8x8__mult_8x8_slice_mode_default__mult_8x8/",
         "logical_tile_mult_18_mode_mult_8x8__mult_8x8_slice_mode_default__mult_8x8_0/")
    ]

    with open(temp_path, 'r') as temp_file, open(final_path, 'w') as final_file:
        for line in temp_file:
            for pattern, replacement in path_replacements:
                line = re.sub(pattern, replacement, line)
            final_file.write(line)

def generate_clock_constraint(freq: int) -> str:
    """Generate the programming clock constraint string."""
    return f"""
################################### Programming clock Constraint ###################################
create_clock -name prog_clk -period {str(freq)} [get_ports prog_clk]
####################################################################################################\n"""

def process_constraint_line(line: str, tile_mappings: zip) -> str:
    """Process a single constraint line with replacements."""
    if CREATE_CLOCK_KEYWORD not in line:
        line = line.replace(FPGA_TOP_PREFIX, '')
        for orig, new in tile_mappings:
            line = line.replace(orig, new)
    return line

def fix_sdc_paths(
    submodules, 
    sub_modules_instances, 
    freq
) -> None:
    """
    Fix SDC paths and add clock constraints for FPGA tiles.
    
    Args:
        submodules: Dictionary mapping tile names to their original module names
        sub_modules_instances: Dictionary mapping tile names to their instance names
        freq: Tuple of frequency constraints (prog_clk frequency is freq[2])
    
    Raises:
        IOError: If there are issues reading/writing SDC files
        KeyError: If tile mappings are inconsistent
    """
    try:
        for sdc_file in SDC_DIR.glob("*.sdc"):
            tile_name = sdc_file.stem
            
            # Skip if tile not found in mappings
            if tile_name not in submodules or tile_name not in sub_modules_instances:
                print(f"Skipping {sdc_file.name}: tile not found in submodules")
                continue

            # Read and process constraints
            with open(sdc_file, 'r') as f:
                constraints = f.readlines()

            # Create mapping pairs for replacement
            tile_mappings = zip(
                submodules[tile_name], 
                sub_modules_instances[tile_name]
            )

            # Process each constraint line
            new_constraints = [
                process_constraint_line(line, tile_mappings) 
                for line in constraints
            ]

            # Write updated constraints back to file
            with open(sdc_file, 'w') as f:
                f.writelines(new_constraints)
                f.write(generate_clock_constraint(freq[2]))

    except IOError as e:
        print(f"Error processing SDC files: {e}")
        raise
    except KeyError as e:
        print(f"Invalid tile mapping: {e}")
        raise

def generate_tile_based_sdcs(freq: Tuple[int, int, int]) -> None:
    """
    Generate tile-based SDC files with timing constraints.
    """
    submodules, sub_modules_instances = get_submodules()
    if not submodules or not sub_modules_instances:
        print("Failed to get submodules")
        return
        
    tiles = list(submodules.keys())
    for tile in tiles:
        create_sdc(tile, submodules[tile], freq)
    fix_sdc_paths(submodules, sub_modules_instances, freq)
