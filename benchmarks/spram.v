module spram (clk, write_enable, write_data, addr, read_data);
parameter DATA_WIDTH = 8;
parameter ADDR_WIDTH = 11;

input clk;
input write_enable;
input [7: 0] write_data;
input [10 : 0] addr; 
output reg [7 : 0] read_data;
reg [7:0] read_dataNext;


reg [DATA_WIDTH - 1 : 0] mem [2**ADDR_WIDTH - 1 : 0];

always @(posedge clk) begin
	read_data <= read_dataNext;
	if (write_enable)
		mem[addr] <= write_data;
	else 
		read_dataNext <= mem[addr];
end

endmodule
