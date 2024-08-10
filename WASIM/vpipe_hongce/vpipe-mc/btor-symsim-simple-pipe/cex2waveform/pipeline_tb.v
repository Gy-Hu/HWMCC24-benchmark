`timescale 1ns/100ps
`include "/home/fwj/vpipe-mc/btor-symsim-simple-pipe/cex2waveform/pipeline.v"




module pipeline_tb;

parameter SYSCLK_PERIOD = 100;

reg SYSCLK;
reg NSYSRESET;
reg SYSEVENT;
reg [7:0] SYSINST;
reg [1:0] DUMMY_R;
reg SYSINST_VALID;
reg SYSSTALLEX;
reg SYSSTALLWB;
wire SYSINST_READY;
wire [7:0] DUMMY_DATA;
wire [7:0] reg0, reg1, reg2, reg3;
wire [1:0] scb0, scb1, scb2, scb3;
reg [7:0] reg_in0, reg_in1, reg_in2, reg_in3;
reg [7:0] regin[3:0];
reg [2:0] scbin[3:0];




initial
begin
    SYSCLK = 1'b1;
    NSYSRESET = 1'b1;
end

/*iverilog */
initial
begin            
    $dumpfile("wave.vcd");        //生成的vcd文件名称
    $dumpvars(0, pipeline_tb);    //tb模块名称
end
/*iverilog */


initial begin
    #(SYSCLK_PERIOD * 1)
        NSYSRESET = 1'b0;
    #(SYSCLK_PERIOD * 1)
        SYSINST = 8'h77;
        SYSINST_VALID = 1'b1;
        SYSSTALLEX = 1'b0;
        SYSSTALLWB = 1'b1;
    #(SYSCLK_PERIOD * 1 )
        SYSINST = 8'h64;
        SYSINST_VALID = 1'b0;
        SYSSTALLEX = 1'b0;
        SYSSTALLWB = 1'b0;
        // DUMMY_R = 2'b00;
    #(SYSCLK_PERIOD * 2 )
        $stop;
end


// initial
// begin
//     #0
//         regin[0] = 8'h64;
//         regin[1] = 8'h64;
//         regin[2] = 8'h64;
//         regin[3] = 8'h64;

//         scbin[0] = 2'h0;
//         scbin[1] = 2'h2;
//         scbin[2] = 2'h0;
//         scbin[3] = 2'h0;
        


//     #(SYSCLK_PERIOD * 1 )
//         NSYSRESET = 1'b0;
//         SYSEVENT = 1'b0;

//     #(SYSCLK_PERIOD * 0.5 )
//         SYSEVENT = 1'b1;
//     #(SYSCLK_PERIOD * 1 )
//         SYSEVENT = 1'b0;
//     #(SYSCLK_PERIOD * 0.5 )
//         NSYSRESET = 1'b0;
//         SYSINST = 8'h77;
//         SYSINST_VALID = 1'b1;
//         SYSSTALLEX = 1'b0;
//         SYSSTALLWB = 1'b1;
//         DUMMY_R = 2'b00;
    
//     #(SYSCLK_PERIOD * 1 )
//         NSYSRESET = 1'b0;
//         SYSINST = 8'h64;
//         SYSINST_VALID = 1'b0;
//         SYSSTALLEX = 1'b0;
//         SYSSTALLWB = 1'b0;
//         DUMMY_R = 2'b00;
//     #(SYSCLK_PERIOD * 2 )
//         $stop;
        
// end

always @(SYSCLK)
    #(SYSCLK_PERIOD / 2.0) SYSCLK <= !SYSCLK;

pipeline_v pipeline_ut0 (
    // Inputs
    .clk(SYSCLK),
    .rst(NSYSRESET),
    .event1(SYSEVENT),
    .inst(SYSINST),
    .inst_valid(SYSINST_VALID),
    .stallex(SYSSTALLEX),
    .stallwb(SYSSTALLWB),
    .dummy_read_rf(DUMMY_R),
    .regin(regin),
    .scbin(scbin),

    // Outputs
    .inst_ready(SYSINST_READY),
    .dummy_rf_data(DUMMY_DATA),
    .regout0(reg0),
    .regout1(reg1),
    .regout2(reg2),
    .regout3(reg3),
    .scbout0(scb0),
    .scbout1(scb1),
    .scbout2(scb2),
    .scbout3(scb3)

    
);

endmodule