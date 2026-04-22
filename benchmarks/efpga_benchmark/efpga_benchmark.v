// =============================================================================
// File      : efpga_benchmark.v
// Purpose   : eFPGA SoC Integration Benchmark – Top-Level Interface Wrapper
// =============================================================================
// This module is a thin interface shell.  This module can be used as a top 
// level wrapper for any eFPGA SoC integration benchmark.  The interface is
// designed to according to the eFPGA subsystem integration.
// =============================================================================

`timescale 1ns/1ps

module efpga_benchmark 
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


endmodule