/*

This file contains the interface with the ILA synthesis tools

--Hongce Zhang (hongcez@princeton.edu)

*/
#include <iostream>
#include <fstream>
#include <iomanip>
#include <cassert>

#include "sim.h"
#include "processor.h"
#include "sim_interface.hh"

const std::string inFileName  = "assign.in";
const std::string outFileName = "result.out";

// private structure for regs
#define NUM_BASE_REG (32+1)
const char * BaseRegName[] = {
    "x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", 
    "x8", "x9", "x10", "x11", "x12", "x13", "x14", "x15", 
    "x16", "x17", "x18", "x19", "x20", "x21", "x22", "x23", 
    "x24", "x25", "x26", "x27", "x28", "x29", "x30", "x31",
    "pc"
};
#define NUM_CSR_REG 31
const char * CSRRegName[] = {
    "misa","mstatus","mtvec","medeleg","mideleg","mip","mie","mscratch","mepc","mcause","mbadaddr",
    "sstatus","sedeleg","sideleg","sie","sip","sptbr","stvec","sscratch","sepc","scause","sbadaddr",
    "ustatus","uie","utvec","uscratch","uepc","ucause","ubadaddr","uip",
    "Priv"
};
#define NUM_REG (NUM_CSR_REG + NUM_BASE_REG)

uint64_t regList[NUM_REG];
bool modified[NUM_REG];


int findIdx(const std::string &is) 
{
    for(int idx = 0; idx < NUM_CSR_REG; idx ++)
        if(is == CSRRegName[idx])
            return idx + NUM_BASE_REG;
    return -1;
}

void Fatal(const std::string &s)
{
    std::cerr<<"Fatal error: "<<s<<std::endl;
    exit(1);
}

ILAsimInterface::ILAsimInterface()
{
    for(int idx=0;idx<NUM_REG;idx++)
        modified[idx] = false;
}

void ILAsimInterface::attach_memory(sim_t & sim)
{ sim.memRep = &simMemory; free(sim.mem); sim.mem = NULL; }

void ILAsimInterface::load(bool isa32)
{
    std::ifstream inFile(inFileName);

    if(inFile.fail())
        Fatal(inFileName + " is not accessible!");

    inFile >> std::hex >> inst;
    //if (isa32)
    //  inst = ((int64_t(inst)) << 32) >> 32; //Sign-Extend 32bit to 64 bit #HACKS

    std::string name;
    // read in gpr
    for(int idx=0; idx < NUM_BASE_REG ; idx++) {
        inFile >> name;
        if(name != BaseRegName[idx] )
            std::cerr<<"<W> Change unordered assignment:"<< name <<" to "<<BaseRegName[idx] << std::endl;
        inFile >> regList[idx];
	//if (isa32)
    //      regList[idx] = ((int64_t(regList[idx])) << 32) >> 32;
    }

    // load CSRs
    inFile >> name;
    assert(name == ".CSR_BEGIN");
    while(name != ".CSR_END")
    {
        inFile >> name;
        if(name == ".CSR_END")
            break;
        int idx = findIdx(name);
        if(idx==-1) 
            Fatal("unrecognized register!");
        inFile>>std::hex>>regList[idx];
	//if (isa32)
	//  regList[idx] = ((int64_t(regList[idx])) << 32) >> 32;
        modified[idx] = true;
    }

    // load memory
    simMemory.loadFromFile(inFile, isa32);

    inFile.close();
}

insn_bits_t ILAsimInterface::getInst()
{
    return inst;
}


#define forceCSR(csrName) else if(name == #csrName) proc->get_state()->csrName = regList[idx]
#define setCSR(csrName, stateID)  else if(name == #csrName) proc->set_csr(stateID, regList[idx])

void ILAsimInterface::assign_state(state_t * state, processor_t * proc)
{
    // GPR
    if(regList[0]) {
        std::cerr<<"<W> Forcing $x0 to be 0."<<std::endl;
        regList[0] = 0;
    }
    for(int idx = 0; idx < 32; idx ++) {
        state->XPR.write(idx,regList[idx]);
    }
    // PC
    state->pc = regList[32];

    // CSRs
    bool setPriv = false;
    for(int idx = NUM_BASE_REG; idx < NUM_REG; idx ++) {
        if(modified[idx] == false)
            continue;
        std::string name = CSRRegName[idx-NUM_BASE_REG];
        if(name == "misa") {
            std::cout<<"<INFO>: fixed ISA:" << std::hex << proc->get_csr(CSR_MISA) 
                << " Unchange : " << std::hex << regList[idx]<<std::endl;
            }
        setCSR(mstatus, CSR_MSTATUS);
        setCSR(mtvec, CSR_MTVEC);
        forceCSR(mideleg); //setCSR(mideleg, CSR_MIDELEG);
        setCSR(medeleg, CSR_MEDELEG);
        forceCSR(mip);//setCSR(mip, CSR_MIP); we cannot use that because they are not enough
        forceCSR(mie);//setCSR(mie, CSR_MIE);
        setCSR(mscratch, CSR_MSCRATCH);
        setCSR(mepc, CSR_MEPC);
        setCSR(mcause, CSR_MCAUSE);
        setCSR(mbadaddr, CSR_MBADADDR);
        //setCSR(misa, CSR_MISA); // RV32

        setCSR(sstatus, CSR_SSTATUS);
        //setCSR(sedeleg, stateID);
        //setCSR(sideleg, stateID);
        setCSR(sie, CSR_SIE);
        setCSR(sip, CSR_SIP);
        setCSR(sptbr, CSR_SPTBR);
        setCSR(stvec, CSR_STVEC);
        setCSR(sscratch, CSR_SSCRATCH);
        setCSR(sepc, CSR_SEPC);
        setCSR(scause, CSR_SCAUSE);
        setCSR(sbadaddr, CSR_SBADADDR);

        //setCSR(ustatus, stateID);
        //setCSR(uedeleg, stateID);
        //setCSR(uideleg, stateID);
        //setCSR(uie, stateID);
        //setCSR(uip, stateID);
        //setCSR(utvec, stateID);
        //setCSR(uscratch, stateID);
        //setCSR(uepc, stateID);

        else if(name == "Priv")
            proc->set_privilege(regList[idx]),setPriv = true;
        else
            Fatal("Unknown CSR register:" + name );

    }
    if(!setPriv)
        proc->set_privilege(0); // user-level is default setting
    // memory is not needed
}

#define getCSR(csrName, stateID)  outFile<< std::string(#csrName) <<" "<<std::hex<< proc->get_csr(stateID) << std::endl

void ILAsimInterface::dump_state(state_t * state, processor_t * proc, bool isa32)
{
    // including the memory
    std::ofstream outFile(outFileName);

    // dump GPR
    for(int idx=0;idx<32;idx++) {
      if (isa32) 
        outFile << "x"<<std::dec<<idx<<" "<<std::hex<< (state->XPR[idx] & 0xFFFFFFFF) <<std::endl;
      else
        outFile << "x"<<std::dec<<idx<<" "<<std::hex<< state->XPR[idx] <<std::endl;    }

    if (isa32)
      outFile<<"pc "<<std::hex<< (state->pc & 0xFFFFFFFF) <<std::endl;
    else
      outFile<<"pc "<<std::hex<< state->pc <<std::endl;

    // dump CSR
    outFile << ".CSR_BEGIN" <<std::endl;

    getCSR(misa, CSR_MISA); // RV32
    getCSR(mstatus, CSR_MSTATUS);
    getCSR(mtvec, CSR_MTVEC);
    getCSR(mideleg, CSR_MIDELEG);
    getCSR(medeleg, CSR_MEDELEG);
    getCSR(mip, CSR_MIP);
    getCSR(mie, CSR_MIE);
    getCSR(mscratch, CSR_MSCRATCH);
    getCSR(mepc, CSR_MEPC);
    getCSR(mcause, CSR_MCAUSE);
    getCSR(mbadaddr, CSR_MBADADDR);

    getCSR(sstatus, CSR_SSTATUS);
    //getCSR(sedeleg, stateID);
    //getCSR(sideleg, stateID);
    getCSR(sie, CSR_SIE);
    getCSR(sip, CSR_SIP);
    getCSR(sptbr, CSR_SPTBR);
    getCSR(stvec, CSR_STVEC);
    getCSR(sscratch, CSR_SSCRATCH);
    getCSR(sepc, CSR_SEPC);
    getCSR(scause, CSR_SCAUSE);
    getCSR(sbadaddr, CSR_SBADADDR);

    //getCSR(ustatus, stateID);
    //getCSR(uedeleg, stateID);
    //getCSR(uideleg, stateID);
    //getCSR(uie, stateID);
    //getCSR(uip, stateID);
    //getCSR(utvec, stateID);
    //getCSR(uscratch, stateID);
    //getCSR(uepc, stateID);
    outFile<< "Priv" <<" "<<std::hex<< state->prv << std::endl;
    outFile << ".CSR_END" <<std::endl;

    // dump memory
    simMemory.dumpMemory(outFile, isa32);

    outFile.close();
}

//-------------------------------------------------------------

InstSimMemory::InstSimMemory():dirty(false),addr_buffed(0)
{

}

void InstSimMemory::loadFromFile(std::istream &ins, bool isa32)
{
    // format:
    // N(decimal) default(hex)
    // addr data (both hex)

    int NoPairs;
    uint64_t addr;
    uint64_t data;

    ins >> std::dec >> NoPairs>>std::hex>>defVal; 
    //if (isa32)
    //  defVal = ((int64_t(defVal)) << 32) >> 32;
    for (int idx = 0; idx < NoPairs; idx ++) {
        ins >> std::hex >> addr >> std::hex >> data;
	//if (isa32){
	//  addr = ((int64_t(addr)) << 32) >> 32;
	//  data = ((int64_t(data)) << 32) >> 32;
	//}
        if(data != defVal)
            internal_storage[addr] = data;
    }
    //this->isa32 = isa32;

}
void InstSimMemory::merge_back_changes()
{
    if(dirty) {
        dirty = false;
        for(uint64_t addr = addr_buffed, idx = 0; idx < 64; addr++, idx ++) {
            //if(defVal < 256 && (unsigned char)tempStorage[idx] == defVal) {
            //    if(internal_storage[addr] != defVal)
            //        internal_storage.erase(addr); //let's remove it 
                // else no change
            //}
            //else
                internal_storage[addr] = tempStorage[idx] & 0xff;
        }
    }
}

char InstSimMemory::getByte(uint64_t word, uint64_t idx)
{
    idx = idx % 4;
    return (word >> (idx*8) ) & 0xff;
}

char * InstSimMemory::getMemoryAtAddr(uint64_t addr)
{
    merge_back_changes();

    // fork the content
    addr_buffed = addr;
    uint64_t mask = isa32 ?  0xffffffff : 0xffffffffffffffff;
    for(uint64_t addop = addr, idx = 0; idx < 64; idx ++ , addop = (addop + 1) & mask ) {
        if( internal_storage.find(addop) == internal_storage.end() ) {
            //if (defVal < 256)
            //    tempStorage[idx] = defVal;
            //else {
                tempStorage[idx] = getByte(defVal, addop%4); // little-endian!
            //}
        }
        else
            tempStorage[idx] = internal_storage[addop];
    }

    dirty = true;
    return tempStorage;
}

void InstSimMemory::dumpMemory(std::ostream &os, bool isa32)
{
    if (isa32)
      os << std::dec << internal_storage.size()<<" " << std::hex << (defVal & 0xFFFFFFFF) << std::endl;
    else
      os << std::dec << internal_storage.size()<<" " << std::hex << defVal << std::endl;
    for (auto pos = internal_storage.begin(); pos != internal_storage.end(); ++pos ) {
      if (isa32)
        os << std::hex << (pos->first & 0xFFFFFFFF) <<" " << (pos->second & 0xFFFFFFFF) << std::endl;
      else
        os << std::hex << pos->first <<" " << pos->second << std::endl;
    }
}
