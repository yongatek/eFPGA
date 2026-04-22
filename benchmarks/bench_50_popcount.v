module bench_50_popcount (
    input clk,
    input reset,
    input [15:0] data_in,
    output reg [4:0] count
  );

  integer i;
  reg [4:0] temp_count;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      count <= 0;
    end
    else
    begin
      temp_count = 0;
      for (i = 0; i < 16; i = i + 1)
      begin
        if (data_in[i])
          temp_count = temp_count + 1;
      end
      count <= temp_count;
    end
  end

endmodule
