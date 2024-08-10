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
__EDCOND__,
__IEND__,
__ILA_SO_odata,
__VLG_O_odata,
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
output            __EDCOND__;
output            __IEND__;
output      [7:0] __ILA_SO_odata;
output      [7:0] __VLG_O_odata;
output reg      [4:0] __CYCLE_CNT__;
output reg            __START__;
output reg            __STARTED__;
output reg            __ENDED__;
output reg            __2ndENDED__;
output reg            __RESETED__;
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
wire            clk;
(* keep *) wire            dummy_reset;
wire            rst;
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
top RTL(
    .addr(__VLG_I_addr),
    .clk(clk),
    .data(__VLG_I_data),
    .odata(__VLG_O_odata),
    .ren(__VLG_I_ren),
    .rst(dummy_reset),
    .wen(__VLG_I_wen)
);
endmodule
