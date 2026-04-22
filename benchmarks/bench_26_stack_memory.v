module bench_26_stack_memory (
    input clk,
    input GLOBAL_RESET,
    input push,
    input pop,
    input [7:0] data_in,
    output reg [7:0] data_out,
    output full,
    output empty
  );

  reg [7:0] mem [31:0];
  reg [4:0] sp;

  assign full = (sp == 31);
  assign empty = (sp == 0);

  always @(posedge clk or negedge GLOBAL_RESET)
  begin
    if (~GLOBAL_RESET)
    begin
      sp <= 0;
      data_out <= 0;
    end
    else
    begin
      if (push && !full)
      begin
        mem[sp] <= data_in;
        sp <= sp + 1;
      end
      else if (pop && !empty)
      begin
        sp <= sp - 1;
        data_out <= mem[sp - 1];
      end
    end
  end

endmodule
