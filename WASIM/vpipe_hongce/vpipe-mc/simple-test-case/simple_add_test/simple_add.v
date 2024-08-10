
module top(input wire clk, input wire rst, input wire [7:0] a, input wire [7:0] b, output wire [7:0] out);

    A a1(.clk(clk),.rst(rst),.a(a),.b(b),.out(out));
    
    reg [7:0] tmp_1;
    reg [7:0] tmp_2;
    reg [7:0] tmp_3;
    reg [7:0] tmp_4;

    always @(posedge clk) begin
        if(rst) begin
            tmp_1 <= 0;
            tmp_2 <= 0;
        end

        else begin
            tmp_1 <= a;
            tmp_2 <= b;
        end
    end

    always @(posedge clk) begin
        if(rst) begin
            tmp_3 <= 0;
            tmp_4 <= 0;
        end
        else begin
            tmp_3 <= tmp_1;
            tmp_4 <= tmp_2;
        end
    end
    
    wire [7:0] out2 = tmp_3 + tmp_4;


    assert property (out == out2);

endmodule


module A(input wire clk, input wire rst, input wire [7:0] a, input wire [7:0] b, output reg [7:0] out);


    reg [7:0] tmp_1;
    reg [7:0] tmp_2;



    always @(posedge clk) begin
        if(rst) begin
            tmp_1 <= 0;
            tmp_2 <= 0;
        end
        else begin
            tmp_1 <= a;
            tmp_2 <= b;
        end
    end

    always @(posedge clk) begin
        if(rst)
            out <= 0;
        else
            out <= tmp_1 + tmp_2;
    end


    // reg [7:0] t1;
    // reg [7:0] t2;

    // always @(posedge clk) begin
	// t1 <= b;
	// t2 <= t1;
    // end


endmodule
