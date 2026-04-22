module bench_48_stopwatch (
    input clk,
    input reset,
    input start_stop,
    output reg [5:0] seconds,
    output reg [5:0] minutes
  );

  reg running;
  reg [23:0] prescaler; // Assume fast clock, divide down

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      seconds <= 0;
      minutes <= 0;
      running <= 0;
      prescaler <= 0;
    end
    else
    begin
      if (start_stop)
        running <= ~running;

      if (running)
      begin
        if (prescaler == 24'd100000)
        begin // Mock value
          prescaler <= 0;
          if (seconds == 59)
          begin
            seconds <= 0;
            if (minutes == 59)
              minutes <= 0;
            else
              minutes <= minutes + 1;
          end
          else
            seconds <= seconds + 1;
        end
        else
          prescaler <= prescaler + 1;
      end
    end
  end

endmodule
