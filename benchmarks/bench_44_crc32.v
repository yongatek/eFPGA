module bench_44_crc32 (
    input clk,
    input reset,
    input [7:0] data_in,
    input valid,
    output reg [31:0] crc_out
  );

  always @(posedge clk or posedge reset)
  begin
    if (reset)
    begin
      crc_out <= 32'hFFFFFFFF;
    end
    else if (valid)
    begin
      // Simplified CRC-like operation for synthesis stress
      crc_out <= {crc_out[30:0], 1'b0} ^ data_in ^ (crc_out[31] ? 32'h04C11DB7 : 32'h0);
    end
  end

endmodule
