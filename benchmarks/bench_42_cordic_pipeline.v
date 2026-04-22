module bench_42_cordic_pipeline (
    input clk,
    input reset,
    input signed [7:0] x_in,
    input signed [7:0] y_in,
    output reg signed [7:0] x_out,
    output reg signed [7:0] y_out
  );
  // 3 stage simple rotation pipeline (Mock functionality)
  reg signed [7:0] x1, y1, x2, y2;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      x1<=0;
      y1<=0;
      x2<=0;
      y2<=0;
      x_out<=0;
      y_out<=0;
    end
    else
    begin
      // Stage 1
      x1 <= $signed(x_in - (y_in >>> 1));
      y1 <= $signed(y_in + (x_in >>> 1));

      // Stage 2
      x2 <= $signed(x1 - (y1 >>> 2));
      y2 <= $signed(y1 + (x1 >>> 2));

      // Stage 3
      x_out <= $signed(x2 - (y2 >>> 3));
      y_out <= $signed(y2 + (x2 >>> 3));
    end
  end

endmodule
