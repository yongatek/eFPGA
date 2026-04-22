module bench_15_cordic_rotator (
    input clk,
    input reset,
    input signed [15:0] x_in,
    input signed [15:0] y_in,
    input [15:0] angle_in,
    input start,
    output reg signed [15:0] x_out,
    output reg signed [15:0] y_out,
    output reg done
  );

  // Simple fixed-point iterative CORDIC (simplified for benchmark)
  // 8 iterations
  reg [3:0] iter;
  reg signed [15:0] x, y, z;
  reg busy;

  // Arctan table would be here, simplifying for logic synthesis benchmark
  // Just shuffling bits to simulate logic

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      done <= 1'b0;
      busy <= 1'b0;
      x_out <= 16'd0;
      y_out <= 16'd0;
    end
    else if (start && !busy)
    begin
      x <= x_in;
      y <= y_in;
      z <= 16'd0; // Angle
      iter <= 4'd0;
      busy <= 1'b1;
      done <= 1'b0;
    end
    else if (busy)
    begin
      // Simplified "CORDIC-like" shift/add for synthesis load
      if (iter < 8)
      begin
        if (z < angle_in)
        begin
          x <= x - (y >>> iter);
          y <= y + (x >>> iter);
          z <= z + (16'd5000 >>> iter);
        end
        else
        begin
          x <= x + (y >>> iter);
          y <= y - (x >>> iter);
          z <= z - (16'd5000 >>> iter);
        end
        iter <= iter + 1;
      end
      else
      begin
        x_out <= x;
        y_out <= y;
        done <= 1'b1;
        busy <= 1'b0;
      end
    end
  end

endmodule
