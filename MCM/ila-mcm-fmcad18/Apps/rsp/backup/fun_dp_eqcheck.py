# those functions are dropped out eqcheck.py


    def POAhead2Store(self, parent_instruction_1, e1, parent_instruction_2, e2):
        def constrainIntervals(ts1,ts2):
            # ts1 is the init , and ts2 is the interval
            assert len(ts1.L1FifoTails) == len(ts2.L1FifoTailDeltas)
            assert len(ts1.L1FifoHeads) == len(ts2.L1FifoHeadDeltas)
            assert len(ts1.L1FifoTails) == len(ts2.L1FifoHeads)
            for sname in ts1.L1FifoHeads.keys():
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
        ts1     = self.addInitFrame(InitStep_fifo)
        tsBList = self.addInstBeforeCheckFrame(init = ts1, inst = parent_instruction_1, Eid = e1)  # inst = ??
        ts2     = self.addIntervalFrame(IntervalStep_fifo)  # we need to make sure that this ts will read from previous one

        self.ConstraintList.append( HB(ts1,tsBList[0]) )
        self.ConstraintList.append( HB(tsBList[-1],ts2) )

        self.ConstrainPi(init = ts1)

        tsU = self.addInstUnderCheckFrame(init = ts2, inst = parent_instruction_2, Eid = e2)
        self.ConstrainPi(init = ts2)
        ## TODO:  add the invariants
        constrainIntervals(ts1,ts2)


    def addInitFrame(self, initStepClassName):
        ts = initStepClassName( num_dev = self.num_dev, num_wg = self.num_wg, num_t = self.num_t, TsNameToObj = self.TsNameToObj , overwriteTimeStamp = 0 )
        self.tsList.append( ts )
        return ts

    def addIntervalFrame(self, intervalStepClassName):
        ts = intervalStepClassName( num_dev = self.num_dev, num_wg = self.num_wg, num_t = self.num_t, TsNameToObj = self.TsNameToObj,
        TsThatWritesVar = self.TsThatWritesVar ,  ConstraintList = self.ConstraintList , PiVarList = self.PiVarList  )
        self.tsList.append( ts )
        return ts

    def addInstBeforeCheckFrame(self, init, inst, Eid ):
        clInstruction = rfMapInst[ inst ] # if should be in the refinement mapping
        instructions_in_the_chain = self.addAChain( parentInstruction = inst, Eid = Eid, childInstructions = clInstruction, prevTimeStamp = init.timestamp )
        return instructions_in_the_chain

    def addInstUnderCheckFrame(self, init, inst, Eid):
        clInstruction = rfMapInst[ inst ] # if should be in the refinement mapping
        instructions_in_the_chain = self.addAChain( parentInstruction = inst, Eid = Eid, childInstructions = clInstruction, prevTimeStamp = init.timestamp )
        return instructions_in_the_chain

    def ConstrainPi(self, init ):
        self.setPiFun(init = init, PiVarList = self.PiVarList, TsThatWritesVar = self.TsThatWritesVar )
        """ push pi var to a stack """
        self.PiVarListOld.update(self.PiVarList)
        self.PiVarList = {}
        """ push TsThatWritesVar """
        self.TsThatWritesVarOld.update(self.TsThatWritesVar)
        self.TsThatWritesVar = {}


    # Let's add pi function
    def setPiFun(self, init, PiVarList , TsThatWritesVar ): # by default should be self.PiVarList
        for sname, piVar, tsRef, VAddr in PiVarList.values():
            # check its name, so repetition
            piVarName = str(piVar)
            if piVarName in self.ConstrainedPiVarNames:
                continue # else:
            self.ConstrainedPiVarNames.add(piVarName)

            timestamp = tsRef.timestamp

            writerTraceSteps = TsThatWritesVar.get(sname,[])

            OrClauses = []

            # build initial write:
            # address will match, as always
            # decode is always true
            # time stamp satisfied
            

            """ we need to make sure it does not read from it self """
            if init is not tsRef: 
                fr_hb_list = []
                for writeTs in writerTraceSteps:
                    if writeTs is tsRef: continue
                    if sname in writeTs.inst.updateDict:
                        addr = writeTs.inst.updateDict[sname] [1]
                        fr_hb_list.append( z3.Implies( z3.And( addr == VAddr , writeTs.inst.decodeFunc ) , HB( tsRef , writeTs ) ) )
                        #             
                readFromInit = z3.And( piVar == init.state(sname, VAddr), z3.And(fr_hb_list) )
                OrClauses.append(readFromInit)

            # we constrain them even when their decode is not true ???
            # FIXME : Check this --- it should be okay, because we will constrain every decode to be true

            for traceStep in writerTraceSteps:
                if traceStep is tsRef: continue
                constraint = mm.build_rf_constraint(sname, piVar, VAddr, TsThatWritesVar,  read = tsRef, write = traceStep) # 3 update check
                constraint = z3.Implies( tsRef.inst.decodeFunc , constraint ) #  check decode 
                OrClauses.append(constraint)
                # but we will add all the inst to be true???

            self.ConstraintList.append( z3.Or(OrClauses) )