// =============================================================================
// Submodule : mode_test_benchmark
// Purpose   : All benchmark logic – modes, header management, datapath, FSM
// =============================================================================
// Notes on Fanout Reduction:
// Controls are explicitly duplicated 4 times to reduce fanout from ~128 to ~16.
// Datapath registers (result, shreg, counter_r) are created as 4 explicit
// 16-bit physical registers (e.g. result0, result1...) so that open-source
// synthesis tools do not mangle arrays assigned from multiple always blocks.
// =============================================================================

module counter (
    input  wire        clk,
    input  wire        reset_n,

    // Data In
    input  wire [63:0] data_in,
    input  wire        data_in_strobe,
    output wire        data_in_ready,

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
    reg start;
    assign data_out_strobe = data_out_ready & start;
    reg interrupt_r;
    assign interrupt = interrupt_r;

    reg [31:0] counter;
    reg [31:0] data_in_reg;
    always@(posedge clk) begin
        interrupt_r           <= 1'b0;
        if(~reset_n) begin
            counter         <= 32'h00000000;
            data_in_reg     <= 32'h00000000;
            start           <= 1'b0;
        end
        else begin
            if(data_in_strobe) begin
                if(data_in[31:0] == 32'hABCDABCD)
                    start <= 1;
                else if (data_in[63:0] == 64'hFFFFFFFFFFFFFFFF)
                    interrupt_r <= 1;
                data_in_reg <= data_in;                
            end
            if(data_out_ready & start) begin
                counter <= counter + 1;
            end       
        end
    end
    assign data_in_ready = data_out_ready;
    assign data_out         = {data_in_reg, counter};
    assign gpio_out = (~ gpio_in) + counter[3:0];

endmodule
