module MUX2(I1, I0, S, Z);
    input  I1;
    input  I0;
    input  S;
    output Z;

    assign Z = S ? I1 : I0;

    specify
        specparam tpd = 0.05;
        (I0, I1, S *> Z) = tpd;
    endspecify

endmodule
