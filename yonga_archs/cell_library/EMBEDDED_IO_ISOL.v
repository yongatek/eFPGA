module EMBEDDED_IO_ISOL (SOC_IN, SOC_OUT, SOC_DIR, FPGA_IN, FPGA_OUT, FPGA_DIR, ISOL);

  input SOC_IN;
  input FPGA_OUT;
  input FPGA_DIR;
  input ISOL;
  output SOC_OUT;
  output SOC_DIR;
  output FPGA_IN;

  assign FPGA_IN =    ISOL & SOC_IN     ;
  assign SOC_OUT =    ISOL & FPGA_OUT   ;
  assign SOC_DIR = ~( ISOL & FPGA_DIR ) ;
    
endmodule
