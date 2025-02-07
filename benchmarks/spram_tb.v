module spram_tb ();

	reg clk;
	reg [10:0] addr;
	reg [7:0] din;
	reg wen;
	wire [7:0] dout;

	initial begin
		clk[0] <= 1'b0;
		while(1) begin
			#5
			clk[0] <= !clk[0];
		end
	end

	spram_top_formal_verification FPGA_DUT(
		.clk(clk),
		.write_enable(wen),
		.write_data(din),
		.addr(addr),
		.read_data(dout)
	);
	
	initial begin
	$monitor(dout);
	$dumpfile("spram_formal.vcd");
	$dumpvars(1, spram_tb);
	
	addr = 11'b000_0000_0000;
	wen = 1;
	din=8'b00000000;
	#10;
	
	addr = 11'b000_0000_1000;
	wen = 1;
	din=8'b00000001;
	#10;
	
	addr = 11'b000_1000_0000;
	wen = 1;
	din=8'b00000010;
	#10;
	
	addr = 11'b010_0000_0000;
	wen = 1;
	din=8'b00000011;
	#10;
	
	addr = 11'b100_0000_0000;
	wen = 1;
	din=8'b00000100;
	#10;
	
	addr = 11'b100_0000_0001;
	wen = 1;
	din=8'b00000101;
	#10;
	
	wen =0;
	addr = 11'b000_0000_0000;
	#10;
	addr = 11'b000_0000_1000;
	#10;
	addr = 11'b000_1000_0000;
	#10;
	addr = 11'b010_0000_0000;
	#10;
	addr = 11'b100_0000_0000;
	#10;
	addr = 11'b100_0000_0001;
	#10;
	addr = 11'b000_0000_0000;
	#10;
	addr = 11'b100_0000_0001;
	wen = 1;
	din=8'b00000110;
	#10;
	wen = 0 ;
	#20;
	$finish;
	end
	
endmodule
