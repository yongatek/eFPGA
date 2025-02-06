module mux(i0, i1, s, o);

  input i0, i1, s;
  output o;

  assign o = s? i1 : i0;

endmodule