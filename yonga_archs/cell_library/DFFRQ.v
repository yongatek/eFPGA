module DFFRQ (CDN, CP, D, Q);
  input CDN; 
  input CP; 
  input D;  
  output Q;
  
  reg q_reg;

  always @ (posedge CP or negedge CDN)
    if (~CDN) begin
      q_reg <= 1'b0;
    end else begin
      q_reg <= D;
    end
  
  assign Q = q_reg;

endmodule 