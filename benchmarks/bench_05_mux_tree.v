module bench_05_mux_tree (
    input [31:0] in0, 
    input [31:0] in1, 
    input [31:0] in2,
    input [1:0] sel,
    output [31:0] out
  );

  reg [31:0] mux_out;

  always @(*)
  begin
      case (sel)
      2'b00:
        mux_out = 32'b0;
      2'b01:
        mux_out = in0;
      2'b10:
        mux_out = in1;
      2'b11:
        mux_out = in2;
      default:
        mux_out = 32'b0;
    endcase
  end

  assign out = mux_out;

endmodule
