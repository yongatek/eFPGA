module bench_33_bus_arbiter (
    input clk,
    input reset,
    input req0, 
    input req1, 
    input req2, 
    input req3,
    output reg gnt0, 
    output reg gnt1, 
    output reg gnt2, 
    output reg gnt3
  );

  reg [1:0] state; // Round Robin Pointer

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      state <= 0;
      {gnt0, gnt1, gnt2, gnt3} <= 0;
    end
    else
    begin
      {gnt0, gnt1, gnt2, gnt3} <= 0;
      case (state)
        0:
          if (req0)
          begin
            gnt0 <= 1;
            state <= 1;
          end
          else if (req1)
          begin
            gnt1 <= 1;
            state <= 2;
          end
          else if (req2)
          begin
            gnt2 <= 1;
            state <= 3;
          end
          else if (req3)
          begin
            gnt3 <= 1;
            state <= 0;
          end
        1:
          if (req1)
          begin
            gnt1 <= 1;
            state <= 2;
          end
          else if (req2)
          begin
            gnt2 <= 1;
            state <= 3;
          end
          else if (req3)
          begin
            gnt3 <= 1;
            state <= 0;
          end
          else if (req0)
          begin
            gnt0 <= 1;
            state <= 1;
          end
        2:
          if (req2)
          begin
            gnt2 <= 1;
            state <= 3;
          end
          else if (req3)
          begin
            gnt3 <= 1;
            state <= 0;
          end
          else if (req0)
          begin
            gnt0 <= 1;
            state <= 1;
          end
          else if (req1)
          begin
            gnt1 <= 1;
            state <= 2;
          end
        3:
          if (req3)
          begin
            gnt3 <= 1;
            state <= 0;
          end
          else if (req0)
          begin
            gnt0 <= 1;
            state <= 1;
          end
          else if (req1)
          begin
            gnt1 <= 1;
            state <= 2;
          end
          else if (req2)
          begin
            gnt2 <= 1;
            state <= 3;
          end
      endcase
    end
  end

endmodule
