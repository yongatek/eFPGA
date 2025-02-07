module sfifo (clk, reset, w_en, r_en, data_in, data_out, full, empty);
  input clk, reset;
  input w_en, r_en;
  input [7:0] data_in;
  output [7:0] data_out;
  output full, empty;
  
  reg [7:0] w_ptr, r_ptr;
  
  reg [7:0] mem[255:0];
  
  assign data_out = mem[r_ptr];
  
  always@(posedge clk) begin
    if(reset) begin
        w_ptr <= 0; r_ptr <= 0;
      end 
      else begin
        if(w_en & !full)begin
          mem[w_ptr] <= data_in;
          w_ptr <= w_ptr + 1;
        end
        if(r_en & !empty) begin
          r_ptr <= r_ptr + 1;
        end
    end
  end

  assign full = ((w_ptr+1'b1) == r_ptr);
  assign empty = (w_ptr == r_ptr);
  
	
endmodule
