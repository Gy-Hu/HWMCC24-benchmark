/* PREHEADER */

`define true  1'b1

`define false 1'b0



/* END OF PREHEADER */
module wrapper(
__ILA_I_inst,
__VLG_I_dummy_read_rf,
__VLG_I_inst,
__VLG_I_inst_valid,
__VLG_I_stallex,
__VLG_I_stallwb,
____auxvar0__recorder_init__,
____auxvar1__recorder_init__,
____auxvar2__recorder_init__,
____auxvar3__recorder_init__,
clk,
dummy_reset,
rst,
RTL__DOT__ex_go,
RTL__DOT__ex_wb_rd,
RTL__DOT__ex_wb_reg_wen,
RTL__DOT__ex_wb_valid,
RTL__DOT__id_ex_rd,
RTL__DOT__id_ex_reg_wen,
RTL__DOT__id_ex_valid,
RTL__DOT__id_go,
RTL__DOT__inst,
RTL__DOT__inst_ready,
RTL__DOT__inst_valid,
RTL__DOT__registers_0_,
RTL__DOT__registers_1_,
RTL__DOT__registers_2_,
RTL__DOT__registers_3_,
RTL__DOT__scoreboard_0_,
RTL__DOT__scoreboard_1_,
RTL__DOT__scoreboard_2_,
RTL__DOT__scoreboard_3_,
RTL__DOT__wb_go,
__EDCOND__,
__IEND__,
__ILA_SO_r0,
__ILA_SO_r1,
__ILA_SO_r2,
__ILA_SO_r3,
__VLG_O_dummy_rf_data,
__VLG_O_inst_ready,
__all_assert_wire__,
__all_assume_wire__,
__sanitycheck_wire__,
additional_mapping_control_assume__p0__,
input_map_assume___p1__,
invariant_assume__p2__,
invariant_assume__p3__,
invariant_assume__p4__,
invariant_assume__p5__,
invariant_assume__p6__,
invariant_assume__p7__,
invariant_assume__p8__,
invariant_assume__p9__,
issue_decode__p10__,
issue_valid__p11__,
noreset__p12__,
post_value_holder__p13__,
post_value_holder__p14__,
post_value_holder__p15__,
post_value_holder__p16__,
post_value_holder_overly_constrained__p25__,
post_value_holder_overly_constrained__p26__,
post_value_holder_overly_constrained__p27__,
post_value_holder_overly_constrained__p28__,
post_value_holder_triggered__p29__,
post_value_holder_triggered__p30__,
post_value_holder_triggered__p31__,
post_value_holder_triggered__p32__,
stage_tracker_ex_wb_iuv_enter_cond,
stage_tracker_ex_wb_iuv_exit_cond,
stage_tracker_id_ex_iuv_enter_cond,
stage_tracker_id_ex_iuv_exit_cond,
stage_tracker_if_id_iuv_enter_cond,
stage_tracker_if_id_iuv_exit_cond,
stage_tracker_wb_iuv_enter_cond,
stage_tracker_wb_iuv_exit_cond,
variable_map_assert__p21__,
variable_map_assert__p22__,
variable_map_assert__p23__,
variable_map_assert__p24__,
variable_map_assume___p17__,
variable_map_assume___p18__,
variable_map_assume___p19__,
variable_map_assume___p20__,
__CYCLE_CNT__,
__START__,
__STARTED__,
__ENDED__,
__2ndENDED__,
__RESETED__,
__auxvar0__recorder,
__auxvar0__recorder_sn_vhold,
__auxvar0__recorder_sn_condmet,
__auxvar1__recorder,
__auxvar1__recorder_sn_vhold,
__auxvar1__recorder_sn_condmet,
__auxvar2__recorder,
__auxvar2__recorder_sn_vhold,
__auxvar2__recorder_sn_condmet,
__auxvar3__recorder,
__auxvar3__recorder_sn_vhold,
__auxvar3__recorder_sn_condmet,
stage_tracker_if_id_iuv,
stage_tracker_id_ex_iuv,
stage_tracker_ex_wb_iuv,
stage_tracker_wb_iuv
);
input      [7:0] __ILA_I_inst;
input      [1:0] __VLG_I_dummy_read_rf;
input      [7:0] __VLG_I_inst;
input            __VLG_I_inst_valid;
input            __VLG_I_stallex;
input            __VLG_I_stallwb;
input      [7:0] ____auxvar0__recorder_init__;
input      [7:0] ____auxvar1__recorder_init__;
input      [7:0] ____auxvar2__recorder_init__;
input      [7:0] ____auxvar3__recorder_init__;
input            clk;
input            dummy_reset;
input            rst;
output            RTL__DOT__ex_go;
output      [1:0] RTL__DOT__ex_wb_rd;
output            RTL__DOT__ex_wb_reg_wen;
output            RTL__DOT__ex_wb_valid;
output      [1:0] RTL__DOT__id_ex_rd;
output            RTL__DOT__id_ex_reg_wen;
output            RTL__DOT__id_ex_valid;
output            RTL__DOT__id_go;
output      [7:0] RTL__DOT__inst;
output            RTL__DOT__inst_ready;
output            RTL__DOT__inst_valid;
output      [7:0] RTL__DOT__registers_0_;
output      [7:0] RTL__DOT__registers_1_;
output      [7:0] RTL__DOT__registers_2_;
output      [7:0] RTL__DOT__registers_3_;
output      [1:0] RTL__DOT__scoreboard_0_;
output      [1:0] RTL__DOT__scoreboard_1_;
output      [1:0] RTL__DOT__scoreboard_2_;
output      [1:0] RTL__DOT__scoreboard_3_;
output            RTL__DOT__wb_go;
output            __EDCOND__;
output            __IEND__;
output      [7:0] __ILA_SO_r0;
output      [7:0] __ILA_SO_r1;
output      [7:0] __ILA_SO_r2;
output      [7:0] __ILA_SO_r3;
output      [7:0] __VLG_O_dummy_rf_data;
output            __VLG_O_inst_ready;
output            __all_assert_wire__;
output            __all_assume_wire__;
output            __sanitycheck_wire__;
output            additional_mapping_control_assume__p0__;
output            input_map_assume___p1__;
output            invariant_assume__p2__;
output            invariant_assume__p3__;
output            invariant_assume__p4__;
output            invariant_assume__p5__;
output            invariant_assume__p6__;
output            invariant_assume__p7__;
output            invariant_assume__p8__;
output            invariant_assume__p9__;
output            issue_decode__p10__;
output            issue_valid__p11__;
output            noreset__p12__;
output            post_value_holder__p13__;
output            post_value_holder__p14__;
output            post_value_holder__p15__;
output            post_value_holder__p16__;
output            post_value_holder_overly_constrained__p25__;
output            post_value_holder_overly_constrained__p26__;
output            post_value_holder_overly_constrained__p27__;
output            post_value_holder_overly_constrained__p28__;
output            post_value_holder_triggered__p29__;
output            post_value_holder_triggered__p30__;
output            post_value_holder_triggered__p31__;
output            post_value_holder_triggered__p32__;
output            stage_tracker_ex_wb_iuv_enter_cond;
output            stage_tracker_ex_wb_iuv_exit_cond;
output            stage_tracker_id_ex_iuv_enter_cond;
output            stage_tracker_id_ex_iuv_exit_cond;
output            stage_tracker_if_id_iuv_enter_cond;
output            stage_tracker_if_id_iuv_exit_cond;
output            stage_tracker_wb_iuv_enter_cond;
output            stage_tracker_wb_iuv_exit_cond;
output            variable_map_assert__p21__;
output            variable_map_assert__p22__;
output            variable_map_assert__p23__;
output            variable_map_assert__p24__;
output            variable_map_assume___p17__;
output            variable_map_assume___p18__;
output            variable_map_assume___p19__;
output            variable_map_assume___p20__;
output reg      [7:0] __CYCLE_CNT__;
output reg            __START__;
output reg            __STARTED__;
output reg            __ENDED__;
output reg            __2ndENDED__;
output reg            __RESETED__;
output reg      [7:0] __auxvar0__recorder;
output reg      [7:0] __auxvar0__recorder_sn_vhold;
output reg            __auxvar0__recorder_sn_condmet;
output reg      [7:0] __auxvar1__recorder;
output reg      [7:0] __auxvar1__recorder_sn_vhold;
output reg            __auxvar1__recorder_sn_condmet;
output reg      [7:0] __auxvar2__recorder;
output reg      [7:0] __auxvar2__recorder_sn_vhold;
output reg            __auxvar2__recorder_sn_condmet;
output reg      [7:0] __auxvar3__recorder;
output reg      [7:0] __auxvar3__recorder_sn_vhold;
output reg            __auxvar3__recorder_sn_condmet;
output reg            stage_tracker_if_id_iuv;
output reg            stage_tracker_id_ex_iuv;
output reg            stage_tracker_ex_wb_iuv;
output reg            stage_tracker_wb_iuv;
(* keep *) wire            RTL__DOT__ex_go;
(* keep *) wire      [1:0] RTL__DOT__ex_wb_rd;
(* keep *) wire            RTL__DOT__ex_wb_reg_wen;
(* keep *) wire            RTL__DOT__ex_wb_valid;
(* keep *) wire      [1:0] RTL__DOT__id_ex_rd;
(* keep *) wire            RTL__DOT__id_ex_reg_wen;
(* keep *) wire            RTL__DOT__id_ex_valid;
(* keep *) wire            RTL__DOT__id_go;
(* keep *) wire      [7:0] RTL__DOT__inst;
(* keep *) wire            RTL__DOT__inst_ready;
(* keep *) wire            RTL__DOT__inst_valid;
(* keep *) wire      [7:0] RTL__DOT__registers_0_;
(* keep *) wire      [7:0] RTL__DOT__registers_1_;
(* keep *) wire      [7:0] RTL__DOT__registers_2_;
(* keep *) wire      [7:0] RTL__DOT__registers_3_;
(* keep *) wire      [1:0] RTL__DOT__scoreboard_0_;
(* keep *) wire      [1:0] RTL__DOT__scoreboard_1_;
(* keep *) wire      [1:0] RTL__DOT__scoreboard_2_;
(* keep *) wire      [1:0] RTL__DOT__scoreboard_3_;
(* keep *) wire            RTL__DOT__wb_go;
wire            __2ndIEND__;
(* keep *) wire            __EDCOND__;
(* keep *) wire            __IEND__;
(* keep *) wire      [7:0] __ILA_I_inst;
(* keep *) wire      [7:0] __ILA_SO_r0;
(* keep *) wire      [7:0] __ILA_SO_r1;
(* keep *) wire      [7:0] __ILA_SO_r2;
(* keep *) wire      [7:0] __ILA_SO_r3;
(* keep *) wire            __ILA_simplePipe_decode_of_NAND__;
(* keep *) wire            __ILA_simplePipe_valid__;
(* keep *) wire            __ISSUE__;
(* keep *) wire      [1:0] __VLG_I_dummy_read_rf;
(* keep *) wire      [7:0] __VLG_I_inst;
(* keep *) wire            __VLG_I_inst_valid;
(* keep *) wire            __VLG_I_stallex;
(* keep *) wire            __VLG_I_stallwb;
(* keep *) wire      [7:0] __VLG_O_dummy_rf_data;
(* keep *) wire            __VLG_O_inst_ready;
wire      [7:0] ____auxvar0__recorder_init__;
wire      [7:0] ____auxvar1__recorder_init__;
wire      [7:0] ____auxvar2__recorder_init__;
wire      [7:0] ____auxvar3__recorder_init__;
(* keep *) wire            __all_assert_wire__;
(* keep *) wire            __all_assume_wire__;
wire            __auxvar0__recorder_sn_cond;
wire      [7:0] __auxvar0__recorder_sn_value;
wire            __auxvar1__recorder_sn_cond;
wire      [7:0] __auxvar1__recorder_sn_value;
wire            __auxvar2__recorder_sn_cond;
wire      [7:0] __auxvar2__recorder_sn_value;
wire            __auxvar3__recorder_sn_cond;
wire      [7:0] __auxvar3__recorder_sn_value;
(* keep *) wire            __sanitycheck_wire__;
wire            additional_mapping_control_assume__p0__;
wire            clk;
(* keep *) wire            dummy_reset;
wire            input_map_assume___p1__;
wire            invariant_assume__p2__;
wire            invariant_assume__p3__;
wire            invariant_assume__p4__;
wire            invariant_assume__p5__;
wire            invariant_assume__p6__;
wire            invariant_assume__p7__;
wire            invariant_assume__p8__;
wire            invariant_assume__p9__;
wire            issue_decode__p10__;
wire            issue_valid__p11__;
wire            noreset__p12__;
wire            post_value_holder__p13__;
wire            post_value_holder__p14__;
wire            post_value_holder__p15__;
wire            post_value_holder__p16__;
wire            post_value_holder_overly_constrained__p25__;
wire            post_value_holder_overly_constrained__p26__;
wire            post_value_holder_overly_constrained__p27__;
wire            post_value_holder_overly_constrained__p28__;
wire            post_value_holder_triggered__p29__;
wire            post_value_holder_triggered__p30__;
wire            post_value_holder_triggered__p31__;
wire            post_value_holder_triggered__p32__;
wire            rst;
(* keep *) wire            stage_tracker_ex_wb_iuv_enter_cond;
(* keep *) wire            stage_tracker_ex_wb_iuv_exit_cond;
(* keep *) wire            stage_tracker_id_ex_iuv_enter_cond;
(* keep *) wire            stage_tracker_id_ex_iuv_exit_cond;
(* keep *) wire            stage_tracker_if_id_iuv_enter_cond;
(* keep *) wire            stage_tracker_if_id_iuv_exit_cond;
(* keep *) wire            stage_tracker_wb_iuv_enter_cond;
(* keep *) wire            stage_tracker_wb_iuv_exit_cond;
wire            variable_map_assert__p21__;
wire            variable_map_assert__p22__;
wire            variable_map_assert__p23__;
wire            variable_map_assert__p24__;
wire            variable_map_assume___p17__;
wire            variable_map_assume___p18__;
wire            variable_map_assume___p19__;
wire            variable_map_assume___p20__;
always @(posedge clk) begin
if (rst) __CYCLE_CNT__ <= 0;
else if ( ( __START__ || __STARTED__ ) &&  __CYCLE_CNT__ < 137) __CYCLE_CNT__ <= __CYCLE_CNT__ + 1;
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
simplePipe__DOT__NAND ILA (
   .__START__(__START__),
   .clk(clk),
   .inst(__ILA_I_inst),
   .rst(rst),
   .__ILA_simplePipe_decode_of_NAND__(__ILA_simplePipe_decode_of_NAND__),
   .__ILA_simplePipe_valid__(__ILA_simplePipe_valid__),
   .r0(__ILA_SO_r0),
   .r1(__ILA_SO_r1),
   .r2(__ILA_SO_r2),
   .r3(__ILA_SO_r3),
   .__COUNTER_start__n3()
);
assign __EDCOND__ = ((stage_tracker_wb_iuv)==(1))&&(__STARTED__) ;
assign __IEND__ = (((((stage_tracker_wb_iuv)==(1))&&(__STARTED__))&&(__RESETED__))&&(!(__ENDED__)))&&(1'b1) ;
assign __auxvar0__recorder_sn_cond = (((stage_tracker_ex_wb_iuv)&&(RTL__DOT__wb_go))&&((__START__)||(__STARTED__)))&&(!(__ENDED__)) ;
assign __auxvar0__recorder_sn_value = RTL__DOT__registers_0_ ;
assign __auxvar1__recorder_sn_cond = (((stage_tracker_ex_wb_iuv)&&(RTL__DOT__wb_go))&&((__START__)||(__STARTED__)))&&(!(__ENDED__)) ;
assign __auxvar1__recorder_sn_value = RTL__DOT__registers_1_ ;
assign __auxvar2__recorder_sn_cond = (((stage_tracker_ex_wb_iuv)&&(RTL__DOT__wb_go))&&((__START__)||(__STARTED__)))&&(!(__ENDED__)) ;
assign __auxvar2__recorder_sn_value = RTL__DOT__registers_2_ ;
assign __auxvar3__recorder_sn_cond = (((stage_tracker_ex_wb_iuv)&&(RTL__DOT__wb_go))&&((__START__)||(__STARTED__)))&&(!(__ENDED__)) ;
assign __auxvar3__recorder_sn_value = RTL__DOT__registers_3_ ;
assign stage_tracker_if_id_iuv_enter_cond = __START__ ;
assign stage_tracker_if_id_iuv_exit_cond = RTL__DOT__id_go ;
assign stage_tracker_id_ex_iuv_enter_cond = (stage_tracker_if_id_iuv)&&(RTL__DOT__id_go) ;
assign stage_tracker_id_ex_iuv_exit_cond = RTL__DOT__ex_go ;
assign stage_tracker_ex_wb_iuv_enter_cond = (stage_tracker_id_ex_iuv)&&(RTL__DOT__ex_go) ;
assign stage_tracker_ex_wb_iuv_exit_cond = RTL__DOT__wb_go ;
assign stage_tracker_wb_iuv_enter_cond = (stage_tracker_ex_wb_iuv)&&(RTL__DOT__wb_go) ;
assign stage_tracker_wb_iuv_exit_cond = 1 ;
assign additional_mapping_control_assume__p0__ = (!(__START__))||((RTL__DOT__inst_ready)&&(RTL__DOT__inst_valid)) ;
assign input_map_assume___p1__ = (!(__START__))||((__ILA_I_inst)==(RTL__DOT__inst)) ;
assign invariant_assume__p2__ = (RTL__DOT__scoreboard_0_[1:1])==(((RTL__DOT__id_ex_valid)&&(RTL__DOT__id_ex_reg_wen))&&((RTL__DOT__id_ex_rd)==(2'd0))) ;
assign invariant_assume__p3__ = (RTL__DOT__scoreboard_0_[0:0])==(((RTL__DOT__ex_wb_valid)&&(RTL__DOT__ex_wb_reg_wen))&&((RTL__DOT__ex_wb_rd)==(2'd0))) ;
assign invariant_assume__p4__ = (RTL__DOT__scoreboard_1_[1:1])==(((RTL__DOT__id_ex_valid)&&(RTL__DOT__id_ex_reg_wen))&&((RTL__DOT__id_ex_rd)==(2'd1))) ;
assign invariant_assume__p5__ = (RTL__DOT__scoreboard_1_[0:0])==(((RTL__DOT__ex_wb_valid)&&(RTL__DOT__ex_wb_reg_wen))&&((RTL__DOT__ex_wb_rd)==(2'd1))) ;
assign invariant_assume__p6__ = (RTL__DOT__scoreboard_2_[1:1])==(((RTL__DOT__id_ex_valid)&&(RTL__DOT__id_ex_reg_wen))&&((RTL__DOT__id_ex_rd)==(2'd2))) ;
assign invariant_assume__p7__ = (RTL__DOT__scoreboard_2_[0:0])==(((RTL__DOT__ex_wb_valid)&&(RTL__DOT__ex_wb_reg_wen))&&((RTL__DOT__ex_wb_rd)==(2'd2))) ;
assign invariant_assume__p8__ = (RTL__DOT__scoreboard_3_[1:1])==(((RTL__DOT__id_ex_valid)&&(RTL__DOT__id_ex_reg_wen))&&((RTL__DOT__id_ex_rd)==(2'd3))) ;
assign invariant_assume__p9__ = (RTL__DOT__scoreboard_3_[0:0])==(((RTL__DOT__ex_wb_valid)&&(RTL__DOT__ex_wb_reg_wen))&&((RTL__DOT__ex_wb_rd)==(2'd3))) ;
assign issue_decode__p10__ = (!(__START__))||(__ILA_simplePipe_decode_of_NAND__) ;
assign issue_valid__p11__ = (!(__START__))||(__ILA_simplePipe_valid__) ;
assign noreset__p12__ = (!(__RESETED__))||(!(dummy_reset)) ;
assign post_value_holder__p13__ = (!((((__START__)||(__STARTED__))&&(!(__auxvar0__recorder_sn_condmet)))&&((stage_tracker_ex_wb_iuv)&&(RTL__DOT__wb_go))))||((__auxvar0__recorder)==(RTL__DOT__registers_0_)) ;
assign post_value_holder__p14__ = (!((((__START__)||(__STARTED__))&&(!(__auxvar1__recorder_sn_condmet)))&&((stage_tracker_ex_wb_iuv)&&(RTL__DOT__wb_go))))||((__auxvar1__recorder)==(RTL__DOT__registers_1_)) ;
assign post_value_holder__p15__ = (!((((__START__)||(__STARTED__))&&(!(__auxvar2__recorder_sn_condmet)))&&((stage_tracker_ex_wb_iuv)&&(RTL__DOT__wb_go))))||((__auxvar2__recorder)==(RTL__DOT__registers_2_)) ;
assign post_value_holder__p16__ = (!((((__START__)||(__STARTED__))&&(!(__auxvar3__recorder_sn_condmet)))&&((stage_tracker_ex_wb_iuv)&&(RTL__DOT__wb_go))))||((__auxvar3__recorder)==(RTL__DOT__registers_3_)) ;
assign variable_map_assume___p17__ = (!(__START__))||(((!(__START__))||((__ILA_SO_r0)==(__auxvar0__recorder)))&&((!((!(__START__))&&(1'b1)))||((__ILA_SO_r0)==(RTL__DOT__registers_0_)))) ;
assign variable_map_assume___p18__ = (!(__START__))||(((!(__START__))||((__ILA_SO_r1)==(__auxvar1__recorder)))&&((!((!(__START__))&&(1'b1)))||((__ILA_SO_r1)==(RTL__DOT__registers_1_)))) ;
assign variable_map_assume___p19__ = (!(__START__))||(((!(__START__))||((__ILA_SO_r2)==(__auxvar2__recorder)))&&((!((!(__START__))&&(1'b1)))||((__ILA_SO_r2)==(RTL__DOT__registers_2_)))) ;
assign variable_map_assume___p20__ = (!(__START__))||(((!(__START__))||((__ILA_SO_r3)==(__auxvar3__recorder)))&&((!((!(__START__))&&(1'b1)))||((__ILA_SO_r3)==(RTL__DOT__registers_3_)))) ;
assign variable_map_assert__p21__ = (!(__IEND__))||(((!(__START__))||((__ILA_SO_r0)==(__auxvar0__recorder)))&&((!((!(__START__))&&(1'b1)))||((__ILA_SO_r0)==(RTL__DOT__registers_0_)))) ;
assign variable_map_assert__p22__ = (!(__IEND__))||(((!(__START__))||((__ILA_SO_r1)==(__auxvar1__recorder)))&&((!((!(__START__))&&(1'b1)))||((__ILA_SO_r1)==(RTL__DOT__registers_1_)))) ;
assign variable_map_assert__p23__ = (!(__IEND__))||(((!(__START__))||((__ILA_SO_r2)==(__auxvar2__recorder)))&&((!((!(__START__))&&(1'b1)))||((__ILA_SO_r2)==(RTL__DOT__registers_2_)))) ;
assign variable_map_assert__p24__ = (!(__IEND__))||(((!(__START__))||((__ILA_SO_r3)==(__auxvar3__recorder)))&&((!((!(__START__))&&(1'b1)))||((__ILA_SO_r3)==(RTL__DOT__registers_3_)))) ;
assign post_value_holder_overly_constrained__p25__ = (!((__auxvar0__recorder_sn_condmet)&&(__auxvar0__recorder_sn_cond)))||((__auxvar0__recorder_sn_value)==(__auxvar0__recorder_sn_vhold)) ;
assign post_value_holder_overly_constrained__p26__ = (!((__auxvar1__recorder_sn_condmet)&&(__auxvar1__recorder_sn_cond)))||((__auxvar1__recorder_sn_value)==(__auxvar1__recorder_sn_vhold)) ;
assign post_value_holder_overly_constrained__p27__ = (!((__auxvar2__recorder_sn_condmet)&&(__auxvar2__recorder_sn_cond)))||((__auxvar2__recorder_sn_value)==(__auxvar2__recorder_sn_vhold)) ;
assign post_value_holder_overly_constrained__p28__ = (!((__auxvar3__recorder_sn_condmet)&&(__auxvar3__recorder_sn_cond)))||((__auxvar3__recorder_sn_value)==(__auxvar3__recorder_sn_vhold)) ;
assign post_value_holder_triggered__p29__ = (!(__IEND__))||((__auxvar0__recorder_sn_condmet)||(__auxvar0__recorder_sn_cond)) ;
assign post_value_holder_triggered__p30__ = (!(__IEND__))||((__auxvar1__recorder_sn_condmet)||(__auxvar1__recorder_sn_cond)) ;
assign post_value_holder_triggered__p31__ = (!(__IEND__))||((__auxvar2__recorder_sn_condmet)||(__auxvar2__recorder_sn_cond)) ;
assign post_value_holder_triggered__p32__ = (!(__IEND__))||((__auxvar3__recorder_sn_condmet)||(__auxvar3__recorder_sn_cond)) ;
pipeline_v RTL(
    .RTL__DOT__ex_go(RTL__DOT__ex_go),
    .RTL__DOT__ex_wb_rd(RTL__DOT__ex_wb_rd),
    .RTL__DOT__ex_wb_reg_wen(RTL__DOT__ex_wb_reg_wen),
    .RTL__DOT__ex_wb_valid(RTL__DOT__ex_wb_valid),
    .RTL__DOT__id_ex_rd(RTL__DOT__id_ex_rd),
    .RTL__DOT__id_ex_reg_wen(RTL__DOT__id_ex_reg_wen),
    .RTL__DOT__id_ex_valid(RTL__DOT__id_ex_valid),
    .RTL__DOT__id_go(RTL__DOT__id_go),
    .RTL__DOT__inst(RTL__DOT__inst),
    .RTL__DOT__inst_ready(RTL__DOT__inst_ready),
    .RTL__DOT__inst_valid(RTL__DOT__inst_valid),
    .RTL__DOT__registers_0_(RTL__DOT__registers_0_),
    .RTL__DOT__registers_1_(RTL__DOT__registers_1_),
    .RTL__DOT__registers_2_(RTL__DOT__registers_2_),
    .RTL__DOT__registers_3_(RTL__DOT__registers_3_),
    .RTL__DOT__scoreboard_0_(RTL__DOT__scoreboard_0_),
    .RTL__DOT__scoreboard_1_(RTL__DOT__scoreboard_1_),
    .RTL__DOT__scoreboard_2_(RTL__DOT__scoreboard_2_),
    .RTL__DOT__scoreboard_3_(RTL__DOT__scoreboard_3_),
    .RTL__DOT__wb_go(RTL__DOT__wb_go),
    .clk(clk),
    .dummy_read_rf(__VLG_I_dummy_read_rf),
    .dummy_rf_data(__VLG_O_dummy_rf_data),
    .inst(__VLG_I_inst),
    .inst_ready(__VLG_O_inst_ready),
    .inst_valid(__VLG_I_inst_valid),
    .rst(dummy_reset),
    .stallex(__VLG_I_stallex),
    .stallwb(__VLG_I_stallwb)
);
assign __all_assert_wire__ = (variable_map_assert__p21__) && (variable_map_assert__p22__) && (variable_map_assert__p23__) && (variable_map_assert__p24__) ;
normalassert: assert property ( __all_assert_wire__ ); // the only assertion 

assign __all_assume_wire__ = (additional_mapping_control_assume__p0__)&& (input_map_assume___p1__)&& (invariant_assume__p2__)&& (invariant_assume__p3__)&& (invariant_assume__p4__)&& (invariant_assume__p5__)&& (invariant_assume__p6__)&& (invariant_assume__p7__)&& (invariant_assume__p8__)&& (invariant_assume__p9__)&& (issue_decode__p10__)&& (issue_valid__p11__)&& (noreset__p12__)&& (post_value_holder__p13__)&& (post_value_holder__p14__)&& (post_value_holder__p15__)&& (post_value_holder__p16__)&& (variable_map_assume___p17__)&& (variable_map_assume___p18__)&& (variable_map_assume___p19__)&& (variable_map_assume___p20__) ;
all_assume: assume property ( __all_assume_wire__ ); // the only sanity assertion 

assign __sanitycheck_wire__ = (post_value_holder_overly_constrained__p25__) && (post_value_holder_overly_constrained__p26__) && (post_value_holder_overly_constrained__p27__) && (post_value_holder_overly_constrained__p28__) && (post_value_holder_triggered__p29__) && (post_value_holder_triggered__p30__) && (post_value_holder_triggered__p31__) && (post_value_holder_triggered__p32__) ;
sanitycheck: assert property ( __sanitycheck_wire__ ); // the only assumption 

always @(posedge clk) begin
   if(rst) begin
       __auxvar0__recorder <= ____auxvar0__recorder_init__;
       __auxvar0__recorder_sn_condmet <= 1'b0;
       __auxvar1__recorder <= ____auxvar1__recorder_init__;
       __auxvar1__recorder_sn_condmet <= 1'b0;
       __auxvar2__recorder <= ____auxvar2__recorder_init__;
       __auxvar2__recorder_sn_condmet <= 1'b0;
       __auxvar3__recorder <= ____auxvar3__recorder_init__;
       __auxvar3__recorder_sn_condmet <= 1'b0;
       stage_tracker_if_id_iuv<= 1'b0;
       stage_tracker_id_ex_iuv<= 1'b0;
       stage_tracker_ex_wb_iuv<= 1'b0;
       stage_tracker_wb_iuv<= 1'b0;
   end
   else if(1) begin
       __auxvar0__recorder <= __auxvar0__recorder;
       if (__auxvar0__recorder_sn_cond ) begin __auxvar0__recorder_sn_condmet <= 1'b1; __auxvar0__recorder_sn_vhold <= __auxvar0__recorder_sn_value; end
       __auxvar1__recorder <= __auxvar1__recorder;
       if (__auxvar1__recorder_sn_cond ) begin __auxvar1__recorder_sn_condmet <= 1'b1; __auxvar1__recorder_sn_vhold <= __auxvar1__recorder_sn_value; end
       __auxvar2__recorder <= __auxvar2__recorder;
       if (__auxvar2__recorder_sn_cond ) begin __auxvar2__recorder_sn_condmet <= 1'b1; __auxvar2__recorder_sn_vhold <= __auxvar2__recorder_sn_value; end
       __auxvar3__recorder <= __auxvar3__recorder;
       if (__auxvar3__recorder_sn_cond ) begin __auxvar3__recorder_sn_condmet <= 1'b1; __auxvar3__recorder_sn_vhold <= __auxvar3__recorder_sn_value; end
       if(stage_tracker_if_id_iuv_enter_cond) begin stage_tracker_if_id_iuv <= 1'b1;
       end
       else if(stage_tracker_if_id_iuv_exit_cond) begin stage_tracker_if_id_iuv <= 1'b0;
       end
       if(stage_tracker_id_ex_iuv_enter_cond) begin stage_tracker_id_ex_iuv <= 1'b1;
       end
       else if(stage_tracker_id_ex_iuv_exit_cond) begin stage_tracker_id_ex_iuv <= 1'b0;
       end
       if(stage_tracker_ex_wb_iuv_enter_cond) begin stage_tracker_ex_wb_iuv <= 1'b1;
       end
       else if(stage_tracker_ex_wb_iuv_exit_cond) begin stage_tracker_ex_wb_iuv <= 1'b0;
       end
       if(stage_tracker_wb_iuv_enter_cond) begin stage_tracker_wb_iuv <= 1'b1;
       end
       else if(stage_tracker_wb_iuv_exit_cond) begin stage_tracker_wb_iuv <= 1'b0;
       end
   end
end
endmodule
module simplePipe__DOT__NAND(
__START__,
clk,
inst,
rst,
__ILA_simplePipe_decode_of_NAND__,
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
output            __ILA_simplePipe_decode_of_NAND__;
output            __ILA_simplePipe_valid__;
output reg      [7:0] r0;
output reg      [7:0] r1;
output reg      [7:0] r2;
output reg      [7:0] r3;
output reg      [7:0] __COUNTER_start__n3;
wire            __ILA_simplePipe_decode_of_NAND__;
wire            __ILA_simplePipe_valid__;
wire            __START__;
wire      [1:0] bv_2_0_n5;
wire      [1:0] bv_2_1_n9;
wire      [1:0] bv_2_2_n11;
wire      [1:0] bv_2_3_n1;
wire            clk;
wire      [7:0] inst;
wire      [1:0] n0;
wire            n10;
wire            n12;
wire      [7:0] n13;
wire      [7:0] n14;
wire      [7:0] n15;
wire      [1:0] n16;
wire            n17;
wire            n18;
wire            n19;
wire            n2;
wire      [7:0] n20;
wire      [7:0] n21;
wire      [7:0] n22;
wire      [7:0] n23;
wire      [7:0] n24;
wire      [7:0] n25;
wire            n26;
wire      [7:0] n27;
wire            n28;
wire      [7:0] n29;
wire            n30;
wire      [7:0] n31;
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
assign bv_2_3_n1 = 2'h3 ;
assign n2 =  ( n0 ) == ( bv_2_3_n1 )  ;
assign __ILA_simplePipe_decode_of_NAND__ = n2 ;
assign n4 = inst[1:0] ;
assign bv_2_0_n5 = 2'h0 ;
assign n6 =  ( n4 ) == ( bv_2_0_n5 )  ;
assign n7 = inst[5:4] ;
assign n8 =  ( n7 ) == ( bv_2_0_n5 )  ;
assign bv_2_1_n9 = 2'h1 ;
assign n10 =  ( n7 ) == ( bv_2_1_n9 )  ;
assign bv_2_2_n11 = 2'h2 ;
assign n12 =  ( n7 ) == ( bv_2_2_n11 )  ;
assign n13 =  ( n12 ) ? ( r2 ) : ( r3 ) ;
assign n14 =  ( n10 ) ? ( r1 ) : ( n13 ) ;
assign n15 =  ( n8 ) ? ( r0 ) : ( n14 ) ;
assign n16 = inst[3:2] ;
assign n17 =  ( n16 ) == ( bv_2_0_n5 )  ;
assign n18 =  ( n16 ) == ( bv_2_1_n9 )  ;
assign n19 =  ( n16 ) == ( bv_2_2_n11 )  ;
assign n20 =  ( n19 ) ? ( r2 ) : ( r3 ) ;
assign n21 =  ( n18 ) ? ( r1 ) : ( n20 ) ;
assign n22 =  ( n17 ) ? ( r0 ) : ( n21 ) ;
assign n23 =  ( n15 ) & ( n22 )  ;
assign n24 = ~ ( n23 ) ;
assign n25 =  ( n6 ) ? ( n24 ) : ( r0 ) ;
assign n26 =  ( n4 ) == ( bv_2_1_n9 )  ;
assign n27 =  ( n26 ) ? ( n24 ) : ( r1 ) ;
assign n28 =  ( n4 ) == ( bv_2_2_n11 )  ;
assign n29 =  ( n28 ) ? ( n24 ) : ( r2 ) ;
assign n30 =  ( n4 ) == ( bv_2_3_n1 )  ;
assign n31 =  ( n30 ) ? ( n24 ) : ( r3 ) ;
always @(posedge clk) begin
   if(rst) begin
       r0 <= r0_randinit ;
       r1 <= r1_randinit ;
       r2 <= r2_randinit ;
       r3 <= r3_randinit ;
       __COUNTER_start__n3 <= 0;
   end
   else if(__START__ && __ILA_simplePipe_valid__) begin
       if ( __ILA_simplePipe_decode_of_NAND__ ) begin 
           __COUNTER_start__n3 <= 1; end
       else if( (__COUNTER_start__n3 >= 1 ) && ( __COUNTER_start__n3 < 255 )) begin
           __COUNTER_start__n3 <= __COUNTER_start__n3 + 1; end
       if (__ILA_simplePipe_decode_of_NAND__) begin
           r0 <= n25 ;
       end
       if (__ILA_simplePipe_decode_of_NAND__) begin
           r1 <= n27 ;
       end
       if (__ILA_simplePipe_decode_of_NAND__) begin
           r2 <= n29 ;
       end
       if (__ILA_simplePipe_decode_of_NAND__) begin
           r3 <= n31 ;
       end
   end
end
endmodule
`default_nettype none

// Hongce Zhang @ Princeton
// A simple pipelined processor
// that can only do add/sub/nop/and
// with only 4 registers
// for simplicity, we even make the instruction part
// as input
// ADD/SUB/AND 2-bit op, 2-bit rs1, 2-bit rs2, 2-bit rd
// SET         2-bit op, 4bit imm 2-bit rd

// -- ID --|-- EX --|-- WB
//    ^          |      |
//    |          |      |
//    -------------------
// forwarding

`define  OP_NOP 2'b00
`define  OP_ADD 2'b01
`define  OP_SET 2'b10
`define  OP_NAND 2'b11

module pipeline_v(
    input wire clk, input wire rst, 
    input wire [7:0] inst, input wire inst_valid, output wire inst_ready,
    input wire stallex, input wire stallwb,
    input wire [1:0] dummy_read_rf, output wire [7:0] dummy_rf_data 
, output wire [7:0] RTL__DOT__inst, output wire [1:0] RTL__DOT__scoreboard_3_, output wire [1:0] RTL__DOT__scoreboard_1_, output wire [1:0] RTL__DOT__scoreboard_0_, output wire  RTL__DOT__wb_go, output wire  RTL__DOT__inst_ready, output wire  RTL__DOT__id_go, output wire [1:0] RTL__DOT__scoreboard_2_, output wire  RTL__DOT__id_ex_valid, output wire  RTL__DOT__ex_wb_reg_wen, output wire [7:0] RTL__DOT__registers_3_, output wire [1:0] RTL__DOT__ex_wb_rd, output wire  RTL__DOT__inst_valid, output wire  RTL__DOT__ex_go, output wire  RTL__DOT__id_ex_reg_wen, output wire  RTL__DOT__ex_wb_valid, output wire [1:0] RTL__DOT__id_ex_rd, output wire [7:0] RTL__DOT__registers_0_, output wire [7:0] RTL__DOT__registers_1_, output wire [7:0] RTL__DOT__registers_2_);

// TODO: finish this
// check invariant
// run inst sim


// main pipeline
reg [7:0] if_id_inst;
// can be removed
reg [7:0] id_ex_inst;
reg [7:0] ex_wb_inst;

reg [7:0] id_ex_operand1;
reg [7:0] id_ex_operand2;
reg [1:0] id_ex_op;
reg [1:0] id_ex_rd;
reg       id_ex_reg_wen;

reg [7:0] ex_wb_val;
reg [1:0] ex_wb_rd;
reg       ex_wb_reg_wen;

reg [7:0] registers[3:0];


// interlocking
// using ready valid signal

wire stallif = 0;
wire if_go;

reg if_id_valid;
wire id_if_ready;
wire id_go;
wire stallid = 0;

reg id_ex_valid;
wire ex_id_ready;
wire ex_go;

reg ex_wb_valid;
wire wb_ex_ready;
wire wb_go;


//
// IF --|-- ID --|-- EX --|-- WB
//          ^         |       |
//          |         |       |
//          -------------------
// forwarding logic

wire [1:0] forwarding_id_wdst;
wire       forwarding_id_wen;
wire [1:0] forwarding_ex_wdst;
wire       forwarding_ex_wen;


// plus ex_go
wire [7:0] ex_forwarding_val;

// plus wb_go
wire [7:0] wb_forwarding_val;

reg [1:0] scoreboard[0:3]; // for reg 0-3

// --------------------------------------
// scoreboard
wire [1:0] scoreboard_nxt[0:3];

assign scoreboard_nxt[0][1] = 
    id_go ? forwarding_id_wen && forwarding_id_wdst == 2'd0 : 
    ex_go ? 1'b0 :  scoreboard[0][1];

assign scoreboard_nxt[0][0] = 
    ex_go ? forwarding_ex_wen && forwarding_ex_wdst == 2'd0 : 
    wb_go ? 1'b0 :  scoreboard[0][0];

assign scoreboard_nxt[1][1] = 
    id_go ? forwarding_id_wen && forwarding_id_wdst == 2'd1 : 
    ex_go ? 1'b0 : scoreboard[1][1];

assign scoreboard_nxt[1][0] = 
    ex_go ? forwarding_ex_wen && forwarding_ex_wdst == 2'd1 : 
    wb_go ? 1'b0 :  scoreboard[1][0];

assign scoreboard_nxt[2][1] = 
    id_go ? forwarding_id_wen && forwarding_id_wdst == 2'd2 : 
    ex_go ? 1'b0 : scoreboard[2][1];

assign scoreboard_nxt[2][0] = 
    ex_go ? forwarding_ex_wen && forwarding_ex_wdst == 2'd2 : 
    wb_go ? 1'b0 : scoreboard[2][0];

assign scoreboard_nxt[3][1] = 
    id_go ? forwarding_id_wen && forwarding_id_wdst == 2'd3 : 
    ex_go ? 1'b0 : scoreboard[3][1];

assign scoreboard_nxt[3][0] = 
    ex_go ? forwarding_ex_wen && forwarding_ex_wdst == 2'd3 : 
    wb_go ? 1'b0 : scoreboard[3][0];

// in reality, this will be generate
always @(posedge clk) begin
    if (rst) begin
        scoreboard[0] <= 0;
        scoreboard[1] <= 0;
        scoreboard[2] <= 0;
        scoreboard[3] <= 0;
    end else begin
        scoreboard[0] <= scoreboard_nxt[0];
        scoreboard[1] <= scoreboard_nxt[1];
        scoreboard[2] <= scoreboard_nxt[2];
        scoreboard[3] <= scoreboard_nxt[3];
    end
end

// --------------------------------------
// IF

assign inst_ready = ~stallif && (id_if_ready || ~if_id_valid);
assign if_go = inst_valid && inst_ready;

always @(posedge clk) begin
    if(rst) begin
        if_id_valid <= 0;
    end
    if(if_go) begin
        if_id_valid <= inst_valid && ~stallif;
        if_id_inst <= inst;
    end else begin
        if(id_go)
            if_id_valid <= 1'b0;
    end
end

// --------------------------------------
// ID

// datapath
wire [1:0] op = if_id_inst[7:6];
wire [1:0] rs1= if_id_inst[5:4];
wire [1:0] rs2= if_id_inst[3:2];
wire [1:0] rd = if_id_inst[1:0];
wire [7:0] immd = {4'd0, if_id_inst[5:2]};
wire id_wen = op == `OP_ADD || op == `OP_SET || op == `OP_NAND;

wire [1:0] rs1_write_loc = scoreboard[rs1];
wire [1:0] rs2_write_loc = scoreboard[rs2];
wire [7:0] rs1_val = registers[rs1];
wire [7:0] rs2_val = registers[rs2];

wire [7:0] id_rs1_val = rs1_write_loc == 2'b00 ? rs1_val :
                        rs1_write_loc == 2'b01 ? wb_forwarding_val :
                        ex_forwarding_val ; // 10/11

wire [7:0] id_rs2_val = rs2_write_loc == 2'b00 ? rs2_val :
                        rs2_write_loc == 2'b01 ? wb_forwarding_val :
                        ex_forwarding_val ; // 10/11

wire [7:0] id_operand1 = op == `OP_SET ? immd : id_rs1_val;
wire [7:0] id_operand2 = id_rs2_val;

// forwarding output
assign forwarding_id_wdst = rd;
assign forwarding_id_wen  = if_id_valid && id_wen;

// control
assign id_if_ready = !stallid && 
    ( ex_id_ready || ( !id_ex_valid ) );
assign id_go = if_id_valid & id_if_ready;


always @(posedge clk) begin
    if(rst) begin
        id_ex_reg_wen <= 1'b0;
        id_ex_valid <= 1'b0;
    end
    else begin
        if(id_go) begin
            id_ex_inst <= if_id_inst;

            id_ex_valid <= if_id_valid & ~stallid;
            id_ex_op <= op;
            id_ex_reg_wen <= id_wen;
            id_ex_rd <= rd;
            id_ex_operand1 <= id_operand1;
            id_ex_operand2 <= id_operand2;
        end else begin
            if(ex_go)
                id_ex_valid <= 1'b0;
        end
    end
end

// --------------------------------------
// EX

// datapath
wire[7:0] ex_alu_result =  id_ex_op == `OP_ADD ? id_ex_operand1 + id_ex_operand2 :
                           id_ex_op == `OP_SET ? id_ex_operand1 :
                           id_ex_op == `OP_NAND ? ~(id_ex_operand1 & id_ex_operand2) :
                                                 8'bxxxxxxxx; // `OP_NOP
assign ex_forwarding_val = ex_alu_result;

assign forwarding_ex_wdst = id_ex_rd;
assign forwarding_ex_wen  = id_ex_valid && id_ex_reg_wen;

// control
assign ex_id_ready = !stallex && 
    ( wb_ex_ready || ( !ex_wb_valid ) );
// stallex  wb_ex_ready  ex_wb_valid    ex_id_ready
//    1          x           x          0
//    0          1           x          1
//    0          0           0          1
//    0          0           1          0

assign ex_go = id_ex_valid && ex_id_ready;


always @(posedge clk) begin
    if (rst) begin
        // reset
        ex_wb_reg_wen <= 1'b0;
        ex_wb_valid   <= 1'b0;
    end
    else begin
        if (ex_go) begin
            ex_wb_inst <= id_ex_inst;
            
            ex_wb_valid <= id_ex_valid && !stallex;
            ex_wb_reg_wen <= id_ex_reg_wen;
            ex_wb_val <= ex_alu_result;
            ex_wb_rd <= id_ex_rd;
        end else begin
            if(wb_go)
                ex_wb_valid <= 1'b0;
        end
    end
end


// --------------------------------------


// WB
assign wb_ex_ready = !stallwb;
assign wb_go = ex_wb_valid && wb_ex_ready;

assign wb_forwarding_val = ex_wb_val;

always @(posedge clk ) begin
   if (wb_go && ex_wb_reg_wen) begin
    registers[ex_wb_rd] <= ex_wb_val;
    end
end

// dummy read
assign dummy_rf_data = registers[dummy_read_rf];


// formal properties
/*
assert property (scoreboard[0][1] == ( id_ex_valid && id_ex_reg_wen && id_ex_rd == 2'd0));
assert property (scoreboard[0][0] == ( ex_wb_valid && ex_wb_reg_wen && ex_wb_rd == 2'd0));

assert property (scoreboard[1][1] == ( id_ex_valid && id_ex_reg_wen && id_ex_rd == 2'd1));
assert property (scoreboard[1][0] == ( ex_wb_valid && ex_wb_reg_wen && ex_wb_rd == 2'd1));

assert property (scoreboard[2][1] == ( id_ex_valid && id_ex_reg_wen && id_ex_rd == 2'd2));
assert property (scoreboard[2][0] == ( ex_wb_valid && ex_wb_reg_wen && ex_wb_rd == 2'd2));

assert property (scoreboard[3][1] == ( id_ex_valid && id_ex_reg_wen && id_ex_rd == 2'd3));
assert property (scoreboard[3][0] == ( ex_wb_valid && ex_wb_reg_wen && ex_wb_rd == 2'd3));
*/
 assign RTL__DOT__registers_2_ = registers[2];
 assign RTL__DOT__registers_1_ = registers[1];
 assign RTL__DOT__registers_0_ = registers[0];
 assign RTL__DOT__id_ex_rd = id_ex_rd;
 assign RTL__DOT__ex_wb_valid = ex_wb_valid;
 assign RTL__DOT__id_ex_reg_wen = id_ex_reg_wen;
 assign RTL__DOT__ex_go = ex_go;
 assign RTL__DOT__inst_valid = inst_valid;
 assign RTL__DOT__ex_wb_rd = ex_wb_rd;
 assign RTL__DOT__registers_3_ = registers[3];
 assign RTL__DOT__ex_wb_reg_wen = ex_wb_reg_wen;
 assign RTL__DOT__id_ex_valid = id_ex_valid;
 assign RTL__DOT__scoreboard_2_ = scoreboard[2];
 assign RTL__DOT__id_go = id_go;
 assign RTL__DOT__inst_ready = inst_ready;
 assign RTL__DOT__wb_go = wb_go;
 assign RTL__DOT__scoreboard_0_ = scoreboard[0];
 assign RTL__DOT__scoreboard_1_ = scoreboard[1];
 assign RTL__DOT__scoreboard_3_ = scoreboard[3];
 assign RTL__DOT__inst = inst;
endmodule
