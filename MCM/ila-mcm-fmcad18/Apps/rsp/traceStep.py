
import openclrsp
import gpuModel
from mmodels import hrf as mm
from collections import namedtuple
z3 = gpuModel.z3

# ev_FETCH_L1 R(Devview)  inst_LD R(Wvview)

# program order is only on instructions
# env can be added how ?

# for load we don't need ?

tsCtr = 0
def uniqueName():
    global tsCtr
    tsCtr += 1
    return 'ts'+str(tsCtr)

varCtr = 0
def varUniqueName():
    global varCtr
    varCtr += 1
    return 'var'+str(varCtr)

class InitStep_any(object):
    def __init__(self, num_dev, num_wg, num_t, TsNameToObj, overwriteTimeStamp = None ):
        self.otherEntityAddrBackup = []

        self.name = 'global_init_any_'+uniqueName()
        TsNameToObj[self.name] = self

        self.decodeFunc = True
        self.inst = dummyInst(decodeFunc = True, name = 'INIT', updateDict = [])
        # will write to all states

        self.state_name_addr_map = {} # stateName + '@' + str(addr) -> val
        self.InitValFixed = {} # let's try this first
        #    'rmwed'      :  False,
        #    'L2fr'       :  True, # VALID
        #    'L2hy'       :  False, # CLEAN
        #    'locked' :  False #,
        #    #'L1fr'   :  False, # INVALID
        #    #'L1hy'   :  0,
        #    }

        if overwriteTimeStamp is None:
            self.timestamp = z3.Int(  self.name + '_timestamp' )
        else:
            self.timestamp = overwriteTimeStamp


    def existsVA(self, a):
        for sa in self.otherEntityAddrBackup:
            if gpuModel.SyntacticAddrEqv(sa, a):
                return sa
        # else
        self.otherEntityAddrBackup.append(a)
        return a


    def state(self,name, addr): # returns the default value of a state # usually, it should be independent of addr
        sname = gpuModel.removeEntity(name)
        if sname in self.InitValFixed: # this is independent of the entity
            return self.InitValFixed[sname]
        entity = gpuModel.getEntity(name)
        # name here is state@d,w,t

        addrSame = self.existsVA(addr)
        idxIntoMap = name + '$' + ( addrSame.vaid if not addrSame.anyAddr else '' ) # state@d,w,t$addr
        if idxIntoMap in self.state_name_addr_map:
            return self.state_name_addr_map[idxIntoMap]

        # else
        newVar = gpuModel.newVariable( name, name +'_'+varUniqueName() ) # every read may create a new variable
        self.state_name_addr_map[idxIntoMap] = newVar


        return newVar
 
    def getConcreteModel(self, z3model):
        concreteTime = self.timestamp if isinstance(self.timestamp, int) else z3model[self.timestamp] 
        decodeCond = self.decodeFunc if  isinstance(self.decodeFunc,bool) else z3model.eval(self.decodeFunc) # True
        defCollection = {}
        readCollection = {}
        # no read at this point

        for sname, z3expr in self.state_name_addr_map.items():
            defCollection[sname] = z3model[z3expr]
        return concreteTime, decodeCond, defCollection, readCollection

class InitStep_fifo(object): # should provide all dwt address read (this is global initial)
    def __init__(self, num_dev, num_wg, num_t, TsNameToObj, overwriteTimeStamp = None ):
        self.otherEntityAddrBackup = []

        self.name = 'global_init_fifo_'+uniqueName()
        TsNameToObj[self.name] = self

        self.decodeFunc = True
        self.inst = dummyInst(decodeFunc = True, name = 'INIT', updateDict = [])
        # will write to all states

        self.state_name_addr_map = {} # stateName + '@' + str(addr) -> val
        self.InitValFixed = {
            'rmwed'      :  False,
            'L2fr'       :  True, # VALID
            'L2hy'       :  False, # CLEAN
            'locked' :  False #,
            #'L1fr'   :  False, # INVALID
            #'L1hy'   :  0,
            }
        self.L1FifoHeads = {}  # dev,wg -> var
        for devIdx in range(num_dev):
            for wgIdx in range(num_wg):
                stateName = 'L1fifohead@%d,%d' % (devIdx, wgIdx)
                varName = stateName +'_'+varUniqueName()
                self.L1FifoHeads[ stateName ] = gpuModel.newVariable(stateName, varName)
        self.L1FifoTails = {} # dev,wg -> var
        for devIdx in range(num_dev):
            for wgIdx in range(num_wg):
                stateName = 'L1fifotail@%d,%d' % (devIdx, wgIdx)
                varName = stateName +'_'+varUniqueName()
                self.L1FifoTails[ stateName ] = gpuModel.newVariable(stateName, varName)

        if overwriteTimeStamp is None:
            self.timestamp = z3.Int(  self.name + '_timestamp' )
        else:
            self.timestamp = overwriteTimeStamp


    def existsVA(self, a):
        for sa in self.otherEntityAddrBackup:
            if gpuModel.SyntacticAddrEqv(sa, a):
                return sa
        # else
        self.otherEntityAddrBackup.append(a)
        return a


    def state(self,name, addr): # returns the default value of a state # usually, it should be independent of addr
        sname = gpuModel.removeEntity(name)
        if sname in self.InitValFixed: # this is independent of the entity
            return self.InitValFixed[sname]
        entity = gpuModel.getEntity(name)
        # name here is state@d,w,t

        if sname in ['L1fifohead', 'L1fifotail']:
            if name in self.L1FifoHeads:
                return self.L1FifoHeads[name]
            elif name in self.L1FifoTails:
                return self.L1FifoTails[name]
            else:
                print '<E> : accessing fifohead/tail out of range:',name
                assert False 

        addrSame = self.existsVA(addr)
        idxIntoMap = name + '$' + ( addrSame.vaid if not addrSame.anyAddr else '' ) # state@d,w,t$addr
        if idxIntoMap in self.state_name_addr_map:
            return self.state_name_addr_map[idxIntoMap]

        # else
        newVar = gpuModel.newVariable( name, name +'_'+varUniqueName() ) # every read may create a new variable
        self.state_name_addr_map[idxIntoMap] = newVar


        return newVar
 
    def getConcreteModel(self, z3model):
        concreteTime = self.timestamp if isinstance(self.timestamp, int) else z3model[self.timestamp] 
        decodeCond = self.decodeFunc if  isinstance(self.decodeFunc,bool) else z3model.eval(self.decodeFunc) # True
        defCollection = {}
        readCollection = {}
        # no read at this point

        for sname, z3var in self.L1FifoHeads.items():
            defCollection[sname] = z3model[z3var]
        for sname, z3var in self.L1FifoTails.items():
            defCollection[sname] = z3model[z3var]

        for sname, z3expr in self.state_name_addr_map.items():
            defCollection[sname] = z3model[z3expr]
        return concreteTime, decodeCond, defCollection, readCollection

dummyInst = namedtuple('dummyInst','decodeFunc name updateDict')


class IntervalStep_frKeep(object):# should provide all dwt address read (this is global initial)
    def __init__(self,  num_dev, num_wg, num_t,  TsNameToObj, ConstraintList, PiVarList , overwriteTimeStamp = None ):
        self.TsNameToObj = TsNameToObj
        self.ConstraintList = ConstraintList
        self.PiVarList = PiVarList

        self.name = 'interval'+uniqueName()
        self.TsNameToObj[self.name] = self

        self.inst = dummyInst(decodeFunc = True, name = 'INTERVAL_frKeep', updateDict = [])

        self.decodeFunc = True
        # will write to all the states
        # basically, all the later states must consider reading from it

        self.otherEntityAddrBackup = []
        self.state_name_addr_map = {} # stateName + '@' + str(addr) -> val
        self.InitValFixed = { }
        #    'rmwed'      :  False,
        #    'L2fr'       :  True, # VALID
        #    'L2hy'       :  False, # CLEAN
        #    'locked' :  False #,
        #    #'L1fr'   :  False, # INVALID
        #    #'L1hy'   :  0,
        #    }
        if overwriteTimeStamp is None:
            self.timestamp = z3.Int( self.name + '_timestamp' )
        else:
            self.timestamp = overwriteTimeStamp

        # build them before the read (they are there any way)
        # not possible, you can enumerate all the addresses !!!
        """self.L1frCache = {}
        for devIdx in range(num_dev):
            for wgIdx in range(num_wg):
                stateName = 'L1fr@%d,%d' % (devIdx, wgIdx)
                Eid = gpuModel.entity(devIdx, wgIdx)
                self.L1frCache[ stateName ] = self.stateReadFunc( 'L1fr', entity =  )"""

    def existsVA(self, a):
        for sa in self.otherEntityAddrBackup:
            if gpuModel.SyntacticAddrEqv(sa, a):
                return sa
        # else
        self.otherEntityAddrBackup.append(a)
        return a


    def state(self,name, addr): # returns the default value of a state # usually, it should be independent of addr
        # the name here is name@d,w,t format, and we can extract entity from it
        sname = gpuModel.removeEntity(name)
        if sname in self.InitValFixed: # this is independent of the entity
            return self.InitValFixed[sname]
        entity = gpuModel.getEntity(name)
        # name here is state@d,w,t

        if sname in ['L1fr']:
            return self.stateReadFunc( sname, entity = entity , addr = addr ) 
            # we will get the one set by 
            # an earlier step (Keep L1fr)

        # otherwise we create the variable to make it arbitrary
        addrSame = self.existsVA(addr)  # cached addr in case we encounter syntactically the same one
        idxIntoMap = name + '$' + ( addrSame.vaid if not addrSame.anyAddr else '' ) # state@d,w,t$addr
        if idxIntoMap in self.state_name_addr_map:
            return self.state_name_addr_map[idxIntoMap] # any maybe we have created it and cached it
 
        # else, we will create a new one
        newVar = gpuModel.newVariable( name, name +'_'+varUniqueName() ) # every read may create a new variable
        self.state_name_addr_map[idxIntoMap] = newVar

        return newVar

    def stateReadFunc(self, stateName, addr = None , entity = None):
        if entity is None:
            entity = self.entity
        FullAddr, FullEid = gpuModel.setAddr(stateName, entity , addr) # get the default entity setting
        FullName = gpuModel.setSname(stateName, FullEid)
        # we need to get the current entity 
        # else it is a shared var, create PI variable for it
        piVarName = 'pi_' + self.name + '_' + FullName + ( '' if FullAddr.anyAddr else FullAddr.vaid)
        if piVarName not in self.PiVarList:
            piVar = gpuModel.newVariable( FullName , piVarName)
            self.PiVarList[piVarName] = (FullName, piVar, self, FullAddr)
        else:
            #print '<W>: piVar:', piVarName, 'already created! 1'
            piVar = self.PiVarList[piVarName][1]
        return piVar

    def getConcreteModel(self, z3model):
        concreteTime = z3model[self.timestamp]
        decodeCond = self.decodeFunc if  isinstance(self.decodeFunc,bool) else z3model.eval(self.decodeFunc) # True
        defCollection = {}
        readCollection = {}

        for sname, piVar, tsRef, FullAddr in self.PiVarList.values():
            if tsRef.name == self.name:
                readCollection[sname] = (z3model[piVar], FullAddr)

        for sname, z3expr in self.state_name_addr_map.items():
            defCollection[sname] = z3model[z3expr]
        return concreteTime, decodeCond, defCollection, readCollection



class IntervalStep_fifo(object):# should provide all dwt address read (this is global initial)
    def __init__(self,  num_dev, num_wg, num_t, TsThatWritesVar, TsNameToObj, ConstraintList, PiVarList , overwriteTimeStamp = None ):
        self.TsThatWritesVar = TsThatWritesVar
        self.TsNameToObj = TsNameToObj
        self.ConstraintList = ConstraintList
        self.PiVarList = PiVarList

        self.name = 'interval'+uniqueName()
        self.TsNameToObj[self.name] = self

        self.inst = dummyInst(decodeFunc = True, name = 'INTERVAL', updateDict = [])

        self.decodeFunc = True
        # will write to all the states
        # basically, all the later states must consider reading from it

        self.otherEntityAddrBackup = []
        self.state_name_addr_map = {} # stateName + '@' + str(addr) -> val
        self.InitValFixed = {
            'rmwed'      :  False,
            'L2fr'       :  True, # VALID
            'L2hy'       :  False, # CLEAN
            'locked' :  False #,
            #'L1fr'   :  False, # INVALID
            #'L1hy'   :  0,
            }
        if overwriteTimeStamp is None:
            self.timestamp = z3.Int( self.name + '_timestamp' )
        else:
            self.timestamp = overwriteTimeStamp

        # build them before the read (they are there any way)
        self.L1FifoHeadDeltas = {}
        self.L1FifoTailDeltas = {}

        self.L1FifoHeads = {} 
        for devIdx in range(num_dev):
            for wgIdx in range(num_wg):
                stateName = 'L1fifohead@%d,%d' % (devIdx, wgIdx)
                Eid = gpuModel.entity(devIdx, wgIdx)
                varName = stateName +'_delta_'+varUniqueName()
                delta = gpuModel.newVariable(stateName, varName)
                self.L1FifoHeadDeltas[ stateName ] = delta
                self.L1FifoHeads[ stateName ] = delta + self.stateReadFunc( 'L1fifohead', entity = Eid )
        self.L1FifoTails = {}
        for devIdx in range(num_dev):
            for wgIdx in range(num_wg):
                stateName = 'L1fifotail@%d,%d' % (devIdx, wgIdx)
                Eid = gpuModel.entity(devIdx, wgIdx)
                varName = stateName +'_delta_'+varUniqueName()
                delta = gpuModel.newVariable(stateName, varName)
                self.L1FifoTailDeltas[ stateName ] = delta
                self.L1FifoTails[ stateName ] = delta + self.stateReadFunc( 'L1fifotail', entity = Eid )



    def existsVA(self, a):
        for sa in self.otherEntityAddrBackup:
            if gpuModel.SyntacticAddrEqv(sa, a):
                return sa
        # else
        self.otherEntityAddrBackup.append(a)
        return a


    def state(self,name, addr): # returns the default value of a state # usually, it should be independent of addr
        sname = gpuModel.removeEntity(name)
        if sname in self.InitValFixed: # this is independent of the entity
            return self.InitValFixed[sname]
        entity = gpuModel.getEntity(name)
        # name here is state@d,w,t

        if sname in ['L1fifohead', 'L1fifotail']:
            if name in self.L1FifoHeads:
                return self.L1FifoHeads[name] 
            elif name in self.L1FifoTails:
                return self.L1FifoTails[name] 
            else:
                print '<E> : accessing fifohead/tail out of range:', name
                assert False 

        addrSame = self.existsVA(addr)
        idxIntoMap = name + '$' + ( addrSame.vaid if not addrSame.anyAddr else '' ) # state@d,w,t$addr
        if idxIntoMap in self.state_name_addr_map:
            return self.state_name_addr_map[idxIntoMap]

        # else
        newVar = gpuModel.newVariable( name, name +'_'+varUniqueName() ) # every read may create a new variable
        self.state_name_addr_map[idxIntoMap] = newVar

        return newVar

    def stateReadFunc(self, stateName, addr = None , entity = None):
        if entity is None:
            entity = self.entity
        FullAddr, FullEid = gpuModel.setAddr(stateName, entity , addr)
        FullName = gpuModel.setSname(stateName, FullEid)
        # we need to get the current entity 
        # else it is a shared var, create PI variable for it
        piVarName = 'pi_' + self.name + '_' + FullName + ( '' if FullAddr.anyAddr else FullAddr.vaid)
        if piVarName not in self.PiVarList:
            piVar = gpuModel.newVariable( FullName , piVarName)
            self.PiVarList[piVarName] = (FullName, piVar, self, FullAddr)
        else:
            #print '<W>: piVar:', piVarName, 'already created! 1'
            piVar = self.PiVarList[piVarName][1]
        return piVar

    def getConcreteModel(self, z3model):
        concreteTime = z3model[self.timestamp]
        decodeCond = self.decodeFunc if  isinstance(self.decodeFunc,bool) else z3model.eval(self.decodeFunc) # True
        defCollection = {}
        readCollection = {}

        for sname, piVar, tsRef, FullAddr in self.PiVarList.values():
            if tsRef.name == self.name:
                readCollection[sname] = (z3model[piVar], FullAddr)

        for sname, z3var in self.L1FifoHeads.items():
            defCollection[sname] = z3model.eval(z3var) # end value
        for sname, z3var in self.L1FifoTails.items():
            defCollection[sname] = z3model.eval(z3var) # end value

        for sname, z3expr in self.state_name_addr_map.items():
            defCollection[sname] = z3model[z3expr]
        return concreteTime, decodeCond, defCollection, readCollection


class TraceStep(object):

    def _getWrite(self):
        self.Writes= set(self.inst.updateDict.keys())

        for write in self.Writes:
            if write not in self.TsThatWritesVar:
                self.TsThatWritesVar[write] = set([])
            self.TsThatWritesVar[write].add(self)


    def __init__(self,entity, TsThatWritesVar, TsNameToObj, ConstraintList, PiVarList ) : #  tell me which instruction to execute
        assert (TsThatWritesVar is not None and TsNameToObj is not None 
            and ConstraintList is not None and PiVarList is not None )
        
        self.TsThatWritesVar = TsThatWritesVar
        self.TsNameToObj     = TsNameToObj
        self.ConstraintList  = ConstraintList
        self.PiVarList       = PiVarList


        self.name = uniqueName()
        self.entity = entity
        self.TsNameToObj[self.name] = self # register itself
        """
        self.wvopTsNameList = # mm
        self.Reads =  # mm
        self.Write = # mm
        """
        self.timestamp = z3.Int('n_'+ self.name)
        self.defVars = {} # state name -> def z3 var\

    def existsVA(self, a):
        for sa in self.otherEntityAddrBackup:
            if SyntacticAddrEqv(sa, a):
                return sa
        self.otherEntityAddrBackup.append(a)
        return a

    def assignInst(self,inst): 
        self.inst = inst
        self._getWrite()

    def stateReadFunc(self, stateName, addr = None , entity = None):
        """TODO: rewrite this part"""
        if entity is None:
            entity = self.entity
        FullAddr,FullEid = gpuModel.setAddr(stateName, entity , addr)
        FullName = gpuModel.setSname(stateName, FullEid)
        # we need to get the current entity 
        # else it is a shared var, create PI variable for it
        piVarName = 'pi_' + self.name + '_' + FullName + ( '' if FullAddr.anyAddr else FullAddr.vaid)
        if piVarName not in self.PiVarList:
            piVar = gpuModel.newVariable( FullName , piVarName)
            self.PiVarList[piVarName] = (FullName, piVar, self, FullAddr)
        else:
            #print '<W>: piVar:', piVarName, 'already created! 1'
            piVar = self.PiVarList[piVarName][1]
        return piVar

    def getConcreteModel(self, z3model):
        concreteTime = z3model[self.timestamp]
        decodeCond = self.inst.decodeFunc if  isinstance(self.inst.decodeFunc,bool) else z3model.eval(self.inst.decodeFunc)
        defCollection = {}
        readCollection = {}

        for sname, piVar, tsRef, FullAddr in self.PiVarList.values():
            if tsRef.name == self.name:
                readCollection[sname] = (z3model[piVar], FullAddr)
        for sname, (z3expr, FullAddr) in self.inst.updateDict.items():
            if isinstance(z3expr, bool) or isinstance(z3expr, int) or isinstance(z3expr,str):
                val = z3expr
            else:
                val = z3model.eval(z3expr)
            defCollection[sname] = (val, FullAddr )
        return concreteTime, decodeCond, defCollection, readCollection



    def BuildFrame(self):
        pass
        # first get dict
        # no incoming result dict

        # now the state update function are all the expressions
        # the read from must take into account that it cannot read from a
        # non-valid result

        # inst. 
        # now resultDict is not containing anything useful
        # but self.inst.updateDict[statename]