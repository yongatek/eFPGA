module spram_1024x8 (
	input clk,
	input wen,
	input[0:9] addr,
	input[0:7] d_in,
	output[0:7] d_out );

	reg[0:7] ram[0:1023];
	reg[0:7] internal;


	assign d_out = internal;
	always @(posedge clk) begin
		if(wen) begin
			ram[addr] <= d_in;
		end	else begin
			internal <= ram[addr];
		end
	end

endmodule