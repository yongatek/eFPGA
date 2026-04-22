module bench_21_ram_single_1k (
    input clk,
    input we,
    input [4:0] addr,
    input [7:0] data_in,
    output reg [7:0] data_out
  );

  reg [7:0] mem [31:0];

  always @(posedge clk)
  begin
    if (we)
      mem[addr] <= data_in;
    data_out <= mem[addr];
  end

endmodule
