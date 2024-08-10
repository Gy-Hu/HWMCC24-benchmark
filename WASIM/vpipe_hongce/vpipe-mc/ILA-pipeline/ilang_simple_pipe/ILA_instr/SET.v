module SET(
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
wire      [1:0] bv_2_0_n1;
wire      [1:0] bv_2_1_n6;
wire      [1:0] bv_2_2_n9;
wire      [1:0] bv_2_3_n12;
wire      [7:0] inst;
wire      [1:0] n0;
wire            n10;
wire      [7:0] n11;
wire            n13;
wire      [7:0] n14;
wire            n2;
wire      [3:0] n3;
wire      [7:0] n4;
wire      [7:0] n5;
wire            n7;
wire      [7:0] n8;
wire      [7:0] r0;
wire      [7:0] r0_next;
wire      [7:0] r1;
wire      [7:0] r1_next;
wire      [7:0] r2;
wire      [7:0] r2_next;
wire      [7:0] r3;
wire      [7:0] r3_next;
assign n0 = inst[1:0] ;
assign bv_2_0_n1 = 2'h0 ;
assign n2 =  ( n0 ) == ( bv_2_0_n1 )  ;
assign n3 = inst[5:2] ;
assign n4 =  {4'd0 , n3}  ;
assign n5 =  ( n2 ) ? ( n4 ) : ( r0 ) ;
assign r0_next = n5 ;
assign bv_2_1_n6 = 2'h1 ;
assign n7 =  ( n0 ) == ( bv_2_1_n6 )  ;
assign n8 =  ( n7 ) ? ( n4 ) : ( r1 ) ;
assign r1_next = n8 ;
assign bv_2_2_n9 = 2'h2 ;
assign n10 =  ( n0 ) == ( bv_2_2_n9 )  ;
assign n11 =  ( n10 ) ? ( n4 ) : ( r2 ) ;
assign r2_next = n11 ;
assign bv_2_3_n12 = 2'h3 ;
assign n13 =  ( n0 ) == ( bv_2_3_n12 )  ;
assign n14 =  ( n13 ) ? ( n4 ) : ( r3 ) ;
assign r3_next = n14 ;
endmodule
