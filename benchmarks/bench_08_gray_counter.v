module bench_08_gray_counter (
    input clk,
    input reset,
    input enable,
    output reg [7:0] gray_out
  );

  reg [7:0] binary_count;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      binary_count <= 8'b0;
      gray_out <= 8'b0;
    end
    else if (enable)
    begin
      binary_count <= binary_count + 1;
      gray_out <= {binary_count[7], binary_count[7:1] ^ binary_count[6:0]};
    end
  end

endmodule
