module full_adder
(
input a_i,
input b_i,
input cin_i,
output s_o,
output cout_o
);

wire and1, and2, and3;

xor G1 (s_o,a_i,b_i,cin_i);
and G2 (and1,a_i,b_i);
and G3 (and2,a_i,cin_i);
and G4 (and3,b_i,cin_i);
or G5 (cout_o,and1,and2,and3);

endmodule