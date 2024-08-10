module test(input wire clk, input wire rst, input wire [3:0] w,
    //input wire stall1in, input wire stall2in, input wire stall3in,
    input wire [3:0] reg_init,
    output wire [3:0] out);

reg [3:0] stage1; //读取reg,相当于ID = instruction decode,还有forwarding
reg [3:0] stage2; //做真正（*2+1）的运算，相当于EX = execution
reg [3:0] stage3; //视作reg, （*2+1），存储结果，相当于WB = write back
//tag用来追踪某条instruction
reg tag0;
reg tag1;
reg tag2;
reg tag3;
reg tag4;

//没有用到
// wire stall3 = stall3in; 
// wire stall2 = stall2in || stall3;
// wire stall1 = stall1in || stall2;

reg wen_stage1, wen_stage2, wen_stage3; //wen = write enable , 0 - 不能写， 1 - 能写

always @(posedge clk) begin
  if(rst) begin
    stage1 <= 0;
    stage2 <= 0;
    stage3 <= w; //初始值不确定
    {tag4,tag3,tag2,tag1,tag0} <= 1; //视作 <0,0,0,0,1>
    {wen_stage1, wen_stage2, wen_stage3} <= 1; //视作 <0,0,1>
  end else begin
        //1在每个周期都向左移动一位，跟踪instruction用的标志
        tag0 <= 1'b0;
        tag1 <= tag0;
        tag2 <= tag1;
        tag3 <= tag2;
        tag4 <= tag3;

        //这部分是同时执行，不要想成C一样的顺序执行

        wen_stage1 <= wen_stage3; //使stage 1有效
        wen_stage2 <= wen_stage1; //下个周期，使stage 2有效

        //cycle1
        stage1 <= //把stage3的结果赋值给stage1
          wen_stage1 ? stage1 * 2 + 1 :  // cycle 2的故事
          // wen_stage2 ? stage2 :
          wen_stage3 ? stage3 : stage3; //cycle 1的故事

        //cycle2
        stage2 <= stage1 * 2 + 1 ; //相当于把初始值w（未知）*2+1 
        //cycle3
        stage3 <= wen_stage2 ? stage2 : stage3; //如果能写就写stage2，不能就保持。相当于把w做运算以后存储在stage3里面
  end
end

assign out = stage3;

//辅助变量reg_v，类似value holder 
reg [3:0] reg_v;
always @(posedge clk) begin
  if(rst)
    reg_v <= reg_init; //初始值不确定，这个是一个input的值
  else
    reg_v <= reg_v; //不reset就一直不变
end

//reg_v加个运算
reg [3:0] reg_v_comp;
always @(posedge clk) begin
  // if((tag2 && !tag3))
    reg_v_comp <= reg_v *2 + 1;
end

//实际上想写stage3@tag2 *2 +1（上一个cycle的stage 3 *2+1是不是等于这个cycle的stage 3的值)
assume property (~(tag2) || (reg_v == stage3)); //引入辅助变量，假设辅助变量和上一个cycle的stage 3相等
assert property (~(tag3) || (reg_v_comp == stage3)); //假设上一条相等，我们看一下下一个cycle是不是相等
//当tag3成立的时候，后面reg_v_comp和stage3相等
//这个property assertion是可以用ILAng自动生成（这里是手写）

endmodule

//transition relation (这部分就是把verilog convert to transition function)
// TRANS:
// (let (($e1 (bvadd #b0001 (bvmul stage1 #b0010)))) 
// (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand 
// (bvand (bvnot (bvand tag2 (bvnot (ite (= stage3 reg_v) #b1 #b0)))) 
//        (bvnot (bvand tag2.next (bvnot (ite (= stage3.next reg_v.next) #b1 #b0))))) 
//                                       (ite (= stage3.next (ite (= #b1 rst) w (ite (= #b1 wen_stage2) stage2 stage3))) #b1 #b0)) 
//                                  (ite (= tag3.next (bvand (bvnot rst) tag2)) #b1 #b0)) 
//                                  (ite (= reg_v_comp.next (bvadd (bvmul reg_v #b0010) #b0001)) #b1 #b0)) 
//                                  (ite (= tag2.next (bvand (bvnot rst) tag1)) #b1 #b0)) 
//                                  (ite (= reg_v.next (ite (= #b1 rst) ((_ extract 3 0) reg_init) reg_v)) #b1 #b0)) 
//                                  (ite (= stage1.next (ite (= #b1 rst) #b0000 (ite (= #b1 wen_stage1) $e1 stage3))) #b1 #b0)) 
//                                  (ite (= stage2.next (ite (= #b1 rst) #b0000 $e1)) #b1 #b0)) (ite (= rst tag0.next) #b1 #b0)) 
//                                  (ite (= tag1.next (bvand (bvnot rst) tag0)) #b1 #b0)) (ite (= wen_stage1.next (bvand (bvnot rst) wen_stage3)) #b1 #b0)) 
//                                  (ite (= wen_stage2.next (bvand (bvnot rst) wen_stage1)) #b1 #b0)) (ite (= wen_stage3.next (bvnot (bvand (bvnot rst) (bvnot wen_stage3)))) #b1 #b0)))


//inductive invaraint

//因为是inductive，上一个cycle成立，下一个cycle也一定成立 （只要有transition relation就可以足够推出下一个cycle也成立）
// INVAR: (let (($e1 (bvmul reg_v #b0010))) (let (($e2 (bvadd $e1 #b0001))) (let (($e3 (= $e1 (bvmul stage1 #b0010)))) 
// (bvand (bvnot (bvand tag3 (bvnot (ite (= stage3 reg_v_comp) #b1 #b0)))) //把True/False 转 1/0, SMT-lib会区分。 相当于 不会出现 [(tag3是1) AND (stage3和reg_v_comp不相等)]
// (bvand (bvnot (bvand (ite (= stage3 stage2) #b1 #b0) (bvand tag2 (bvnot (ite (= stage3 $e2) #b1 #b0))))) //相当于 不会出现 [(stage 3和stage 2相等) AND (tag2 AND (stage 3和$reg_v *2 +1不相等))]
// (bvand (bvnot (bvand tag2 (bvnot (ite (= stage2 $e2) #b1 #b0))))
// (bvand (bvnot (bvand (bvnot (ite $e3 #b1 #b0)) (bvand tag1 (bvand (ite (= stage3 reg_v) #b1 #b0) (bvnot wen_stage2))))) 
// (bvand (bvnot (bvand tag0 wen_stage2)) 
// (bvand (bvnot (bvand (bvnot (ite $e3 #b1 #b0)) (bvand wen_stage2 (ite (= reg_v stage2) #b1 #b0))))
// (bvand (bvnot (ite (= stage2 #b0010) #b1 #b0)) 
// (bvand (bvnot (bvand tag1 (bvnot wen_stage1))) 
// (bvand wen_stage3 //相当于wen_stage3一直是1
// (bvand (bvnot (bvand tag2 (bvnot wen_stage2))) 
// (bvand (bvnot (bvand (ite (= #b0000 stage2) #b1 #b0) wen_stage2)) 
// (bvnot (bvand wen_stage2 (ite (= stage2 $e1) #b1 #b0)))))))))))))))))

//let后面是临时变量，可以视作tmp类似的（或者宏）
//bvmul是bit_vector乘法，bvadd是bit_vector加法，bvnot是bit vector每一位取反
//实际上就是bvand部分连接起来的东西
//ite = if xx then xx else xx