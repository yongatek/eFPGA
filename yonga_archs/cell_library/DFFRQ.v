module DFFRQ (RST, CK, D, Q);
  input RST; 
  input CK; 
  input D;  
  output Q;
  
  reg q_reg;

  always @ (posedge CK or negedge RST)
    if (~RST) begin
      q_reg <= 1'b0;
    end else begin
      q_reg <= D;
    end
  
  assign Q = q_reg;

endmodule 