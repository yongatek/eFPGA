module bench_37_uart_tx (
    input clk,
    input reset,
    input [7:0] data_in,
    input tx_start,
    output reg tx,
    output reg busy
  );

  reg [3:0] bit_cnt;
  reg [15:0] baud_cnt;
  reg [9:0] shift_reg; // Start + Data + Stop

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      tx <= 1;
      busy <= 0;
      baud_cnt <= 0;
    end
    else
    begin
      if (busy)
      begin
        if (baud_cnt == 16'd100)
        begin
          baud_cnt <= 0;
          shift_reg <= shift_reg >> 1;
          tx <= shift_reg[0];
          bit_cnt <= bit_cnt + 1;
          if (bit_cnt == 9)
          begin
            busy <= 0;
          end
        end
        else
        begin
          baud_cnt <= baud_cnt + 1;
        end
      end
      else if (tx_start)
      begin
        busy <= 1;
        shift_reg <= {1'b1, data_in, 1'b0}; // Stop, Data, Start
        baud_cnt <= 0;
        bit_cnt <= 0;
        tx <= 0; // Start bit immediately? Logic simplified.
      end
    end
  end

endmodule
