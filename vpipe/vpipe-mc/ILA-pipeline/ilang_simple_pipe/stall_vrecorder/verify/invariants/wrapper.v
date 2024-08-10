/* PREHEADER */

`define true  1'b1

`define false 1'b0



/* END OF PREHEADER */
module wrapper(
__ILA_I_inst,
__STARTED__,
__START__,
__VLG_I_dummy_read_rf,
__VLG_I_inst,
__VLG_I_inst_valid,
__VLG_I_stallex,
__VLG_I_stallwb,
clk,
rst,
RTL__DOT__ex_wb_rd,
RTL__DOT__ex_wb_reg_wen,
RTL__DOT__ex_wb_valid,
RTL__DOT__id_ex_rd,
RTL__DOT__id_ex_reg_wen,
RTL__DOT__id_ex_valid,
RTL__DOT__scoreboard_0_,
RTL__DOT__scoreboard_1_,
RTL__DOT__scoreboard_2_,
RTL__DOT__scoreboard_3_,
__ILA_SO_r0,
__ILA_SO_r1,
__ILA_SO_r2,
__ILA_SO_r3,
__VLG_O_dummy_rf_data,
__VLG_O_inst_ready,
__all_assert_wire__,
invariant_assert__p0__,
invariant_assert__p1__,
invariant_assert__p2__,
invariant_assert__p3__,
invariant_assert__p4__,
invariant_assert__p5__,
invariant_assert__p6__,
invariant_assert__p7__
);
input      [7:0] __ILA_I_inst;
input            __STARTED__;
input            __START__;
input      [1:0] __VLG_I_dummy_read_rf;
input      [7:0] __VLG_I_inst;
input            __VLG_I_inst_valid;
input            __VLG_I_stallex;
input            __VLG_I_stallwb;
input            clk;
input            rst;
output      [1:0] RTL__DOT__ex_wb_rd;
output            RTL__DOT__ex_wb_reg_wen;
output            RTL__DOT__ex_wb_valid;
output      [1:0] RTL__DOT__id_ex_rd;
output            RTL__DOT__id_ex_reg_wen;
output            RTL__DOT__id_ex_valid;
output      [1:0] RTL__DOT__scoreboard_0_;
output      [1:0] RTL__DOT__scoreboard_1_;
output      [1:0] RTL__DOT__scoreboard_2_;
output      [1:0] RTL__DOT__scoreboard_3_;
output      [7:0] __ILA_SO_r0;
output      [7:0] __ILA_SO_r1;
output      [7:0] __ILA_SO_r2;
output      [7:0] __ILA_SO_r3;
output      [7:0] __VLG_O_dummy_rf_data;
output            __VLG_O_inst_ready;
output            __all_assert_wire__;
output            invariant_assert__p0__;
output            invariant_assert__p1__;
output            invariant_assert__p2__;
output            invariant_assert__p3__;
output            invariant_assert__p4__;
output            invariant_assert__p5__;
output            invariant_assert__p6__;
output            invariant_assert__p7__;
(* keep *) wire      [1:0] RTL__DOT__ex_wb_rd;
(* keep *) wire            RTL__DOT__ex_wb_reg_wen;
(* keep *) wire            RTL__DOT__ex_wb_valid;
(* keep *) wire      [1:0] RTL__DOT__id_ex_rd;
(* keep *) wire            RTL__DOT__id_ex_reg_wen;
(* keep *) wire            RTL__DOT__id_ex_valid;
(* keep *) wire      [1:0] RTL__DOT__scoreboard_0_;
(* keep *) wire      [1:0] RTL__DOT__scoreboard_1_;
(* keep *) wire      [1:0] RTL__DOT__scoreboard_2_;
(* keep *) wire      [1:0] RTL__DOT__scoreboard_3_;
(* keep *) wire      [7:0] __ILA_I_inst;
(* keep *) wire      [7:0] __ILA_SO_r0;
(* keep *) wire      [7:0] __ILA_SO_r1;
(* keep *) wire      [7:0] __ILA_SO_r2;
(* keep *) wire      [7:0] __ILA_SO_r3;
(* keep *) wire      [1:0] __VLG_I_dummy_read_rf;
(* keep *) wire      [7:0] __VLG_I_inst;
(* keep *) wire            __VLG_I_inst_valid;
(* keep *) wire            __VLG_I_stallex;
(* keep *) wire            __VLG_I_stallwb;
(* keep *) wire      [7:0] __VLG_O_dummy_rf_data;
(* keep *) wire            __VLG_O_inst_ready;
(* keep *) wire            __all_assert_wire__;
wire            clk;
wire            invariant_assert__p0__;
wire            invariant_assert__p1__;
wire            invariant_assert__p2__;
wire            invariant_assert__p3__;
wire            invariant_assert__p4__;
wire            invariant_assert__p5__;
wire            invariant_assert__p6__;
wire            invariant_assert__p7__;
wire            rst;
assign invariant_assert__p0__ = (RTL__DOT__scoreboard_0_[1:1])==(((RTL__DOT__id_ex_valid)&&(RTL__DOT__id_ex_reg_wen))&&((RTL__DOT__id_ex_rd)==(2'd0))) ;
assign invariant_assert__p1__ = (RTL__DOT__scoreboard_0_[0:0])==(((RTL__DOT__ex_wb_valid)&&(RTL__DOT__ex_wb_reg_wen))&&((RTL__DOT__ex_wb_rd)==(2'd0))) ;
assign invariant_assert__p2__ = (RTL__DOT__scoreboard_1_[1:1])==(((RTL__DOT__id_ex_valid)&&(RTL__DOT__id_ex_reg_wen))&&((RTL__DOT__id_ex_rd)==(2'd1))) ;
assign invariant_assert__p3__ = (RTL__DOT__scoreboard_1_[0:0])==(((RTL__DOT__ex_wb_valid)&&(RTL__DOT__ex_wb_reg_wen))&&((RTL__DOT__ex_wb_rd)==(2'd1))) ;
assign invariant_assert__p4__ = (RTL__DOT__scoreboard_2_[1:1])==(((RTL__DOT__id_ex_valid)&&(RTL__DOT__id_ex_reg_wen))&&((RTL__DOT__id_ex_rd)==(2'd2))) ;
assign invariant_assert__p5__ = (RTL__DOT__scoreboard_2_[0:0])==(((RTL__DOT__ex_wb_valid)&&(RTL__DOT__ex_wb_reg_wen))&&((RTL__DOT__ex_wb_rd)==(2'd2))) ;
assign invariant_assert__p6__ = (RTL__DOT__scoreboard_3_[1:1])==(((RTL__DOT__id_ex_valid)&&(RTL__DOT__id_ex_reg_wen))&&((RTL__DOT__id_ex_rd)==(2'd3))) ;
assign invariant_assert__p7__ = (RTL__DOT__scoreboard_3_[0:0])==(((RTL__DOT__ex_wb_valid)&&(RTL__DOT__ex_wb_reg_wen))&&((RTL__DOT__ex_wb_rd)==(2'd3))) ;
pipeline_v RTL(
    .RTL__DOT__ex_wb_rd(RTL__DOT__ex_wb_rd),
    .RTL__DOT__ex_wb_reg_wen(RTL__DOT__ex_wb_reg_wen),
    .RTL__DOT__ex_wb_valid(RTL__DOT__ex_wb_valid),
    .RTL__DOT__id_ex_rd(RTL__DOT__id_ex_rd),
    .RTL__DOT__id_ex_reg_wen(RTL__DOT__id_ex_reg_wen),
    .RTL__DOT__id_ex_valid(RTL__DOT__id_ex_valid),
    .RTL__DOT__scoreboard_0_(RTL__DOT__scoreboard_0_),
    .RTL__DOT__scoreboard_1_(RTL__DOT__scoreboard_1_),
    .RTL__DOT__scoreboard_2_(RTL__DOT__scoreboard_2_),
    .RTL__DOT__scoreboard_3_(RTL__DOT__scoreboard_3_),
    .clk(clk),
    .dummy_read_rf(__VLG_I_dummy_read_rf),
    .dummy_rf_data(__VLG_O_dummy_rf_data),
    .inst(__VLG_I_inst),
    .inst_ready(__VLG_O_inst_ready),
    .inst_valid(__VLG_I_inst_valid),
    .rst(rst),
    .stallex(__VLG_I_stallex),
    .stallwb(__VLG_I_stallwb)
);
assign __all_assert_wire__ = (invariant_assert__p0__) && (invariant_assert__p1__) && (invariant_assert__p2__) && (invariant_assert__p3__) && (invariant_assert__p4__) && (invariant_assert__p5__) && (invariant_assert__p6__) && (invariant_assert__p7__) ;
normalassert: assert property ( __all_assert_wire__ ); // the only assertion 

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
, output wire [1:0] RTL__DOT__scoreboard_3_, output wire [1:0] RTL__DOT__scoreboard_1_, output wire [1:0] RTL__DOT__scoreboard_0_, output wire [1:0] RTL__DOT__ex_wb_rd, output wire  RTL__DOT__ex_wb_reg_wen, output wire  RTL__DOT__id_ex_reg_wen, output wire  RTL__DOT__ex_wb_valid, output wire [1:0] RTL__DOT__id_ex_rd, output wire [1:0] RTL__DOT__scoreboard_2_, output wire  RTL__DOT__id_ex_valid);

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
 assign RTL__DOT__id_ex_valid = id_ex_valid;
 assign RTL__DOT__scoreboard_2_ = scoreboard[2];
 assign RTL__DOT__id_ex_rd = id_ex_rd;
 assign RTL__DOT__ex_wb_valid = ex_wb_valid;
 assign RTL__DOT__id_ex_reg_wen = id_ex_reg_wen;
 assign RTL__DOT__ex_wb_reg_wen = ex_wb_reg_wen;
 assign RTL__DOT__ex_wb_rd = ex_wb_rd;
 assign RTL__DOT__scoreboard_0_ = scoreboard[0];
 assign RTL__DOT__scoreboard_1_ = scoreboard[1];
 assign RTL__DOT__scoreboard_3_ = scoreboard[3];
endmodule
