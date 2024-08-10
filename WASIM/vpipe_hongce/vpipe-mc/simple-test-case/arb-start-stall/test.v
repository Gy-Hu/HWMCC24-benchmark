module test(input wire clk, input wire rst, input wire [3:0] w,
    input wire stall1in, input wire stall2in, input wire stall3in, //这里的in是什么意思
    input wire [3:0] reg_init, //这个用来干啥
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

//因为stage3是最后一步，所以不用关心stage2 & 1是否ready
wire stage3_ready = ! stall3in; //当stage3 stall的时候变更stage3的准备状态（没有stall才算准备好了） - 针对stage来说
wire stage3_valid = wen_stage2; //stage2可写的时候（也就是EX执行的时候），告诉stage3接收这条instruction（表示不是bubble） - 针对instruction来说
wire stage3_go = stage3_ready & stage3_valid; //stage3准备好并且instruction有效，可以正常执行stage3

//stage2没有stall的时候，还要看stage3是否ready
wire stage2_ready = stall2in ? 1'b0 : (!wen_stage2 ? 1'b1 : stage3_ready ); //wen_stage2代表这里是否有bubble，0代表有bubble
wire stage2_go    = wen_stage1 & stage2_ready; //当stage1可写并且stage2准备好的时候，可以正常执行stage2（为什么这里不用stage2_valid?）
// go就是把stage1的指令拿过来并且执行
// ready只是关心能不能接收指令，不关心是否有指令进来执行

// stall2in wen_stage2  stage3_ready | stage2_ready //能不能把stage1的指令拿过来（如果有的话）
//   1        x          x           |  0           stage2入口关闭的时候，stage2不可能顺利执行了
//   0        0          x           |  1           stage2入口没有关闭，查看是否存在bubble在stage2，有的话就吃掉bubble
//   0        1          0           |  0           stage2入口没有关闭，没有bubble，因为stage3没有准备好，所以无法顺利执行
//   0        1          1           |  1           stage2入口没有关闭，没有bubble，stage3准备好了，所以可以顺利执行

//wire stage1_ready = stall1in ? 1'b0 : stage2_ready; //当stage1 stall的时候，stage1没准备好，stage1没有stall的时候，stage2准备好了
wire stage1_ready = stall1in ? 1'b0:(!wen_stage1 ? 1'b1 : stage2_ready);
wire stage1_go = 1'b1 & stage1_ready; //当stage1准备好的时候，stage1就可以正常执行


// wire stall3 = stall3in;
// wire stall2 = stall2in ||(stall3); // stall2in || stall3 也就是stage2入口关闭，或者stage3处于stall状态
// wire stall1 = stall1in ||(wen_stage2 & stall2); // stall1in || stall2 也就是stage1入口关闭，或者 stage2可写且stage2处于stall状态



always @(posedge clk) begin
  if(rst) begin
//    stage1 <= 0;
//    stage2 <= 0;
//    stage3 <= w;
//    {wen_stage1, wen_stage2} <= 0;
    {tag4,tag3,tag2,tag1,tag0} <= 1;
  end else begin

      tag0 <= stage1_go ? 1'b0 : tag0; 
      tag1 <= stage1_go ? tag0 : ( stage2_go ? 1'b0 : tag1);
      tag2 <= stage2_go ? tag1 : ( stage3_go ? 1'b0 : tag2);
      tag3 <= stage3_go ? tag2 : 1'b0;


        wen_stage1 <= stage1_go ? 1'b1 : ( stage2_go ? 1'b0 : wen_stage1) ;        
        wen_stage2 <= stage2_go ? wen_stage1 : ( stage3_go ? 1'b0 : wen_stage2);

      if(stage1_go)
        stage1 <= //和直接写等号有啥不同
          wen_stage1 ? stage1 * 2 + 1 : 
          wen_stage2 ? stage2 :
          stage3 ;

      if(stage2_go)
        stage2 <= stage1 * 2 + 1 ;

      if(stage3_go)
        stage3 <= wen_stage2 ? stage2 : stage3;
  end
end

assign out = stage3; //wire和assign感觉很像

/*
assert property (!(tag0 && tag1));
assert property (!(tag1 && tag2));
assert property (!(tag2 && tag3));
assert property (!(tag3 && tag4));

assert property (!(tag1 && ~wen_stage1));
assert property (!(tag2 && ~wen_stage2));
*/

/*
(bvand (bvand (bvand 
  (bvnot (bvand tag1 (bvnot wen_stage1))) 
  (bvnot (bvand tag2 (bvnot wen_stage2)))) 

(bvand (bvand 
  (bvnot (bvand tag0 tag1)) 
  (bvnot (bvand tag1 tag2))) 
(bvand 
  (bvnot (bvand tag2 tag3)) 
  (bvnot (bvand tag3 tag4))))) 
(bvand 
  (bvnot tag4) 
  (bvnot (bvand tag0 tag2))))

*/

reg [3:0] reg_v;
always @(posedge clk) begin
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

endmodule

