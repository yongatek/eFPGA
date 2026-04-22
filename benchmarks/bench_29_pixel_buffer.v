module bench_29_pixel_buffer (
    input clk,
    input [7:0] pixel_in,
    output [7:0] pixel_out_0,
    output [7:0] pixel_out_1,
    output [7:0] pixel_out_2
  );

  reg [7:0] line0 [15:0];
  reg [7:0] line1 [15:0];
  reg [7:0] line2 [15:0];

  reg [3:0] ptr;

  always @(posedge clk)
  begin
    line0[ptr] <= pixel_in;
    line1[ptr] <= line0[ptr];
    line2[ptr] <= line1[ptr];

    ptr <= ptr + 1;
  end

  assign pixel_out_0 = line0[ptr];
  assign pixel_out_1 = line1[ptr];
  assign pixel_out_2 = line2[ptr];

endmodule
