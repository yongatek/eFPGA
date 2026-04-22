module bench_31_fsm_mealy (
    input clk,
    input reset,
    input in_a,
    output reg out_z
  );

  reg [1:0] state, next_state;
  localparam S0 = 2'b00, S1 = 2'b01, S2 = 2'b10;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
      state <= S0;
    else
      state <= next_state;
  end

  always @(*)
  begin
    next_state = state;
    out_z = 0;
    case (state)
      S0:
        if (in_a)
          next_state = S1;
      S1:
      begin
        if (in_a)
          next_state = S2;
        else
          next_state = S0;
      end
      S2:
      begin
        if (in_a)
        begin
          next_state = S0;
          out_z = 1;
        end
        else
          next_state = S0;
      end
    endcase
  end

endmodule
