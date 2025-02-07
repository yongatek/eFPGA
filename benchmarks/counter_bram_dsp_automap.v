module counter_bram_dsp_automap (
	clk,
	reset,
	mult_a, 
	mult_b,
	and_all_bram_douts,
	data_out,
	mult_out,
	result,
	ops_on_mult
);

	input clk;
	input reset;
	input [17:0] mult_a;
	input [17:0] mult_b;
	reg [17:0] mult_a_reg, mult_b_reg;

	output reg [31:0] result;
	output [7:0] data_out;
	output [35:0] mult_out;
	output wire and_all_bram_douts;
	output reg ops_on_mult;
	reg [31:0] counter;
	reg ren, wen;
	reg [9:0] waddr;
	reg [9:0] raddr;
	
	reg Do0_bram_0_reg;
	wire [7:0] Do0_bram;
	
	assign mult_out = mult_a_reg * mult_b_reg;
	
	reg [7:0] ram[0:1023];
  	reg [7:0] internal;

  	assign data_out = internal;

  	always @(posedge clk) begin
    	if(wen) begin
      		ram[waddr] <= result[7:0];
    	end
  	end

  	always @(posedge clk) begin
    	if(ren) begin
      		internal <= ram[raddr];
    	end
  	end
	
	assign and_all_bram_douts = &data_out;
	
	always @(posedge clk or posedge reset) begin
		if (reset) begin
			counter <= 0;
			ren <= 0;
			wen <= 0;
			waddr <= 0;
			raddr <= 0;
			result <= 0;
			mult_a_reg <= 0;
			mult_b_reg <= 0;
		end
		else begin
			mult_a_reg <= mult_a;
			mult_b_reg <= mult_b;
			ops_on_mult <= (mult_out - 5 == 0) | (counter == 1);
			wen <= 0;
			ren <= 0;
			result <= counter;
			counter <= counter + 1;
			if(counter < 10)begin
				wen <= 1;
				waddr <= waddr + 1;
			end else if (counter < 15)begin
				ren <= 1;
				raddr <= raddr + 1;
				if (counter == 14) begin
					counter <= 0;
				end
			end
		end
	end
endmodule

