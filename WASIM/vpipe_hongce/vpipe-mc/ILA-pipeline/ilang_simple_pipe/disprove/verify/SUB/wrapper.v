/* PREHEADER */

`define true  1'b1

`define false 1'b0



/* END OF PREHEADER */
module wrapper(
__ILA_I_inst,
__VLG_I_dummy_read_rf,
__VLG_I_inst,
clk,
dummy_reset,
rst,
RTL__DOT__ex_alu_result,
RTL__DOT__ex_wb_rd,
RTL__DOT__ex_wb_reg_wen,
RTL__DOT__ex_wb_val,
RTL__DOT__id_ex_rd,
RTL__DOT__id_ex_reg_wen,
RTL__DOT__inst,
RTL__DOT__reg_0_w_stage,
RTL__DOT__reg_1_w_stage,
RTL__DOT__reg_2_w_stage,
RTL__DOT__reg_3_w_stage,
RTL__DOT__registers_0_,
RTL__DOT__registers_1_,
RTL__DOT__registers_2_,
RTL__DOT__registers_3_,
__EDCOND__,
__IEND__,
__ILA_SO_r0,
__ILA_SO_r1,
__ILA_SO_r2,
__ILA_SO_r3,
__VLG_O_dummy_rf_data,
__all_assert_wire__,
__all_assume_wire__,
input_map_assume___p0__,
invariant_assume__p10__,
invariant_assume__p11__,
invariant_assume__p12__,
invariant_assume__p13__,
invariant_assume__p14__,
invariant_assume__p15__,
invariant_assume__p16__,
invariant_assume__p1__,
invariant_assume__p2__,
invariant_assume__p3__,
invariant_assume__p4__,
invariant_assume__p5__,
invariant_assume__p6__,
invariant_assume__p7__,
invariant_assume__p8__,
invariant_assume__p9__,
issue_decode__p17__,
issue_valid__p18__,
noreset__p19__,
variable_map_assert__p24__,
variable_map_assert__p25__,
variable_map_assert__p26__,
variable_map_assert__p27__,
variable_map_assume___p20__,
variable_map_assume___p21__,
variable_map_assume___p22__,
variable_map_assume___p23__,
__CYCLE_CNT__,
__START__,
__STARTED__,
__ENDED__,
__2ndENDED__,
__RESETED__
);
input      [7:0] __ILA_I_inst;
input      [1:0] __VLG_I_dummy_read_rf;
input      [7:0] __VLG_I_inst;
input            clk;
input            dummy_reset;
input            rst;
output      [7:0] RTL__DOT__ex_alu_result;
output      [1:0] RTL__DOT__ex_wb_rd;
output            RTL__DOT__ex_wb_reg_wen;
output      [7:0] RTL__DOT__ex_wb_val;
output      [1:0] RTL__DOT__id_ex_rd;
output            RTL__DOT__id_ex_reg_wen;
output      [7:0] RTL__DOT__inst;
output      [1:0] RTL__DOT__reg_0_w_stage;
output      [1:0] RTL__DOT__reg_1_w_stage;
output      [1:0] RTL__DOT__reg_2_w_stage;
output      [1:0] RTL__DOT__reg_3_w_stage;
output      [7:0] RTL__DOT__registers_0_;
output      [7:0] RTL__DOT__registers_1_;
output      [7:0] RTL__DOT__registers_2_;
output      [7:0] RTL__DOT__registers_3_;
output            __EDCOND__;
output            __IEND__;
output      [7:0] __ILA_SO_r0;
output      [7:0] __ILA_SO_r1;
output      [7:0] __ILA_SO_r2;
output      [7:0] __ILA_SO_r3;
output      [7:0] __VLG_O_dummy_rf_data;
output            __all_assert_wire__;
output            __all_assume_wire__;
output            input_map_assume___p0__;
output            invariant_assume__p10__;
output            invariant_assume__p11__;
output            invariant_assume__p12__;
output            invariant_assume__p13__;
output            invariant_assume__p14__;
output            invariant_assume__p15__;
output            invariant_assume__p16__;
output            invariant_assume__p1__;
output            invariant_assume__p2__;
output            invariant_assume__p3__;
output            invariant_assume__p4__;
output            invariant_assume__p5__;
output            invariant_assume__p6__;
output            invariant_assume__p7__;
output            invariant_assume__p8__;
output            invariant_assume__p9__;
output            issue_decode__p17__;
output            issue_valid__p18__;
output            noreset__p19__;
output            variable_map_assert__p24__;
output            variable_map_assert__p25__;
output            variable_map_assert__p26__;
output            variable_map_assert__p27__;
output            variable_map_assume___p20__;
output            variable_map_assume___p21__;
output            variable_map_assume___p22__;
output            variable_map_assume___p23__;
output reg      [4:0] __CYCLE_CNT__;
output reg            __START__;
output reg            __STARTED__;
output reg            __ENDED__;
output reg            __2ndENDED__;
output reg            __RESETED__;
(* keep *) wire      [7:0] RTL__DOT__ex_alu_result;
(* keep *) wire      [1:0] RTL__DOT__ex_wb_rd;
(* keep *) wire            RTL__DOT__ex_wb_reg_wen;
(* keep *) wire      [7:0] RTL__DOT__ex_wb_val;
(* keep *) wire      [1:0] RTL__DOT__id_ex_rd;
(* keep *) wire            RTL__DOT__id_ex_reg_wen;
(* keep *) wire      [7:0] RTL__DOT__inst;
(* keep *) wire      [1:0] RTL__DOT__reg_0_w_stage;
(* keep *) wire      [1:0] RTL__DOT__reg_1_w_stage;
(* keep *) wire      [1:0] RTL__DOT__reg_2_w_stage;
(* keep *) wire      [1:0] RTL__DOT__reg_3_w_stage;
(* keep *) wire      [7:0] RTL__DOT__registers_0_;
(* keep *) wire      [7:0] RTL__DOT__registers_1_;
(* keep *) wire      [7:0] RTL__DOT__registers_2_;
(* keep *) wire      [7:0] RTL__DOT__registers_3_;
wire            __2ndIEND__;
(* keep *) wire            __EDCOND__;
(* keep *) wire            __IEND__;
(* keep *) wire      [7:0] __ILA_I_inst;
(* keep *) wire      [7:0] __ILA_SO_r0;
(* keep *) wire      [7:0] __ILA_SO_r1;
(* keep *) wire      [7:0] __ILA_SO_r2;
(* keep *) wire      [7:0] __ILA_SO_r3;
(* keep *) wire            __ILA_simplePipe_decode_of_SUB__;
(* keep *) wire            __ILA_simplePipe_valid__;
(* keep *) wire            __ISSUE__;
(* keep *) wire      [1:0] __VLG_I_dummy_read_rf;
(* keep *) wire      [7:0] __VLG_I_inst;
(* keep *) wire      [7:0] __VLG_O_dummy_rf_data;
(* keep *) wire            __all_assert_wire__;
(* keep *) wire            __all_assume_wire__;
wire            clk;
(* keep *) wire            dummy_reset;
wire            input_map_assume___p0__;
wire            invariant_assume__p10__;
wire            invariant_assume__p11__;
wire            invariant_assume__p12__;
wire            invariant_assume__p13__;
wire            invariant_assume__p14__;
wire            invariant_assume__p15__;
wire            invariant_assume__p16__;
wire            invariant_assume__p1__;
wire            invariant_assume__p2__;
wire            invariant_assume__p3__;
wire            invariant_assume__p4__;
wire            invariant_assume__p5__;
wire            invariant_assume__p6__;
wire            invariant_assume__p7__;
wire            invariant_assume__p8__;
wire            invariant_assume__p9__;
wire            issue_decode__p17__;
wire            issue_valid__p18__;
wire            noreset__p19__;
wire            rst;
wire            variable_map_assert__p24__;
wire            variable_map_assert__p25__;
wire            variable_map_assert__p26__;
wire            variable_map_assert__p27__;
wire            variable_map_assume___p20__;
wire            variable_map_assume___p21__;
wire            variable_map_assume___p22__;
wire            variable_map_assume___p23__;
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
simplePipe__DOT__SUB ILA (
   .__START__(__START__),
   .clk(clk),
   .inst(__ILA_I_inst),
   .rst(rst),
   .__ILA_simplePipe_decode_of_SUB__(__ILA_simplePipe_decode_of_SUB__),
   .__ILA_simplePipe_valid__(__ILA_simplePipe_valid__),
   .r0(__ILA_SO_r0),
   .r1(__ILA_SO_r1),
   .r2(__ILA_SO_r2),
   .r3(__ILA_SO_r3),
   .__COUNTER_start__n3()
);
assign __EDCOND__ = ((__CYCLE_CNT__)==(5'd1))&&(__STARTED__) ;
assign __IEND__ = (((((__CYCLE_CNT__)==(5'd1))&&(__STARTED__))&&(__RESETED__))&&(!(__ENDED__)))&&(1'b1) ;
assign input_map_assume___p0__ = (!(__START__))||((__ILA_I_inst)==(RTL__DOT__inst)) ;
assign invariant_assume__p1__ = (!((RTL__DOT__reg_0_w_stage)==(2'b00)))||((((RTL__DOT__id_ex_reg_wen)==(0))||((RTL__DOT__id_ex_rd)!=(2'd0)))&&(((RTL__DOT__ex_wb_reg_wen)==(0))||((RTL__DOT__ex_wb_rd)!=(2'd0)))) ;
assign invariant_assume__p2__ = (!((RTL__DOT__reg_1_w_stage)==(2'b00)))||((((RTL__DOT__id_ex_reg_wen)==(0))||((RTL__DOT__id_ex_rd)!=(2'd1)))&&(((RTL__DOT__ex_wb_reg_wen)==(0))||((RTL__DOT__ex_wb_rd)!=(2'd1)))) ;
assign invariant_assume__p3__ = (!((RTL__DOT__reg_2_w_stage)==(2'b00)))||((((RTL__DOT__id_ex_reg_wen)==(0))||((RTL__DOT__id_ex_rd)!=(2'd2)))&&(((RTL__DOT__ex_wb_reg_wen)==(0))||((RTL__DOT__ex_wb_rd)!=(2'd2)))) ;
assign invariant_assume__p4__ = (!((RTL__DOT__reg_3_w_stage)==(2'b00)))||((((RTL__DOT__id_ex_reg_wen)==(0))||((RTL__DOT__id_ex_rd)!=(2'd3)))&&(((RTL__DOT__ex_wb_reg_wen)==(0))||((RTL__DOT__ex_wb_rd)!=(2'd3)))) ;
assign invariant_assume__p5__ = (!((RTL__DOT__reg_0_w_stage)==(2'b10)))||((((RTL__DOT__id_ex_reg_wen)==(1))&&((RTL__DOT__id_ex_rd)==(2'd0)))&&(((RTL__DOT__ex_wb_reg_wen)==(0))||((RTL__DOT__ex_wb_rd)!=(2'd0)))) ;
assign invariant_assume__p6__ = (!((RTL__DOT__reg_1_w_stage)==(2'b10)))||((((RTL__DOT__id_ex_reg_wen)==(1))&&((RTL__DOT__id_ex_rd)==(2'd1)))&&(((RTL__DOT__ex_wb_reg_wen)==(0))||((RTL__DOT__ex_wb_rd)!=(2'd1)))) ;
assign invariant_assume__p7__ = (!((RTL__DOT__reg_2_w_stage)==(2'b10)))||((((RTL__DOT__id_ex_reg_wen)==(1))&&((RTL__DOT__id_ex_rd)==(2'd2)))&&(((RTL__DOT__ex_wb_reg_wen)==(0))||((RTL__DOT__ex_wb_rd)!=(2'd2)))) ;
assign invariant_assume__p8__ = (!((RTL__DOT__reg_3_w_stage)==(2'b10)))||((((RTL__DOT__id_ex_reg_wen)==(1))&&((RTL__DOT__id_ex_rd)==(2'd3)))&&(((RTL__DOT__ex_wb_reg_wen)==(0))||((RTL__DOT__ex_wb_rd)!=(2'd3)))) ;
assign invariant_assume__p9__ = (!((RTL__DOT__reg_0_w_stage)==(2'b11)))||((((RTL__DOT__id_ex_reg_wen)==(1))&&((RTL__DOT__id_ex_rd)==(2'd0)))&&(((RTL__DOT__ex_wb_reg_wen)==(1))&&((RTL__DOT__ex_wb_rd)==(2'd0)))) ;
assign invariant_assume__p10__ = (!((RTL__DOT__reg_1_w_stage)==(2'b11)))||((((RTL__DOT__id_ex_reg_wen)==(1))&&((RTL__DOT__id_ex_rd)==(2'd1)))&&(((RTL__DOT__ex_wb_reg_wen)==(1))&&((RTL__DOT__ex_wb_rd)==(2'd1)))) ;
assign invariant_assume__p11__ = (!((RTL__DOT__reg_2_w_stage)==(2'b11)))||((((RTL__DOT__id_ex_reg_wen)==(1))&&((RTL__DOT__id_ex_rd)==(2'd2)))&&(((RTL__DOT__ex_wb_reg_wen)==(1))&&((RTL__DOT__ex_wb_rd)==(2'd2)))) ;
assign invariant_assume__p12__ = (!((RTL__DOT__reg_3_w_stage)==(2'b11)))||((((RTL__DOT__id_ex_reg_wen)==(1))&&((RTL__DOT__id_ex_rd)==(2'd3)))&&(((RTL__DOT__ex_wb_reg_wen)==(1))&&((RTL__DOT__ex_wb_rd)==(2'd3)))) ;
assign invariant_assume__p13__ = (!((RTL__DOT__reg_0_w_stage)==(2'b01)))||((((RTL__DOT__id_ex_reg_wen)==(0))||((RTL__DOT__id_ex_rd)!=(2'd0)))&&(((RTL__DOT__ex_wb_reg_wen)==(1))&&((RTL__DOT__ex_wb_rd)==(2'd0)))) ;
assign invariant_assume__p14__ = (!((RTL__DOT__reg_1_w_stage)==(2'b01)))||((((RTL__DOT__id_ex_reg_wen)==(0))||((RTL__DOT__id_ex_rd)!=(2'd1)))&&(((RTL__DOT__ex_wb_reg_wen)==(1))&&((RTL__DOT__ex_wb_rd)==(2'd1)))) ;
assign invariant_assume__p15__ = (!((RTL__DOT__reg_2_w_stage)==(2'b01)))||((((RTL__DOT__id_ex_reg_wen)==(0))||((RTL__DOT__id_ex_rd)!=(2'd2)))&&(((RTL__DOT__ex_wb_reg_wen)==(1))&&((RTL__DOT__ex_wb_rd)==(2'd2)))) ;
assign invariant_assume__p16__ = (!((RTL__DOT__reg_3_w_stage)==(2'b01)))||((((RTL__DOT__id_ex_reg_wen)==(0))||((RTL__DOT__id_ex_rd)!=(2'd3)))&&(((RTL__DOT__ex_wb_reg_wen)==(1))&&((RTL__DOT__ex_wb_rd)==(2'd3)))) ;
assign issue_decode__p17__ = (!(__START__))||(__ILA_simplePipe_decode_of_SUB__) ;
assign issue_valid__p18__ = (!(__START__))||(__ILA_simplePipe_valid__) ;
assign noreset__p19__ = (!(__RESETED__))||(!(dummy_reset)) ;
assign variable_map_assume___p20__ = (!(__START__))||(((((!((RTL__DOT__reg_0_w_stage)==(2'b10)))||((RTL__DOT__ex_alu_result)==(__ILA_SO_r0)))&&((!((!((RTL__DOT__reg_0_w_stage)==(2'b10)))&&((RTL__DOT__reg_0_w_stage)==(2'b11))))||((RTL__DOT__ex_alu_result)==(__ILA_SO_r0))))&&((!(((!((RTL__DOT__reg_0_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_0_w_stage)==(2'b10)))&&((RTL__DOT__reg_0_w_stage)==(2'b11)))))&&((RTL__DOT__reg_0_w_stage)==(2'b01))))||((RTL__DOT__ex_wb_val)==(__ILA_SO_r0))))&&((!((((!((RTL__DOT__reg_0_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_0_w_stage)==(2'b10)))&&((RTL__DOT__reg_0_w_stage)==(2'b11)))))&&(!(((!((RTL__DOT__reg_0_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_0_w_stage)==(2'b10)))&&((RTL__DOT__reg_0_w_stage)==(2'b11)))))&&((RTL__DOT__reg_0_w_stage)==(2'b01)))))&&((RTL__DOT__reg_0_w_stage)==(2'b00))))||((RTL__DOT__registers_0_)==(__ILA_SO_r0)))) ;
assign variable_map_assume___p21__ = (!(__START__))||(((((!((RTL__DOT__reg_1_w_stage)==(2'b10)))||((RTL__DOT__ex_alu_result)==(__ILA_SO_r1)))&&((!((!((RTL__DOT__reg_1_w_stage)==(2'b10)))&&((RTL__DOT__reg_1_w_stage)==(2'b11))))||((RTL__DOT__ex_alu_result)==(__ILA_SO_r1))))&&((!(((!((RTL__DOT__reg_1_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_1_w_stage)==(2'b10)))&&((RTL__DOT__reg_1_w_stage)==(2'b11)))))&&((RTL__DOT__reg_1_w_stage)==(2'b01))))||((RTL__DOT__ex_wb_val)==(__ILA_SO_r1))))&&((!((((!((RTL__DOT__reg_1_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_1_w_stage)==(2'b10)))&&((RTL__DOT__reg_1_w_stage)==(2'b11)))))&&(!(((!((RTL__DOT__reg_1_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_1_w_stage)==(2'b10)))&&((RTL__DOT__reg_1_w_stage)==(2'b11)))))&&((RTL__DOT__reg_1_w_stage)==(2'b01)))))&&((RTL__DOT__reg_1_w_stage)==(2'b00))))||((RTL__DOT__registers_1_)==(__ILA_SO_r1)))) ;
assign variable_map_assume___p22__ = (!(__START__))||(((((!((RTL__DOT__reg_2_w_stage)==(2'b10)))||((RTL__DOT__ex_alu_result)==(__ILA_SO_r2)))&&((!((!((RTL__DOT__reg_2_w_stage)==(2'b10)))&&((RTL__DOT__reg_2_w_stage)==(2'b11))))||((RTL__DOT__ex_alu_result)==(__ILA_SO_r2))))&&((!(((!((RTL__DOT__reg_2_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_2_w_stage)==(2'b10)))&&((RTL__DOT__reg_2_w_stage)==(2'b11)))))&&((RTL__DOT__reg_2_w_stage)==(2'b01))))||((RTL__DOT__ex_wb_val)==(__ILA_SO_r2))))&&((!((((!((RTL__DOT__reg_2_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_2_w_stage)==(2'b10)))&&((RTL__DOT__reg_2_w_stage)==(2'b11)))))&&(!(((!((RTL__DOT__reg_2_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_2_w_stage)==(2'b10)))&&((RTL__DOT__reg_2_w_stage)==(2'b11)))))&&((RTL__DOT__reg_2_w_stage)==(2'b01)))))&&((RTL__DOT__reg_2_w_stage)==(2'b00))))||((RTL__DOT__registers_2_)==(__ILA_SO_r2)))) ;
assign variable_map_assume___p23__ = (!(__START__))||(((((!((RTL__DOT__reg_3_w_stage)==(2'b10)))||((__ILA_SO_r3)==(RTL__DOT__ex_alu_result)))&&((!((!((RTL__DOT__reg_3_w_stage)==(2'b10)))&&((RTL__DOT__reg_3_w_stage)==(2'b11))))||((__ILA_SO_r3)==(RTL__DOT__ex_alu_result))))&&((!(((!((RTL__DOT__reg_3_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_3_w_stage)==(2'b10)))&&((RTL__DOT__reg_3_w_stage)==(2'b11)))))&&((RTL__DOT__reg_3_w_stage)==(2'b01))))||((RTL__DOT__ex_wb_val)==(__ILA_SO_r3))))&&((!((((!((RTL__DOT__reg_3_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_3_w_stage)==(2'b10)))&&((RTL__DOT__reg_3_w_stage)==(2'b11)))))&&(!(((!((RTL__DOT__reg_3_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_3_w_stage)==(2'b10)))&&((RTL__DOT__reg_3_w_stage)==(2'b11)))))&&((RTL__DOT__reg_3_w_stage)==(2'b01)))))&&((RTL__DOT__reg_3_w_stage)==(2'b00))))||((RTL__DOT__registers_3_)==(__ILA_SO_r3)))) ;
assign variable_map_assert__p24__ = (!(__IEND__))||(((((!((RTL__DOT__reg_0_w_stage)==(2'b10)))||((RTL__DOT__ex_alu_result)==(__ILA_SO_r0)))&&((!((!((RTL__DOT__reg_0_w_stage)==(2'b10)))&&((RTL__DOT__reg_0_w_stage)==(2'b11))))||((RTL__DOT__ex_alu_result)==(__ILA_SO_r0))))&&((!(((!((RTL__DOT__reg_0_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_0_w_stage)==(2'b10)))&&((RTL__DOT__reg_0_w_stage)==(2'b11)))))&&((RTL__DOT__reg_0_w_stage)==(2'b01))))||((RTL__DOT__ex_wb_val)==(__ILA_SO_r0))))&&((!((((!((RTL__DOT__reg_0_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_0_w_stage)==(2'b10)))&&((RTL__DOT__reg_0_w_stage)==(2'b11)))))&&(!(((!((RTL__DOT__reg_0_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_0_w_stage)==(2'b10)))&&((RTL__DOT__reg_0_w_stage)==(2'b11)))))&&((RTL__DOT__reg_0_w_stage)==(2'b01)))))&&((RTL__DOT__reg_0_w_stage)==(2'b00))))||((RTL__DOT__registers_0_)==(__ILA_SO_r0)))) ;
assign variable_map_assert__p25__ = (!(__IEND__))||(((((!((RTL__DOT__reg_1_w_stage)==(2'b10)))||((RTL__DOT__ex_alu_result)==(__ILA_SO_r1)))&&((!((!((RTL__DOT__reg_1_w_stage)==(2'b10)))&&((RTL__DOT__reg_1_w_stage)==(2'b11))))||((RTL__DOT__ex_alu_result)==(__ILA_SO_r1))))&&((!(((!((RTL__DOT__reg_1_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_1_w_stage)==(2'b10)))&&((RTL__DOT__reg_1_w_stage)==(2'b11)))))&&((RTL__DOT__reg_1_w_stage)==(2'b01))))||((RTL__DOT__ex_wb_val)==(__ILA_SO_r1))))&&((!((((!((RTL__DOT__reg_1_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_1_w_stage)==(2'b10)))&&((RTL__DOT__reg_1_w_stage)==(2'b11)))))&&(!(((!((RTL__DOT__reg_1_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_1_w_stage)==(2'b10)))&&((RTL__DOT__reg_1_w_stage)==(2'b11)))))&&((RTL__DOT__reg_1_w_stage)==(2'b01)))))&&((RTL__DOT__reg_1_w_stage)==(2'b00))))||((RTL__DOT__registers_1_)==(__ILA_SO_r1)))) ;
assign variable_map_assert__p26__ = (!(__IEND__))||(((((!((RTL__DOT__reg_2_w_stage)==(2'b10)))||((RTL__DOT__ex_alu_result)==(__ILA_SO_r2)))&&((!((!((RTL__DOT__reg_2_w_stage)==(2'b10)))&&((RTL__DOT__reg_2_w_stage)==(2'b11))))||((RTL__DOT__ex_alu_result)==(__ILA_SO_r2))))&&((!(((!((RTL__DOT__reg_2_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_2_w_stage)==(2'b10)))&&((RTL__DOT__reg_2_w_stage)==(2'b11)))))&&((RTL__DOT__reg_2_w_stage)==(2'b01))))||((RTL__DOT__ex_wb_val)==(__ILA_SO_r2))))&&((!((((!((RTL__DOT__reg_2_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_2_w_stage)==(2'b10)))&&((RTL__DOT__reg_2_w_stage)==(2'b11)))))&&(!(((!((RTL__DOT__reg_2_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_2_w_stage)==(2'b10)))&&((RTL__DOT__reg_2_w_stage)==(2'b11)))))&&((RTL__DOT__reg_2_w_stage)==(2'b01)))))&&((RTL__DOT__reg_2_w_stage)==(2'b00))))||((RTL__DOT__registers_2_)==(__ILA_SO_r2)))) ;
assign variable_map_assert__p27__ = (!(__IEND__))||(((((!((RTL__DOT__reg_3_w_stage)==(2'b10)))||((__ILA_SO_r3)==(RTL__DOT__ex_alu_result)))&&((!((!((RTL__DOT__reg_3_w_stage)==(2'b10)))&&((RTL__DOT__reg_3_w_stage)==(2'b11))))||((__ILA_SO_r3)==(RTL__DOT__ex_alu_result))))&&((!(((!((RTL__DOT__reg_3_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_3_w_stage)==(2'b10)))&&((RTL__DOT__reg_3_w_stage)==(2'b11)))))&&((RTL__DOT__reg_3_w_stage)==(2'b01))))||((RTL__DOT__ex_wb_val)==(__ILA_SO_r3))))&&((!((((!((RTL__DOT__reg_3_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_3_w_stage)==(2'b10)))&&((RTL__DOT__reg_3_w_stage)==(2'b11)))))&&(!(((!((RTL__DOT__reg_3_w_stage)==(2'b10)))&&(!((!((RTL__DOT__reg_3_w_stage)==(2'b10)))&&((RTL__DOT__reg_3_w_stage)==(2'b11)))))&&((RTL__DOT__reg_3_w_stage)==(2'b01)))))&&((RTL__DOT__reg_3_w_stage)==(2'b00))))||((RTL__DOT__registers_3_)==(__ILA_SO_r3)))) ;
pipeline_v RTL(
    .RTL__DOT__ex_alu_result(RTL__DOT__ex_alu_result),
    .RTL__DOT__ex_wb_rd(RTL__DOT__ex_wb_rd),
    .RTL__DOT__ex_wb_reg_wen(RTL__DOT__ex_wb_reg_wen),
    .RTL__DOT__ex_wb_val(RTL__DOT__ex_wb_val),
    .RTL__DOT__id_ex_rd(RTL__DOT__id_ex_rd),
    .RTL__DOT__id_ex_reg_wen(RTL__DOT__id_ex_reg_wen),
    .RTL__DOT__inst(RTL__DOT__inst),
    .RTL__DOT__reg_0_w_stage(RTL__DOT__reg_0_w_stage),
    .RTL__DOT__reg_1_w_stage(RTL__DOT__reg_1_w_stage),
    .RTL__DOT__reg_2_w_stage(RTL__DOT__reg_2_w_stage),
    .RTL__DOT__reg_3_w_stage(RTL__DOT__reg_3_w_stage),
    .RTL__DOT__registers_0_(RTL__DOT__registers_0_),
    .RTL__DOT__registers_1_(RTL__DOT__registers_1_),
    .RTL__DOT__registers_2_(RTL__DOT__registers_2_),
    .RTL__DOT__registers_3_(RTL__DOT__registers_3_),
    .clk(clk),
    .dummy_read_rf(__VLG_I_dummy_read_rf),
    .dummy_rf_data(__VLG_O_dummy_rf_data),
    .inst(__VLG_I_inst),
    .rst(dummy_reset)
);
assign __all_assert_wire__ = (variable_map_assert__p24__) && (variable_map_assert__p25__) && (variable_map_assert__p26__) && (variable_map_assert__p27__) ;
normalassert: assert property ( __all_assert_wire__ ); // the only assertion 

assign __all_assume_wire__ = (input_map_assume___p0__)&& (invariant_assume__p1__)&& (invariant_assume__p2__)&& (invariant_assume__p3__)&& (invariant_assume__p4__)&& (invariant_assume__p5__)&& (invariant_assume__p6__)&& (invariant_assume__p7__)&& (invariant_assume__p8__)&& (invariant_assume__p9__)&& (invariant_assume__p10__)&& (invariant_assume__p11__)&& (invariant_assume__p12__)&& (invariant_assume__p13__)&& (invariant_assume__p14__)&& (invariant_assume__p15__)&& (invariant_assume__p16__)&& (issue_decode__p17__)&& (issue_valid__p18__)&& (noreset__p19__)&& (variable_map_assume___p20__)&& (variable_map_assume___p21__)&& (variable_map_assume___p22__)&& (variable_map_assume___p23__) ;
all_assume: assume property ( __all_assume_wire__ ); // the only sanity assertion 

endmodule
module simplePipe__DOT__SUB(
__START__,
clk,
inst,
rst,
__ILA_simplePipe_decode_of_SUB__,
__ILA_simplePipe_valid__,
r0,
r1,
r2,
r3,
__COUNTER_start__n3
);
input            __START__;
input            clk;
input      [7:0] inst;
input            rst;
output            __ILA_simplePipe_decode_of_SUB__;
output            __ILA_simplePipe_valid__;
output reg      [7:0] r0;
output reg      [7:0] r1;
output reg      [7:0] r2;
output reg      [7:0] r3;
output reg      [7:0] __COUNTER_start__n3;
wire            __ILA_simplePipe_decode_of_SUB__;
wire            __ILA_simplePipe_valid__;
wire            __START__;
wire      [1:0] bv_2_0_n5;
wire      [1:0] bv_2_1_n9;
wire      [1:0] bv_2_2_n1;
wire      [1:0] bv_2_3_n28;
wire            clk;
wire      [7:0] inst;
wire      [1:0] n0;
wire            n10;
wire            n11;
wire      [7:0] n12;
wire      [7:0] n13;
wire      [7:0] n14;
wire      [1:0] n15;
wire            n16;
wire            n17;
wire            n18;
wire      [7:0] n19;
wire            n2;
wire      [7:0] n20;
wire      [7:0] n21;
wire      [7:0] n22;
wire      [7:0] n23;
wire            n24;
wire      [7:0] n25;
wire            n26;
wire      [7:0] n27;
wire            n29;
wire      [7:0] n30;
wire      [1:0] n4;
wire            n6;
wire      [1:0] n7;
wire            n8;
(* keep *) wire      [7:0] r0_randinit;
(* keep *) wire      [7:0] r1_randinit;
(* keep *) wire      [7:0] r2_randinit;
(* keep *) wire      [7:0] r3_randinit;
wire            rst;
assign __ILA_simplePipe_valid__ = 1'b1 ;
assign n0 = inst[7:6] ;
assign bv_2_2_n1 = 2'h2 ;
assign n2 =  ( n0 ) == ( bv_2_2_n1 )  ;
assign __ILA_simplePipe_decode_of_SUB__ = n2 ;
assign n4 = inst[1:0] ;
assign bv_2_0_n5 = 2'h0 ;
assign n6 =  ( n4 ) == ( bv_2_0_n5 )  ;
assign n7 = inst[5:4] ;
assign n8 =  ( n7 ) == ( bv_2_0_n5 )  ;
assign bv_2_1_n9 = 2'h1 ;
assign n10 =  ( n7 ) == ( bv_2_1_n9 )  ;
assign n11 =  ( n7 ) == ( bv_2_2_n1 )  ;
assign n12 =  ( n11 ) ? ( r2 ) : ( r3 ) ;
assign n13 =  ( n10 ) ? ( r1 ) : ( n12 ) ;
assign n14 =  ( n8 ) ? ( r0 ) : ( n13 ) ;
assign n15 = inst[3:2] ;
assign n16 =  ( n15 ) == ( bv_2_0_n5 )  ;
assign n17 =  ( n15 ) == ( bv_2_1_n9 )  ;
assign n18 =  ( n15 ) == ( bv_2_2_n1 )  ;
assign n19 =  ( n18 ) ? ( r2 ) : ( r3 ) ;
assign n20 =  ( n17 ) ? ( r1 ) : ( n19 ) ;
assign n21 =  ( n16 ) ? ( r0 ) : ( n20 ) ;
assign n22 =  ( n14 ) - ( n21 )  ;
assign n23 =  ( n6 ) ? ( n22 ) : ( r0 ) ;
assign n24 =  ( n4 ) == ( bv_2_1_n9 )  ;
assign n25 =  ( n24 ) ? ( n22 ) : ( r1 ) ;
assign n26 =  ( n4 ) == ( bv_2_2_n1 )  ;
assign n27 =  ( n26 ) ? ( n22 ) : ( r2 ) ;
assign bv_2_3_n28 = 2'h3 ;
assign n29 =  ( n4 ) == ( bv_2_3_n28 )  ;
assign n30 =  ( n29 ) ? ( n22 ) : ( r3 ) ;
always @(posedge clk) begin
   if(rst) begin
       r0 <= r0_randinit ;
       r1 <= r1_randinit ;
       r2 <= r2_randinit ;
       r3 <= r3_randinit ;
       __COUNTER_start__n3 <= 0;
   end
   else if(__START__ && __ILA_simplePipe_valid__) begin
       if ( __ILA_simplePipe_decode_of_SUB__ ) begin 
           __COUNTER_start__n3 <= 1; end
       else if( (__COUNTER_start__n3 >= 1 ) && ( __COUNTER_start__n3 < 255 )) begin
           __COUNTER_start__n3 <= __COUNTER_start__n3 + 1; end
       if (__ILA_simplePipe_decode_of_SUB__) begin
           r0 <= n23 ;
       end
       if (__ILA_simplePipe_decode_of_SUB__) begin
           r1 <= n25 ;
       end
       if (__ILA_simplePipe_decode_of_SUB__) begin
           r2 <= n27 ;
       end
       if (__ILA_simplePipe_decode_of_SUB__) begin
           r3 <= n30 ;
       end
   end
end
endmodule

// Hongce Zhang @ Princeton
// A simple pipelined processor
// that can only do add/sub/nop/and
// with only 4 registers
// for simplicity, we even make the instruction part
// as input
// 2-bit op, 2-bit rs1, 2-bit rs2, 2-bit rd
// -- ID --|-- EX --|-- WB
//    ^          |      |
//    |          |      |
//    -------------------
// forwarding

`define  OP_NOP 2'b00
`define  OP_ADD 2'b01
`define  OP_SUB 2'b10
`define  OP_AND 2'b11

module pipeline_v(input wire clk, input wire rst, input wire [7:0] inst, input wire [1:0] dummy_read_rf, output wire [7:0] dummy_rf_data , output wire [7:0] RTL__DOT__registers_3_, output wire [7:0] RTL__DOT__registers_2_, output wire [7:0] RTL__DOT__registers_1_, output wire [1:0] RTL__DOT__reg_3_w_stage, output wire [1:0] RTL__DOT__reg_2_w_stage, output wire [1:0] RTL__DOT__reg_0_w_stage, output wire [7:0] RTL__DOT__ex_alu_result, output wire  RTL__DOT__id_ex_reg_wen, output wire  RTL__DOT__ex_wb_reg_wen, output wire [1:0] RTL__DOT__reg_1_w_stage, output wire [7:0] RTL__DOT__inst, output wire [1:0] RTL__DOT__ex_wb_rd, output wire [7:0] RTL__DOT__ex_wb_val, output wire [7:0] RTL__DOT__registers_0_, output wire [1:0] RTL__DOT__id_ex_rd);

wire [1:0] op; 
wire [1:0] rs1;
wire [1:0] rs2;
wire [1:0] rd; 
wire id_wen;

// main pipeline
reg [7:0] id_ex_rs1_val;
reg [7:0] id_ex_rs2_val;
reg [1:0] id_ex_op;
reg [1:0] id_ex_rd;
reg       id_ex_reg_wen;

wire[7:0] ex_alu_result;
reg [7:0] ex_wb_val;
reg [1:0] ex_wb_rd;
reg       ex_wb_reg_wen;

reg [7:0] registers[3:0];

// -----------------------------------------------------------
// simple score board : track where are the writes
// -0-0- no where that writes, no fw
// -0-1- fw from WB
// -1-0- fw from EX
// -1-1- fw from EX
reg [1:0] reg_0_w_stage;
reg [1:0] reg_1_w_stage;
reg [1:0] reg_2_w_stage;
reg [1:0] reg_3_w_stage;
wire [1:0] reg_0_w_stage_nxt = {1'b0, reg_0_w_stage[1]};
wire [1:0] reg_1_w_stage_nxt = {1'b0, reg_1_w_stage[1]};// reg_1_w_stage >> 1;
wire [1:0] reg_2_w_stage_nxt = {1'b0, reg_2_w_stage[1]};// reg_2_w_stage >> 1;
wire [1:0] reg_3_w_stage_nxt = {1'b0, reg_3_w_stage[1]};// reg_3_w_stage >> 1;

//-------------------------------------------------------------------
// ID


wire [7:0] id_rs1_val;
wire [7:0] id_rs2_val;

wire [1:0] rs1_stage_info;
wire [1:0] rs2_stage_info;
wire [7:0] rs1_val;
wire [7:0] rs2_val;

//-------------------------------------------------------------------

assign op = inst[7:6];
assign rs1= inst[5:4];
assign rs2= inst[3:2];
assign rd = inst[1:0];
assign id_wen = op == `OP_ADD || op == `OP_SUB || op == `OP_AND;

assign dummy_rf_data =  dummy_read_rf == 0 ? registers[0] : 
                        dummy_read_rf == 1 ? registers[1] : 
                        dummy_read_rf == 2 ? registers[2] : 
                            registers[3];



// -----------------------------------------------------------
// simple score board : track where are the writes
always @(posedge clk) begin
    if (rst) 
        // reset
        reg_0_w_stage <= 2'b0;
    else  begin
        if(id_wen && rd == 0)
            reg_0_w_stage <= reg_0_w_stage_nxt | 2'b10;
        else
            reg_0_w_stage <= reg_0_w_stage_nxt;
    end
end

always @(posedge clk) begin
    if (rst) 
        // reset
        reg_1_w_stage <= 2'b0;
    else  begin
        if(id_wen && rd == 1)
            reg_1_w_stage <= reg_1_w_stage_nxt | 2'b10;
        else
            reg_1_w_stage <= reg_1_w_stage_nxt;
    end
end

always @(posedge clk) begin
    if (rst) 
        // reset
        reg_2_w_stage <= 2'b0;
    else  begin
        if(id_wen && rd == 2)
            reg_2_w_stage <= reg_2_w_stage_nxt | 2'b10;
        else
            reg_2_w_stage <= reg_2_w_stage_nxt;
    end
end

always @(posedge clk) begin
    if (rst) 
        // reset
        reg_3_w_stage <= 2'b0;
    else  begin
        if(id_wen && rd == 3)
            reg_3_w_stage <= reg_3_w_stage_nxt | 2'b10;
        else
            reg_3_w_stage <= reg_3_w_stage_nxt;
    end
end

// -----------------------------------------------------------
// ID
// forwarding

assign rs1_stage_info = rs1 == 2'd0 ? reg_0_w_stage : 
                            rs1 == 2'd1 ? reg_1_w_stage : 
                            rs1 == 2'd2 ? reg_2_w_stage : 
                                       reg_3_w_stage ;

assign rs2_stage_info = rs2 == 2'd0 ? reg_0_w_stage : 
                            rs2 == 2'd1 ? reg_1_w_stage : 
                            rs2 == 2'd2 ? reg_2_w_stage : 
                                       reg_3_w_stage ;


assign rs1_val =        rs1 == 2'd0 ? registers[0] :
                        rs1 == 2'd1 ? registers[1] :
                        rs1 == 2'd2 ? registers[2] :
                            registers[3];
assign rs2_val =    rs2 == 2'd0 ? registers[0] :
                        rs2 == 2'd1 ? registers[1] :
                        rs2 == 2'd2 ? registers[2] :
                            registers[3];

assign id_rs1_val = rs1_stage_info == 2'b00 ? rs1_val :
                    rs1_stage_info == 2'b01 ? ex_wb_val :
                    ex_alu_result ; // 10/11

assign id_rs2_val = rs1_stage_info == 2'b00 ? rs1_val :
                    rs1_stage_info == 2'b01 ? ex_wb_val :
                    ex_alu_result ; // 10/11

always @(posedge clk) begin
    if(rst) begin
        id_ex_reg_wen <= 1'b0;
    end
    else begin
        id_ex_op <= op;
        id_ex_reg_wen <= id_wen;
        id_ex_rd <= rd;
        id_ex_rs1_val <= id_rs1_val;
        id_ex_rs2_val <= id_rs2_val;
    end
end
// EX

assign ex_alu_result =  id_ex_op == `OP_ADD ? id_ex_rs1_val + id_ex_rs2_val :
                        id_ex_op == `OP_SUB ? id_ex_rs1_val - id_ex_rs2_val :
                        id_ex_op == `OP_AND ? id_ex_rs1_val & id_ex_rs2_val :
                        8'bxxxxxxxx;

always @(posedge clk) begin
    if (rst) begin
        // reset
        ex_wb_reg_wen <= 1'b0;
    end
    else begin
        ex_wb_reg_wen <= id_ex_reg_wen;
        ex_wb_val <= ex_alu_result;
        ex_wb_rd <= id_ex_rd;
    end
end


// WB
always @(posedge clk ) begin
    if (ex_wb_reg_wen) begin
        registers[ex_wb_rd] <= ex_wb_val;
    end
end


/*inner_assign_list*/

 assign RTL__DOT__id_ex_rd = id_ex_rd;
 assign RTL__DOT__registers_0_ = registers[0];
 assign RTL__DOT__ex_wb_val = ex_wb_val;
 assign RTL__DOT__ex_wb_rd = ex_wb_rd;
 assign RTL__DOT__inst = inst;
 assign RTL__DOT__reg_1_w_stage = reg_1_w_stage;
 assign RTL__DOT__ex_wb_reg_wen = ex_wb_reg_wen;
 assign RTL__DOT__id_ex_reg_wen = id_ex_reg_wen;
 assign RTL__DOT__ex_alu_result = ex_alu_result;
 assign RTL__DOT__reg_0_w_stage = reg_0_w_stage;
 assign RTL__DOT__reg_2_w_stage = reg_2_w_stage;
 assign RTL__DOT__reg_3_w_stage = reg_3_w_stage;
 assign RTL__DOT__registers_1_ = registers[1];
 assign RTL__DOT__registers_2_ = registers[2];
 assign RTL__DOT__registers_3_ = registers[3];
endmodule
