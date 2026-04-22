module ff_mem(
		input clk, 
		input GLOBAL_RESET,
		input write_i,
		input [1:0] be_sel_i,
		input [3:0] addr_i,
		input [15:0] data_i,
		input [7:0] bram_d_i,
		input [12:0] bram_a, 
		output reg [7:0] bram_d_o, 
		output [15:0] data_o,
		output [23:0] product
);


	reg [7 : 0] ram [8191 : 0];

	always @(posedge clk) begin
		if (write_i)
			ram[bram_a] <= bram_d_i;
		else 
			bram_d_o <= ram[bram_a];
	end

	reg [7:0] mem [0:63]; 
	assign product = mem[0] * mem[1]   *  mem[2] ;
 
	 
	assign data_o[7:0] = mem[{addr_i[3:0], 2'b00}];
	assign data_o[15:8] = mem[{addr_i[3:0], 2'b01}];


	integer i;
	always@(posedge clk)begin
		if(GLOBAL_RESET)begin
		 for(i=0;i<63;i=i+1)begin
			mem[i] <= 0;			
		end	
	end else begin 
		mem[{addr_i[3:0],2'b00}] <= (write_i & be_sel_i[0]) ? data_i[0+:8] : mem[{addr_i[3:0], 2'b00}];
		mem[{addr_i[3:0],2'b01}] <= (write_i & be_sel_i[1]) ? data_i[8+:8] : mem[{addr_i[3:0], 2'b01}];
	end 	
   end 
endmodule 
