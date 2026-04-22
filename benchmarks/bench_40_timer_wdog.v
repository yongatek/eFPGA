module bench_40_timer_wdog (
    input clk,
    input reset,
    input kick,
    output reg wdog_reset_out
  );

  reg [15:0] count;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      count <= 0;
      wdog_reset_out <= 0;
    end
    else
    begin
      if (kick)
      begin
        count <= 0;
      end
      else
      begin
        if (count == 16'hFFFF)
        begin
          wdog_reset_out <= 1;
        end
        else
        begin
          count <= count + 1;
          wdog_reset_out <= 0;
        end
      end
    end
  end

endmodule
