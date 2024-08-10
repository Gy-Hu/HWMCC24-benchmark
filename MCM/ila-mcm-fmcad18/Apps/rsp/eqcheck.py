from traceStep import *
import axiom


# ---------------------------
# Configurations
# ---------------------------

FORCE_ALL_INST_DECODE_TRUE = True
DEBUG = False


# ---------------------------
# Prerequisites
# ---------------------------




def LAnd(l):
    if len(l) == 0:
        return z3.BoolVal(True)
    elif len(l) == 1:
        return l[0]
    else:
        return z3.And(l)

def LOr(l):
    if len(l) == 0:
        return z3.BoolVal(True)
    elif len(l) == 1:
        return l[0]
    else:
        return z3.Or(l)

# ---------------------------



# clInstruction = openclrsp.CL_load_DV_N
# gpuInstruction = [ gpuModel.ev_FETCH_L1 , gpuModel.inst_LD , gpuModel.inst_INV_L1_WG ]

wvopListTp = namedtuple('wvopListTp','WG DV addr value')
rvopListTp = namedtuple('rvopListTp','WG DV addr value')

prevEVsequence = { gpuModel.inst_LD: [gpuModel.ev_FETCH_L1] ,
                   gpuModel.inst_INC_L1 : [gpuModel.ev_FETCH_L1] }

postEVsequence = {
    gpuModel.inst_ST: [ gpuModel.ev_FLUSH_L1,  gpuModel.ev_DEQLOC_L1 ],  # fetch will also need this
    gpuModel.inst_INC_L1 : [ gpuModel.ev_FLUSH_L1 , gpuModel.ev_DEQLOC_L1 ]
}
blockSequence = {
    gpuModel.inst_FLU_L1_DV : gpuModel.ev_DEQMARKER_L1,  # will wait for many of it
    gpuModel.inst_FLU_L1_WG : gpuModel.ev_DEQMARKER_L1
}
# pre is already modeled in the sequence

rfMapInst = { 
    openclrsp.CL_load_na_or_WG: [ gpuModel.inst_LD ],
    openclrsp.CL_load_DV_N:     [ gpuModel.inst_LD , gpuModel.inst_INV_L1_WG ], #Corret : [ gpuModel.inst_LD , gpuModel.inst_INV_L1_WG ], # wrong implementation: [ gpuModel.inst_INV_L1_WG , gpuModel.inst_LD   ],
    openclrsp.CL_load_DV_R:     [ gpuModel.inst_LD , gpuModel.inst_FLU_L1_DV  ,  gpuModel.inst_INV_L1_WG ], #[ gpuModel.inst_LK_L2, gpuModel.inst_FLU_L1_DV, gpuModel.inst_INV_L1_WG, gpuModel.inst_LD, gpuModel.inst_UL_L2 ],  # new: [ gpuModel.inst_LD , gpuModel.inst_FLU_L1_DV  ,  gpuModel.inst_INV_L1_WG ]  original : [ gpuModel.inst_LK_L2, gpuModel.inst_FLU_L1_DV, gpuModel.inst_INV_L1_WG, gpuModel.inst_LD, gpuModel.inst_UL_L2 ]
    openclrsp.CL_store_na_or_WG:[ gpuModel.inst_ST ],
    openclrsp.CL_store_DV_N:    [ gpuModel.inst_FLU_L1_WG,  gpuModel.inst_ST ],
    openclrsp.CL_store_DV_R:    [ gpuModel.inst_LK_rmw_DV, gpuModel.inst_FLU_L1_DV, gpuModel.inst_INV_L1_DV, gpuModel.inst_ST, gpuModel.inst_FLU_L1_WG, gpuModel.inst_INV_L1_DV, gpuModel.inst_UL_rmw_DV ], # Wrong : [ gpuModel.inst_LK_L2, gpuModel.inst_FLU_L1_WG, gpuModel.inst_ST, gpuModel.inst_INV_L1_DV, gpuModel.inst_UL_L2 ], # this was the wrong thing
    openclrsp.CL_fetch_inc_WG:  [ gpuModel.inst_INC_L1 ]
 }


def HB(a,b):
    return a.timestamp < b.timestamp

def HBd(a,b):
    return z3.Implies( z3.And( a.inst.decodeFunc, b.inst.decodeFunc), a.timestamp < b.timestamp )



# =============================================
#                EQ CHECKER
# =============================================


class eqchecker(object):
    def __init__(self,  num_dev, num_wg, num_t):
        self.PiVarList = {} # pi_var_name (ts + statename) -> [ (sname, pivar, ts, addr ) ]
        self.PiVarListOld = {}
        self.TsThatWritesVar = {}
        self.TsThatWritesVarOld = {}
        self.TsNameToObj     = {}
        self.ConstraintList  = []
        self.runProp = []

        self.num_of_parent_inst_in_scene = 0
        self.tsList = [] # Note this is not a list of PO

        self.PrevDecode = None # Note that the prev decode may be in 

        self.num_dev, self.num_wg, self.num_t = num_dev, num_wg, num_t

        self.ConstrainedPiVarNames = set([]) # set of String : name of the PiVar 

        self.L1fr_read_from = {} # ld --> fetch (if fetch.decode then must read from fetch else must others)
        # ======================================
        # below is the content of the collector
        # ======================================

        self.load_na_or_WG_list = []
        self.load_DV_N_list = []
        self.load_DV_R_list = []
        self.store_na_or_WG_list = []
        self.store_DV_N_list = []
        self.store_DV_R_list = []
        self.LOAD_list = []
        self.STORE_list = []
        self.rmw_list = []
        self.name_to_list_mapping = {'load_na_or_WG':[self.load_na_or_WG_list, self.LOAD_list],
            'load_DV_N':[self.load_DV_N_list ,self.LOAD_list],
            'load_DV_R':[self.load_DV_R_list ,self.LOAD_list],
            'store_na_or_WG':[self.store_na_or_WG_list ,self.STORE_list],
            'store_DV_N':[self.store_DV_N_list ,self.STORE_list],
            'store_DV_R':[self.store_DV_R_list ,self.STORE_list],
            'fetch_inc_WG':[self.rmw_list, self.LOAD_list,self.STORE_list],
            }

    def addToList(self,inst):   
        for lref in self.name_to_list_mapping[inst.name]:
            lref.append(inst)

    def addParentInst(self, addr, reg, e1, inst_func):
        def dummyRead(sname,addr = 0, entity = 0):
            return 0
        #state = lambda stateName, addr = None , overWriteVA = None: ts1.stateReadFunc(stateName,addr,overWriteVA)

        paramDict = {'x': addr, 'r' :reg, 'Eid': e1 , 'state':dummyRead }
        inst = inst_func( **paramDict )
        self.addToList(inst)
        return inst


    def addInstToScene(self, addr, reg, e1, inst_func, decodeWaitList, slot = None): 
        # need to plug-in additional decode in the beginning, if it is not None, will add
        # unless specify slot, will not provide
        # addr = z3.Int('addr'+str(self.num_of_inst_in_scene) ) # the order here matters
        # reg  = z3.Int('reg' +str(self.num_of_inst_in_scene) ) # the order here matters
        # and you need to check if you need an entity or not
        # e1 = self._genEntity() # entity for the instruction

        ts1 = TraceStep(entity = e1, 
            TsThatWritesVar = self.TsThatWritesVar , 
            TsNameToObj = self.TsNameToObj, 
            ConstraintList = self.ConstraintList, 
            PiVarList = self.PiVarList )
        self.tsList.append(ts1) # tsList is gathering all these

        # concretize the instruction 
        state = lambda stateName, addr = None , entity = None: ts1.stateReadFunc(stateName,addr,entity)

        paramDict = {'x': addr, 'r' :reg, 'Eid': e1 , 'state':state, 'num_dev':self.num_dev, 'num_wg': self.num_wg , 'num_t': self.num_t }
        if slot is not None:
            paramDict['slot'] = slot

        inst = inst_func( **paramDict ) # get the instruction

        # here is the logic for the pause after flush
        if decodeWaitList is not None: # then it should be a list
            if len( decodeWaitList ) == 1:
                extraDecodeExpr = ts1.stateReadFunc( 'L1fifotail' ) == decodeWaitList[0] # Previous is FLU_WG
            else:
                assert len( decodeWaitList ) == self.num_wg
                extraDecodeExpr = z3.And( [ \
                    ts1.stateReadFunc('L1fifotail' , entity = gpuModel.entity(e1.d, wgId )  ) == decodeWaitList[wgId] \
                    for wgId in range(self.num_wg) ] )

            inst.decodeFunc = z3.And( inst.decodeFunc, extraDecodeExpr )
            # change the decode function when necessary
        ts1.assignInst(inst)            #  r
        return inst,ts1




    # PO relations are added by axioms
    # w/r vop relations are added by axioms
    # prev decode may be in effect for another instruction, but not in our case
    # but still it would be best to add parent instruction according their program order ??


    def addAChain(self, Eid, parentInstruction, childInstructions, prevTimeStamp): # for one parent-instruction -> should return one child instruction
        #             entity
        # gen addrs
        addr = z3.Int('addr'+str(self.num_of_parent_inst_in_scene) ) # the order here matters
        reg  = z3.Int('reg' +str(self.num_of_parent_inst_in_scene) ) # the order here matters
        # and you need to check if you need an entity or not
        # e1 = self._genEntity() # entity for the instruction
        self.num_of_parent_inst_in_scene += 1

        pInst_ref = self.addParentInst(addr = addr, reg = reg, e1 = Eid, inst_func = parentInstruction) #addr, reg, e1, inst_func

        prevTs = None

        blockSeqSlotList = []
        instructions_in_the_chain = []

        for uinst in childInstructions:
            _ , tsRef = self.addInstToScene(addr = addr, reg = reg, e1 = Eid, inst_func = uinst, decodeWaitList = self.PrevDecode )
            instructions_in_the_chain.append(tsRef)

            self.ConstraintList.append( tsRef.timestamp > prevTimeStamp ) 
            # every child instruction step is later than init or the previous barrier (not including evs)
            if prevTs is not None:
                self.ConstraintList.append( HB(prevTs, tsRef) ) # tsRef.timestamp > prevTs.timestamp ) 
                # constraint 2: child instruction po
            else: # prevTs is None
                assert self.PrevDecode is None
                # check that flush is not the last child instruction !!!
            self.PrevDecode = None # reset it 

            # constraint #3: child instructions must be executed
            self.ConstraintList.append( tsRef.inst.decodeFunc  ) # Constriant DECODE


            # here, start to
            # check the need to add additional environmental transition
            if uinst in prevEVsequence: # FETCH -> LD
                seq = prevEVsequence[uinst]
                assert len(seq) == 1 # we only handle the case with one fetch (RVOP)
                fetch_ev = seq[0]
                inst_sub, tsRef_sub = self.addInstToScene(addr = addr , reg = reg, e1 = Eid, inst_func = fetch_ev, decodeWaitList = None, slot = None)
                # we don't require its decode to be true
                valueToBeWritten = tsRef.inst.updateDict[gpuModel.setSname('r',Eid)][0] # get from updateDict
                pInst_ref.rvop = rvopListTp( WG = tsRef, DV = tsRef_sub, addr = addr, value = valueToBeWritten )
                pInst_ref.timestamp = tsRef.timestamp
                self.ConstraintList.append( HBd(tsRef_sub, tsRef) ) # only guarantee if both decodes are true
                self.ConstraintList.append( tsRef_sub.timestamp > 0 )
                self.L1fr_read_from[tsRef] = tsRef_sub



            if uinst in postEVsequence: # ST -> will 
                seq = postEVsequence[uinst]
                parent_or_prev_ts = tsRef # the one that will happenBefore it
                tmpTsList = []
                # get the slot
                storeFIFOSlot = tsRef.stateReadFunc('L1fifotail')
                for post_inst in seq:
                    inst_sub, tsRef_sub = self.addInstToScene(addr = addr , reg = reg, e1 = Eid, inst_func = post_inst, decodeWaitList = None, slot = storeFIFOSlot)
                    self.ConstraintList.append( HB(parent_or_prev_ts, tsRef_sub) ) # parent_or_prev_ts.timestamp < tsRef_sub.timestamp )
                    self.ConstraintList.append( tsRef_sub.timestamp > 0 )
                    # 
                    parent_or_prev_ts = tsRef_sub
                    tmpTsList.append(tsRef_sub)

                valueToBeRead = tsRef.stateReadFunc('r', addr = reg) # get from read its local register value
                pInst_ref.wvop = wvopListTp( WG =  tsRef, DV = tmpTsList[0], addr = addr, value = valueToBeRead )
                pInst_ref.timestamp = tsRef.timestamp


            if uinst in blockSequence: # FLUSH: either the device or workgroup 
                blockSeqSlotList = []
                flush_ev = blockSequence[uinst] # it will only be one instruction
                # but still you won't need to change decode ?
                if uinst is gpuModel.inst_FLU_L1_DV:
                    # in this case we will need to create #WG flush MARKER and 
                    for wgId in range(self.num_wg):
                        # read the slot from tsRef 
                        DEQ_MARKER_ENTITY = gpuModel.entity(Eid.d, wgId )

                        slot = tsRef.stateReadFunc( 'L1fifohead' , entity = DEQ_MARKER_ENTITY)  # dep marker will need this 
                        blockSeqSlotList.append(slot + 1)
                        # create a ts after it
                        inst_sub, tsRef_sub = self.addInstToScene(addr = addr , reg = reg, e1 = DEQ_MARKER_ENTITY, inst_func = flush_ev, decodeWaitList = None, slot = slot)
                        self.ConstraintList.append( HB(tsRef, tsRef_sub) ) # tsRef_sub.timestamp > tsRef.timestamp )
                        self.ConstraintList.append( tsRef_sub.timestamp > 0 )
                    # concat decode for all Wg
                    # may be we can directly instantiate the function (to z3expr) here without calling it 
                    self.PrevDecode = blockSeqSlotList 

                elif uinst is gpuModel.inst_FLU_L1_WG:
                    slot = tsRef.stateReadFunc('L1fifohead') # dep marker will need this 
                    flush_ev = blockSequence[uinst] # it will only be one instruction
                    
                    self.PrevDecode = [ slot +1 ]

                    inst_sub, tsRef_sub = self.addInstToScene(addr = addr , reg = reg, e1 = Eid, inst_func = flush_ev, decodeWaitList = None, slot = slot)
                    self.ConstraintList.append( HB(tsRef, tsRef_sub) ) # tsRef_sub.timestamp > tsRef.timestamp )
                else:
                    assert False # we won't support other cases

                # depends on which one WG or DV
                # we need to add decode expr once or all

            # add happen before before instructions
            prevTs = tsRef
        # set the end and start
        pInst_ref.begin = instructions_in_the_chain[0]
        pInst_ref.end   = instructions_in_the_chain[-1]
        return instructions_in_the_chain

# Let's add pi function
    def setPiFunAW(self, PiVarList , TsThatWritesVar, AllWriteTsList ): # by default should be self.PiVarList
        for sname, piVar, tsRef, VAddr in PiVarList.values():
            # check its name, so repetition
            piVarName = str(piVar)
            if piVarName in self.ConstrainedPiVarNames:
                continue # else:
            self.ConstrainedPiVarNames.add(piVarName)

            timestamp = tsRef.timestamp

            writerTraceSteps = TsThatWritesVar.get(sname,[])

            fetch_ts = None
            if gpuModel.removeEntity(sname) == 'L1fr' and tsRef in self.L1fr_read_from:
                fetch_ts = self.L1fr_read_from[tsRef]
                # fetch_ts.inst.decodeFunc => rf
                constraint = mm.build_rf_constraint(sname, piVar, VAddr, TsThatWritesVar,  read = tsRef, write = fetch_ts, AllWriteTsList = []) # 3 update check
                constraint = z3.Implies( fetch_ts.inst.decodeFunc , z3.Implies( tsRef.inst.decodeFunc , constraint ))
                self.ConstraintList.append( constraint )

            OrClauses = []

            for traceStep in list(writerTraceSteps) + AllWriteTsList:
                if traceStep is tsRef: continue
                if traceStep is fetch_ts: continue # this will disallow read from the fetch
                constraint = mm.build_rf_constraint(sname, piVar, VAddr, TsThatWritesVar,  read = tsRef, write = traceStep, AllWriteTsList = AllWriteTsList) # 3 update check
                constraint = z3.Implies( tsRef.inst.decodeFunc , constraint ) #  check decode 
                OrClauses.append(constraint)
                # but we will add all the inst to be true???
            if fetch_ts is not None:
                self.ConstraintList.append( z3.Implies( z3.Not(fetch_ts.inst.decodeFunc), z3.Or(OrClauses) ) )
            else:
                self.ConstraintList.append( z3.Or(OrClauses) )


    def POAhead2Store(self, parent_instruction_1, e1, parent_instruction_2, e2):
        def constrainIntervals(ts1,ts2):
            # ts1 is the init , and ts2 is the interval
            assert len(ts1.L1FifoTails) == len(ts2.L1FifoTailDeltas)
            assert len(ts1.L1FifoHeads) == len(ts2.L1FifoHeadDeltas)
            assert len(ts1.L1FifoTails) == len(ts2.L1FifoHeads)
            for sname in ts1.L1FifoHeads.keys(): # this is actually for all dw
                head_name = sname
                tail_name = sname.replace('head','tail')
                self.ConstraintList.append( ts1.L1FifoHeads[head_name] >= 0 )
                self.ConstraintList.append( ts1.L1FifoTails[tail_name] >= 0 )
                self.ConstraintList.append( ts1.L1FifoHeads[head_name] >= ts1.L1FifoTails[tail_name] )

                self.ConstraintList.append( ts2.L1FifoHeadDeltas[head_name] >= 0 )
                self.ConstraintList.append( ts2.L1FifoTailDeltas[tail_name] >= 0 )
                self.ConstraintList.append( ts2.L1FifoHeadDeltas[head_name] == ts2.L1FifoTailDeltas[tail_name] )
            # these are the environmental constraint

        #first get the micro instructions
        tsInit = InitStep_fifo( num_dev = self.num_dev, num_wg = self.num_wg, num_t = self.num_t, TsNameToObj = self.TsNameToObj , overwriteTimeStamp = 0 )
        self.tsList.append( tsInit )

        tsBList = self.addAChain( parentInstruction = parent_instruction_1, Eid = e1, 
            childInstructions = rfMapInst[ parent_instruction_1 ], prevTimeStamp = tsInit.timestamp )

        tsInterval = IntervalStep_fifo( num_dev = self.num_dev, num_wg = self.num_wg, num_t = self.num_t, TsNameToObj = self.TsNameToObj,
            TsThatWritesVar = self.TsThatWritesVar ,  ConstraintList = self.ConstraintList , PiVarList = self.PiVarList  )
        self.tsList.append( tsInterval )

        tsU = self.addAChain( parentInstruction = parent_instruction_2, Eid = e2, 
            childInstructions = rfMapInst[ parent_instruction_2 ], prevTimeStamp = tsInterval.timestamp )

        self.ConstraintList.append( HB(tsInit,tsBList[0]) ) # do we really need this?
        self.ConstraintList.append( HB(tsBList[-1],tsInterval) )
        # tsInterval --HB--> tsU is guaranteed by addAChain
        
        self.setPiFunAW( PiVarList = self.PiVarList, TsThatWritesVar = self.TsThatWritesVar, AllWriteTsList = [tsInit, tsInterval] )

        ## TODO:  add the invariants
        constrainIntervals(tsInit,tsInterval)

    def POAfter2Load(self, parent_instruction_1, e1, parent_instruction_2, e2):
        #first get the micro instructions
        # add init frame
        # add instr @ check frame
        # add instr that separate
        # add inst @ after frame
        tsInit = InitStep_any( num_dev = self.num_dev, num_wg = self.num_wg, num_t = self.num_t, TsNameToObj = self.TsNameToObj , overwriteTimeStamp = 0 )
        self.tsList.append(tsInit)
        tsUnderCheck = self.addAChain( parentInstruction = parent_instruction_1, Eid = e1, 
            childInstructions = rfMapInst[parent_instruction_1], prevTimeStamp = tsInit.timestamp )
        tsInterval = IntervalStep_frKeep( num_dev = self.num_dev, num_wg = self.num_wg, num_t = self.num_t, TsNameToObj = self.TsNameToObj,
            ConstraintList = self.ConstraintList , PiVarList = self.PiVarList  )
        self.tsList.append(tsInterval)

        # here let's backup the whole thing
        """ push pi var to a stack """
        #self.setPiFun(init = tsInit, PiVarList = self.PiVarList, TsThatWritesVar = self.TsThatWritesVar)
        #self.PiVarListOld = self.PiVarList #.update(self.PiVarList)
        #self.PiVarList = {}
        """ push TsThatWritesVar """
        #self.TsThatWritesVarOld = self.TsThatWritesVar #.update(self.TsThatWritesVar)
        #self.TsThatWritesVar = {}
        tsAfterCheck = self.addAChain( parentInstruction = parent_instruction_2, Eid = e2, 
            childInstructions = rfMapInst[parent_instruction_2], prevTimeStamp = tsInterval.timestamp ) # instructions are PO after tsInterval
        # this will update the PiVarList associated with IntervalStep_frKeep
        # 

        #self.setPiFun(init = tsInterval, PiVarList = self.PiVarList, TsThatWritesVar = self.TsThatWritesVar)
        self.setPiFunAW( PiVarList = self.PiVarList, TsThatWritesVar = self.TsThatWritesVar, AllWriteTsList = [tsInit, tsInterval] )
        # redo this, but the constrained ones should be okay, because no repetition is there
        self.setPiFunAW( PiVarList = self.PiVarList, TsThatWritesVar = self.TsThatWritesVar, AllWriteTsList = [tsInit, tsInterval] )
        # do it twice because in the first case, there are pi var generated (on demand) 

        #assert ('pi_intervalts5_L1fr@0,0addr0' in self.PiVarList)
        #assert ('pi_intervalts5_L1fr@0,0addr1' in self.PiVarList)

        self.ConstraintList.append( HB(tsInit,tsUnderCheck[0]) )  # do we really need this?
        self.ConstraintList.append( HB(tsUnderCheck[-1],tsInterval) )
        # self.ConstraintList.append( HB(tsInterval,tsAfterCheck[0]) )  # we don't need this, it is already enforced

        ## TODO:  add the invariants
    
    # you will need rf relation as a function
    def PO3SLL(self, parent_instruction_1, e1, parent_instruction_2, e2, parent_instruction_3, e3): # for store_DV_Rs : axiom 3
        def constrainIntervals(ts1): #,ts2):
            # ts1 is the init , and ts2 is the interval
            #assert len(ts1.L1FifoTails) == len(ts2.L1FifoTailDeltas)
            #assert len(ts1.L1FifoHeads) == len(ts2.L1FifoHeadDeltas)
            #assert len(ts1.L1FifoTails) == len(ts2.L1FifoHeads)
            for sname in ts1.L1FifoHeads.keys(): # this is actually for all dw
                head_name = sname
                tail_name = sname.replace('head','tail')
                self.ConstraintList.append( ts1.L1FifoHeads[head_name] >= 0 )
                self.ConstraintList.append( ts1.L1FifoTails[tail_name] >= 0 )
                self.ConstraintList.append( ts1.L1FifoHeads[head_name] >= ts1.L1FifoTails[tail_name] )

                #self.ConstraintList.append( ts2.L1FifoHeadDeltas[head_name] >= 0 )
                #self.ConstraintList.append( ts2.L1FifoTailDeltas[tail_name] >= 0 )
                #self.ConstraintList.append( ts2.L1FifoHeadDeltas[head_name] == ts2.L1FifoTailDeltas[tail_name] )
            

        #first get the micro instructions
        tsInit = InitStep_fifo( num_dev = self.num_dev, num_wg = self.num_wg, num_t = self.num_t, TsNameToObj = self.TsNameToObj , overwriteTimeStamp = 0 ) #InitStep_any( num_dev = self.num_dev, num_wg = self.num_wg, num_t = self.num_t, TsNameToObj = self.TsNameToObj , overwriteTimeStamp = 0 )
        self.tsList.append( tsInit )

        tsBListS1 = self.addAChain( parentInstruction = parent_instruction_1, Eid = e1, 
            childInstructions = rfMapInst[ parent_instruction_1 ], prevTimeStamp = tsInit.timestamp )

        tsIntervalSL = IntervalStep_frKeep( num_dev = self.num_dev, num_wg = self.num_wg, num_t = self.num_t, TsNameToObj = self.TsNameToObj,
              ConstraintList = self.ConstraintList , PiVarList = self.PiVarList  )
        self.tsList.append( tsIntervalSL )

        tsBListS2 = self.addAChain( parentInstruction = parent_instruction_2, Eid = e2, 
            childInstructions = rfMapInst[ parent_instruction_2 ], prevTimeStamp = tsIntervalSL.timestamp )

        tsIntervalLL = IntervalStep_frKeep( num_dev = self.num_dev, num_wg = self.num_wg, num_t = self.num_t, TsNameToObj = self.TsNameToObj,
            ConstraintList = self.ConstraintList , PiVarList = self.PiVarList  )
        self.tsList.append( tsIntervalLL )

        tsUListR = self.addAChain( parentInstruction = parent_instruction_3, Eid = e3, 
            childInstructions = rfMapInst[ parent_instruction_3 ], prevTimeStamp = tsIntervalLL.timestamp )

        #self.ConstraintList.append( HB(tsInit,tsBListS1[0]) )
        self.ConstraintList.append( HB(tsBListS1[-1], tsIntervalSL) )
        self.ConstraintList.append( HB(tsBListS2[-1], tsIntervalLL) )

        # tsIntervalSL --HB--> tsU is guaranteed by addAChain
        
        self.setPiFunAW( PiVarList = self.PiVarList, TsThatWritesVar = self.TsThatWritesVar, AllWriteTsList = [tsInit, tsIntervalSL, tsIntervalLL] )
        self.setPiFunAW( PiVarList = self.PiVarList, TsThatWritesVar = self.TsThatWritesVar, AllWriteTsList = [tsInit, tsIntervalSL, tsIntervalLL] )
        constrainIntervals(tsInit)



    def PO3SSL(self, parent_instruction_1, e1, parent_instruction_2, e2, parent_instruction_3, e3): # for load_DV_Rs : axiom 3
        def constrainIntervals(ts1,ts2, ts3):
            # ts1 is the init , and ts2 is the interval
            assert len(ts1.L1FifoTails) == len(ts2.L1FifoTailDeltas)
            assert len(ts1.L1FifoHeads) == len(ts2.L1FifoHeadDeltas)
            assert len(ts1.L1FifoTails) == len(ts2.L1FifoHeads)
            assert len(ts1.L1FifoTails) == len(ts3.L1FifoTailDeltas)
            assert len(ts1.L1FifoHeads) == len(ts3.L1FifoHeadDeltas)
            assert len(ts1.L1FifoTails) == len(ts3.L1FifoHeads)

            for sname in ts1.L1FifoHeads.keys(): # this is actually for all dw
                head_name = sname
                tail_name = sname.replace('head','tail')
                self.ConstraintList.append( ts1.L1FifoHeads[head_name] >= 0 )
                self.ConstraintList.append( ts1.L1FifoTails[tail_name] >= 0 )
                self.ConstraintList.append( ts1.L1FifoHeads[head_name] >= ts1.L1FifoTails[tail_name] )

                self.ConstraintList.append( ts2.L1FifoHeadDeltas[head_name] >= 0 )
                self.ConstraintList.append( ts2.L1FifoTailDeltas[tail_name] >= 0 )
                self.ConstraintList.append( ts2.L1FifoHeads[head_name] >= ts2.L1FifoTails[tail_name] )

                self.ConstraintList.append( ts3.L1FifoHeadDeltas[head_name] >= 0 )
                self.ConstraintList.append( ts3.L1FifoTailDeltas[tail_name] >= 0 )
                self.ConstraintList.append( ts3.L1FifoHeads[head_name] >= ts3.L1FifoTails[tail_name] )

                self.ConstraintList.append( ts2.L1FifoHeadDeltas[head_name] + ts3.L1FifoHeadDeltas[head_name] >= 
                    ts2.L1FifoTailDeltas[tail_name] + ts3.L1FifoTailDeltas[tail_name] )

            # these are the environmental constraint

        #first get the micro instructions
        tsInit = InitStep_fifo( num_dev = self.num_dev, num_wg = self.num_wg, num_t = self.num_t, TsNameToObj = self.TsNameToObj , overwriteTimeStamp = 0 )
        self.tsList.append( tsInit )

        tsBListS1 = self.addAChain( parentInstruction = parent_instruction_1, Eid = e1, 
            childInstructions = rfMapInst[ parent_instruction_1 ], prevTimeStamp = tsInit.timestamp )

        tsIntervalSS = IntervalStep_fifo( num_dev = self.num_dev, num_wg = self.num_wg, num_t = self.num_t, TsNameToObj = self.TsNameToObj,
            TsThatWritesVar = self.TsThatWritesVar ,  ConstraintList = self.ConstraintList , PiVarList = self.PiVarList  )
        self.tsList.append( tsIntervalSS )

        tsBListS2 = self.addAChain( parentInstruction = parent_instruction_2, Eid = e2, 
            childInstructions = rfMapInst[ parent_instruction_2 ], prevTimeStamp = tsIntervalSS.timestamp )

        tsIntervalSL = IntervalStep_fifo( num_dev = self.num_dev, num_wg = self.num_wg, num_t = self.num_t, TsNameToObj = self.TsNameToObj,
            TsThatWritesVar = self.TsThatWritesVar ,  ConstraintList = self.ConstraintList , PiVarList = self.PiVarList  )
        self.tsList.append( tsIntervalSL )

        tsUListR = self.addAChain( parentInstruction = parent_instruction_3, Eid = e3, 
            childInstructions = rfMapInst[ parent_instruction_3 ], prevTimeStamp = tsIntervalSL.timestamp )

        #self.ConstraintList.append( HB(tsInit,tsBListS1[0]) )
        self.ConstraintList.append( HB(tsBListS1[-1], tsIntervalSS) )
        self.ConstraintList.append( HB(tsBListS2[-1], tsIntervalSL) )

        # tsIntervalSS --HB--> tsU is guaranteed by addAChain
        
        self.setPiFunAW( PiVarList = self.PiVarList, TsThatWritesVar = self.TsThatWritesVar, AllWriteTsList = [tsInit, tsIntervalSS, tsIntervalSL] )

        ## TODO:  add the invariants
        constrainIntervals(tsInit,tsIntervalSS,tsIntervalSL)

    def add_check_axiom(self):
        #axiom.store_dv_r_3(self)
        #axiom.load_dv_r_3(self)
        axiom.PO2Axioms(self)


    def pushInstConstraintAndCheck(self):
        self.solver = z3.Solver()
        s = self.solver
        s.set(unsat_core=True if DEBUG else False)

        idx = 0
        for c in self.ConstraintList:
            if DEBUG:
                print >>self.logcat, idx,':', c
            #raw_input()
                if c is False:
                    print '<W>: False cannot be satisfied'
                elif c is True:
                    pass
                else:
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

        if len(self.runProp) == 0:
            print '<W>: no property specified.'
            return            
        else:
            runProp = z3.Not( LAnd(self.runProp) )
            if DEBUG:
                print >> self.logcat, 'rp : ', runProp
                s.assert_and_track(runProp,'rp')
            else:
                s.add(runProp)
            # extract module
            result = s.check()
            print result

        if result == z3.unsat: # this may use the old one
            if DEBUG:
                print >>self.logcat, s.unsat_core()
        elif result == z3.sat:
            self.model  = s.model()
            print 'negation is witnessed'
            #self.printModel()
        else:
            print 'status Unknown'

        return result

    def printModel(self):
        print >> self.logcat, '====================== MODEL ====================='
        for ts in self.tsList:
            print >>self.logcat, ts.name, ' entity:', ts.entity.toName() if 'entity' in ts.__dict__ else 'GLOBAL'
            t,d,val,readCol = ts.getConcreteModel(self.model)
            instName = ts.inst.name if 'inst' in ts.__dict__ else 'INIT'
            print >>self.logcat, '@%s, %s:%s'%(str(t), instName, d)
            for n,v in readCol.items():
                if isinstance(v, tuple):
                    value = str(v[0]) + '\taddr: ' + str('ANY' if v[1].anyAddr else ( 'z3:' + str(v[1].eval(self.model) ) + ', id:' + v[1].vaid ) )
                    print >> self.logcat, '\t (Read %s = %s)' % (n, value )
                else:
                    print >>self.logcat, '\t (Read %s = %s)' % (n, str(v) )
            for n,v in val.items():
                if isinstance(v, tuple):
                    value = str(v[0]) + '\taddr: ' + str('ANY' if v[1].anyAddr else ( 'z3:' + str(v[1].eval(self.model) ) + ', id:' + v[1].vaid ) )
                    print >>self.logcat, '\t %s:%s' % (n,value)
                else:
                    print >>self.logcat, '\t %s:%s' % (n,str(v))
        self.logcat.flush()


def check2store(num_dev,num_wg,num_t):
    #for devIdx1 in range(num_dev):
    #    for wgId1 in range(num_wg):
    #        for tIdx1 in range(num_t):
    devIdx1 = 0; wgId1 = 0; tIdx1 = 0
    for devIdx2 in range(num_dev):
        for wgId2 in range(num_wg):
            for tIdx2 in range(num_t):
                eqc = eqchecker(num_dev,num_wg,num_t)
                eqc.logcat = open('eqcheck.log', 'wt')
                eid1 = gpuModel.entity(devIdx1,wgId1,tIdx1)
                eid2 = gpuModel.entity(devIdx2,wgId2,tIdx2)
                eqc.POAhead2Store(parent_instruction_1 = openclrsp.CL_store_DV_R, e1 = eid1, 
                    parent_instruction_2 = openclrsp.CL_store_na_or_WG, e2 = eid2 )
                eqc.add_check_axiom()
                if eqc.pushInstConstraintAndCheck() != z3.sat:
                    print 'unrealistic scenario!'
                    assert False
                if eqc.solve() == z3.sat:
                    print 'Ordering is not guaranteed.'
                    eqc.printModel()
                    assert False
                eqc.logcat.close()

def checkSSL(num_dev,num_wg,num_t):
    devIdx1 = 0; wgId1 = 0; tIdx1 = 0
    #for devIdx1 in range(num_dev):
    #    for wgId1 in range(num_wg):
    #        for tIdx1 in range(num_t):
    for devIdx2 in range(num_dev):
        for wgId2 in range(num_wg):
            for tIdx2 in range(num_t):
                for devIdx3 in range(num_dev):
                    for wgId3 in range(num_wg):
                        for tIdx3 in range(num_t):
                            eqc = eqchecker(num_dev,num_wg,num_t)
                            eqc.logcat = open('eqcheck.log', 'wt')
                            eid1 = gpuModel.entity(devIdx1,wgId1,tIdx1)
                            eid2 = gpuModel.entity(devIdx2,wgId2,tIdx2)
                            eid3 = gpuModel.entity(devIdx3,wgId3,tIdx3)
                            eqc.PO3SSL(
                                parent_instruction_1 = openclrsp.CL_store_DV_N, e1 = eid1, 
                                parent_instruction_2 = openclrsp.CL_store_DV_N, e2 = eid2,
                                parent_instruction_3 = openclrsp.CL_load_DV_R, e3 = eid3
                                 )
                            eqc.add_check_axiom()
                            if eqc.pushInstConstraintAndCheck() != z3.sat:
                                print 'unrealistic scenario!'
                                assert False
                            
                            #eqc.printModel()
                            #eqc.logcat.close()
                            #exit(1)

                            if eqc.solve() == z3.sat:
                                print 'Ordering is not guaranteed.'
                                eqc.printModel()
                                assert False
                            eqc.logcat.close()


                            #eqc.printModel()
                            #eqc.logcat.close()
                            #exit(1)

def checkSLL(num_dev,num_wg,num_t):
    devIdx1 = 0; wgId1 = 0; tIdx1 = 0
    #devIdx2 = 0; wgId2 = 1; tIdx2 = 0
    #devIdx3 = 0; wgId3 = 0; tIdx3 = 0
    #for devIdx1 in range(num_dev):
    #    for wgId1 in range(num_wg):
    #        for tIdx1 in range(num_t):
    for devIdx2 in range(num_dev):
        for wgId2 in range(num_wg):
            for tIdx2 in range(num_t):
                for devIdx3 in range(num_dev):
                    for wgId3 in range(num_wg):
                        for tIdx3 in range(num_t):
                            eqc = eqchecker(num_dev,num_wg,num_t)
                            eqc.logcat = open('eqcheck.log', 'wt')
                            eid1 = gpuModel.entity(devIdx1,wgId1,tIdx1)
                            eid2 = gpuModel.entity(devIdx2,wgId2,tIdx2)
                            eid3 = gpuModel.entity(devIdx3,wgId3,tIdx3)
                            eqc.PO3SLL(
                                parent_instruction_1 = openclrsp.CL_store_DV_R, e1 = eid1, 
                                parent_instruction_2 = openclrsp.CL_load_na_or_WG, e2 = eid2,
                                parent_instruction_3 = openclrsp.CL_load_na_or_WG, e3 = eid3
                                 )
                            eqc.add_check_axiom()
                            if eqc.pushInstConstraintAndCheck() != z3.sat:
                                print 'unrealistic scenario!'
                                assert False

                            if eqc.solve() == z3.sat:
                                print 'Ordering is not guaranteed.'
                                eqc.printModel()
                                assert False
                            eqc.logcat.close()




def check2load(num_dev,num_wg,num_t):
    devIdx1 = 0; wgId1 = 0; tIdx1 = 0
    #for devIdx1 in range(num_dev):
    #    for wgId1 in range(num_wg):
    #        for tIdx1 in range(num_t):
    for devIdx2 in range(num_dev):
        for wgId2 in range(num_wg):
            for tIdx2 in range(num_t):
                eqc = eqchecker(num_dev,num_wg,num_t)
                eqc.logcat = open('eqcheck.log', 'wt')
                eid1 = gpuModel.entity(devIdx1,wgId1,tIdx1)
                eid2 = gpuModel.entity(devIdx2,wgId2,tIdx2)
                eqc.POAfter2Load(parent_instruction_1 = openclrsp.CL_load_DV_N, e1 = eid1, 
                    parent_instruction_2 = openclrsp.CL_load_DV_N, e2 = eid2 )
                eqc.add_check_axiom()
                if eqc.pushInstConstraintAndCheck() != z3.sat:
                    print 'unrealistic scenario!'
                    assert False
                
                #eqc.printModel()
                #eqc.logcat.close()
                #exit(1)

                if eqc.solve() == z3.sat:
                    print 'Ordering is not guaranteed.'
                    eqc.printModel()
                    assert False
                eqc.logcat.close()

if __name__ == '__main__':
    #check2store(2,2,2)   # should also check for store_DV_R to previous stores AXIOM 1 2
    check2load(2,2,2)
    #checkSSL(2,2,2)
    #checkSLL(2,2,2)










