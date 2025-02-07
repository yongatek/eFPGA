module mult_8x8 (sign, A, B, Y);

    parameter A_width = 8;
    parameter B_width = 8;

    input [A_width-1:0] A;
    input [B_width-1:0] B;
    input sign;
    output [A_width+B_width-1:0] Y;

    assign Y = sign ? $signed(A) * $signed(B) : A * B;

    specify
        specparam tpd = 1.2;
        (A, B, sign *> Y) = tpd;
    endspecify

endmodule
