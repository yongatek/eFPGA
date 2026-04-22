module bench_22_ram_dual_1k (
    input clk,
    input we_a, we_b,
    input [4:0] addr_a, 
    input [4:0] addr_b,
    input [7:0] data_in_a, 
    input [7:0] data_in_b,
    output reg [7:0] data_out_a, 
    output reg [7:0] data_out_b
  );

  reg [7:0] mem [31:0];

  always @(posedge clk)
  begin
    if (we_a)
      mem[addr_a] <= data_in_a;
    data_out_a <= mem[addr_a];
  end

  always @(posedge clk)
  begin
    if (we_b)
      mem[addr_b] <= data_in_b;
    data_out_b <= mem[addr_b];
  end

endmodule
