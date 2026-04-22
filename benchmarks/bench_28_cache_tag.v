module bench_28_cache_tag (
    input clk,
    input GLOBAL_RESET,
    input [3:0] index,
    input [19:0] tag_in,
    input we,
    output reg hit
  );

  reg [20:0] tag_mem [15:0];

  always @(posedge clk or negedge GLOBAL_RESET)
  begin
    if (~GLOBAL_RESET)
    begin
      hit <= 0;
    end
    else
    begin
      if (we)
      begin
        tag_mem[index] <= {1'b1, tag_in};
      end

      if (tag_mem[index][20] && tag_mem[index][19:0] == tag_in)
        hit <= 1'b1;
      else
        hit <= 1'b0;
    end
  end

endmodule
