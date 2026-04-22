module bench_49_sha256_mock (
    input clk,
    input reset,
    input [14:0] a, 
    input [15:0] b, 
    input [15:0] c,
    output reg [15:0] out
  );
  // Reduced to 16-bit to lower IO pressure (<143 pins)
  // Ch(x, y, z) = (x & y) ^ (~x & z)
  // Maj(x, y, z) = (x & y) ^ (x & z) ^ (y & z)

  wire [15:0] ch = (a & b) ^ (~a & c);
  wire [15:0] maj = (a & b) ^ (a & c) ^ (b & c);

  always @(posedge clk or posedge reset)
  begin
    if (reset)
      out <= 0;
    else
      out <= ch + maj + 16'h2f98;
  end

endmodule
