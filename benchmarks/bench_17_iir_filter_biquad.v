module bench_17_iir_filter_biquad (
    input clk,
    input reset,
    input signed [15:0] x_in,
    output reg signed [31:0] y_out
  );
  // Direct Form I
  // y[n] = b0*x[n] + b1*x[n-1] + b2*x[n-2] - a1*y[n-1] - a2*y[n-2]

  // Coefficients (scaled)
  parameter signed [15:0] B0 = 16'd1000;
  parameter signed [15:0] B1 = 16'd2000;
  parameter signed [15:0] B2 = 16'd1000;
  parameter signed [15:0] A1 = 16'd500;
  parameter signed [15:0] A2 = 16'd250;

  reg signed [15:0] x0, x1, x2;
  reg signed [31:0] y0, y1, y2;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      x0 <= 0;
      x1 <= 0;
      x2 <= 0;
      y0 <= 0;
      y1 <= 0;
      y2 <= 0;
      y_out <= 0;
    end
    else
    begin
      x0 <= x_in;
      x1 <= x0;
      x2 <= x1;

      y2 <= y1;
      y1 <= y0;

      y0 <= $signed($signed(B0*x0) + $signed(B1*x1) + $signed(B2*x2) - $signed(A1*y1) - $signed(A2*y2));

      y_out <= y0;
    end
  end

endmodule
