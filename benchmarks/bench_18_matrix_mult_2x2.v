module bench_18_matrix_mult_2x2 (
    input clk,
    input reset,
    // Matrix A
    input [7:0] a11, 
    input [7:0] a12,
    input [7:0] a21, 
    input [7:0] a22,
    // Matrix B
    input [7:0] b11, 
    input [7:0] b12,
    input [7:0] b21, 
    input [7:0] b22,
    // Result C
    output reg [16:0] c11, 
    output reg [16:0] c12,
    output reg [16:0] c21, 
    output reg [16:0] c22
  );

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      c11 <= 0;
      c12 <= 0;
      c21 <= 0;
      c22 <= 0;
    end
    else
    begin
      c11 <= (a11 * b11) + (a12 * b21);
      c12 <= (a11 * b12) + (a12 * b22);
      c21 <= (a21 * b11) + (a22 * b21);
      c22 <= (a21 * b12) + (a22 * b22);
    end
  end

endmodule
