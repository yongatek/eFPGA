module bench_06_div_8bit (
    input clk,
    input reset,
    input [7:0] dividend,
    input [7:0] divisor,
    input start,
    output reg [7:0] quotient,
    output reg [7:0] remainder,
    output reg done,
    output reg busy
  );

  reg [3:0] count;
  reg [15:0] reg_remainder;
  reg [7:0] reg_divisor;

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      quotient <= 8'b0;
      remainder <= 8'b0;
      done <= 1'b0;
      busy <= 1'b0;
      count <= 4'd8;
    end
    else if (start && !busy)
    begin
      reg_divisor <= divisor;
      reg_remainder <= {8'b0, dividend};
      quotient <= 8'b0;
      count <= 4'd8;
      busy <= 1'b1;
      done <= 1'b0;
    end
    else if (busy)
    begin
      if (count > 0)
      begin
        reg_remainder = reg_remainder << 1;
        if (reg_remainder[15:8] >= reg_divisor)
        begin
          reg_remainder[15:8] = reg_remainder[15:8] - reg_divisor;
          reg_remainder[0] = 1'b1;
        end
        count <= count - 1;
      end
      else
      begin
        quotient <= reg_remainder[7:0];
        remainder <= reg_remainder[15:8];
        busy <= 1'b0;
        done <= 1'b1;
      end
    end
  end

endmodule
