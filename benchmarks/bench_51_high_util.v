module bench_51_high_util (
    input clk,
    input [3:0] we,
    input [10:0] addr,
    input [31:0] data_in,
    output reg [31:0] data_out,
    output reg [31:0] mult_out,
    input [27:0] xor_in,
    input GLOBAL_RESET,
    output reg [1:0] xor_out
  );

  reg [28:0] xor_in_reg, xor_in_reg2;

  reg [31:0] mult_out_tmp1, mult_out_tmp2, mult_out_tmp3, reg_data;
  reg [31:0] reg_mem [15:0]; //these will be implemented with regs due to our hardware
  reg [31:0] mem [2047:0];

  `ifdef SIMULATION
  integer jj;
  initial begin
    for (jj=0; jj<2048; jj=jj+1) 
      mem[jj] = 0;
  end
  `endif 
  integer ii;
  
  reg [2:0] addr_3b;
  reg [3:0] addr_4b;
  
  always@* begin
    addr_3b = addr[2:0];
    addr_4b = addr[3:0];
  end

  always @(posedge clk)
  begin
    data_out    <= 0;
    xor_in_reg  <= xor_in;
    xor_in_reg2 <= xor_in_reg;
    xor_out[0]  <= ^xor_in;
    xor_out[1]  <= ^xor_in_reg2;
    
    if(|we) begin
      mem[addr] <= data_in;
    end else begin
      data_out <= mem[addr];
    end

    if(~GLOBAL_RESET) begin
      xor_in_reg    <= 0;
      xor_in_reg2   <= 0;      
      xor_out[0]    <= 0;
      xor_out[1]    <= 0;
      mult_out_tmp1 <= 0;
      mult_out_tmp2 <= 0;
      mult_out_tmp3 <= 0;
      reg_data      <= 0;
      for(ii=0; ii < 16; ii = ii +1) begin
        reg_mem[ii] <= 0;
      end
    end else begin
      if (we[0])
        reg_mem[addr_3b][7:0]   <= data_in[7:0];
      if (we[1])
        reg_mem[addr_3b][15:8]  <= data_in[15:8];
      if (we[2])
        reg_mem[addr_3b][23:16] <= data_in[23:16];
      if (we[3])
        reg_mem[addr_3b][31:24] <= data_in[31:24];
      mult_out_tmp1 <= (reg_mem[0] * reg_mem[1]) & (reg_mem[2] * reg_mem[3]) ;
      mult_out_tmp2 <= (reg_mem[4] * reg_mem[5]) & (reg_mem[6] * reg_mem[7]) ;
      mult_out_tmp3 <= (mult_out_tmp1 * mult_out_tmp2);
      reg_data      <= reg_mem[addr_4b];
      mult_out      <= mult_out_tmp2 & reg_data;
    end
  end

  
endmodule