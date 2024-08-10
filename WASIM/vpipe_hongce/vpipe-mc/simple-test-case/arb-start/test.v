module test(input wire clk, input wire rst, input wire [3:0] w,
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


reg wen_stage1, wen_stage2, wen_stage3;

//不是完全的任意状态，而是 “任意可达到的状态” ，这个就是environment invariant
//这部分会加到transition relation里面 （验证指令的assumption）
assume property (wen_stage3 == 1); 
assume property (~(wen_stage2 & ~wen_stage1)); //不可能出现wen_stage2是1，然后wen_stage1是0的情况 （用时序的部分考虑一下）- 这种状态不可达

always @(posedge clk) begin
  if(rst) begin //给一个任意的状态，不给stage一个初始状态
    // stage1 <= 0;
    // stage2 <= 0;
    // stage3 <= w;
    // {wen_stage1, wen_stage2, wen_stage3} <= 1;
    {tag4,tag3,tag2,tag1,tag0} <= 1;
  end else begin
        tag0 <= 1'b0; //注意不要用等号，用等号不可以综合
        tag1 <= tag0;
        tag2 <= tag1;
        tag3 <= tag2;
        tag4 <= tag3;

        wen_stage1 <= wen_stage3;
        wen_stage2 <= wen_stage1;

        stage1 <= 
          wen_stage1 ? stage1 * 2 + 1 : 
        //wen_stage2 ? stage2 :
          wen_stage3 ? stage3 : stage3;

        stage2 <= stage1 * 2 + 1 ;
        stage3 <= wen_stage2 ? stage2 : stage3;
  end
end

assign out = stage3;

reg [3:0] reg_v;
always @(posedge clk) begin
  //reg_v <= reg_init;
  if(rst)
    reg_v <= reg_init;
  else
    reg_v <= reg_v;
end

reg [3:0] reg_v_comp;
always @(posedge clk) begin
  // if((tag2 && !tag3))
    reg_v_comp <= reg_v *2 + 1;
end


wire [3:0] reg_v_mul2_plus1 = reg_v*2+1;

assume property (~(tag2 ) || (reg_v == stage3));
assert property (~(tag3 ) || (reg_v_comp == stage3));
//assert property (!(reg_v == stage2 && wen_stage2 && reg_v!=stage1));
//assert property (!(tag1 && !wen_stage1));
//assert property (!(tag2 && !wen_stage2));
//assert property (wen_stage3);
//assert property (! ( tag2 && !tag3 && stage2 != reg_v_mul2_plus1) );

// argument ts
// flag=0 |-> stage2.next == .. && stage3.next == .. && ..

endmodule

