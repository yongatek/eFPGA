module bench_01_alu_8bit (
    input clk,
    input reset,
    input [7:0] a,
    input [7:0] b,
    input [2:0] opcode,
    output reg [15:0] result
);

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            result <= 16'b0;
        end else begin
            case (opcode)
                3'b000: result <= a + b;
                3'b001: result <= a - b;
                3'b010: result <= a * b;
                3'b011: result <= a & b;
                3'b100: result <= a | b;
                3'b101: result <= a ^ b;
                3'b110: result <= ~(a | b);
                3'b111: result <= {a, b}; // Concatenate
            endcase
        end
    end

endmodule
