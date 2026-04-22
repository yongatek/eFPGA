module bench_16_fir_filter_4tap (
    input clk,
    input reset,
    input signed [15:0] sample_in,
    output reg signed [31:0] sample_out
  );

  parameter signed [15:0] C0 = 16'd100;
  parameter signed [15:0] C1 = 16'd200;
  parameter signed [15:0] C2 = 16'd300;
  parameter signed [15:0] C3 = 16'd100;

  reg signed [15:0] x0, x1, x2, x3;
  reg signed [31:0] p0, p1, p2, p3;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      x0 <= 0;
      x1 <= 0;
      x2 <= 0;
      x3 <= 0;
      p0 <= 0;
      p1 <= 0;
      p2 <= 0;
      p3 <= 0;
      sample_out <= 0;
    end
    else
    begin
      x0 <= sample_in;
      x1 <= x0;
      x2 <= x1;
      x3 <= x2;

      p0 <= $signed(x0 * C0);
      p1 <= $signed(x1 * C1);
      p2 <= $signed(x2 * C2);
      p3 <= $signed(x3 * C3);

      sample_out <= $signed($signed(p0 + p1) + $signed(p2 + p3));
    end
  end

endmodule
