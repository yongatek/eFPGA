module bench_09_parity_check (
    input clk,
    input reset,
    input [31:0] data_in,
    output reg parity_out
  );

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      parity_out <= 1'b0;
    end
    else
    begin
      parity_out <= ^data_in;
    end
  end

endmodule
