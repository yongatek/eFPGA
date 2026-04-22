module $__MY_SPRAM_1024x8 (
  output [0:7] PORT_A_RD_DATA,
  input PORT_A_WR_EN,
  input [0:9] PORT_A_ADDR,
  input [0:7] PORT_A_WR_DATA,
  input PORT_A_CLK,  
  );

 generate
    single_port_ram #() _TECHMAP_REPLACE_ (
      .clk    (PORT_A_CLK),
      .wen    (PORT_A_WR_EN),
      .addr    (PORT_A_ADDR),
      .d_in    (PORT_A_WR_DATA),
      .d_out    (PORT_A_RD_DATA),
       );
      
  endgenerate
endmodule  


