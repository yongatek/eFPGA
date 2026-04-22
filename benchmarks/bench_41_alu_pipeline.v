module bench_41_alu_pipeline (
    input clk,
    input reset,
    input [7:0] a,
    input [7:0] b,
    input [1:0] op,
    output reg [15:0] result
  );

  reg [7:0] a1, b1, a2, b2;
  reg [1:0] op1, op2;
  reg [15:0] res1;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      a1 <= 0;
      b1 <= 0;
      op1 <= 0;
      a2 <= 0;
      b2 <= 0;
      op2 <= 0;
      res1 <= 0;
      result <= 0;
    end
    else
    begin
      // Stage 1
      a1 <= a;
      b1 <= b;
      op1 <= op;

      // Stage 2
      a2 <= a1;
      b2 <= b1;
      op2 <= op1;
      case (op1)
        0:
          res1 <= a1 + b1;
        1:
          res1 <= a1 - b1;
        2:
          res1 <= a1 * b1; // Multiplier inferred
        3:
          res1 <= a1 ^ b1;
      endcase

      // Stage 3
      result <= res1;
    end
  end

endmodule
