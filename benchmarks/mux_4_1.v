module mux_4_1
(
input i0_i,
input i1_i,
input i2_i,
input i3_i,
input sel0_i,
input sel1_i,
output out_o
);

wire muxout1, muxout2;

mux_2_1 MUX1 
(
.i0_i   (i0_i),
.i1_i   (i1_i),
.sel_i  (sel0_i),
.out_o  (muxout1)
);

mux_2_1 MUX2 
(
.i0_i   (i2_i),
.i1_i   (i3_i),
.sel_i  (sel0_i),
.out_o  (muxout2)
);

mux_2_1 MUX3
(
.i0_i   (muxout1),
.i1_i   (muxout2),
.sel_i  (sel1_i),
.out_o  (out_o)
);

endmodule



module mux_2_1
(
input i0_i,
input i1_i,
input sel_i,
output out_o
);

wire not1, and1, and2;

not G1 (not1,sel_i);
and G2 (and1,i0_i,not1);
and G3 (and2,i1_i,sel_i);
or G4 (out_o,and1,and2);

endmodule
