# unrolling

import z3 
# -------------------------

DEBUG = True
STRICT_TEMPLATE = True
ONLY_CONSTRAINT_ON_READABLE_PI = True

# -------------------------

ctr = 0


def uniqueName():
    global ctr
    ctr += 1
    return "ts"+str(ctr)

class InitStep(object):
    def __str__(self):
        entity = 'System:'
        return '%s:%d, #INIT#, W:%s,R:%s' % (entity, self.tid, str(self.Writes), str(self.Reads))
    def _entity(self):
        return 'System:'
    def __init__(self, localStates, tid = 0, overwriteTs = None, TsThatWritesVar = None, TsNameToObj = None):
        assert TsThatWritesVar is not None and TsNameToObj is not None
        self.name = 'tid_' + str(tid) + "_init_" + uniqueName()
        self.tid  = tid
        self.localStates = localStates
        if overwriteTs is not None:
            self.timestamp = overwriteTs
        else:
            self.timestamp = z3.Int('n_'+ self.name)
        TsNameToObj[self.name] = self # register itself
        # get read write
        self.Reads = set([])
        self.Writes= set(localStates)
        self.resultDict = {}
        self.decodeExpr = True
        # no need to register read (no read)
        for write in self.Writes:
            if write not in TsThatWritesVar:
                TsThatWritesVar[write] = set([])
            TsThatWritesVar[write].add(self)

        for state in localStates:
            self.resultDict[state] = 0  # assume init to 0

class EndStep(object):
    def __str__(self):
        entity = 'System:'
        return '%s:%d, #END#, W:%s,R:%s' % (entity, self.tid, str(self.Writes), str(self.Reads))
    def _entity(self):
        return 'System:'
    def __init__(self, localStates, tid = 0, overwriteTs = None, TsThatReadsVar = None, TsNameToObj = None, PiVarList = None):
        assert TsThatReadsVar is not None and TsNameToObj is not None and PiVarList is not None
        self.name = 'tid_' + str(tid) + "_end_global_"
        self.tid  = tid
        self.localStates = localStates
        if overwriteTs is not None:
            self.timestamp = overwriteTs
        else:
            self.timestamp = z3.Int('n_'+ self.name)
        TsNameToObj[self.name] = self # register itself
        # get read write
        self.Reads = set(localStates)
        self.Writes = set([])
        self.PiVarList = PiVarList
        #self.Writes= set([])
        #self.resultDict = {}
        #self.decodeExpr = True it should be okay to not have this, if not, bug exists
        # no need to register read (no read)
        for read in self.Reads:
            if read not in TsThatReadsVar:
                TsThatReadsVar[read] = set([])
            TsThatReadsVar[read].add(self)

    def getAssertFormula(self, func ):
        def stateReadFunc(stateName):
            if stateName == "__tid_suffix__":
                return ("_%d_" % self.tid)
            # else:
            # we still need to create pi variable for it
            piVarName = 'pi_end_' + self.name + '_' + stateName
            if piVarName not in self.PiVarList:
                piVar = z3.Int(piVarName)
                self.PiVarList[piVarName] = (stateName, piVar, self)
            else:
                #print '<W>: piVar:', piVarName, 'already created! 2'
                piVar = self.PiVarList[piVarName][1]
            return piVar

        return func(stateReadFunc) #z3.Implies(self.decodeExpr, func(stateReadFunc) ) 


class TraceStep(object):
    def _entity(self):
        return self.entity

    def __str__(self):
        entity = self._entity()
        return '%s:%d, inst:%s, W:%s,R:%s' % (entity, self.tid, self.inst.name, str(self.Writes), str(self.Reads))

    def __init__(self,inst, SysSharedState, tid = 0, TsThatWritesVar = None, TsNameToObj = None, ConstraintList = None, PiVarList = None) : # tell me which instruction to execute
        assert (TsThatWritesVar is not None and TsNameToObj is not None 
            and ConstraintList is not None and PiVarList is not None )
        
        self.TsThatWritesVar = TsThatWritesVar
        self.TsNameToObj     = TsNameToObj
        self.ConstraintList  = ConstraintList
        self.PiVarList       = PiVarList


        self.name = inst.name + "_" + uniqueName()
        self.inst = inst
        self.tid  = tid
        self.entity = inst.entity
        self.SysSharedState  = SysSharedState
        self.TsNameToObj[self.name] = self # register itself
        """
        self.wvopTsNameList = # mm
        self.Reads =  # mm
        self.Write = # mm
        """
        self._getReadWrite()
        self.timestamp = z3.Int('n_'+ self.name)
        self.defVars = {} # state name -> def z3 var

    def BuildFrame(self, lastTraceStep):
        # first get dict
        assert lastTraceStep is not None
        self.resultDict = lastTraceStep.resultDict.copy()
        # remove shared state from result Dict
        for sname in self.SysSharedState:
            if sname in self.resultDict:
                del self.resultDict[sname]
        incomingResultDict = lastTraceStep.resultDict

        def stateReadFunc(stateName):
            if stateName == "__tid_suffix__":
                return ("_%d_" % self.tid)
            if stateName in self.inst.stlocal and stateName not in CrossThreadLocal: # if it is local state, just return from previous step
                return incomingResultDict[stateName]
            # else it is a shared var, create PI variable for it
            piVarName = 'pi_' + self.name + '_' + stateName
            if piVarName not in self.PiVarList:
                piVar = z3.Int(piVarName)
                self.PiVarList[piVarName] = (stateName, piVar, self)
            else:
                #print '<W>: piVar:', piVarName, 'already created! 1'
                piVar = self.PiVarList[piVarName][1]
            return piVar


        decodeExpr = self.inst.decodeFunc(stateReadFunc)
        if STRICT_TEMPLATE:
            self.decodeExpr = z3.And( lastTraceStep.decodeExpr , decodeExpr) # instead of just decodeExpr
        else:
            self.decodeExpr = decodeExpr

        for sname,func in self.inst.updateDict.items():
            # create new variable (definition)
            definition = z3.Int('def_local_' + self.name + '_' + sname )
            value      = func(stateReadFunc)

            if STRICT_TEMPLATE:
                constraint = definition == value 
            else:
                constraint = z3.If (decodeExpr, definition == value , definition == stateReadFunc(sname) )

            self.ConstraintList.append(constraint )

            self.resultDict[sname] = definition

            mm.regWriteView(sname, definition, self) # not passing value
            # make sure it only refers to some var already defined

            self.defVars[sname] = definition
            # so now the extra part of resultDict is the Write/\SysSharedState

        mm.createWriteView(self, self.TsNameToObj, self.TsThatWritesVar, self.ConstraintList) # here it really creates

    def getAssertFormula(self, func ):
        def stateReadFunc(stateName):
            if stateName == "__tid_suffix__":
                return ("_%d_" % self.tid)
            if stateName in self.resultDict:
                return self.resultDict[stateName]
            # else:
            # we still need to create pi variable for it
            piVarName = 'pi_' + self.name + '_' + stateName
            if piVarName not in self.PiVarList:
                piVar = z3.Int(piVarName)
                self.PiVarList[piVarName] = (stateName, piVar, self)
            else:
                #print '<W>: piVar:', piVarName, 'already created! 2'
                piVar = self.PiVarList[piVarName][1]
            return piVar

        return  z3.And(self.decodeExpr, func(stateReadFunc) )  #z3.Implies(self.decodeExpr, func(stateReadFunc) ) 

    def _getReadWrite(self):
        self.Reads = set([])
        self.Writes= set([])
        def setRead(name):
            if name == "__tid_suffix__":
                return ("_%d_" % self.tid)
            self.Reads.add(name)
            return 0

        self.inst.decodeFunc(setRead)
        for sname,func in self.inst.updateDict.items():
            func(setRead)
        # update TsThatReads/WriteVar
        for read in self.Reads:
            if read not in self.TsThatReadsVar:
                self.TsThatReadsVar[read] = set([])
            self.TsThatReadsVar[read].add(self.name)

        # call mm to initial WVop    
        mm.bookKeepWrite(self, self.TsNameToObj, self.TsThatWritesVar)    

        for write in self.Writes:
            if write not in self.TsThatWritesVar:
                self.TsThatWritesVar[write] = set([])
            self.TsThatWritesVar[write].add(self)



    def extractTsResultFromModel(self, model):
        concreteTime = model[self.timestamp]
        decodeCond   = self.decodeExpr if isinstance(self.decodeExpr,bool) else model.eval(self.decodeExpr)
        defCollection = {}
        readCollection = {}

        for sname, z3var in self.defVars.items():
            defCollection[sname] = model[z3var]

        for sname, piVar, tsRef in self.PiVarList.values():
            if tsRef.name == self.name: # if it is on current frame
                readCollection[sname] = model[piVar]

        return concreteTime,decodeCond,defCollection,readCollection



class unroller(object):
    def _sanity_check(self, NoThread, TemplateProgram, localStates, SysSharedState ):
        assert len(NoThread) == len(TemplateProgram) and len(NoThread) == len(localStates)
        # 
        self.entityNameList = []
        for cidx in range(len(NoThread)):
            entityName = None
            core_local_states = set(localStates[cidx])
            for inst in TemplateProgram[cidx]:
                if entityName is None:
                    entityName = inst.entity
                else:
                    assert entityName == inst.entity
                assert set(inst.stlocal) == core_local_states
            assert entityName is not None
            self.entityNameList.append(entityName)

    def __init__(self, NoThread, TemplateProgram, localStates, SysSharedState ):
        """NoThread = (2,1,1) , localStates = [ProcState, DevState, CEState]"""
        self._sanity_check( NoThread, TemplateProgram, localStates, SysSharedState )
        # this will creates entityNameList

        # Bounds
        self.NumOfEntity = len(NoThread)
        self.NoThread = NoThread
        self.TemplateProgram = TemplateProgram
        self.states = []
        self.SysSharedState = SysSharedState
        for s in localStates:
            self.states.extend(s)
        self.states.extend(SysSharedState)

        # unroll related
        self.TsThatReadsVar = {}
        self.TsThatWritesVar = {}
        self.TsNameToObj = {}
        self.TsPOList = []

        self.PiVarList = {} # dict of tuples: z3PiVar, traceStepRef (timestamp)
        self.ConstraintList = []
        self.runConstraintList = []
        self.runTProp = None

        self.logcat = None

        # internal use
        # (entityId,instName,round) -> ts_ref
        self.relTsLookupDict = {}
        self.TsNameToRelLookup = {} # ts name -> (entityId,instName,round)

    def litmus_getRelRefTuple(self,instName, eid , rnd = 1):
        return (eid,instName, rnd)
    def litmus_makeTsLocalFence(self, relRefTuple):
        ts = self.relTsLookupDict[relRefTuple]
        mm.make_thread_local_fence(fence_ts = ts, TsPOList = self.TsPOList, ConstraintList = self.ConstraintList)

    def unroll(self):

        # do unrolling
        tsCnt = 0
        tid = 0

        globalBeginEvent = InitStep( self.SysSharedState + CrossThreadLocal , tid = 0, overwriteTs = 0, TsThatWritesVar = self.TsThatWritesVar, TsNameToObj = self.TsNameToObj)
        globalEndEvent   = EndStep ( self.SysSharedState , tid = 0, TsThatReadsVar = self.TsThatReadsVar, TsNameToObj = self.TsNameToObj, PiVarList = self.PiVarList )
        self.globalBeginEvent = globalBeginEvent
        self.globalEndEvent   = globalEndEvent
        self.TsNameToRelLookup[globalEndEvent.name] = "<rel_should_never_refer_to>"

        # system init events
        for Eidx in range(self.NumOfEntity): # entity idx  # global synchronous reset and local reset!
            nTh = self.NoThread[Eidx]
            for noRound in range(nTh):
                self.TsPOList.append([])
                tid += 1

                carveOutCrossInit = set(self.TemplateProgram[Eidx][0].stlocal) - set(CrossThreadLocal)

                self.TsPOList[-1].append( InitStep(list(carveOutCrossInit), tid, overwriteTs = 0, TsThatWritesVar = self.TsThatWritesVar, TsNameToObj = self.TsNameToObj ) ) # maybe we should use a synchronous init event?
                tsCnt += 1
                for inst in self.TemplateProgram[Eidx]:

                    ts = TraceStep(inst, self.SysSharedState, tid = tid, TsThatWritesVar = self.TsThatWritesVar, 
                        PiVarList = self.PiVarList, TsNameToObj = self.TsNameToObj, ConstraintList = self.ConstraintList, 
                        TsThatReadsVar = self.TsThatReadsVar )

                    self.TsPOList[-1].append( ts )
                    tsCnt += 1
                    relTsLookupKey = (self.entityNameList[Eidx], inst.name, noRound+1 ) 
                    self.relTsLookupDict[relTsLookupKey] = ts
                    self.TsNameToRelLookup[ts.name] = relTsLookupKey

        # global event must precede every other events
        for threadProgram in self.TsPOList:
            tsBegin = threadProgram[1]
            tsEnd   = threadProgram[-1]
            self.ConstraintList.append( tsBegin.timestamp > globalBeginEvent.timestamp)
            self.ConstraintList.append( tsEnd.timestamp < globalEndEvent.timestamp)
            # only constrain on the beginning and ends no need for others

            #ConstraintList.append( ts.timestamp < tsCnt+1 )

        # add Ts PO: including thread local init event
        for threadProgram in self.TsPOList:
            for tsIdx in range(len(threadProgram)-1):
                PO_HB = threadProgram[tsIdx].timestamp < threadProgram[tsIdx + 1].timestamp
                self.ConstraintList.append(PO_HB)

        # For each Ts do Varible Def
        for threadProgram in self.TsPOList:
            for tsIdx in range(1,len(threadProgram)):
                threadProgram[tsIdx].BuildFrame(threadProgram[tsIdx-1])

        mm.addHB(self.ConstraintList, self.TsPOList)

    def enforce_CO_or_FR(self, tp, relId1, relId2):
        assert tp == 'co' or tp == 'fr'
        ts1 = self.relTsLookupDict[ relId1 ]
        ts2 = self.relTsLookupDict[ relId2 ]

        if tp == 'co':
            constraint = mm.co_hb(ts1, ts2)
        elif tp == 'fr':
            constraint = mm.fr_hb(ts1, ts2)

        self.ConstraintList.append(constraint)


    def finalizePiFun(self, rf_force = {} ): # rf_force is a dict of rf-relation: read (KEY) <- write
        # print log
        rf_force_local = rf_force.copy() # make a copy because we will modify it
        if DEBUG:
            mm.printPossibleReadFrom(self._logcat(), self.PiVarList.values(), self.TsThatWritesVar)
        # add PI function
        for sname, piVar, ts in self.PiVarList.values(): # k
            timestamp = ts.timestamp
            writerTraceSteps = self.TsThatWritesVar[sname] #mm.possibleRFts(TsThatWritesVar, sname, ts)

            OrClauses = []

            # lookup if the read is registered as a special rf relation
            read_relId_tuple = self.TsNameToRelLookup[ts.name]

            if read_relId_tuple in rf_force_local:
                # ts->tuple->lookup in rf_force (find the write)->back to ref
                writeTsRef = self.relTsLookupDict[ rf_force_local[ read_relId_tuple ] ]
                #print writeTsRef.name,ts.name
                assert writeTsRef is not ts
                constraint = mm.build_rf_constraint(sname, piVar,self.TsThatWritesVar,  read = ts, write = writeTsRef)
                if ONLY_CONSTRAINT_ON_READABLE_PI:
                    constraint = z3.Implies(ts.decodeExpr, constraint)
                OrClauses = [constraint]
                del rf_force_local[ read_relId_tuple ]

            else:
                for traceStep in writerTraceSteps: # i
                    if traceStep is ts:
                        continue
                    constraint = mm.build_rf_constraint(sname, piVar,self.TsThatWritesVar,  read = ts, write = traceStep)
                    if ONLY_CONSTRAINT_ON_READABLE_PI:
                        constraint = z3.Implies(ts.decodeExpr, constraint)                
                    OrClauses.append(constraint)
            # special case:
            # read from initial (rf_init)

            if len(OrClauses) == 0:
                print '<E>: no writer for state: ',sname,'. It should at least appear in the init steps.'
                assert False
            elif len(OrClauses) == 1:
                self.ConstraintList.append( OrClauses[0])
            else:
                self.ConstraintList.append( z3.Or(OrClauses) )
# assertion (properties)
# for all tracestep on Dev End
# so such PC = and ... = 
    
    def addPropertyOnSingleFrames(self, runProperty, frameCond):
        """
        runProperty = lambda state: z3.And( state('SMImageAddr') == BAD_IMAGE , state('DevPC') == IMImageAddr )
        frameCond   = lambda ts: ts.entity == 'device:'
        """
        for threadProgram in self.TsPOList:
            for ts in threadProgram[1:]: # not working on the initial one anyway
                if frameCond(ts):
                    self.runConstraintList.append( ts.getAssertFormula(runProperty) )

    def addPropertyOnEnding(self,runProperty):
        self.runConstraintList.append( self.globalEndEvent.getAssertFormula(runProperty) )


    def dumpDebugInfoToFile(fname):
        self.logcat = open(fname,'wt') 
    def _logcat(self):
        if self.logcat is not None:
            return self.logcat
        self.logcat = open("log/unroll.log",'wt') 
        return self.logcat


    def printModel(self):
        for threadProgram in self.TsPOList:
            print >>self.logcat, threadProgram[1]._entity()," #%d" % threadProgram[1].tid
            for ts in threadProgram[1:]:
                t,d,val,readCol = ts.extractTsResultFromModel(self.model)
                print >>self.logcat, '@%s, %s:%s'%(str(t), ts.inst.name, d)
                for n,v in readCol.items():
                    print >>self.logcat, '\t (Read %s = %s)' % (n,str(v))

                for n,v in val.items():
                    print >>self.logcat, '\t %s:%s' % (n,str(v))
                # display related views    
                mm.extractViewResultForTs(self.logcat, ts, self.model)

    def buildRunProp(self, func = z3.And):
        self.runTProp = func(self.runConstraintList)
        print >> self.logcat, 'runProp :', self.runTProp        

    def pushInstConstraintAndCheck(self):
        self.solver = z3.Solver()
        s = self.solver
        s.set(unsat_core=True if DEBUG else False)

        idx = 0
        for c in self.ConstraintList:
            if DEBUG:
                print >>self.logcat, idx,':', c
            #raw_input()
                s.assert_and_track(c,'n'+str(idx))
                idx += 1
            else:
                s.add(c)

        result = s.check()
        print 'w.o. run Property:', result 

        self.modelCheckResult = result

        if result == z3.sat:
            self.model  = s.model()
        else: # unsat
            if DEBUG:
                print >>self.logcat, s.unsat_core()
            print '<W>: Not all the reads can be executed! Trace debug info dumped.'

        return result


    def solve(self):
        if self.modelCheckResult == z3.unsat:
            print '<W>: inconsistent model. Won\'t continue to check the properties.'
            return

        s = self.solver

        if self.runTProp is None and self.runConstraintList:
            print '<E>: you need to call buildRunProp to provide proper way to chain runProp together'
            assert False 
        elif self.runTProp is None and not self.runConstraintList:
            print '<INFO>: no run property specified. Won\'t continue.'
            return
        else:
            s.assert_and_track(self.runTProp,'rp')
            # extract module
            result = s.check()
            print result

        if result == z3.unsat: # this may use the old one
            if DEBUG:
                print >>self.logcat, s.unsat_core()
        elif result == z3.sat:
            self.model  = s.model()
            self.printModel()
        else:
            print 'status Unknown'

        self.logcat.close()
        self.logcat = None
        return result


# this is a dirty fix
CrossThreadLocal = ['active','DevIdx1','DevIdx2']

def test_main():
    import OoO as soc
    #import soc
    NoThread = (2,2,2);
    localStates = ( soc.ProcState, soc.DevState, soc.CEState )
    TemplateProgram = ( soc.ProcInst, soc.DevInst, soc.CEInst )
    SysSharedState  = soc.SysSharedState

    runProperty = lambda state: z3.And( state('IMImageAddr') == soc.BAD_IMAGE , state('DevPC') == soc.IMImageAddr )
    frameCond   = lambda ts: ts.entity == 'device:'

    unroll = unroller(NoThread = NoThread, localStates = localStates, 
        TemplateProgram = TemplateProgram, SysSharedState = SysSharedState)

    unroll.unroll()
    unroll.addPropertyOnSingleFrames( runProperty = runProperty, frameCond = frameCond)
    unroll.finalizePiFun()
    unroll.buildRunProp(func = z3.Or)
    unroll.pushInstConstraintAndCheck()
    #unroll.printModel()
    unroll.solve()


if __name__ == '__main__':
    test_main()


