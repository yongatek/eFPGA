module mac_4(a, b, c, out, a_in, a_out, clk, GLOBAL_RESET);
input clk;
input GLOBAL_RESET;
input [3 : 0] a;
input [3 : 0] b;
input [3 : 0] c;
input [31:0] a_in;
output [3 : 0] out;
output reg [31:0] a_out;
reg [31:0] a1, a2, a3;

assign out = a * b + c;

always@(posedge clk, negedge GLOBAL_RESET) begin
    if(~GLOBAL_RESET) begin
        a_out <= 0;
        a3 <=    0;
        a2 <=    0;
        a1 <=    0;
    end else begin
        a_out <= a3;
        a3 <= a2;
        a2 <= a1;
        a1 <= a_in;
    end
end
endmodule









