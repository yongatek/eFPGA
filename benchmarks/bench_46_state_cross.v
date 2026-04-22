module bench_46_state_cross (
    input clk,
    input reset,
    input [1:0] sel0, 
    input [1:0] sel1, 
    input [1:0] sel2, 
    input [1:0] sel3,
    input [7:0] in0, 
    input [7:0] in1, 
    input [7:0] in2, 
    input [7:0] in3,
    output reg [7:0] out0, 
    output reg [7:0] out1, 
    output reg [7:0] out2, 
    output reg [7:0] out3
  );

  function [7:0] mux4;
    input [1:0] s;
    input [7:0] i0, i1, i2, i3;
    case (s)
      0:
        mux4 = i0;
      1:
        mux4 = i1;
      2:
        mux4 = i2;
      3:
        mux4 = i3;
    endcase
  endfunction

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      out0 <= 0;
      out1 <= 0;
      out2 <= 0;
      out3 <= 0;
    end
    else
    begin
      out0 <= mux4(sel0, in0, in1, in2, in3);
      out1 <= mux4(sel1, in0, in1, in2, in3);
      out2 <= mux4(sel2, in0, in1, in2, in3);
      out3 <= mux4(sel3, in0, in1, in2, in3);
    end
  end

endmodule
