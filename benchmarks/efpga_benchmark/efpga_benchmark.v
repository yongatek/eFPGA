// =============================================================================
// File      : efpga_benchmark.v
// Purpose   : eFPGA SoC Integration Benchmark – Top-Level Interface Wrapper
// =============================================================================
// This module is a thin interface shell.  All functional logic lives in the
// mode_test_benchmark submodule below so that the interface can be reused with
// alternate benchmark implementations by swapping only the submodule.
// =============================================================================

`timescale 1ns/1ps

module efpga_benchmark 
// #( parameter packer_mode = 0,
//                           parameter unpacker_mode = 0)
 (
    input  wire        clk,
    input  wire        reset_n,

    // Data In
    input  wire [63:0] data_in,         // Mode 0 [63:0], mode 1 [31:0], mode 2 [15:0], mode 3 [7:0] 
    input  wire        data_in_strobe,  //
    output wire        data_in_ready,   //

    // Data Out
    output wire [63:0] data_out,
    output wire        data_out_strobe,
    input  wire        data_out_ready,

    // Interrupt
    output wire        interrupt,

    // GPIO
    input  wire [3:0]  gpio_in,
    output wire [3:0]  gpio_out
);

  counter u_core (
    .clk              (clk),
    .reset_n          (reset_n),
    .data_in          (data_in),
    .data_in_strobe   (data_in_strobe),
    .data_in_ready    (data_in_ready),
    .data_out         (data_out),
    .data_out_strobe  (data_out_strobe),
    .data_out_ready   (data_out_ready),
    .interrupt        (interrupt),
    .gpio_in          (gpio_in),
    .gpio_out         (gpio_out)
  );
  // reg [63:0] cnt;
  // reg cnt_valid;
  // assign data_in_ready = 1'b1;
  // assign data_out = cnt;
  // assign data_out_strobe = cnt_valid;
  // assign gpio_out = ~ gpio_in;
  // assign interrupt = cnt > 64;
  // always @(posedge clk) begin
  //   cnt_valid <= 0;
  //   if(~reset_n) begin
  //     cnt <= 64'b0;
  //   end else if(data_out_ready) begin
  //     cnt = cnt + 1;
  //     cnt_valid <=1;
  //   end
  // end

endmodule