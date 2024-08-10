



    assign io_imem_req_bits_pc_reg_1 = io_imem_req_bits_pc_reg + 1;
    assign io_imem_req_bits_pc_reg_2 = io_imem_req_bits_pc_reg + 2;
    assign io_imem_req_bits_pc_reg_3 = io_imem_req_bits_pc_reg + 3;


    assign io_imem_resp_bits_data = {    io_imem_resp_bits_byte_3,
                                         io_imem_resp_bits_byte_2,
                                         io_imem_resp_bits_byte_1,
                                         io_imem_resp_bits_byte_0
                                         };
    always @(posedge clk) begin
        if(rst)
            io_imem_req_bits_pc_reg <= 0;
         else begin
            if (RTL.io_imem_req_valid)  // req is ready all the time!
                io_imem_req_bits_pc_reg <= RTL.io_imem_req_bits_pc;
            else if (RTL.io_imem_resp_valid && RTL.io_imem_resp_ready) begin
                io_imem_req_bits_pc_reg <= io_imem_req_bits_pc_reg + 32'd4;
            end
        end
     end 
     assign io_imem_resp_bits_pc = io_imem_req_bits_pc_reg;
     // *** DMEM related interface control


     assign valid_buf0_input = RTL.io_dmem_req_valid & RTL.io_dmem_req_ready;
     assign valid_buf1_input = dmem_req_valid_buf_0 & ~RTL.io_dmem_s1_kill; // use #pipeline_ex_monitor# to kill unrelated (not belonging to this instruction)
     assign valid_buf__input = ( dmem_req_valid_buf_1 & ~io_dmem_s2_nack ) ?  dmem_req_valid_buf_1 :   ( io_dmem_resp_valid ? 1'b0 : dmem_req_valid );

     always @(posedge clk) begin
         if(rst) begin
             dmem_req_valid_buf_0 <= 1'b0;
             dmem_req_valid_buf_1 <= 1'b0;
             dmem_req_valid       <= 1'b0;
         end
         else begin
             dmem_req_valid_buf_0 <= valid_buf0_input;
             dmem_req_valid_buf_1 <= valid_buf1_input;
             dmem_req_valid <= valid_buf__input;
         end
     end

    assign io_dmem_s2_nack = dmem_req_valid_buf_1 & ( ( dmem_req_valid & ~ ( io_dmem_resp_valid ) ) | ~io_dmem_ordered_1 );
    assign io_dmem_replay_next = dmem_req_valid & ( ~ io_dmem_resp_valid ) & io_dmem_replay_next_rand;

    // if it is 1, then definitely it will be canceled
    assign io_dmem_ordered = ~( (valid_buf0_input & valid_buf1_input ) |
                                (valid_buf1_input & valid_buf__input ) |
                                (valid_buf0_input & valid_buf__input ) ) ;

    always @(posedge clk) begin
      io_dmem_resp_valid <= io_dmem_replay_next;
    end
    assign io_dmem_resp_bits_replay = io_dmem_resp_valid;


    always @(posedge clk) begin
        if (rst) begin
            io_dmem_ordered_0 <= 1'b0;
            io_dmem_ordered_1 <= 1'b0;
        end
        else begin
            io_dmem_ordered_0 <= io_dmem_ordered;
            io_dmem_ordered_1 <= io_dmem_ordered_0;
        end
    end

    // **** LOGGING **** //

    always @(posedge clk) begin
        if(rst) begin
            ex_monitor_eff <= 1'b0;
        end
        dmem_req_addr_0 <= RTL.io_dmem_req_bits_addr;
        dmem_req_tag_0  <= RTL.io_dmem_req_bits_tag;
        dmem_req_cmd_0  <= RTL.io_dmem_req_bits_cmd;
        dmem_req_typ_0  <= RTL.io_dmem_req_bits_typ;
        dmem_req_data_0 <= RTL.io_dmem_req_bits_data; // This is no use!

        dmem_req_addr_1 <= dmem_req_addr_0;
        dmem_req_tag_1  <= dmem_req_tag_0;
        dmem_req_cmd_1  <= dmem_req_cmd_0;
        dmem_req_typ_1  <= dmem_req_typ_0;
        dmem_req_data_1 <= RTL.io_dmem_s1_data;
        ex_monitor_1    <= #pipeline_ex_monitor#;

        if(dmem_req_valid_buf_1 & ~io_dmem_s2_nack) begin
            dmem_req_addr <= dmem_req_addr_1;
            dmem_req_tag  <= dmem_req_tag_1;
            dmem_req_cmd  <= dmem_req_cmd_1;
            dmem_req_typ  <= dmem_req_typ_1;
            dmem_req_data <= dmem_req_data_1;
            ex_monitor_eff <= ex_monitor_1;
        end
    end

    // *** LOAD sequence monitor auxiliary output
    assign load_not_ack_yet =   (ex_monitor_eff & dmem_req_valid)  |  // REQ valid
                                (dmem_req_valid_buf_1 & ~io_dmem_s2_nack & ex_monitor_1);

    assign resp_a_non_monitored_req = (dmem_req_valid & ~ex_monitor_eff & io_dmem_resp_valid & (dmem_req_cmd == 0) ); // 
    
    // *** END of LOAD sequence monitor auxiliary output

    assign io_dmem_resp_bits_addr = dmem_req_addr;
    assign io_dmem_resp_bits_tag = dmem_req_tag;
    assign io_dmem_resp_bits_cmd = dmem_req_cmd;
    assign io_dmem_resp_bits_typ = dmem_req_typ;


    assign dmem_req_addr0 = dmem_req_addr + 32'd0;
    assign dmem_req_addr1 = dmem_req_addr + 32'd1;
    assign dmem_req_addr2 = dmem_req_addr + 32'd2;
    assign dmem_req_addr3 = dmem_req_addr + 32'd3;


    assign  dmem_req_rdata      = {dmem_req_rdata_byte_3, 
                                   dmem_req_rdata_byte_2,
                                   dmem_req_rdata_byte_1,
                                   dmem_req_rdata_byte_0};


    assign      trans_dmem_req_rdata =  dmem_req_typ == 0 ?  {{ 24{dmem_req_rdata[7]  } }, dmem_req_rdata[7:0] } : // 0 : B
                                        dmem_req_typ == 1 ?  {{ 16{dmem_req_rdata[15] } }, dmem_req_rdata[15:0] } : // 0 : B
                                        dmem_req_typ == 2 ?  { dmem_req_rdata  } : // 0 : B
                                        dmem_req_typ == 4 ?  { 24'b0, dmem_req_rdata[7:0] } : // 0 : B
                                        dmem_req_typ == 5 ?  { 16'b0, dmem_req_rdata[15:0] } : // 0 : B
                                        dmem_req_rdata;


    assign io_dmem_resp_bits_data = ( io_dmem_resp_bits_cmd == 0 ) ? trans_dmem_req_rdata : 32'hxxxxxxxx;
    assign io_dmem_resp_bits_has_data = ( io_dmem_resp_bits_cmd == 0 ); // if it is read(0),  then reply with data


    assign offset_wr_addr  = io_dmem_resp_bits_addr[1:0];
    assign aligned_wr_addr = {io_dmem_resp_bits_addr[31:2], 2'b00};
    assign aligned_wr_addr0 = aligned_wr_addr+32'd0;
    assign aligned_wr_addr1 = aligned_wr_addr+32'd1;
    assign aligned_wr_addr2 = aligned_wr_addr+32'd2;
    assign aligned_wr_addr3 = aligned_wr_addr+32'd3;

    assign aligned_data    = {aligned_byte_3,aligned_byte_2, aligned_byte_1,aligned_byte_0 };
    
    always @(*) begin
        if(io_dmem_resp_bits_typ == 0)      // Byte
            Mask = 32'h000000ff << (offset_wr_addr)*8;
        else if(io_dmem_resp_bits_typ == 1) // Half
            Mask = 32'h0000ffff << (offset_wr_addr)*8;
        else if(io_dmem_resp_bits_typ == 2) // Word
            Mask = 32'hffffffff;
        else
            Mask = 32'hxxxxxxxx;
    end

    always @(*) begin
        if(io_dmem_resp_bits_typ == 0)      // Byte
            OffsetData = {24'h0, dmem_req_data[ 7:0] } << (offset_wr_addr)*8;
        else if(io_dmem_resp_bits_typ == 1) // Half
            OffsetData = {16'h0, dmem_req_data[15:0] } << (offset_wr_addr)*8;
        else if(io_dmem_resp_bits_typ == 2) // Word
            OffsetData = dmem_req_data;
        else
            OffsetData = 32'hxxxxxxxx;
    end

    
    reg[7:0] dmem_array[0:4294967295];

    assign dmem_req_rdata_byte_3 = dmem_array[dmem_req_addr3];
    assign dmem_req_rdata_byte_2 = dmem_array[dmem_req_addr2];
    assign dmem_req_rdata_byte_1 = dmem_array[dmem_req_addr1];
    assign dmem_req_rdata_byte_0 = dmem_array[dmem_req_addr0];

    assign aligned_byte_3 = dmem_array[aligned_wr_addr3];
    assign aligned_byte_2 = dmem_array[aligned_wr_addr2];
    assign aligned_byte_1 = dmem_array[aligned_wr_addr1];
    assign aligned_byte_0 = dmem_array[aligned_wr_addr0];


