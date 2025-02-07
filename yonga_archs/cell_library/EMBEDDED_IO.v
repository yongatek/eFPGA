module EMBEDDED_IO (SOC_IN, SOC_OUT, SOC_DIR, FPGA_IN, FPGA_OUT, FPGA_DIR);

  input SOC_IN;   // Input to drive the inpad signal
  output SOC_OUT; // Output the outpad signal
  output SOC_DIR; // Output the directionality
  output FPGA_IN; // Input data to FPGA
  input FPGA_OUT; // Output data from FPGA
  input FPGA_DIR; // direction control 

  assign FPGA_IN = SOC_IN;
  assign SOC_OUT = FPGA_OUT;
  assign SOC_DIR = FPGA_DIR;
  
endmodule
