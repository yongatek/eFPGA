module ffram_tb();
    
    reg clk = 0;
    always #10 clk <= ~clk;
    wire dout;
    reg addr, reset, din, wen;
    
    ffram_top_formal_verification fpga_dut(clk, addr, reset, din, wen, dout);
    integer errors = 0;
    initial begin
    	$dumpfile("ffram_formal.vcd");
    	$dumpvars(1, ffram_tb);
        addr = 0;
        din = 0;
        wen = 0;
        reset = 1;
        repeat(2)
            @(posedge clk);
        if(dout != 0)
            errors = errors +1;
            
        reset = 0;
        wen = 1;
        din = 1;
        addr = 0;
        @(posedge clk);
        #1;
        if(dout != 1)
            errors = errors +1;

        addr = 1;
        wen = 0;
        din = 1;
        @(posedge clk);
        #1;
        if(dout != 0)
            errors = errors +1;

        addr = 1;
        wen = 1;
        din = 1;
        @(posedge clk);
        #1;
        if(dout != 1)
            errors = errors +1;

        addr = 0;
        wen = 0;
        din = 0;
        @(posedge clk);
        #1;
        if(dout != 1)
            errors = errors +1;

        addr = 1;
        wen = 0;
        din = 0;
        @(posedge clk);
        #1;
        if(dout != 1)
            errors = errors +1;

        addr = 1;
        wen = 1;
        din = 0;
        @(posedge clk);
        #1;
        if(dout != 0)
            errors = errors +1;

        addr = 0;
        wen = 1;
        din = 0;
        @(posedge clk);
        #1;
        if(dout != 0)
            errors = errors +1;

        if(errors > 0)
            $display("Simulation Failed!");
        else
            $display("Simulation Succeed!");
        $finish;
    end

endmodule