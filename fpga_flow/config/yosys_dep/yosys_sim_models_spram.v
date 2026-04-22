module single_port_ram (
	input clk,
	input wen,
	input[0:9] addr,
	input[0:7] d_in,
	output[0:7] d_out,
	);

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

// module mult_8(
//   input sign,
//   input [0:7] A,
//   input [0:7] B,
//   output [0:15] Y
// );
// assign Y = sign? $signed( $signed(A)*$signed(B) ) : A * B;

// endmodule

module mult_16(
  input sign,
  input [0:15] A,
  input [0:15] B,
  output [0:31] Y
);
assign Y = sign? $signed(A)*$signed(B) : A * B;

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

