`timescale 1ns/1ps
module mac_4_tb();

	parameter DATA_WIDTH = 4;  /* declare a parameter. default required */
	reg [DATA_WIDTH - 1 : 0] a, b, c;
	wire [DATA_WIDTH - 1 : 0] out;
	reg clk = 0;

	mac_4_top_formal_verification fpga_dut(a, b, c, out);

	initial forever #10 clk =~ clk;

	integer i;

	reg errors = 0;
	initial begin
		for(i=0; i<10; i=i+1) begin
			@(posedge clk);
			#1;
			a = $random;
			b = $random;
			c = $random;
		end
		if(errors)
			$display("Simulation Failed!");
		else
			$display("Simulation Succeed!");
		$finish;
	end

	always @(posedge clk) begin
		$display("A: %0d, B: %0d, C: %0d, out:%0d", a, b, c, out);
		if(out != a * b + c)
			errors=1;
//			$display("Failed");
//		else
//			$display("Passed");
	end

endmodule









