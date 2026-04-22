module bench_04_shift_reg_64bit (
    input clk,
    input reset,
    input shift_in,
    input shift_en,
    output shift_out
  );

  reg [63:0] shift_reg;

  assign shift_out = shift_reg[63];

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      shift_reg <= 64'b0;
    end
    else if (shift_en)
    begin
      shift_reg <= {shift_reg[62:0], shift_in};
    end
  end

endmodule
