module ADD(
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
wire      [1:0] bv_2_1_n5;
wire      [1:0] bv_2_2_n7;
wire      [1:0] bv_2_3_n25;
wire      [7:0] inst;
wire      [1:0] n0;
wire      [7:0] n10;
wire      [7:0] n11;
wire      [1:0] n12;
wire            n13;
wire            n14;
wire            n15;
wire      [7:0] n16;
wire      [7:0] n17;
wire      [7:0] n18;
wire      [7:0] n19;
wire            n2;
wire      [7:0] n20;
wire            n21;
wire      [7:0] n22;
wire            n23;
wire      [7:0] n24;
wire            n26;
wire      [7:0] n27;
wire      [1:0] n3;
wire            n4;
wire            n6;
wire            n8;
wire      [7:0] n9;
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
assign n3 = inst[5:4] ;
assign n4 =  ( n3 ) == ( bv_2_0_n1 )  ;
assign bv_2_1_n5 = 2'h1 ;
assign n6 =  ( n3 ) == ( bv_2_1_n5 )  ;
assign bv_2_2_n7 = 2'h2 ;
assign n8 =  ( n3 ) == ( bv_2_2_n7 )  ;
assign n9 =  ( n8 ) ? ( r2 ) : ( r3 ) ;
assign n10 =  ( n6 ) ? ( r1 ) : ( n9 ) ;
assign n11 =  ( n4 ) ? ( r0 ) : ( n10 ) ;
assign n12 = inst[3:2] ;
assign n13 =  ( n12 ) == ( bv_2_0_n1 )  ;
assign n14 =  ( n12 ) == ( bv_2_1_n5 )  ;
assign n15 =  ( n12 ) == ( bv_2_2_n7 )  ;
assign n16 =  ( n15 ) ? ( r2 ) : ( r3 ) ;
assign n17 =  ( n14 ) ? ( r1 ) : ( n16 ) ;
assign n18 =  ( n13 ) ? ( r0 ) : ( n17 ) ;
assign n19 =  ( n11 ) + ( n18 )  ;
assign n20 =  ( n2 ) ? ( n19 ) : ( r0 ) ;
assign r0_next = n20 ;
assign n21 =  ( n0 ) == ( bv_2_1_n5 )  ;
assign n22 =  ( n21 ) ? ( n19 ) : ( r1 ) ;
assign r1_next = n22 ;
assign n23 =  ( n0 ) == ( bv_2_2_n7 )  ;
assign n24 =  ( n23 ) ? ( n19 ) : ( r2 ) ;
assign r2_next = n24 ;
assign bv_2_3_n25 = 2'h3 ;
assign n26 =  ( n0 ) == ( bv_2_3_n25 )  ;
assign n27 =  ( n26 ) ? ( n19 ) : ( r3 ) ;
assign r3_next = n27 ;
endmodule
