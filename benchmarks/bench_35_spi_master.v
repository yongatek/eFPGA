module bench_35_spi_master (
    input clk,
    input reset,
    input [7:0] data_in,
    input start,
    output reg mosi,
    input miso,
    output reg sclk,
    output reg done
  );

  reg [3:0] bit_cnt;
  reg [2:0] state; // 0: Idle, 1: Shift
  reg [7:0] shift_reg;
  reg clk_div;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      state <= 0;
      mosi <= 0;
      sclk <= 0;
      done <= 0;
      clk_div <= 0;
    end
    else
    begin
      clk_div <= ~clk_div;
      if (clk_div)
      begin // Slow down SCLK
        case (state)
          0:
          begin
            sclk <= 0;
            done <= 0;
            if (start)
            begin
              shift_reg <= data_in;
              state <= 1;
              bit_cnt <= 0;
            end
          end
          1:
          begin
            sclk <= ~sclk;
            if (sclk == 0)
            begin // Rising edge
              mosi <= shift_reg[7];
            end
            else
            begin // Falling edge
              shift_reg <= {shift_reg[6:0], miso};
              bit_cnt <= bit_cnt + 1;
              if (bit_cnt == 7)
              begin
                state <= 0;
                done <= 1;
              end
            end
          end
        endcase
      end
    end
  end

endmodule
