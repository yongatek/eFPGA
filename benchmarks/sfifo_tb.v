module tb();
  reg clk, reset;
  reg w_en, r_en;
  reg [7:0] data_in;
  wire [7:0] data_out;
  wire full, empty;
  
  sfifo_top_formal_verification sfifo_top_formal_verification 
  		(.clk(clk),  .reset(reset), .w_en(w_en), .r_en(r_en), .data_in(data_in), .data_out(data_out), .full(full), .empty(empty));
  initial begin
	$dumpfile("sfifo_tb.vcd");
	$dumpvars(1, tb);
  end
  initial begin
	  clk = 0;
	  reset = 1;
	  
	  w_en = 0;
	  r_en = 0;
	  
	  data_in = 0;
	  #20;
	  reset = 0;
	  data_in = 1;
	  w_en = 1;
	  #10;
	  
	  data_in = 2;
	  w_en = 1;
	  #10;
	  
	  data_in = 3;
	  w_en = 1;
	  #10;
	  
	  data_in = 4;
	  w_en = 1;
	  #10;
	  
	  w_en = 0;
	  r_en = 1;
	  #40;
	  r_en = 0;
	  
	  #50;
	  $finish;
  end
  
  always #5 clk = ~clk;
  
endmodule
