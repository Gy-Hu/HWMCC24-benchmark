# This is the specification of Sequential Consistency (SC)
import z3

def bookKeepWrite(ts, TsNameToObj, TsThatWritesVar):
    # keep the same (SC/TSO)
    for sname, func in ts.inst.updateDict.items():
        ts.Writes.add(sname)


def regWriteView(sname, z3def, ts):
    pass

def createWriteView(ts, TsNameToObj, TsThatWritesVar, ConstraintList):
    pass


def addHB(ConstraintList, ts):
    pass


def make_thread_local_fence(fence_ts, TsPOList, ConstraintList):
    pass

def co_hb(w1,w2):
    return w1.timestamp < w2.timestamp
def fr_hb(r,w):
    return r.timestamp < w.timestamp

def build_rf_constraint(sname, piVar, TsThatWritesVar, read,write):
    writerTraceSteps = TsThatWritesVar[sname]
    CO_FR_HB = []
    for w2 in writerTraceSteps:
        if w2 is read or w2 is write:
            continue
        # j < i or k < j
        hb = z3.Or( co_hb(w2,write) , fr_hb(read,w2) )
        CO_FR_HB.append ( hb )

    if not CO_FR_HB:
        co_fr_hb = True
    elif len(CO_FR_HB) == 1:
        co_fr_hb = CO_FR_HB[0]
    else:
        co_fr_hb = z3.And(CO_FR_HB)

    return z3.And( 
            piVar == write.resultDict[sname], 
            write.decodeExpr, 
            write.timestamp < read.timestamp,
            co_fr_hb )



#---DEBUG------------------------
def printPossibleReadFrom(logcat, PiVarList, TsThatWritesVar):
    for sname, piVar, ts in PiVarList:
        print >>logcat, 'PI:',piVar, ' of state: ',sname, 'on ts:'
        print >>logcat, str(ts)
        print >>logcat, 'possible read-from:'
        writerTraceSteps = TsThatWritesVar[sname]
        for traceStep in writerTraceSteps:
            if traceStep is ts: continue
            print >>logcat, '\t',str(traceStep)

def extractViewResultForTs(logcat, ts,model):
    pass # no other info

#---AUX------------------


def localStates(ts):
    return ts.inst.stlocal