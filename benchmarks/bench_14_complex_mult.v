module bench_14_complex_mult (
    input clk,
    input reset,
    input signed [15:0] ar, 
    input signed [15:0] ai,
    input signed [15:0] br, 
    input signed [15:0] bi,
    output reg signed [31:0] pr, 
    output reg signed [31:0] pi
  );

  reg signed [31:0] mult_rr, mult_ri, mult_ir, mult_ii;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      pr      <= 32'd0;
      pi      <= 32'd0;
      mult_rr <= 32'd0;
      mult_ri <= 32'd0;
      mult_ir <= 32'd0;
      mult_ii <= 32'd0;
    end
    else
    begin
      mult_rr <= $signed(ar * br);
      mult_ii <= $signed(ai * bi);
      mult_ri <= $signed(ar * bi);
      mult_ir <= $signed(ai * br);

      pr <= $signed(mult_rr - mult_ii);
      pi <= $signed(mult_ri + mult_ir);
    end
  end

endmodule



// Example of manual mapping below

// `ifdef SIMULATION
// module mult_16 (sign, A, B, Y);

//     parameter A_width = 16;
//     parameter B_width = 16;

//     input [A_width-1:0] A;
//     input [B_width-1:0] B;
//     input sign;
//     output [A_width+B_width-1:0] Y;

//     assign Y = sign ? $signed(A) * $signed(B) : A * B;

//     specify
// 	specparam tpd = 1.2;
//         (A, B, sign *> Y) = tpd;
//     endspecify

// endmodule

// `endif



// module bench_14_complex_mult (
//     input clk,
//     input reset,
//     input signed [15:0] ar, 
//     input signed [15:0] ai,
//     input signed [15:0] br, 
//     input signed [15:0] bi,
//     output reg signed [31:0] pr, 
//     output reg signed [31:0] pi
//   );

//   wire signed [31:0] mult_rr, mult_ri, mult_ir, mult_ii;

// mult_16 mult1 (.sign(1'b1), .A(ar), .B(br), .Y(mult_rr));
// mult_16 mult2 (.sign(1'b1), .A(ai), .B(bi), .Y(mult_ii));
// mult_16 mult3 (.sign(1'b1), .A(ar), .B(bi), .Y(mult_ri));
// mult_16 mult4 (.sign(1'b1), .A(ai), .B(br), .Y(mult_ir));

//   always @(posedge clk or posedge reset)
//   begin
//     if (reset)
//     begin
//       pr <= 32'sd0;
//       pi <= 32'sd0;
//     end
//     else
//     begin
//       pr <= $signed(mult_rr) - $signed(mult_ii);
//       pi <= $signed(mult_ri) + $signed(mult_ir);
//     end
//   end

// endmodule
