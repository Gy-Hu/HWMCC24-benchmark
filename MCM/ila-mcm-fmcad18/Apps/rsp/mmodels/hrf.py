import z3

def HB(e1,e2):
    return e1.timestamp < e2.timestamp

def HBd(a,b):
    return z3.Implies( z3.And( a.inst.decodeFunc, b.inst.decodeFunc), a.timestamp < b.timestamp )

def co_hb(w1,w2):
    return w1.timestamp < w2.timestamp
def fr_hb(r,w):
    return r.timestamp < w.timestamp

def either_or(a,b):
    return ( a and not b ) or (b and not a)
def imply(a,b):
    return (not a) or b

def _check_state_is_correctly_and_indeed_updated_in_tracestep(sname, ts):
    assert sname in ts.inst.updateDict or "decodeFunc" in ts.__dict__ # it is a true write or a all write

def build_rf_constraint(sname, piVar, VAddr, TsThatWritesVar, read,write, AllWriteTsList = []): # only talks about possiblity 
    #                                                             dest, src
    writerTraceSteps = TsThatWritesVar.get(sname,[])
    CO_FR_HB = []

        # check for updateDict, 
        # overWriteDict
        # massiveUpdate 
        # addrMatch => co_hb \/ fr_hb
        # 

    # first construct a read-from relation:
    _check_state_is_correctly_and_indeed_updated_in_tracestep(sname, write)

    OR_RF = [] #  will be or-ed together
    if sname in write.inst.updateDict:
        data, addr = write.inst.updateDict[sname] 
        OR_RF.append( z3.And( addr == VAddr , write.inst.decodeFunc , HBd(  write, read ) ,  piVar == data ) )
    else:
        OR_RF.append( z3.And( HB(write,read), write.inst.decodeFunc,  piVar == write.state(sname, VAddr) ) ) 
        # inst decode is true any way
        # addr match need no mention
 
    if len(OR_RF) == 1:
        or_rf_hb = OR_RF[0]
    else:
        or_rf_hb = z3.Or(OR_RF)
    

    CO_FR_HB = []
    for w2 in list(writerTraceSteps) + AllWriteTsList:
        if w2 is read or w2 is write:
            continue
        # j < i or k < j
        _check_state_is_correctly_and_indeed_updated_in_tracestep(sname , w2)

        co_fr_per_write_list = []
        if sname in w2.inst.updateDict:
            data, addr = w2.inst.updateDict[sname]
            co_fr_per_write_list.append( z3.Implies( z3.And( addr == VAddr , w2.inst.decodeFunc ) , z3.Or( HB( w2,write ) , HBd( read , w2 ) ) ) )
        else:
            co_fr_per_write_list.append( z3.Or( HB( w2, write ) , HBd( read, w2 ) ) )
        CO_FR_HB.append( z3.And( co_fr_per_write_list ) )

    if not CO_FR_HB: # len == 0
        co_fr_hb = True
    elif len(CO_FR_HB) == 1:
        co_fr_hb = CO_FR_HB[0]
    else:
        co_fr_hb = z3.And(CO_FR_HB)

    return z3.And( or_rf_hb , co_fr_hb )
    
    
