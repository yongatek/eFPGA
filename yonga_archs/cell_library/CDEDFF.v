module CDEDFF (D, E, CP, CDN, CONFIG_DONE, Q, QN, CD_Q);
  input D, E, CP, CDN, CONFIG_DONE;
  output Q, CD_Q, QN;
  
  reg q_reg;

  always @ (posedge CP or negedge CDN)
    if(~CDN) begin
      q_reg <= 1'b0;
    end else begin
      if (E) begin
        q_reg <= D;
      end else begin
        q_reg <= Q;
      end
    end  

  assign Q    = q_reg;
  assign QN   = ~ q_reg;
  assign CD_Q = CONFIG_DONE & q_reg;

endmodule 