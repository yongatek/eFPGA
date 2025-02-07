module OR2(A1, A2, Z);
    input  A1;
    input  A2;
    output Z;

    assign Z = A1 | A2;

    specify
        specparam tpd = 0.03;
        (A1, A2 *> Z) = tpd;
    endspecify

endmodule
