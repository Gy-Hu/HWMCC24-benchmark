/* PREHEADER */

`define true  1'b1

`define false 1'b0



/* END OF PREHEADER */
module wrapper(
__ILA_I_addr,
__ILA_I_data,
__ILA_I_ren,
__ILA_I_wen,
__VLG_I_addr,
__VLG_I_data,
__VLG_I_ren,
__VLG_I_wen,
clk,
dummy_reset,
rst,
RTL__DOT__addr,
RTL__DOT__data,
RTL__DOT__odata,
RTL__DOT__ren,
RTL__DOT__wen,
__EDCOND__,
__IEND__,
__ILA_SO_odata,
__VLG_O_odata,
__all_assert_wire__,
__all_assume_wire__,
input_map_assume___p0__,
input_map_assume___p1__,
input_map_assume___p2__,
input_map_assume___p3__,
issue_decode__p4__,
issue_valid__p5__,
noreset__p6__,
variable_map_assert__p8__,
variable_map_assume___p7__,
__CYCLE_CNT__,
__START__,
__STARTED__,
__ENDED__,
__2ndENDED__,
__RESETED__
);
input      [3:0] __ILA_I_addr;
input      [7:0] __ILA_I_data;
input            __ILA_I_ren;
input            __ILA_I_wen;
input      [3:0] __VLG_I_addr;
input      [7:0] __VLG_I_data;
input            __VLG_I_ren;
input            __VLG_I_wen;
input            clk;
input            dummy_reset;
input            rst;
output      [3:0] RTL__DOT__addr;
output      [7:0] RTL__DOT__data;
output      [7:0] RTL__DOT__odata;
output            RTL__DOT__ren;
output            RTL__DOT__wen;
output            __EDCOND__;
output            __IEND__;
output      [7:0] __ILA_SO_odata;
output      [7:0] __VLG_O_odata;
output            __all_assert_wire__;
output            __all_assume_wire__;
output            input_map_assume___p0__;
output            input_map_assume___p1__;
output            input_map_assume___p2__;
output            input_map_assume___p3__;
output            issue_decode__p4__;
output            issue_valid__p5__;
output            noreset__p6__;
output            variable_map_assert__p8__;
output            variable_map_assume___p7__;
output reg      [4:0] __CYCLE_CNT__;
output reg            __START__;
output reg            __STARTED__;
output reg            __ENDED__;
output reg            __2ndENDED__;
output reg            __RESETED__;
(* keep *) wire      [3:0] RTL__DOT__addr;
(* keep *) wire      [7:0] RTL__DOT__data;
(* keep *) wire      [7:0] RTL__DOT__odata;
(* keep *) wire            RTL__DOT__ren;
(* keep *) wire            RTL__DOT__wen;
wire            __2ndIEND__;
(* keep *) wire            __EDCOND__;
(* keep *) wire            __IEND__;
(* keep *) wire      [3:0] __ILA_I_addr;
(* keep *) wire      [7:0] __ILA_I_data;
(* keep *) wire            __ILA_I_ren;
(* keep *) wire            __ILA_I_wen;
(* keep *) wire            __ILA_LargeArray_decode_of_READ__;
(* keep *) wire            __ILA_LargeArray_valid__;
(* keep *) wire      [7:0] __ILA_SO_odata;
(* keep *) wire            __ISSUE__;
(* keep *) wire      [3:0] __VLG_I_addr;
(* keep *) wire      [7:0] __VLG_I_data;
(* keep *) wire            __VLG_I_ren;
(* keep *) wire            __VLG_I_wen;
(* keep *) wire      [7:0] __VLG_O_odata;
(* keep *) wire            __all_assert_wire__;
(* keep *) wire            __all_assume_wire__;
wire            clk;
(* keep *) wire            dummy_reset;
wire            input_map_assume___p0__;
wire            input_map_assume___p1__;
wire            input_map_assume___p2__;
wire            input_map_assume___p3__;
wire            issue_decode__p4__;
wire            issue_valid__p5__;
wire            noreset__p6__;
wire            rst;
wire            variable_map_assert__p8__;
wire            variable_map_assume___p7__;
always @(posedge clk) begin
if (rst) __CYCLE_CNT__ <= 0;
else if ( ( __START__ || __STARTED__ ) &&  __CYCLE_CNT__ < 11) __CYCLE_CNT__ <= __CYCLE_CNT__ + 1;
end
always @(posedge clk) begin
if (rst) __START__ <= 1;
else if (__START__ || __STARTED__) __START__ <= 0;
end
always @(posedge clk) begin
if (rst) __STARTED__ <= 0;
else if (__START__) __STARTED__ <= 1;
end
always @(posedge clk) begin
if (rst) __ENDED__ <= 0;
else if (__IEND__) __ENDED__ <= 1;
end
always @(posedge clk) begin
if (rst) __2ndENDED__ <= 1'b0;
else if (__ENDED__ && __EDCOND__ && ~__2ndENDED__)  __2ndENDED__ <= 1'b1; end
assign __2ndIEND__ = __ENDED__ && __EDCOND__ && ~__2ndENDED__ ;
always @(posedge clk) begin
if (rst) __RESETED__ <= 1;
end
assign __ISSUE__ = 1 ;
LargeArray__DOT__READ ILA (
   .__START__(__START__),
   .addr(__ILA_I_addr),
   .clk(clk),
   .data(__ILA_I_data),
   .ren(__ILA_I_ren),
   .rst(rst),
   .wen(__ILA_I_wen),
   .__ILA_LargeArray_decode_of_READ__(__ILA_LargeArray_decode_of_READ__),
   .__ILA_LargeArray_valid__(__ILA_LargeArray_valid__),
   .odata(__ILA_SO_odata),
   .__COUNTER_start__n2()
);
assign __EDCOND__ = ((__CYCLE_CNT__)==(5'd1))&&(__STARTED__) ;
assign __IEND__ = (((((__CYCLE_CNT__)==(5'd1))&&(__STARTED__))&&(__RESETED__))&&(!(__ENDED__)))&&(1'b1) ;
assign input_map_assume___p0__ = (!(__START__))||((__ILA_I_addr)==(RTL__DOT__addr)) ;
assign input_map_assume___p1__ = (!(__START__))||((__ILA_I_data)==(RTL__DOT__data)) ;
assign input_map_assume___p2__ = (!(__START__))||((__ILA_I_ren)==(RTL__DOT__ren)) ;
assign input_map_assume___p3__ = (!(__START__))||((__ILA_I_wen)==(RTL__DOT__wen)) ;
assign issue_decode__p4__ = (!(__START__))||(__ILA_LargeArray_decode_of_READ__) ;
assign issue_valid__p5__ = (!(__START__))||(__ILA_LargeArray_valid__) ;
assign noreset__p6__ = (!(__RESETED__))||(!(dummy_reset)) ;
assign variable_map_assume___p7__ = (!(__START__))||((__ILA_SO_odata)==(RTL__DOT__odata)) ;
assign variable_map_assert__p8__ = (!(__IEND__))||((__ILA_SO_odata)==(RTL__DOT__odata)) ;
top RTL(
    .RTL__DOT__addr(RTL__DOT__addr),
    .RTL__DOT__data(RTL__DOT__data),
    .RTL__DOT__odata(RTL__DOT__odata),
    .RTL__DOT__ren(RTL__DOT__ren),
    .RTL__DOT__wen(RTL__DOT__wen),
    .addr(__VLG_I_addr),
    .clk(clk),
    .data(__VLG_I_data),
    .odata(__VLG_O_odata),
    .ren(__VLG_I_ren),
    .rst(dummy_reset),
    .wen(__VLG_I_wen)
);
assign __all_assert_wire__ = (variable_map_assert__p8__) ;
normalassert: assert property ( __all_assert_wire__ ); // the only assertion 

assign __all_assume_wire__ = (input_map_assume___p0__)&& (input_map_assume___p1__)&& (input_map_assume___p2__)&& (input_map_assume___p3__)&& (issue_decode__p4__)&& (issue_valid__p5__)&& (noreset__p6__)&& (variable_map_assume___p7__) ;
all_assume: assume property ( __all_assume_wire__ ); // the only sanity assertion 

endmodule
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
module top(input clk, input rst, input [3:0] addr, input[7:0] data,
  input wen, input ren, output [7:0] odata, output wire  RTL__DOT__wen, output wire  RTL__DOT__ren, output wire [7:0] RTL__DOT__odata, output wire [7:0] RTL__DOT__data, output wire [3:0] RTL__DOT__addr);

wire array1_sel = addr[3] == 1'b0;
wire array2_sel = addr[3] == 1'b1;
wire [2:0] subaddr = addr[2:0];
wire[7:0] odata1,odata2;

reg array1_sel_d1;
always @(posedge clk) begin
  array1_sel_d1 <= array1_sel;
end

subarray a1(.clk(clk), .rst(rst), .addr(subaddr), .data(data), .wen(wen&array1_sel), .ren(ren&array1_sel), .odata(odata1));
subarray a2(.clk(clk), .rst(rst), .addr(subaddr), .data(data), .wen(wen&array2_sel), .ren(ren&array2_sel), .odata(odata2));

assign odata = array1_sel_d1 ? odata1 : odata2;

 assign RTL__DOT__addr = addr;
 assign RTL__DOT__data = data;
 assign RTL__DOT__odata = odata;
 assign RTL__DOT__ren = ren;
 assign RTL__DOT__wen = wen;
endmodule

module subarray(input clk, input rst, input [2:0] addr, input[7:0] data,
  input wen, input ren, output reg [7:0] odata);

  reg [7:0] array[0:7];
  
    always @(posedge clk) begin
      if(wen)
        array[addr] <= data;
    end

    always @(posedge clk) begin
      if(ren)
        odata <= array[addr];
    end
  
endmodule
