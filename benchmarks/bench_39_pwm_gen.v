module bench_39_pwm_gen (
    input clk,
    input reset,
    input [7:0] duty,
    output reg pwm_out
  );

  reg [7:0] count;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      count <= 0;
      pwm_out <= 0;
    end
    else
    begin
      count <= count + 1;
      if (count < duty)
        pwm_out <= 1;
      else
        pwm_out <= 0;
    end
  end

endmodule
