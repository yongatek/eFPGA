module ff(clk, reset, d, q);

  input clk, d, reset;
  output reg q;

  always @(posedge clk)
    if(reset) 
      q <= 0;
    else 
      q <= d;
    
endmodule