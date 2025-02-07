## This script runs fpga tasks and automates some of the steps
All FPGA tasks can be be run by executing the command 

```sh
python3 fpga_task.py
```

First the script gives the option select the benchmarks you want to run. 
It will recognize any RTL in the benchmark directory **(../benchmarks)**

Note that the benchmark should share the same name as the top module, otherwise it won't be correctly recognized by this script.
Additionally, benchmarks that consist of multiple files should be placed in folder that has the name of the top module, the script will automatically add all the files within the folder

## This script supports the following flows:
<ins>**0: Generate fabric**</ins> &rarr; Generate the netlist and place it under directory  ```$TRISTAN_EFPGA_PATH/yonga_archs/Fabric```

<ins>**1: Generate SDCs**</ins> &rarr; Generate SDCs for a tile-based architecture and place them under directory ```$TRISTAN_EFPGA_PATH/yonga_archs/Fabric```

<ins>**2: Preconfigured tb**</ins> &rarr; Generate a bitstream and a preconfigured tb, and run the simulation

<ins>**3: Custom preconfigured tb**</ins> &rarr; Use a custom testbench with the preconfigured fpga as the DUT

<ins>**4: Full tb**</ins> &rarr; Generate a bitstream and a full tb, and run the simulation

<ins>**5: Generate bitstream**</ins> &rarr; Generates a bitstream

## Some rules to use the script:
- To use the global reset pin automatically, the benchmark should use the name "Reset"

- The global pin is active low. There is no global set signal, so benchmarks using a global reset cannot reset a flop to a non-zero value

- To use a logical reset that is only triggered at the start of the simulation, the benchmark should use the name "reset"
Other names for the reset signal are not recognized and are treated as general inputs (random input stimulus). 
"Reset" and "reset" can also be replaced with other names by modifying the scripts.

- Benchmarks should be placed in ```../benchmarks```
	- To use custom testbenches, the tb should be placed in ```../benchmarks``` and should have a name that matches the top module (<top_module_name>_tb.v)
	- The custom TB should instantiate the wrapper instead of the RTL's top module (the DUT's name should be <top_module_name>_top_formal_verification)

- Pin constraints should be placed in ```../pin_constraints```
	- For both of these the file name has to match the top module
	- If no matching PCF file is found, one is automatically generated using the order which the pins where specified in.
	- Not setting the PCF leaves this to VPR, which is mostly random

- When changing the architecture the yosys synthesis script should be adjusted accordingly (task.conf and yosys_dep files used)

- Previous runs can be cleared by using the script ./clear_run.sh
