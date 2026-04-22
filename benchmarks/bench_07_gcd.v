module bench_07_gcd (
    input clk,
    input reset,
    input [7:0] a_in,
    input [7:0] b_in,
    input start,
    output reg [7:0] gcd_out,
    output reg done
  );

  reg [7:0] a, b;
  reg [1:0] state; // 00: IDLE, 01: COMP, 10: SUB, 11: DONE

  localparam IDLE = 2'b00;
  localparam COMP = 2'b01;
  localparam SUB  = 2'b10;
  localparam DONE = 2'b11;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      state <= IDLE;
      gcd_out <= 8'b0;
      done <= 1'b0;
    end
    else
    begin
      case (state)
        IDLE:
        begin
          if (start)
          begin
            a <= a_in;
            b <= b_in;
            state <= COMP;
            done <= 1'b0;
          end
        end
        COMP:
        begin
          if (a == b)
          begin
            gcd_out <= a;
            state <= DONE;
          end
          else if (b == 0)
          begin
            gcd_out <= a;
            state <= DONE;
          end
          else if (a == 0)
          begin
            gcd_out <= b;
            state <= DONE;
          end
          else
          begin
            state <= SUB;
          end
        end
        SUB:
        begin
          if (a > b)
            a <= a - b;
          else
            b <= b - a;
          state <= COMP;
        end
        DONE:
        begin
          done <= 1'b1;
          state <= IDLE;
        end
      endcase
    end
  end

endmodule
