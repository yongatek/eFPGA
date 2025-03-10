# TRISTAN eFPGA v1.0.0


## Tested With
This project has been tested with the following tool versions:
- **Python** 3.7.9
- **OpenFPGA** 1.2.3012
- **Synopsys VCS** U-2023.03

## OpenFPGA Installation
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

## Directory Hierarchy
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
│   ├── fpga_task.py                #  Script to execute to generate fabric and testbenches
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
│   └── reg4.pcf
├── README.md                       # Repository README (You are here)
├── yonga_archs                     # FPGA fabric architecture directory 
│   ├── cell_library                # Custom primitives used in the FPGA
│   │   ├── BUF.v
│   │   └── ...
│   ├── Fabric                      # Generated fabric
│   │   ├── fabric_hierarchy.txt
│   │   └── ...
│   └── k4N8f_adder_BRAM_DSP        # Proposed architecture for TRISTAN
│       ├── timing.yml              # Describes the delays of hardware primitives, used to model the FPGA's performance
│       ├── tristan_openfpga.xml    # Describes the primitives and low-level connections for the FPGA
│       └── tristan_vpr.xml         # Describes the FPGA architecture
└── yonga_openfpga_shell_scripts    # OpenFPGA shell scripts used for the different tasks of this flow
    ├── full_tb_with_bitstream.openfpga
    └── ...

```

## Requirements Status
| Requirement ID | Requirement Description                                                                                            | Priority    | Category         | Current Status |
|----------------|--------------------------------------------------------------------------------------------------------------------|-------------|------------------|----------------|
| WI3.4.5-1      | eFPGA IP shall have single clock domain.                                                                           | Mandatory   | Functional       | ✓              |
| WI3.4.5-1.1    | All modes shall use the same clock.                                                                                | Mandatory   | Functional       | ✓              |
| WI3.4.5-2      | eFPGA IP shall have single reset domain.                                                                           | Mandatory   | Functional       | ✓              |
| WI3.4.5-2.1    | All synchronous logic elements shall have active-low reset.                                                        | Mandatory   | Functional       | ✓              |
| WI3.4.5-2.2    | All synchronous logic elements shall have synchronous reset.                                                       | Mandatory   | Functional       | ✓              |
| WI3.4.5-3      | eFPGA IP shall have single power domain.                                                                           | Mandatory   | Functional       | ✓              |
| WI3.4.5-4      | eFPGA IP shall have a tile-based architecture.                                                                     | Mandatory   | Functional       | ✓              |
| WI3.4.5-5      | Logic tiles shall have LUTs, registers, and connection blocks.                                                     | Mandatory   | Functional       | ✓              |
| WI3.4.5-5.1    | eFPGA IP shall have 10000 logic tiles.                                                                             | Mandatory   | Functional       | ✓              |
| WI3.4.5-5.2    | Each logic tile shall include 8 logic blocks.                                                                      | Mandatory   | Functional       | ✓              |
| WI3.4.5-5.3    | Each logic block shall include a 4-input LUT.                                                                      | Mandatory   | Functional       | ✓              |
| WI3.4.5-5.4    | Each logic block shall include two FFs.                                                                            | Mandatory   | Functional       | ✓              |
| WI3.4.5-5.5    | Each logic block shall have multiple operating modes.                                                              | Mandatory   | Functional       | ✓              |
| WI3.4.5-6      | I/O tiles shall support bidirectional operation.                                                                   | Mandatory   | Functional       | ✓              |
| WI3.4.5-6-1    | I/O tiles shall have multiple operating modes.                                                                     | Mandatory   | Functional       | ✓              |
| WI3.4.5-6-2    | I/O tiles shall be used to interface with system bus.                                                              | Mandatory   | Functional       | X              |
| WI3.4.5-6-3    | I/O tiles shall be used to interface with external IOs.                                                            | Mandatory   | Functional       | X              |
| WI3.4.5-6-4    | I/O tiles shall be used to interface with control IOs.                                                             | Mandatory   | Functional       | X              |
| WI3.4.5-6-5    | Number of I/Os to interface with the system bus  shall be 100.                                                     | Mandatory   | Functional       | X              |
| WI3.4.5-6-6    | Number of external I/Os  shall be 8.                                                                               | Mandatory   | Functional       | X              |
| WI3.4.5-6-7    | I/O tiles shall be placed at the boundary of IP.                                                                   | Mandatory   | Functional       | ✓              |
| WI3.4.5-7      | eFPGA IP shall have a system bus interface.                                                                        | Mandatory   | Functional       | X              |
| WI3.4.5-7-1    | Bus interface shall be AMBA AXI4-Lite compliant.                                                                   | Mandatory   | Interoperability | X              |
| WI3.4.5-7-2    | Address width of read and write channels shall be 8.                                                               | Mandatory   | Interoperability | X              |
| WI3.4.5-7-3    | Data width of read and write channels shall be 32.                                                                 | Mandatory   | Interoperability | X              |
| WI3.4.5-8      | Memory tiles shall have memory blocks.                                                                             | Mandatory   | Functional       | ✓              |
| WI3.4.5-8-1    | Memory blocks shall have different operating modes.                                                                | Mandatory   | Functional       | X              |
| WI3.4.5-8-2    | Size of total memory blocks shall be at least 180 Kbits.                                                           | Mandatory   | Functional       | ✓              |
| WI3.4.5-8-3    | Memory blocks shall have single-port SRAM macros.                                                                  | Mandatory   | Functional       | ✓              |
| WI3.4.5-8-4    | Memory blocks shall support write-first policy.                                                                    | Mandatory   | Functional       | X              |
| WI3.4.5-8-5    | Memory blocks shall support synchronous read.                                                                      | Mandatory   | Functional       | ✓              |
| WI3.4.5-9      | DSP tiles shall include MAC blocks.                                                                                | Optional    | Functional       | ✓              |
| WI3.4.5-9-1    | MAC blocks shall have two 18-bit inputs and output 36-bit output.                                                  | Optional    | Functional       | ✓              |
| WI3.4.5-9-2    | Number of total DSP tiles shall be 8.                                                                              | Optional    | Functional       | ✓              |
| WI3.4.5-10     | eFPGA IP shall have a configuration logic to program the FPGA fabric.                                              | Mandatory   | Functional       | ✓              |
| WI3.4.5-10-1   | Each tile shall have configuration circuitry to define the interconnection and wiring in tile components.          | Mandatory   | Functional       | ✓              |
| WI3.4.5-10-2   | Switch blocks shall provide the interconnect between the tiles.                                                    | Mandatory   | Functional       | ✓              |
| WI3.4.5-10-3   | All configurable elements shall implement a configuration chain in the FPGA fabric.                                | Mandatory   | Functional       | ✓              |
| WI3.4.5-10-4   | eFPGA IP shall have a JTAG configuration interface.                                                                | Best Effort | Interoperability | X              |
| WI3.4.5-11     | eFPGA IP shall have a test mode.                                                                                   | Best Effort | Functional       | X              |
| WI3.4.5-11-1   | All FFs in located in the logic tiles shall be controllable and observable via a scan chain.                       | Best Effort | Functional       | X              |
| WI3.4.5-11-2   | Each SRAM macro shall have BIST circuitry.                                                                         | Best Effort | Functional       | X              |
| WI3.4.5-12     | eFPGA IP shall have a synthesizable RTL design.                                                                    | Mandatory   | Other            | ✓              |
| WI3.4.5-12-1   | RTL design shall be SystemVerilog-2005 compliant.                                                                  | Mandatory   | Interoperability | ✓              |
| WI3.4.5-12-2   | RTL design shall not contain any primitives that belong to a 3rd party except the functional model of SRAM macros. | Mandatory   | Other            | ✓              |
| WI3.4.5-13     | eFPGA IP shall be verified by functional simulation.                                                               | Mandatory   | Other            | X              |
| WI3.4.5-13-1   | Code coverage shall be at least 90%.                                                                               | Mandatory   | Other            | X              |
| WI3.4.5-13-2   | Functional coverage shall be 100%.                                                                                 | Mandatory   | Other            | X              |
| WI3.4.5-14     | Achievable maximum clock frequency shall be at least 50MHz in TSMC 65nm technology.                                | Mandatory   | Performance      | X              |
| WI3.4.5-15     | eFPGA IP shall be supported by a software stack.                                                                   | Mandatory   | Functional       | X              |
| WI3.4.5-15-1   | Software driver/hardware abstraction layer shall provide low-level routines for the CPU to access to the eFPGA IP. | Mandatory   | Functional       | X              |
| WI3.4.5-15-2   | User-level functions shall provide access to the eFPGA IP for the applications running on the CPU core.            | Mandatory   | Functional       | X              |
