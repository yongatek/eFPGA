module bench_36_i2c_slave (
    input clk,
    input reset,
    input sda_in,
    output reg sda_out,
    output reg sda_oe,
    input scl,
    output reg [7:0] data_rx
  );
  // Simplified I2C slave receiver
  reg [3:0] state;
  reg [2:0] bit_cnt;
  reg [7:0] shift_reg;
  reg sda_prev, scl_prev;

  // Edge detection
  always @(posedge clk)
  begin
    sda_prev <= sda_in;
    scl_prev <= scl;
  end

  wire start_cond = sda_prev && !sda_in && scl;
  wire stop_cond = !sda_prev && sda_in && scl;
  wire scl_rising = !scl_prev && scl;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      state <= 0;
      sda_oe <= 0;
      bit_cnt <= 0;
    end
    else
    begin
      if (start_cond)
        state <= 1;
      else if (stop_cond)
        state <= 0;
      else
      begin
        case (state)
          1:
          begin // Receive Address/Data
            if (scl_rising)
            begin
              shift_reg <= {shift_reg[6:0], sda_in};
              bit_cnt <= bit_cnt + 1;
              if (bit_cnt == 7)
              begin
                state <= 2; // ACK
                data_rx <= {shift_reg[6:0], sda_in};
              end
            end
          end
          2:
          begin // Send ACK
            sda_out <= 0;
            sda_oe <= 1;
            if (scl_rising)
            begin
              state <= 1;
              sda_oe <= 0;
              bit_cnt <= 0;
            end
          end
        endcase
      end
    end
  end

endmodule
