module bench_19_alu_vector (
    input clk,
    input reset,
    input [31:0] vec_a, // 4x 8-bit
    input [31:0] vec_b, // 4x 8-bit
    input [1:0] op,
    output reg [31:0] vec_out
  );

  wire [7:0] a0, a1, a2, a3;
  wire [7:0] b0, b1, b2, b3;
  reg [7:0] r0, r1, r2, r3;

  assign {a3, a2, a1, a0} = vec_a;
  assign {b3, b2, b1, b0} = vec_b;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      vec_out <= 32'b0;
    end
    else
    begin
      case (op)
        2'b00:
        begin
          r0 <= a0 + b0;
          r1 <= a1 + b1;
          r2 <= a2 + b2;
          r3 <= a3 + b3;
        end
        2'b01:
        begin
          r0 <= a0 - b0;
          r1 <= a1 - b1;
          r2 <= a2 - b2;
          r3 <= a3 - b3;
        end
        2'b10:
        begin
          r0 <= a0 & b0;
          r1 <= a1 & b1;
          r2 <= a2 & b2;
          r3 <= a3 & b3;
        end
        2'b11:
        begin
          r0 <= a0 ^ b0;
          r1 <= a1 ^ b1;
          r2 <= a2 ^ b2;
          r3 <= a3 ^ b3;
        end
      endcase
      vec_out <= {r3, r2, r1, r0};
    end
  end

endmodule
