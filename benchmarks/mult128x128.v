module mult128x128(
    input [127:0] in1, in2,
    input clk,
    output [255:0] out
);

    mult #(128) mult_0 (.in1(in1), .in2(in2), .clk(clk), .out(out));

endmodule


module mult #(
        parameter width = 128
    )(
    input [width-1:0] in1, in2,
    input clk, 
    output [2*width-1:0] out
);
    generate
        if(width>16) begin
            wire [width-1:0] out1, out2, out3, out4;
            mult #(width/2) mult_0(.in1(in1[width/2-1:0]),     .in2(in2[width/2-1:0]),     .clk(clk), .out(out1));
            mult #(width/2) mult_1(.in1(in1[width/2-1:0]),     .in2(in2[width-1:width/2]), .clk(clk), .out(out2));
            mult #(width/2) mult_2(.in1(in1[width-1:width/2]), .in2(in2[width/2-1:0]),     .clk(clk), .out(out3));
            mult #(width/2) mult_3(.in1(in1[width-1:width/2]), .in2(in2[width-1:width/2]), .clk(clk), .out(out4));

            wire [width-1:0] out1_r, out2_r, out3_r, out4_r;
            flop #(width) flop_0 (.in(out1), .clk(clk), .out(out1_r));
            flop #(width) flop_1 (.in(out2), .clk(clk), .out(out2_r));
            flop #(width) flop_2 (.in(out3), .clk(clk), .out(out3_r));
            flop #(width) flop_3 (.in(out4), .clk(clk), .out(out4_r));

            wire [2*width-1:0] out_r21, out_r22, tmp1, tmp2;
            assign tmp1 = ( (out1_r              ) + (out2_r << (width/2)) );
            assign tmp2 = ( (out3_r << (width/2) ) + (out4_r << (width  )) );
            flop #(2*width) flop_5 (.in(tmp1), .clk(clk), .out(out_r21));
            flop #(2*width) flop_6 (.in(tmp2), .clk(clk), .out(out_r22));
            assign out = out_r21 + out_r22;   
        end else begin
            assign out = in1 * in2;
        end
    endgenerate
endmodule

module flop #(
        parameter width = 1
    )(
        input [width-1:0] in,
        input clk,
        output reg [width-1:0] out
    );

    always@(posedge clk)
        out <= in;
endmodule