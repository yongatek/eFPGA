//-----------------------------
// 16-bit multiplier
//-----------------------------
module mult_16x16 (
  input [0:0] sign,
  input [15:0] A,
  input [15:0] B,
  output [31:0] Y
);
  parameter A_SIGNED = 0 ;
  parameter B_SIGNED = 0 ;
  parameter A_WIDTH = 16;
  parameter B_WIDTH = 16;
  parameter Y_WIDTH = 32;

  mult_16 #() _TECHMAP_REPLACE_ (
    .sign (0), //A_SIGNED || B_SIGNED),
    .A    (A),
    .B    (B),
    .Y    (Y)
  );

endmodule

