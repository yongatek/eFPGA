`timescale 1ns/1ps
module counter_tb ();

reg clk = 0;
reg reset = 1;
wire [7:0] result;

reg [7:0] tb_result;
reg errors = 0;
initial forever #10 clk =~ clk;
integer i;

counter_top_formal_verification fpga_dut(clk, reset, result);

initial begin
	$dumpfile("counter_formal.vcd");
	$dumpvars(1, counter_tb);
	tb_result <= 0;
	reset = 1;
	#21;
	reset = 0;
	for(i=0; i<127; i=i+1) begin
		@(posedge clk);	
	end
	#1;
	reset = 1;
	#20;
	reset = 0;
	for(i=0; i<255; i=i+1) begin
		@(posedge clk);	
	end
	$display("TB_cnt: %0d, Bench_cnt: %0d", tb_result, result);
	
	if(errors==0)
		$display("Simulation Succeed!");
	else
		$display("Simulation Failed!");
	$finish;
end


always @(posedge clk)
	begin
		if(tb_result != result)
			errors = 1;
		if (reset) 
			tb_result = 0;		
		else 
			tb_result = tb_result + 1;
	end
endmodule
