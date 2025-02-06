module ffram(clk, addr, reset, din, wen, dout);

    input clk, addr, din, wen, reset;
    output dout;

    ff addr0 (.clk(clk), .reset(reset), .d(d0), .q(q0));
    ff addr1 (.clk(clk), .reset(reset), .d(d1), .q(q1));

    mux d0_mux (.i0(q0), .i1(din), .s(~addr & wen), .o(d0));
    mux d1_mux (.i0(q1), .i1(din), .s(addr & wen), .o(d1));
    
    mux dout_mux (.i0(q0), .i1(q1), .s(addr), .o(dout));

endmodule
