module BUF(I, Z);
  input I;
  output Z;

  assign Z = I;

  specify
    specparam tpd = 0.01;
    (I => Z) = tpd;
  endspecify

endmodule

