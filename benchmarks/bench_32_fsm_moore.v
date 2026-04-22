module bench_32_fsm_moore (
    input clk,
    input reset,
    input in_a,
    output reg [1:0] out_state
  );

  reg [1:0] state;
  localparam S0=2'b00, S1=2'b01, S2=2'b10, S3=2'b11;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
      state <= S0;
    else
    begin
      case (state)
        S0:
          if (in_a)
            state <= S1;
        S1:
          if (in_a)
            state <= S2;
          else
            state <= S0;
        S2:
          if (in_a)
            state <= S3;
          else
            state <= S1;
        S3:
          if (!in_a)
            state <= S0;
      endcase
    end
  end

  always @(*) out_state = state;

endmodule
