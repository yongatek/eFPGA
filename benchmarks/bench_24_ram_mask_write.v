module bench_24_ram_mask_write (
    input clk,
    input [3:0] we,
    input [3:0] addr,
    input [31:0] data_in,
    output reg [31:0] data_out
  );

  reg [31:0] mem [15:0];

  always @(posedge clk)
  begin
    if (we[0])
      mem[addr][7:0]   <= data_in[7:0];
    if (we[1])
      mem[addr][15:8]  <= data_in[15:8];
    if (we[2])
      mem[addr][23:16] <= data_in[23:16];
    if (we[3])
      mem[addr][31:24] <= data_in[31:24];

    data_out <= mem[addr];
  end

endmodule
