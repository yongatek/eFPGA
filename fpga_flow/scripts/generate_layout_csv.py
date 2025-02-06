#----------------------------------------------------------------#
# Module:       generate_layout_csv.py
# Company:      Yongatek Microelectronics
# Author:       Ahmad Houraniah
# Version:      0.1.0
# Description:  This script is used to generate the FPGA CSV layout 
#               file based on the generated RTL. 
#----------------------------------------------------------------#

import re
import csv

def parse_verilog(vfile):
    pattern = r'tile_(\d+)__(\d+)_ tile_(\d+)__(\d+)_'
    tiles = []
    with open(vfile, 'r') as file:
        for line in file:
            # Find all matches in the line
            matches = re.findall(pattern, line)
            for match in matches:
                x, y, nx, ny = map(int, match)  # Convert matched strings to integers
                tiles.append([f"tile_{x}__{y}_", nx, ny])
    return tiles

def create_fpga_layout(tiles, grid_size=20):
    # Create an empty grid of the specified size
    grid = [[None] * grid_size for _ in range(grid_size)]
    for name, x, y in tiles:
        grid[y][x] = name  # Place the tile name in the grid at the specified position
    return grid

def write_to_csv(grid, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write the grid to the CSV file (in reversed order for proper top-to-bottom row orientation)
        writer.writerows(grid[::-1])

def gen_layout_csv(size):
    vfile = "../yonga_archs/Fabric/SRC/fpga_top.v"
    output_csv = "../yonga_archs/Fabric/fpga_layout.csv"
    tiles = parse_verilog(vfile)  # Parse the Verilog file for tile information
    grid = create_fpga_layout(tiles, size)  # Create the FPGA layout grid
    write_to_csv(grid, output_csv)  # Write the layout to CSV
