module $__MY_DPRAM_1024x8 (
  output [0:7] PORT_A_RD_DATA,
  input PORT_A_WR_EN,
  input [0:9] PORT_A_ADDR,
  input [0:7] PORT_A_WR_DATA,
  input PORT_A_CLK,  
  output [0:7] PORT_B_RD_DATA,
  input PORT_B_WR_EN,
  input [0:9] PORT_B_ADDR,
  input [0:7] PORT_B_WR_DATA,
  input PORT_B_CLK
  
  );

 generate
    dual_port_ram #() _TECHMAP_REPLACE_ (
      .clk    (PORT_A_CLK),
      .wen1    (PORT_A_WR_EN),
      .addr1    (PORT_A_ADDR),
      .d_in1    (PORT_A_WR_DATA),
      .d_out1    (PORT_A_RD_DATA),
      
      //.clk2    (PORT_B_CLK),
      .wen2    (PORT_B_WR_EN),
      .addr2    (PORT_B_ADDR),
      .d_in2    (PORT_B_WR_DATA),
      .d_out2    (PORT_B_RD_DATA)
 );
      
  endgenerate
endmodule  


