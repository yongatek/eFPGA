module bench_10_sequence_det (
    input clk,
    input reset,
    input bit_in,
    output reg detected
  );

  // Detect 1101
  reg [1:0] state;
  localparam S0 = 2'b00;
  localparam S1 = 2'b01;
  localparam S2 = 2'b10;
  localparam S3 = 2'b11;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      state <= S0;
      detected <= 1'b0;
    end
    else
    begin
      detected <= 1'b0;
      case (state)
        S0:
          if (bit_in)
            state <= S1;
          else
            state <= S0;
        S1:
          if (bit_in)
            state <= S2;
          else
            state <= S0;
        S2:
          if (!bit_in)
            state <= S3;
          else
            state <= S2;
        S3:
        begin
          if (bit_in)
          begin
            state <= S1;
            detected <= 1'b1;
          end
          else
          begin
            state <= S0;
          end
        end
      endcase
    end
  end

endmodule
