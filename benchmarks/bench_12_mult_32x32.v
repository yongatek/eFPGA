module bench_12_mult_32x32 (
    input clk,
    input reset,
    input [31:0] a,
    input [31:0] b,
    output reg [63:0] p
  );

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      p <= 64'b0;
    end
    else
    begin
      p <= a * b;
    end
  end

endmodule
