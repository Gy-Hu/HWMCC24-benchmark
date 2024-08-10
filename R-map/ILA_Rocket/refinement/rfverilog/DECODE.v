    assign isLB = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00000003;
    assign isLW = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00002003;
    assign isLH = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00001003;
    assign isLD = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00003003;
    assign isLBU = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00004003;
    assign isLHU = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00005003;
    assign isLWU = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00006003;
    assign isSB = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00000023;
    assign isSH = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00001023;
    assign isSW = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00002023;
    assign isSD = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00003023;
    assign isBEQ = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00000063;
    assign isBNE = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00001063;
    assign isBLT = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00004063;
    assign isBGE = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00005063;
    assign isBLTU = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00006063;
    assign isBGEU = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00007063;
    assign isJAL = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000007f) == 32'h0000006f;
    assign isJALR = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00000067;
    assign isLUI = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000007f) == 32'h00000037;
    assign isAUIPC = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000007f) == 32'h00000017;
    assign isADDI = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00000013;
    assign isSLTI = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00002013;
    assign isSLTIU = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00003013;
    assign isXORI = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00004013;
    assign isORI = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00006013;
    assign isANDI = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00007013;
    assign isSRLI = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hfe00707f) == 32'h00005013;
    assign isSRAI = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hfe00707f) == 32'h40005013;
    assign isSLLI = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hfe00707f) == 32'h00001013;
    assign isADD = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hfe00707f) == 32'h00000033;
    assign isSUB = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hfe00707f) == 32'h40000033;
    assign isSLL = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hfe00707f) == 32'h00001033;
    assign isSLT = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hfe00707f) == 32'h00002033;
    assign isSLTU = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hfe00707f) == 32'h00003033;
    assign isXOR = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hfe00707f) == 32'h00004033;
    assign isSRL = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hfe00707f) == 32'h00005033;
    assign isSRA = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hfe00707f) == 32'h40005033;
    assign isOR = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hfe00707f) == 32'h00006033;
    assign isAND = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hfe00707f) == 32'h00007033;
    assign isCSRRW = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00001073;
    assign isCSRRS = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00002073;
    assign isCSRRC = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00003073;
    assign isCSRRWI = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00005073;
    assign isCSRRSI = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00006073;
    assign isCSRRCI = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'h0000707f) == 32'h00007073;
    assign isECALL = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hffffffff) == 32'h00000073;
    assign isEBREAK = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hffffffff) == 32'h00100073;
    assign isSRET = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hffffffff) == 32'h10200073;
    assign isMRET = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hffffffff) == 32'h30200073;
    assign isSFENCE_VM = (RTL.ibuf_io_inst_0_bits_inst_bits & 32'hfff07fff) == 32'h10400073;


    assign WBisLB = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00000003;
    assign WBisLW = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00002003;
    assign WBisLH = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00001003;
    assign WBisLD = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00003003;
    assign WBisLBU = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00004003;
    assign WBisLHU = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00005003;
    assign WBisLWU = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00006003;
    assign WBisSB = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00000023;
    assign WBisSH = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00001023;
    assign WBisSW = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00002023;
    assign WBisSD = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00003023;
    assign WBisBEQ = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00000063;
    assign WBisBNE = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00001063;
    assign WBisBLT = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00004063;
    assign WBisBGE = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00005063;
    assign WBisBLTU = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00006063;
    assign WBisBGEU = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00007063;
    assign WBisJAL = (RTL.wb_reg_inst & 32'h0000007f) == 32'h0000006f;
    assign WBisJALR = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00000067;
    assign WBisLUI = (RTL.wb_reg_inst & 32'h0000007f) == 32'h00000037;
    assign WBisAUIPC = (RTL.wb_reg_inst & 32'h0000007f) == 32'h00000017;
    assign WBisADDI = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00000013;
    assign WBisSLTI = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00002013;
    assign WBisSLTIU = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00003013;
    assign WBisXORI = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00004013;
    assign WBisORI = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00006013;
    assign WBisANDI = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00007013;
    assign WBisSRLI = (RTL.wb_reg_inst & 32'hfe00707f) == 32'h00005013;
    assign WBisSRAI = (RTL.wb_reg_inst & 32'hfe00707f) == 32'h40005013;
    assign WBisSLLI = (RTL.wb_reg_inst & 32'hfe00707f) == 32'h00001013;
    assign WBisADD = (RTL.wb_reg_inst & 32'hfe00707f) == 32'h00000033;
    assign WBisSUB = (RTL.wb_reg_inst & 32'hfe00707f) == 32'h40000033;
    assign WBisSLL = (RTL.wb_reg_inst & 32'hfe00707f) == 32'h00001033;
    assign WBisSLT = (RTL.wb_reg_inst & 32'hfe00707f) == 32'h00002033;
    assign WBisSLTU = (RTL.wb_reg_inst & 32'hfe00707f) == 32'h00003033;
    assign WBisXOR = (RTL.wb_reg_inst & 32'hfe00707f) == 32'h00004033;
    assign WBisSRL = (RTL.wb_reg_inst & 32'hfe00707f) == 32'h00005033;
    assign WBisSRA = (RTL.wb_reg_inst & 32'hfe00707f) == 32'h40005033;
    assign WBisOR = (RTL.wb_reg_inst & 32'hfe00707f) == 32'h00006033;
    assign WBisAND = (RTL.wb_reg_inst & 32'hfe00707f) == 32'h00007033;
    assign WBisCSRRW = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00001073;
    assign WBisCSRRS = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00002073;
    assign WBisCSRRC = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00003073;
    assign WBisCSRRWI = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00005073;
    assign WBisCSRRSI = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00006073;
    assign WBisCSRRCI = (RTL.wb_reg_inst & 32'h0000707f) == 32'h00007073;
    assign WBisECALL = (RTL.wb_reg_inst & 32'hffffffff) == 32'h00000073;
    assign WBisEBREAK = (RTL.wb_reg_inst & 32'hffffffff) == 32'h00100073;
    assign WBisSRET = (RTL.wb_reg_inst & 32'hffffffff) == 32'h10200073;
    assign WBisMRET = (RTL.wb_reg_inst & 32'hffffffff) == 32'h30200073;
    assign WBisSFENCE_VM = (RTL.wb_reg_inst & 32'hfff07fff) == 32'h10400073;
    
    assign DECODE_isLoad = isLW | isLB | isLBU | isLH | isLHU;
    assign WBisBranch = WBisBEQ | WBisBNE | WBisBGEU | WBisBGE | WBisBLT | WBisBLTU;
    assign DECODE_validInstructions = 
      isSB | isSH | isSW | isLW | isLB | isLBU | isLH | isLHU |
       isBEQ | isBNE | isBLT | isBGE | isBLTU | isBGEU | isJAL | isJALR | 
      isLUI | isAUIPC | isADDI | isSLTI | isSLTIU | isXORI | isORI | isANDI | 
      isSRLI | isSRAI | isSLLI | isADD | isSUB | isSLL | isSLT | isSLTU | isXOR | 
      isSRL | isSRA | isOR | isAND ;
    assign WB_validInstructions = 
      WBisSB | WBisSH | WBisSW | WBisLW | WBisLB | WBisLBU | WBisLH | WBisLHU |
       WBisBEQ | WBisBNE | WBisBLT | WBisBGE | WBisBLTU | WBisBGEU | WBisJAL | WBisJALR | 
      WBisLUI | WBisAUIPC | WBisADDI | WBisSLTI | WBisSLTIU | WBisXORI | WBisORI | WBisANDI | 
      WBisSRLI | WBisSRAI | WBisSLLI | WBisADD | WBisSUB | WBisSLL | WBisSLT | WBisSLTU | WBisXOR | 
      WBisSRL | WBisSRA | WBisOR | WBisAND ;

    assign WBimmS = { { 20{RTL.wb_reg_inst[31]} } , RTL.wb_reg_inst[31:25], RTL.wb_reg_inst[11:7] };
    assign WBimmI = { { 20{RTL.wb_reg_inst[31]} } , RTL.wb_reg_inst[31:20] };
    assign WBimmJ = { { 11{RTL.wb_reg_inst[31]} } , RTL.wb_reg_inst[31] , RTL.wb_reg_inst[19:12] , RTL.wb_reg_inst[20], RTL.wb_reg_inst[30:21],1'b0 };
    assign WBimmB = { { 19{RTL.wb_reg_inst[31]} } , RTL.wb_reg_inst[31], RTL.wb_reg_inst[7], RTL.wb_reg_inst[30:25], RTL.wb_reg_inst[11:8], 1'b0 };
    assign rf_idx_i = RTL.wb_reg_inst[19:15]; //rs1
    assign loadAddr = RTL.rf_idx_o[1:0] + WBimmI[1:0];
    assign storeAddr= RTL.rf_idx_o[1:0] + WBimmS[1:0];


    always @(posedge clk) begin 
     if(#decode#) begin
        inst_decode_rd <= RTL.ibuf_io_inst_0_bits_inst_bits[11:7];
      end
    end
    