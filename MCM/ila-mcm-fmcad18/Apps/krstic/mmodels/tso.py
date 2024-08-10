# This is the specification of Sequential Consistency (SC)
import z3
import itertools


#---AUX------------------

ctr = 0
def uniqueName():
    global ctr
    ctr += 1
    return "wvop"+str(ctr)

def localStates(ts):
    return ts.inst.stlocal

# tsDefsGroup is a list of 
# (sname, def)

class wvop(object):
    def _entity(self):
        return self.entity
    def __init__(self, ts, tsDefsGroup, TsThatWritesVar, ConstraintList, endStep ):
        self.name = ts.name + "_" + uniqueName()
        self.tid  = ts.tid
        self.entity = ts._entity()
        self.localStates = localStates(ts)
        self.timestamp = z3.Int('n_'+ self.name)
        self.Reads = set([])
        self.decodeExpr = ts.decodeExpr

        self.Writes = set([])
        self.resultDict = {}

        ConstraintList.append( self.timestamp < endStep.timestamp )

        for sname, definition in tsDefsGroup:
            self.Writes.add(sname)
            newDef = z3.Int('def_global_' + self.name + '_' + sname)

            ConstraintList.append( newDef == definition )
            #assert sname in TsThatWritesVar
            #TsThatWritesVar[sname].append(self)
            self.resultDict[sname] = newDef
    def __str__(self):
        return self.name


#---INTERFACE------------------

def bookKeepWrite(ts, TsNameToObj, TsThatWritesVar):
    # keep the same (SC/TSO)
    for sname, func in ts.inst.updateDict.items():
        ts.Writes.add(sname)

tsDefsGroup = []

def regWriteView(sname, z3def, ts):
    if sname not in localStates(ts): # only for shared states
        tsDefsGroup.append( (sname,z3def) )

def createWriteView(ts, TsNameToObj, TsThatWritesVar, ConstraintList):
    global tsDefsGroup
    if len(tsDefsGroup) > 1:
        print '<W> assuming single-copy atomic TSO for ts:', ts.name
        print '<W>     on stateVars:', [x[0] for x in tsDefsGroup]
    elif len(tsDefsGroup) == 0:
        ts.wvopList = []
        tsDefsGroup = []
        return

    endStep = TsNameToObj['tid_0_end_global_']
    # create one external write view operation
    wvop_ext = wvop(ts, tsDefsGroup, TsThatWritesVar, ConstraintList, endStep = endStep)
    ts.wvopList = [wvop_ext]

    tsDefsGroup = []

def addHB_noOrder(ConstraintList,TsPOList):
    # inst -> wvop
    for threadProgram in TsPOList:     # same entity and same thread
        for ts in threadProgram[1:]:
            if len(ts.wvopList) == 0:
                continue
            assert len(ts.wvopList) == 1
            ConstraintList.append( ts.timestamp < ts.wvopList[0].timestamp )
    # re-organize them based on entity
    Entity2TsDict = {}
    for threadProgram in TsPOList:     # same entity and same thread
        for ts in threadProgram[1:]:
            ename = ts._entity()
            if ename not in Entity2TsDict: Entity2TsDict[ename] = []
            Entity2TsDict[ename].append(ts)

    for tsList in Entity2TsDict.values():
        for ts1,ts2 in itertools.combinations(tsList, 2):
            if ts1.wvopList and ts2.wvopList:
                constraint = z3.Implies(ts1.timestamp<ts2.timestamp , ts1.wvopList[0].timestamp < ts2.wvopList[0].timestamp )
                ConstraintList.append ( constraint )
                constraint = z3.Implies(ts2.timestamp<ts1.timestamp , ts2.wvopList[0].timestamp < ts1.wvopList[0].timestamp )
                ConstraintList.append ( constraint )
                if ts1.wvopList[0].Writes.intersection(ts2.wvopList[0].Writes):
                    ConstraintList.append( ts1.wvopList[0].timestamp != ts2.wvopList[0].timestamp )
            # only enforce non eq time if they are write variable have intersection
            if ts1.Writes.intersection(ts2.Writes):
                ConstraintList.append( ts1.timestamp !=  ts2.timestamp )

    # wvop -> wvop
    """
    for tid1 in range(len(TsPOList)):  # same entity cross thread
        for tid2 in range(tid1, len(TsPOList)): # for every pair
            if TsPOList[tid1][1]._entity() != TsPOList[tid2][1]._entity():
                continue
            for ts1 in TsPOList[tid1][1:]:
                if not ts1.wvopList:
                    continue 
                for ts2 in TsPOList[tid2][1:]:
                    if not ts2.wvopList:
                        continue
                    if ts1 is ts2: continue
                    constraint = z3.Implies(ts1.timestamp<ts2.timestamp , ts1.wvopList[0].timestamp < ts2.wvopList[0].timestamp )
                    ConstraintList.append ( constraint )
                    constraint = z3.Implies(ts2.timestamp<ts1.timestamp , ts2.wvopList[0].timestamp < ts1.wvopList[0].timestamp )
                    ConstraintList.append ( constraint )

    for tid1 in range(len(TsPOList)):  # same entity cross thread
        for tid2 in range(len(TsPOList)): # for every pair
            if TsPOList[tid1][1]._entity() != TsPOList[tid2][1]._entity():
                for ts1 in TsPOList[tid1][1:]:
                    for ts2 in TsPOList[tid2][1:]:
                        if ts1 is ts2:
                            continue
                        ConstraintList.append( z3.Or( ts1.timestamp<ts2.timestamp , ts2.timestamp<ts1.timestamp ) )
    
    for threadProgram in TsPOList:     # same entity and same thread
        for tsIdx in range(1,len(threadProgram)):
            for tsIdx2 in range(tsIdx+1, len(threadProgram)):
                ts1 = threadProgram[tsIdx]
                ts2 = threadProgram[tsIdx2]
                ConstraintList.append( z3.Or( ts1.timestamp<ts2.timestamp , ts2.timestamp<ts1.timestamp ) )

    """

def addHB(ConstraintList,TsPOList):
    # inst -> wvop
    # wvop -> wvop
    for tid1 in range(len(TsPOList)):  # same entity cross thread
        for tid2 in range(len(TsPOList)):
            if tid1 == tid2:
                continue
            if TsPOList[tid1][1]._entity() != TsPOList[tid2][1]._entity():
                continue
            for ts1 in TsPOList[tid1][1:]:
                if not ts1.wvopList:
                    continue
                for ts2 in TsPOList[tid2][1:]:
                    if not ts2.wvopList:
                        continue
                    constraint = z3.Implies(ts1.timestamp<ts2.timestamp , ts1.wvopList[0].timestamp < ts2.wvopList[0].timestamp )
                    ConstraintList.append ( constraint )


    for threadProgram in TsPOList:     # same entity and same thread
        prevWVopStamp = None
        for ts in threadProgram[1:]:
            if len(ts.wvopList) == 0:
                continue
            assert len(ts.wvopList) == 1
            ConstraintList.append( ts.timestamp < ts.wvopList[0].timestamp )
            if prevWVopStamp is not None:
                ConstraintList.append( prevWVopStamp < ts.wvopList[0].timestamp )
            prevWVopStamp = ts.wvopList[0].timestamp  # hhb

def make_thread_local_fence(fence_ts, TsPOList, ConstraintList):
    # find the index of the fence_ts in the list
    fence_idx = None
    program   = None
    for threadProgram in TsPOList:
        for tsIdx in range(1,len(threadProgram)):
            if threadProgram[tsIdx].name == fence_ts.name:
                assert fence_idx == None
                fence_idx = tsIdx
                program   = threadProgram
                # must and only appear once
    assert fence_idx is not None
    # now add fence
    for tsIdx in range(1,len(program)):
        if tsIdx < fence_idx:
            # enforce fence onto it
            for wvop_ts in program[tsIdx].wvopList:
                wvop_HB = wvop_ts.timestamp < fence_ts.timestamp
                ConstraintList.append(wvop_HB)
            

def co_hb(w1,w2):
    if w1._entity() == w2._entity() or w1._entity() == 'System:': # coi
        return w1.timestamp < w2.timestamp
    elif w2._entity() == 'System:':
        return False
    else:
        return w1.wvopList[0].timestamp < w2.wvopList[0].timestamp
def fr_hb(r,w):
    if r._entity() == w._entity(): # fri
        return r.timestamp < w.timestamp
    elif w._entity() == 'System:':
        return False
    else:
        return r.timestamp < w.wvopList[0].timestamp

def build_rf_constraint(sname, piVar, TsThatWritesVar, read,write):
    writerTraceSteps = TsThatWritesVar[sname]
    CO_FR_HB = []
    for w2 in writerTraceSteps:
        if w2 is read or w2 is write:
            continue
        # j < i or k < j
        hb = z3.Implies( w2.decodeExpr, z3.Or( co_hb(w2,write) , fr_hb(read,w2) ) )
        CO_FR_HB.append ( hb )

    if not CO_FR_HB:
        co_fr_hb = True
    elif len(CO_FR_HB) == 1:
        co_fr_hb = CO_FR_HB[0]
    else:
        co_fr_hb = z3.And(CO_FR_HB)


    if write._entity() == read._entity() or write._entity() == 'System:':
        # rfi
        w = write
    else:
        # rfe
        w = write.wvopList[0]
    return z3.And( 
            piVar == w.resultDict[sname], 
            w.decodeExpr, 
            w.timestamp < read.timestamp,
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
            print >>logcat, '\t',str(traceStep), 
            if traceStep._entity() == ts._entity():
                print >> logcat, 'RFI '
            elif traceStep._entity() == 'System:':
                print >> logcat, 'RF_init '
            else:
                print >> logcat, 'RFE ',str(traceStep.wvopList[0])
#raw_input()
def extractViewResultForTs(logcat, ts, model):
    for wv in ts.wvopList:
        for sname,definition in wv.resultDict.items():
            print >>logcat, '\t\tupdating global: %s = %s @ %s' % (sname, str( model[definition] ), str( model[wv.timestamp] ) )