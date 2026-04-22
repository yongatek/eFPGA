module bench_53_inout_test_142_outputs (
    input ins,
    output wire [141:0] outs
  );

assign outs = {142{ins}};  
endmodule
