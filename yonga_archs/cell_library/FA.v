module FA(A, B, CI, S, CO);
  input A, B, CI;
  output S, CO;

  assign S = A ^ B ^ CI;
  assign CO = (A & B) | (A & CI) | (B & CI);

  specify
    specparam tpd = 0.05;
    (A, B, CI *> S) = tpd;
    (A, B, CI *> CO) = tpd;
  endspecify

endmodule
