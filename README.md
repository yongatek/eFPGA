# TRISTAN eFPGA v1.2.0
TRISTAN eFPGA IP aims to provide an industrial-quality, open-source hardware building block for the RISC-V ecosystem. The proposed eFPGA architecture is highly customizable and can be used to implement various types of hardware accelerators and offload specific processor tasks.

## FPGA Resources

| Tile | Count | Description |
| :--- | :---: | :--- |
| **CLB** | 188 | 8 BLEs/block (fracturable LUT4, 2 FFs, hard adder). Supports carry chains. |
| **BRAM** | 10 | 1 KB SPRAM per block. |
| **DSP** | 20 | 16×16 signed multipliers. |
| **GPIO** | 11 | 13 IOs per block. |

### Derived Totals
* **FFs:** $188 \times 8 \times 2 = 3008$
* **LUT4:** $188 \times 8 = 1504$
* **LUT3 (Fractured):** $188 \times 8 \times 2 = 3008$
* **Adders:** $188 \times 8 = 1504$

## Getting Started

### Directory Hierarchy
```bash
eFPGA
│
├── benchmarks                      # Benchmarks
│   ├── adder_comb.v
│   ├── ...
├── docker_entrypoint.sh            # Script to use the Docker installation of OpenFPGA
├── docs                            # Documentation
│   └── eFPGA_Documentation.pdf
├── fpga_flow                       # Flow-related configs and scripts
│   ├── clear_run.sh                # Clears previous runs
│   ├── config                      # Configuration directory for the OpenFPGA task
│   │   ├── constraints             # OpenFPGA physical constraints
│   │   ├── yosys_dep               # Synthesis scripts and models
│   │   └── ...
│   ├── fpga_task.py                # Script to execute to generate fabric and testbenches
│   ├── README.md                   # Flow README
│   ├── runXXX                      # (Generated) Each run creates a new directory
│   └── scripts                     # Helper classes and methods
│       ├── benchmark.py
│       └── ...
├── misc                            # Simulation settings files for OpenFPGA
│   ├── fixed_sim_openfpga_2clk.xml
│   └── fixed_sim_openfpga.xml
├── pin_constraints                 # Pin constraint files for benchmarks
│   ├── mac_4.pcf
│   └── ...
├── README.md                       # Repository README
├── yonga_archs                     # FPGA fabric architecture directory 
│   ├── cell_library                # Cells used to build the FPGA fabric
│   │   ├── BUF.v
│   │   └── ...
│   ├── Fabric                      # Generated fabric
│   │   ├── fabric_hierarchy.txt
│   │   └── ...
│   └── k4N8f_adder_BRAM_DSP        # eFPGA Architecture 
│       ├── fabric_key.xml          # Describes the configuration chain order
│       ├── fabric_rename.xml       # Renames generated tiles name for consistancy accross different layouts.
│       ├── resources.json          # Records resources for the FPGA layout, used to generate reports.
│       ├── routing_rename.xml      # Used for SDC generation.
│       ├── tristan_openfpga.xml    # Describes the primitives and low-level connections for the FPGA
│       ├── timing.yml              # Describes the delays of hardware primitives, used to model the FPGA's performance
│       └── tristan_vpr.xml         # Describes the FPGA architecture
├── yonga_openfpga_shell_scripts    # OpenFPGA shell scripts used for the different tasks of this flow
│   ├── full_tb_with_bitstream.openfpga
│   └── ...
└── software/
    ├── efpga_ctrl.c
    ├── efpga_ctrl.h
    └── eFPGA_regs.h
```

### Tools
This project has been tested with the following tool versions:
- **Python** 3.7.9
- **OpenFPGA** 1.2.3592
- **Synopsys VCS** U-2023.03

### OpenFPGA Installation
```
This repo supports both docker and standalone installations of OpenFPGA. 
To use standalone installations, source openfpga.sh  from the OpenFPGA installation path before running the fpga_task.py script, 
otherwise, the repo will default to a docker installation.
```

### Running OpenFPGA tasks
OpenFPGA tasks are extensively automated through Python scripts. To utilize these scripts, run the script ```fpga_flow/fpga_task.py```, which provides the following options:
```
cd eFPGA/fpga_flow/
python3 fpga_task.py 
      0: Generates Fabric
      1: Generates SDCs
      2-4: Simulates Design
      5: Generates bitstream
```
Please refer to [FPGA Flow README](fpga_flow/README.md) under the directory ```./fpga_flow``` for detailed information regarding the script.

## Verification Results

### Toggle Coverage of Functional Tiles
The table below lists the toggle coverage for each functional tile, representing the percentage of nets and registers toggled during simulation.

| Tile | Toggle Coverage (%) |
| :--- | :--- |
| tile_0__1_ | 80.7 |
| tile_0__2_ | 97.54 |
| tile_11__1_ | 85.89 |
| tile_11__2_ | 99.51 |
| tile_1__0_ | 96.30 |
| tile_1__1_ | 88.8 |
| tile_1__2_ | 99.82 |
| tile_1__4_ | 99.77 |
| tile_1__9_ | 99.82 |
| tile_2__9_ | 99.82 |
| tile_1__5_ | 99.83 |
| tile_1__8_ | 99.93 |
| **Average** | **95.64** |

### Functional Coverage of Basic Logic Elements
The following table summarizes the verified operational modes for the Basic Logic Elements (BLE). All defined configurations achieved full functional coverage.

| CLB Mode | LUT Structure (A) | LUT Structure (B) | ADDER | Flip-Flop (A) | Flip-Flop (B) | Is it covered at least once? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| LUT4 | | | | | | YES |
| LUT4 | | | | FF | | YES |
| LUT3 | | | | | | YES |
| LUT3 | | | | | FF | YES |
| LUT3 | | ADDER | | | | YES |
| LUT3 | | ADDER | | FF | | YES |
| | LUT3 | | | | | YES |
| | LUT3 | | | | FF | YES |
| | LUT3 | | ADDER | | | YES |
| | LUT3 | | ADDER | | FF | YES |
| LUT3 | LUT3 | | | | | YES |
| LUT3 | LUT3 | | | FF | | YES |
| LUT3 | LUT3 | | | | FF | YES |
| LUT3 | LUT3 | | | FF | FF | YES |
| LUT3 | LUT3 | | ADDER | | | YES |
| LUT3 | LUT3 | | ADDER | FF | FF | YES |

## Benchmarks Results

A select set of workloads mapped to the fabric to evaluate resource utilization across different domains:

| Benchmark | IO | CLB | DSP | BRAM |
|  :--- | :---: | :---: | :---: | :---: |
| `bench_12_mult_32x32` | 130/143 | 57/188 | 9/20 | 0/10 |
| `bench_17_iir_filter_biquad` | 50/143 | 37/188 | 7/20 | 0/10 |
| `bench_16_fir_filter_4tap` | 50/143 | 22/188 | 4/20 | 0/10 |
| `bench_30_memory_bank` | 24/143 | 130/188 | 0/20 | 0/10 |
| `ff_mem` | 94/143 | 82/188 | 3/20 | 8/10 |
| `bench_23_fifo_1k` | 22/143 | 80/188 | 0/20 | 0/10 |
| `bench_19_alu_vector` | 100/143 | 28/188 | 0/20 | 0/10 |
| `bench_41_alu_pipeline` | 36/143 | 11/188 | 1/20 | 0/10 |
| `bench_35_spi_master` | 15/143 | 6/188 | 0/20 | 0/10 |
| `bench_03_fsm_traffic` | 7/143 | 1/188 | 0/20 | 0/10 |
