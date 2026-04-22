module bench_30_memory_bank (
    input clk,
    input [1:0] bank_sel,
    input [3:0] addr,
    input [7:0] data_in,
    input we,
    output reg [7:0] data_out
  );

  reg [7:0] bank0 [15:0];
  reg [7:0] bank1 [15:0];
  reg [7:0] bank2 [15:0];
  reg [7:0] bank3 [15:0];

  always @(posedge clk)
  begin
    if (we)
    begin
      case (bank_sel)
        2'b00:
          bank0[addr] <= data_in;
        2'b01:
          bank1[addr] <= data_in;
        2'b10:
          bank2[addr] <= data_in;
        2'b11:
          bank3[addr] <= data_in;
      endcase
    end

    case (bank_sel)
      2'b00:
        data_out <= bank0[addr];
      2'b01:
        data_out <= bank1[addr];
      2'b10:
        data_out <= bank2[addr];
      2'b11:
        data_out <= bank3[addr];
    endcase
  end

endmodule
