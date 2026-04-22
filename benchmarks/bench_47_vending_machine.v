module bench_47_vending_machine (
    input clk,
    input reset,
    input coin_5,
    input coin_10,
    input select_A, // Cost 15
    output reg dispense,
    output reg [4:0] change
  );

  reg [4:0] balance;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      balance <= 0;
      dispense <= 0;
      change <= 0;
    end
    else
    begin
      dispense <= 0;
      change <= 0;
      if (coin_5)
        balance <= balance + 5;
      else if (coin_10)
        balance <= balance + 10;

      if (select_A && balance >= 15)
      begin
        dispense <= 1;
        change <= balance - 15;
        balance <= 0;
      end
    end
  end

endmodule
