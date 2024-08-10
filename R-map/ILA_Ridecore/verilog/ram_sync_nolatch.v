`include "constants.vh"
`default_nettype none

// this one has been used in arf
module ram_sync_nolatch_4r2w #(
                               parameter BRAM_ADDR_WIDTH = `ADDR_LEN,
                               parameter BRAM_DATA_WIDTH = `DATA_LEN,
                               parameter DATA_DEPTH      = 32
                               ) 
   (
    input wire                        clk,
    input wire [BRAM_ADDR_WIDTH-1:0]  raddr1,
    input wire [BRAM_ADDR_WIDTH-1:0]  raddr2,
    input wire [BRAM_ADDR_WIDTH-1:0]  raddr3,
    input wire [BRAM_ADDR_WIDTH-1:0]  raddr4,
    output wire [BRAM_DATA_WIDTH-1:0] rdata1,
    output wire [BRAM_DATA_WIDTH-1:0] rdata2,
    output wire [BRAM_DATA_WIDTH-1:0] rdata3,
    output wire [BRAM_DATA_WIDTH-1:0] rdata4,
    input wire [BRAM_ADDR_WIDTH-1:0]  waddr1,
    input wire [BRAM_ADDR_WIDTH-1:0]  waddr2,
    input wire [BRAM_DATA_WIDTH-1:0]  wdata1,
    input wire [BRAM_DATA_WIDTH-1:0]  wdata2,
    input wire                        we1,
    input wire                        we2
    );

   reg [BRAM_DATA_WIDTH-1:0]                                   mem [0:DATA_DEPTH-1];
   
   assign rdata1 = mem[raddr1];
   assign rdata2 = mem[raddr2];
   assign rdata3 = mem[raddr3];
   assign rdata4 = mem[raddr4];
   
   always @ (posedge clk) begin
      if (we1)
        mem[waddr1] <= wdata1;
      if (we2)
        mem[waddr2] <= wdata2;
   end
endmodule // ram_sync_nolatch_4r2w

`default_nettype wire
