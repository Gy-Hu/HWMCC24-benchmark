import ply.yacc as yacc

from litmusLex import tokens
import totalCheck


inst_name_fmt = "{coreID}_{globalID}_{TYPE}"
pc_name_fmt   = "c{coreID}_pc"
var_name_fmt  = "a{address}"
def getEntity(coreID): return "c{coreID}".format(coreID = coreID)
def getCoreID(entity): return int(entity[1:])
def instName2gid(name): return int(name.split('_')[1])
def instName2cid(name): return int(name.split('_')[0])


class Instruction(object):
    def __init__(self,name, decodeFunc = None):
        self.name = name
        self.decodeFunc = decodeFunc
        self.updateDict = {}
    def setUpdateToState(self,stateName,func):
        self.updateDict[stateName] = func
    def changeDecodeFunc(self,decodeFunc):
        self.decodeFunc = decodeFunc
    def setILA_st(self,stlocal):
        self.stlocal = stlocal
    def setEntity(self,entity):
        self.entity = entity
    def toStr(self, num_tab = 0):
        retStr = '\t'*num_tab
        retStr+= '[Inst] '+self.name+'\n'+'\t'*num_tab
        retStr+= 'localStates: '+str(self.stlocal)+'\n'+'\t'*num_tab
        retStr+= 'entity: '+self.entity+'\n'+'\t'*num_tab
        retStr+= 'updates: '+str(self.updateDict.keys())
        return retStr
    
# we need global ending event

class litmusTestInstructions(object):
    # unroller uses:
    def unroller_get_templateProgram_local_state(self, coreID = None):  
        if coreID is not None:
            return (self.templateProgram[coreID], self.localStates[coreID])

        templateProgram = []
        localStates     = []
        for cid in self.cores:
            templateProgram.append(self.templateProgram[cid])
            localStates.append(self.localStates[cid])
        return (templateProgram,localStates)
    def unroller_get_sharedStates(self):
        return list(self.addrs)
    def unroller_gid2instName_and_eid(self, inst_gid):
        inst_ref = self.gid2inst[inst_gid]
        inst_name= inst_ref.name
        return ( inst_name ,  getEntity( instName2cid(inst_name) ) )
    def unroller_instName2Name_and_eid(self, inst_name):
        return ( inst_name, getEntity( instName2cid( inst_name ) ) )

    def Print_parse_result(self):
        print '< Alternative >'
        print '----------------------'
        print '\t #cores:',self.num_cores
        print '\t cids:', self.cores
        print '\t #addrs:',self.addrs
        print '\t Begin Per Core PO Info:'

        templateProg, localStates = self.unroller_get_templateProgram_local_state()

        cid = 0
        for prog in templateProg:
            print '\t\t Cid:',cid
            print '\t\t local:',localStates[cid]
            for inst in prog:
                print '\t\t inst:'
                print inst.toStr(num_tab = 3)
            cid += 1
        
        print 'Fences: ',self.set_of_fences
        print 'rels:',self.set_of_rel
        print '#ending: ', len(self.endingAsserts)
        print 

    def __init__(self):
        # for unroller feeds
        self.num_cores = 0
        self.num_of_inst_per_core = {}
        self.cores = set([])
        self.localStates = {}
        self.addrs = set([])

        self.per_core_inst_list = {}

        self.set_of_fences = set([])  # set of instruction_name
        self.set_of_read_assert = {}  # instruction_name -> property
        self.set_of_rel = set([])     # set of (type, gid1, gid2) type = rf,fr,co   *NO* po !!!

        # internal use
        self.po_list = []
        self.set_of_inst_names = set([])
        self.gid2inst = {}            # gid -> inst ref

        # for parser use
        self.outcome = 'Unknown'
        self.endingAsserts = []       # list of z3 cond

    def add_inst(self, coreID, globalID, op_addr_data_tuple):
        """This function only adds to per_core_inst_list,
        it does not change set decode / pc update"""

        # add to cores
        if coreID not in self.cores:
            self.cores.add(coreID)
            self.num_cores += 1
        coreCnt = self.num_of_inst_per_core.get(coreID,0)
        self.num_of_inst_per_core[coreID] = coreCnt + 1 # actually not used in the instruction name
        # because at the current stage we are not able to determine the real po

        inst_name = inst_name_fmt.format(coreID = coreID, globalID = globalID, TYPE = op_addr_data_tuple[0])
        # check name repetition
        if inst_name in self.set_of_inst_names:
            print '<E>: instruction name already exists'
            assert False
        self.set_of_inst_names.add(inst_name)

        entity_name = getEntity(coreID = coreID)
        inst = Instruction(inst_name)
        inst.setEntity(entity = entity_name)

        # now set updates
        if op_addr_data_tuple[0] == 'F':
            self.set_of_fences.add( inst_name )
        elif op_addr_data_tuple[0] == 'R':
            var_name = var_name_fmt.format(address = op_addr_data_tuple[1])
            self.set_of_read_assert[inst_name] = lambda state,var_name=var_name,op_addr_data_tuple=op_addr_data_tuple: state(var_name) == op_addr_data_tuple[2] 
            self.addrs.add(var_name)
        elif op_addr_data_tuple[0] == 'W':
            var_name = var_name_fmt.format(address = op_addr_data_tuple[1])
            inst.setUpdateToState(var_name, lambda state,op_addr_data_tuple=op_addr_data_tuple: op_addr_data_tuple[2])
            self.addrs.add(var_name)
        else:
            print 'Unknown opcode:', op_addr_data_tuple[0]
            assert False

        if coreID not in self.per_core_inst_list:
            self.per_core_inst_list[coreID] = []
        self.per_core_inst_list[coreID].append(inst)
        self.gid2inst[globalID] = inst

    def add_rel(self,rel,gid1,gid2):
        if rel == 'po':
            self.po_list.append( (gid1,gid2) )
        else:
            self.set_of_rel.add((rel,gid1,gid2))

    def proc_po(self): # also used to form template program
        # first divide into totality group, according to gid->cid (and check no cross)
        totalityGroup = {} # cid -> list of edges
        for gid1,gid2 in self.po_list:
            inst1name = self.gid2inst[gid1].name
            inst2name = self.gid2inst[gid2].name
            assert instName2cid(inst1name) == instName2cid(inst2name)
            coreID = instName2cid(inst1name)
            if coreID not in totalityGroup: 
                totalityGroup[coreID] = []
            totalityGroup[coreID].append( (gid1,gid2) )

        # add single instruction cores
        for cid in self.cores:
            if cid not in totalityGroup:
                assert len(self.per_core_inst_list[cid]) == 1
                instName = self.per_core_inst_list[cid][0].name
                gid = instName2gid(instName)
                totalityGroup[cid] = [(gid,gid)]

        # also forming program
        self.templateProgram = {}
        for coreID, poL in totalityGroup.items():

            sameCoreGID = [instName2gid(inst.name) for inst in self.per_core_inst_list[coreID] ]
            allNode,orderList = totalCheck.check(poL)

            assert allNode == set(sameCoreGID) # every instruction must in the po relation
            # let's add po orders
            templateProgram = []
            pc_val = 0
            pc_name = pc_name_fmt.format(coreID = coreID)
            self.localStates[coreID] = [pc_name]

            for gid in orderList:
                inst_ref = self.gid2inst[gid]
                inst_ref.changeDecodeFunc(lambda state,pc_name=pc_name,pc_val=pc_val: state(pc_name) == pc_val)
                pc_val += 1
                inst_ref.setUpdateToState(pc_name, lambda state,pc_val=pc_val: pc_val)
                inst_ref.setILA_st([pc_name])
                templateProgram.append(inst_ref)

            self.templateProgram[coreID] = templateProgram


    def set_endingAsserts(self,conds):
        for addr,data in conds:
            var_name = var_name_fmt.format(address = addr)
            cond = lambda state,var_name=var_name,data=data: state(var_name) == data
            self.endingAsserts.append(cond)


AlterLists = [] # list of litmusTestInstructions


def p_litmus(p):
    'litmus : altBlks outcome'
    outcome = p[2] 
    print 'Required outcome:',outcome
    altBlks = p[1]
    for altBlk in altBlks:
        insts = altBlk[0]
        rels  = altBlk[1]
        conds = altBlk[2]
        instCols = litmusTestInstructions()
        for gid,cid,op3tuple in insts:
            instCols.add_inst(coreID = cid, globalID = gid, op_addr_data_tuple = op3tuple)
        for rel,gid1,gid2 in rels:
            instCols.add_rel(rel,gid1,gid2)
        instCols.outcome = outcome
        instCols.set_endingAsserts( conds )
        instCols.proc_po()

        AlterLists.append(instCols)

    # now unpack
    # altBlks: [altblk]
    #        altblk: ([inst], [rel], [cond])
    #               inst: (gid,cid, (op3tuple))
    #               rel : (rel,gid1,gid2)
    #               cond: (addr,val)



def p_altBlks(p):
    """altBlks : altblk 
        | altblk altBlks"""
    if len(p[1:]) == 1:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_altblk(p):
    'altblk : ALTERNATIVE instructions relations conds' # | instructions relations finalConditions
    p[0] = (p[2],p[3],p[4])

def p_instructions(p):
    """instructions : instructions instruction 
        | instruction """
    if len(p[1:]) == 1:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_relations(p):
    """relations : relations relation 
        | relation """
    if len(p[1:]) == 1:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_instruction(p):
    'instruction : ID ID ID ID opcode'
    globalID = p[1]
    coreID   = p[2]
    assert p[3] == 0 and p[4] == 0 # assert threadID and intraInstID are both 0
    p[0] = (globalID,coreID,p[5])
    # okay, now let's construct instruction
    # the rule of forming variables is like this
    # inst_name %coreID_$coreCnt_%globalID_%RWF
    # write vars: c%coreID_pc, W: a%address
    # read vars : add property state('a%address') == ? && and also set pc to the next


    

def p_opcode(p):
    """opcode : LC inst optionalFlags vablock pablock datablock RC
            | LC F FLAG RC"""

    if len(p[1:]) >4 : # Read or Write Instruction
        if p[3]:
            print '<W> Ignore flag: ',p[3]
        assert p[4] == p[5] 
        p[0] = ( p[2],  p[4] , p[6] ) # inst, addr, data
    else: # Fence instruction
        assert p[3] == 'MFENCE'
        p[0] = ( 'F', )

def p_inst(p):
    """inst : R 
        | W 
        | """
    if p[1].lower() == 'read':
        p[0] = 'R'
    elif p[1].lower() == 'write':
        p[0] = 'W'
    else:
        assert False

def p_optionalFlags(p):
    """optionalFlags : empty
        | FLAG"""
    if len(p[1:]) != 0:
        p[0] = p[1]
    else:
        p[0] = None


def p_vablock(p):
    'vablock : LC VA ID ID RC'
    assert p[4] == 0
    p[0] = p[3]

def p_pablock(p):
    'pablock : LC PA ID ID RC'
    assert p[4] == 0
    p[0] = p[3]

def p_datablock(p):
    'datablock : LC DATA ID RC'
    p[0] = p[3]

def p_outcome(p):
    """outcome : FORBIDDEN 
        | PERMITTED
        | REQ"""
    if p[1].lower() == 'required':
        p[0] = 'Permitted'
    else:
        p[0] = p[1]

def p_relation(p):
    'relation : RELATION RL ID ID TO ID ID'
    assert p[4] == 0
    assert p[7] == 0
    rel  = p[2].lower()
    gid1 = p[3]
    gid2 = p[6]
    p[0] = (p[2],gid1,gid2)

def p_conds(p):
    """conds : conds cond 
        | empty """
    if len(p[1:]) == 1:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_cond(p):
    """cond : LC PA ID ID RC EQ ID"""
    assert p[4] == 0
    addr = p[3]
    val  = p[7]
    p[0] = (addr,val)

def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


def parseLitmusTest(fname):
    global AlterLists
    AlterLists = []
    parser = yacc.yacc()
    with open(fname) as fin:
        parser.parse( fin.read() )

if __name__ == '__main__':
    parseLitmusTest('SC_tests/amd3.test')
    for altblk in AlterLists:
        altblk.Print_parse_result()