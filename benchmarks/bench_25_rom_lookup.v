module bench_25_rom_lookup (
    input clk,
    input [7:0] addr,
    output reg [31:0] data_out
  );

  always @(posedge clk)
  begin
    case (addr)
      8'h00:
        data_out <= 32'hDEADBEEF;
      8'h01:
        data_out <= 32'hCAFEBABE;
      8'h02:
        data_out <= 32'hBAADF00D;
      8'hFF:
        data_out <= 32'h12345678;
      default:
        data_out <= {addr, addr, addr, addr}; // Algorithmic generation to save space but check read
    endcase
  end

endmodule
