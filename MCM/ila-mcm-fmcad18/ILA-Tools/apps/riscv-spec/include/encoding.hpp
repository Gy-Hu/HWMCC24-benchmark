/********************

 RISC-V Encoding 

********************/

#ifndef __RISCV_ENCODING_HPP__
#define __RISCV_ENCODING_HPP__

#define XLEN                32
#define INSTR_SIZE          XLEN
#define MEM_WORD_ADDR_LEN   (XLEN-2)
#define MEM_WORD            XLEN


#define OP_LEN  7
#define OPIMM 	BvConst(0x13, OP_LEN)
#define LUI		BvConst(0x37, OP_LEN)
#define AUIPC	BvConst(0x17, OP_LEN)
#define OP		BvConst(0x33, OP_LEN)
#define BRANCH	BvConst(0x63, OP_LEN)
#define JAL		BvConst(0x6f, OP_LEN)
#define JALR	BvConst(0x67, OP_LEN)
#define LOAD	BvConst(0x03, OP_LEN)
#define STORE	BvConst(0x23, OP_LEN)

// funct3 for OPIMM

#define FUNCT3_LEN 3
#define ADDI    BvConst(0x0, FUNCT3_LEN)
#define SLTI    BvConst(0x2, FUNCT3_LEN)
#define SLTIU   BvConst(0x3, FUNCT3_LEN)
#define ANDI    BvConst(0x7, FUNCT3_LEN)
#define ORI     BvConst(0x6, FUNCT3_LEN)
#define XORI    BvConst(0x4, FUNCT3_LEN)
#define SLLI    BvConst(0x1, FUNCT3_LEN)
#define SRLI    BvConst(0x5, FUNCT3_LEN)
#define SRAI    BvConst(0x5, FUNCT3_LEN)

#define FUNCT7_LEN 7
#define SLLIfunct7 BvConst(0x00, FUNCT7_LEN)
#define SRLIfunct7 BvConst(0x00, FUNCT7_LEN)
#define SRAIfunct7 BvConst(0x20, FUNCT7_LEN)
#define funct7_NM  BvConst(0x00, FUNCT7_LEN)
#define funct7_PM  BvConst(0x20, FUNCT7_LEN)

// funct3 for OP
#define ADD     BvConst(0x0 ,  FUNCT3_LEN)
#define SLL     BvConst(0x1 ,  FUNCT3_LEN)
#define SLT     BvConst(0x2 ,  FUNCT3_LEN)
#define SLTU    BvConst(0x3 ,  FUNCT3_LEN)
#define XOR     BvConst(0x4 ,  FUNCT3_LEN)
#define SRL     BvConst(0x5 ,  FUNCT3_LEN)
#define OR      BvConst(0x6 ,  FUNCT3_LEN)
#define AND     BvConst(0x7 ,  FUNCT3_LEN)
#define SUB     BvConst(0x0 ,  FUNCT3_LEN)
#define SRA     BvConst(0x5 ,  FUNCT3_LEN)

// funct 3 for BRANCH
#define BEQ     BvConst(0x0, FUNCT3_LEN)
#define BNE     BvConst(0x1, FUNCT3_LEN)
#define BLT     BvConst(0x4, FUNCT3_LEN)
#define BGE     BvConst(0x5, FUNCT3_LEN)
#define BLTU    BvConst(0x6, FUNCT3_LEN)
#define BGEU    BvConst(0x7, FUNCT3_LEN)

// funct 3 for L/S
#define BYTE    BvConst(0x0 , FUNCT3_LEN)
#define HALF    BvConst(0x1 , FUNCT3_LEN)
#define WORD    BvConst(0x2 , FUNCT3_LEN)
#define DOUBLE  BvConst(0x3 , FUNCT3_LEN)
#define BU      BvConst(0x4 , FUNCT3_LEN)
#define HU      BvConst(0x5 , FUNCT3_LEN)
#define WU      BvConst(0x6 , FUNCT3_LEN)


// --------------- PRIV SPEC ---------------- //

#define MACHINE 0x3
#define SUPERVISER 0x1
#define USER    0x0

#define Machine     BvConst(MACHINE, 2)
#define Supervisor  BvConst(SUPERVISER, 2)
#define User        BvConst(USER, 2)

#define LEGAL_INST_TOTAL 
extern unsigned legalMatch [];
extern unsigned legamMask  [];
extern unsigned prevList   [];

// opcode
//#define LOAD   0b0000011
//#define STORE  0b0100011
#define SYSTEM 0b1110011
inline ExprRef ex_opcode(const ExprRef &inst){ return inst(6,0); }

// funct3
#define CSRRW   0b001
#define CSRRS   0b010
#define CSRRC   0b011
#define CSRRWI  0b101
#define CSRRSI  0b110
#define CSRRCI  0b111
inline ExprRef ex_funct3(const ExprRef &inst){ return inst(14,12); }


// funct12
#define ECALL 0b0
#define EBREAK 0b1
#define ERET 0x100
#define WFI  0x102

// ??
#define SFENCEVMA 0b000100000001
inline ExprRef ex_funct12(const ExprRef &inst){ return inst(31,20); }


// lo address, high address, level, ro 
typedef std::tuple<unsigned,unsigned,unsigned, bool > range;

extern unsigned legalCSRAddr[];
extern unsigned ROCSR[];
extern std::vector<range> CSRNotModeled;

ExprRef isNonDetCSRAddr(const ExprRef & idxBits);
ExprRef isNotModeledCSRAddr(const ExprRef & idxBits);
ExprRef isIlegalCSRAddr(const ExprRef & idxBits);
ExprRef isReadOnlyCSR(const ExprRef & idxBits);


typedef std::set<unsigned> bitslices;
struct CSRfield{
    unsigned addr;
    unsigned level;
    unsigned init;
    CSRfield *parent;
    bitslices RORange;
    bitslices ZeroRange;
    bitslices ConstRange;
};

typedef std::list<CSRfield> CSRInfo_t;
extern CSRInfo_t CSRInfo;




#endif
