module bench_43_sorter_4 (
    input clk,
    input reset,
    input [7:0] in0, 
    input [7:0] in1, 
    input [7:0] in2, 
    input [7:0] in3,
    output reg [7:0] out0, 
    output reg [7:0] out1, 
    output reg [7:0] out2, 
    output reg [7:0] out3
  );

  reg [7:0] s1_0, s1_1, s1_2, s1_3;
  reg [7:0] s2_0, s2_1, s2_2, s2_3;
  reg [7:0] s3_0, s3_1, s3_2, s3_3;

  function [15:0] sort2;
    input [7:0] a, b;
    begin
      if (a > b)
        sort2 = {b, a};
      else
        sort2 = {a, b};
    end
  endfunction

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      {out0, out1, out2, out3} <= 0;
    end
    else
    begin
      // Stage 1: Sort (0,1) and (2,3)
      {s1_0, s1_1} <= sort2(in0, in1);
      {s1_2, s1_3} <= sort2(in2, in3);

      // Stage 2: Sort (0,2) and (1,3)
      {s2_0, s2_2} <= sort2(s1_0, s1_2);
      {s2_1, s2_3} <= sort2(s1_1, s1_3);

      // Stage 3: Sort (1,2)
      s3_0 <= s2_0;
      s3_3 <= s2_3;
      {s3_1, s3_2} <= sort2(s2_1, s2_2);

      {out0, out1, out2, out3} <= {s3_0, s3_1, s3_2, s3_3};
    end
  end

endmodule
