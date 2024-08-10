
/*

This file contains the interface with the ILA synthesis tools

--Hongce Zhang (hongcez@princeton.edu)

*/

#ifndef _RISC_ILA_INTERFACE_H
#define _RISC_ILA_INTERFACE_H

#include <unordered_map>

class InstSimMemory;
class sim_t;
class state_t;


class InstSimMemory
{
    

    typedef std::pair<uint64_t,uint64_t> addr_data_pair; // byte addr
    std::unordered_map<uint64_t,uint64_t> internal_storage;
    uint64_t defVal;
    bool isa32;

    char tempStorage[64]; // char = 1, however 32 bits
    bool dirty;
    uint64_t addr_buffed;

    void merge_back_changes();

    char getByte(uint64_t word, uint64_t idx);

public:

    InstSimMemory();

    void loadFromFile(std::istream &ins, bool isa32=true);

    char * getMemoryAtAddr(uint64_t addr);
    bool addr_is_memory(uint64_t addr) { return true; } // here we will not model any memory-mapped I/O

    void dumpMemory(std::ostream &os, bool isa32);

};

class ILAsimInterface
{


    InstSimMemory simMemory;
    uint64_t inst;

public:
    ILAsimInterface();

    void load(bool isa32=true);
    insn_bits_t getInst();

    void assign_state(state_t * state, processor_t * proc);
    void dump_state(state_t * state, processor_t * proc, bool isa32);

    void attach_memory(sim_t & sim); // use it to check if any other
    // entity is accessing through some other unknown way
    // if not, then our modification is correct!

};


#endif
