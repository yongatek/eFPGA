module bench_13_mac_unit (
    input clk,
    input reset,
    input [15:0] a,
    input [15:0] b,
    input acc_en,
    input clear_acc,
    output reg [39:0] acc_out
  );

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      acc_out <= 40'b0;
    end
    else if (clear_acc)
    begin
      acc_out <= 40'b0;
    end
    else if (acc_en)
    begin
      acc_out <= acc_out + (a * b);
    end
  end

endmodule
