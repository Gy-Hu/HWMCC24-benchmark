module LargeArray__DOT__READ(
__START__,
addr,
clk,
data,
ren,
rst,
wen,
__ILA_LargeArray_decode_of_READ__,
__ILA_LargeArray_valid__,
odata,
__COUNTER_start__n2
);
input            __START__;
input      [3:0] addr;
input            clk;
input      [7:0] data;
input            ren;
input            rst;
input            wen;
output            __ILA_LargeArray_decode_of_READ__;
output            __ILA_LargeArray_valid__;
output reg      [7:0] odata;
output reg      [7:0] __COUNTER_start__n2;
wire            __ILA_LargeArray_decode_of_READ__;
wire            __ILA_LargeArray_valid__;
wire            __START__;
wire      [3:0] addr;
wire            bv_1_1_n0;
wire            clk;
wire      [7:0] data;
wire            n1;
wire      [7:0] n3;
(* keep *) wire      [7:0] odata_randinit;
wire            ren;
wire            rst;
wire            wen;
(* keep *) reg      [7:0] array[15:0];
assign __ILA_LargeArray_valid__ = 1'b1 ;
assign bv_1_1_n0 = 1'h1 ;
assign n1 =  ( ren ) == ( bv_1_1_n0 )  ;
assign __ILA_LargeArray_decode_of_READ__ = n1 ;
assign n3 =  (  array[addr] )  ;
always @(posedge clk) begin
   if(rst) begin
       odata <= odata_randinit ;
       __COUNTER_start__n2 <= 0;
   end
   else if(__START__ && __ILA_LargeArray_valid__) begin
       if ( __ILA_LargeArray_decode_of_READ__ ) begin 
           __COUNTER_start__n2 <= 1; end
       else if( (__COUNTER_start__n2 >= 1 ) && ( __COUNTER_start__n2 < 255 )) begin
           __COUNTER_start__n2 <= __COUNTER_start__n2 + 1; end
       if (__ILA_LargeArray_decode_of_READ__) begin
           odata <= n3 ;
       end
   end
end
endmodule
