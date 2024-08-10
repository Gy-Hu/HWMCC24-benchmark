module NOP(
inst,
r0,
r1,
r2,
r3,
r0_next,
r1_next,
r2_next,
r3_next
);
input      [7:0] inst;
input      [7:0] r0;
input      [7:0] r1;
input      [7:0] r2;
input      [7:0] r3;
output      [7:0] r0_next;
output      [7:0] r1_next;
output      [7:0] r2_next;
output      [7:0] r3_next;
wire      [7:0] inst;
wire      [7:0] r0;
wire      [7:0] r0_next;
wire      [7:0] r1;
wire      [7:0] r1_next;
wire      [7:0] r2;
wire      [7:0] r2_next;
wire      [7:0] r3;
wire      [7:0] r3_next;
assign r0_next = r0 ;
assign r1_next = r1 ;
assign r2_next = r2 ;
assign r3_next = r3 ;
endmodule
