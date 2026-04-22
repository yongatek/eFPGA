module bench_20_dct_1d_4point (
    input clk,
    input reset,
    input signed [7:0] x0, 
    input signed [7:0] x1, 
    input signed [7:0] x2, 
    input signed [7:0] x3,
    output reg signed [15:0] Y0, 
    output reg signed [15:0] Y1, 
    output reg signed [15:0] Y2, 
    output reg signed [15:0] Y3
  );

  // DCT-II 4-point (Unscaled, just transform)
  // C0 = x0 + x1 + x2 + x3
  // C1 ~ x0 + 0.5*x1 - 0.5*x2 - x3 (approximated for logic stress)
  // C2 = x0 - x1 - x2 + x3
  // C3 ~ 0.5*x0 - x1 + x2 - 0.5*x3

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      Y0 <= 0;
      Y1 <= 0;
      Y2 <= 0;
      Y3 <= 0;
    end
    else
    begin
      Y0 <= $signed((x0 + x1) + (x2 + x3));
      Y1 <= $signed((x0 <<< 1) + x1 - x2 - (x3 <<< 1)); // Mock coefficients
      Y2 <= $signed(x0 - x1 - x2 + x3);
      Y3 <= $signed(x0 - (x1 <<< 1) + (x2 <<< 1) - x3);
    end
  end

endmodule
