module INV(I, ZN);
  input I;
  output ZN;

  assign ZN = ~I;

  specify
    specparam tpd = 0.01;
    (I => ZN) = tpd;
  endspecify

endmodule
