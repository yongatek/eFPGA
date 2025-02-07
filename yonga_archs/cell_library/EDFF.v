module EDFF (E, CK, D, Q);
  input E; 
  input CK; 
  input D;  
  output Q;
  
  reg q_reg;

  always @ (posedge CK)
    if (E) begin
      q_reg <= D;
    end else begin
      q_reg <= Q;
    end
  
  assign Q = q_reg;

endmodule 