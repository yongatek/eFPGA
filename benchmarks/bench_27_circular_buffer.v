module bench_27_circular_buffer (
    input clk,
    input reset,
    input wr_en,
    input [7:0] data_in,
    input rd_en,
    output reg [7:0] data_out
  );

  reg [7:0] buffer [31:0];
  reg [4:0] wr_ptr, rd_ptr;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      wr_ptr <= 0;
      rd_ptr <= 0;
      data_out <= 0;
    end
    else
    begin
      if (wr_en)
      begin
        buffer[wr_ptr] <= data_in;
        wr_ptr <= wr_ptr + 1;
      end
      if (rd_en)
      begin
        data_out <= buffer[rd_ptr];
        rd_ptr <= rd_ptr + 1;
      end
    end
  end

endmodule
