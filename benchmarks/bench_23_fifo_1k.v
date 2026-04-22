module bench_23_fifo_1k (
    input clk,
    input reset,
    input wr_en,
    input rd_en,
    input [7:0] data_in,
    output reg [7:0] data_out,
    output full,
    output empty
  );

  reg [7:0] mem [31:0];
  reg [4:0] wr_ptr, rd_ptr;
  reg [5:0] count;

  assign full = (count == 32);
  assign empty = (count == 0);

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      wr_ptr <= 0;
      rd_ptr <= 0;
      count <= 0;
      data_out <= 0;
    end
    else
    begin
      if (wr_en && !full)
      begin
        mem[wr_ptr] <= data_in;
        wr_ptr <= wr_ptr + 1;
      end
      if (rd_en && !empty)
      begin
        data_out <= mem[rd_ptr];
        rd_ptr <= rd_ptr + 1;
      end

      if (wr_en && !full && !(rd_en && !empty))
        count <= count + 1;
      else if (rd_en && !empty && !(wr_en && !full))
        count <= count - 1;
    end
  end

endmodule
