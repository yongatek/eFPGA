module bench_11_mult_16x16 (
    input clk,
    input reset,
    input [15:0] a,
    input [15:0] b,
    output reg [31:0] p
  );

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      p <= 32'b0;
    end
    else
    begin
      p <= a * b;
    end
  end

endmodule
