module simple_pipe(input wire clk, input wire rst, input wire [3:0] w,
    input wire stall1in, input wire stall2in, input wire stall3in, 
    input wire [3:0] reg_init, 
    output wire [3:0] out);

reg [3:0] stage1;
reg [3:0] stage2;
reg [3:0] stage3;
reg tag0;
reg tag1;
reg tag2;
reg tag3;
reg tag4;



reg wen_stage1, wen_stage2;


wire stage3_ready = ! stall3in; 
wire stage3_valid = wen_stage2;
wire stage3_go = stage3_ready & stage3_valid; 


wire stage2_ready = stall2in ? 1'b0 : (!wen_stage2 ? 1'b1 : stage3_ready );
wire stage2_go    = wen_stage1 & stage2_ready; 

// stall2in wen_stage2  stage3_ready | stage2_ready 
//   1        x          x           |  0           
//   0        0          x           |  1           
//   0        1          0           |  0           
//   0        1          1           |  1           


wire stage1_ready = stall1in ? 1'b0:(!wen_stage1 ? 1'b1 : stage2_ready);
wire stage1_go = 1'b1 & stage1_ready; 





always @(posedge clk) begin
  if(rst) begin
    {tag4,tag3,tag2,tag1,tag0} <= 1;
  end else begin

      tag0 <= stage1_go ? 1'b0 : tag0; 
      tag1 <= stage1_go ? tag0 : ( stage2_go ? 1'b0 : tag1);
      tag2 <= stage2_go ? tag1 : ( stage3_go ? 1'b0 : tag2);
      tag3 <= stage3_go ? tag2 : 1'b0;


        wen_stage1 <= stage1_go ? 1'b1 : ( stage2_go ? 1'b0 : wen_stage1) ;        
        wen_stage2 <= stage2_go ? wen_stage1 : ( stage3_go ? 1'b0 : wen_stage2);

      if(stage1_go)
        stage1 <= 
          wen_stage1 ? stage1 * 2 + 1 : 
          wen_stage2 ? stage2 :
          stage3 ;

      if(stage2_go)
        stage2 <= stage1 * 2 + 1 ;

      if(stage3_go)
        stage3 <= wen_stage2 ? stage2 : stage3;
  end
end

assign out = stage3; 


reg [3:0] reg_v;
always @(posedge clk) begin
  if(rst)
    reg_v <= reg_init;
  else
    reg_v <= reg_v;
end

reg [3:0] reg_v_comp;
always @(posedge clk) begin
    reg_v_comp <= reg_v *2 + 1;
end


wire [3:0] reg_v_mul2_plus1 = reg_v*2+1;

assume property (~(tag2 ) || (reg_v == stage3));
assert property (~(tag3 ) || (reg_v_comp == stage3));


endmodule

