module bench_38_uart_rx (
    input clk,
    input reset,
    input rx,
    output reg [7:0] data_out,
    output reg valid
  );

  reg [3:0] state;
  reg [3:0] bit_cnt;
  reg [15:0] baud_cnt;
  reg [7:0] shift_reg;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      state <= 0;
      valid <= 0;
      baud_cnt <= 0;
    end
    else
    begin
      valid <= 0;
      case (state)
        0:
          if (!rx)
          begin
            state <= 1;
            baud_cnt <= 50;
          end // Start bit detected
        1:
        begin // Wait half bit
          if (baud_cnt == 0)
          begin
            state <= 2;
            baud_cnt <= 100;
            bit_cnt <= 0;
          end
          else
            baud_cnt <= baud_cnt - 1;
        end
        2:
        begin // Sampling data
          if (baud_cnt == 0)
          begin
            shift_reg <= {rx, shift_reg[7:1]};
            baud_cnt <= 100;
            bit_cnt <= bit_cnt + 1;
            if (bit_cnt == 7)
              state <= 3;
          end
          else
            baud_cnt <= baud_cnt - 1;
        end
        3:
        begin // Stop bit
          if (baud_cnt == 0)
          begin
            state <= 0;
            valid <= 1;
            data_out <= shift_reg;
          end
          else
            baud_cnt <= baud_cnt - 1;
        end
      endcase
    end
  end

endmodule
