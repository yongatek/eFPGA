module bench_03_fsm_traffic (
    input clk,
    input reset,
    input car_sensor,
    output reg [1:0] main_light, // 00: Red, 01: Yellow, 10: Green
    output reg [1:0] side_light
  );

  reg [1:0] state, next_state;

  localparam S_MAIN_GREEN = 2'b00;
  localparam S_MAIN_YELLOW = 2'b01;
  localparam S_SIDE_GREEN = 2'b10;
  localparam S_SIDE_YELLOW = 2'b11;

  // State Transition
  always @(posedge clk or posedge reset)
  begin
    if (reset)
      state <= S_MAIN_GREEN;
    else
      state <= next_state;
  end

  // Next State Logic
  always @(*)
  begin
    case (state)
      S_MAIN_GREEN:
      begin
        if (car_sensor)
          next_state = S_MAIN_YELLOW;
        else
          next_state = S_MAIN_GREEN;
      end
      S_MAIN_YELLOW:
      begin
        next_state = S_SIDE_GREEN;
      end
      S_SIDE_GREEN:
      begin
        if (!car_sensor)
          next_state = S_SIDE_YELLOW;
        else
          next_state = S_SIDE_GREEN;
      end
      S_SIDE_YELLOW:
      begin
        next_state = S_MAIN_GREEN;
      end
      default:
        next_state = S_MAIN_GREEN;
    endcase
  end

  // Output Logic
  always @(*)
  begin
    case (state)
      S_MAIN_GREEN:
      begin
        main_light = 2'b10; // Green
        side_light = 2'b00; // Red
      end
      S_MAIN_YELLOW:
      begin
        main_light = 2'b01; // Yellow
        side_light = 2'b00; // Red
      end
      S_SIDE_GREEN:
      begin
        main_light = 2'b00; // Red
        side_light = 2'b10; // Green
      end
      S_SIDE_YELLOW:
      begin
        main_light = 2'b00; // Red
        side_light = 2'b01; // Yellow
      end
      default:
      begin
        main_light = 2'b00;
        side_light = 2'b00;
      end
    endcase
  end

endmodule
