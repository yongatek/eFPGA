module dual_port_ram (
	input clk,
	input wen1,
	input[0:9] addr1,
	input[0:7] d_in1,
	output[0:7] d_out1,
	input wen2,
	input[0:9] addr2,
	input[0:7] d_in2,
	output[0:7] d_out2 );

	reg[0:7] ram[0:1023];
	reg[0:7] internal1;
	reg[0:7] internal2;

	assign d_out1 = internal1;

	always @(posedge clk) begin
		if(wen1) begin
			ram[addr1] <= d_in1;
		end	else begin
			internal1 <= ram[addr1];
		end
	end

	assign d_out2 = internal2;

	always @(posedge clk) begin
		if(wen2) begin
			ram[addr2] <= d_in2;
		end	else begin
			internal2 <= ram[addr2];
		end
	end
endmodule

module mult_8(
  input sign,
  input [0:7] A,
  input [0:7] B,
  output [0:15] Y
);
assign Y = sign? $signed( $signed(A)*$signed(B) ) : A * B;

endmodule



(* abc9_box, lib_whitebox *)
module adder(
    output sumout,
    output cout,
    input a,
    input b,
    input cin
);
    assign sumout = a ^ b ^ cin;
    assign cout = (a & b) | ((a | b) & cin);

endmodule

