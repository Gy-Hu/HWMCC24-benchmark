module test(input wire clk, input wire rst, input wire stage_in,
    output wire [3:0] out);

reg [3:0] stage1;
reg [3:0] stage2;
reg [3:0] stage3;
reg tag0;
reg tag1;
reg tag2;
reg tag3;
reg tag4;


reg wen_stage1, wen_stage2, wen_stage3;


assign wen_stage3 =1'b1; 


always @(posedge clk) begin
  if(rst) begin 
    {tag4,tag3,tag2,tag1,tag0} <= 1;
    stage1 <= stage_in;
  end else begin
        tag0 <= 1'b0; 
        tag1 <= tag0;
        tag2 <= tag1;
        tag3 <= tag2;
        tag4 <= tag3;

        wen_stage1 <= wen_stage3;
        wen_stage2 <= wen_stage1;

        stage1 <= 
          wen_stage1 ? stage1 * 2 + 1 : 

          wen_stage3 ? stage3 : stage3;

        stage2 <= stage1 * 2 + 1 ;
        stage3 <= wen_stage2 ? stage2 : stage3;
  end
end

assign out = stage3;


endmodule