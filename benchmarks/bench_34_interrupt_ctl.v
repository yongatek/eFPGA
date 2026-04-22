module bench_34_interrupt_ctl (
    input clk,
    input reset,
    input [7:0] irq,
    output reg irq_out,
    output reg [2:0] vector
  );

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      irq_out <= 0;
      vector <= 0;
    end
    else
    begin
      if (irq[0])
      begin
        irq_out <= 1;
        vector <= 0;
      end
      else if (irq[1])
      begin
        irq_out <= 1;
        vector <= 1;
      end
      else if (irq[2])
      begin
        irq_out <= 1;
        vector <= 2;
      end
      else if (irq[3])
      begin
        irq_out <= 1;
        vector <= 3;
      end
      else if (irq[4])
      begin
        irq_out <= 1;
        vector <= 4;
      end
      else if (irq[5])
      begin
        irq_out <= 1;
        vector <= 5;
      end
      else if (irq[6])
      begin
        irq_out <= 1;
        vector <= 6;
      end
      else if (irq[7])
      begin
        irq_out <= 1;
        vector <= 7;
      end
      else
        irq_out <= 0;
    end
  end

endmodule
