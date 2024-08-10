import z3

class entity(object):
    def __init__(self,*args):
        assert len(args) >= 0 and len(args) <= 3
        self.d = args[0] if len(args) >= 1 else None
        self.w = args[1] if len(args) >= 2 else None
        self.t = args[2] if len(args) >= 3 else None
        anyd = False if len(args) >= 1 else True
        anyw = False if len(args) >= 2 else True
        anyt = False if len(args) >= 3 else True
        assert (not anyd) or anyw # anyd => anyw
        assert (not anyw) or anyt # anyw => anyt
        self.anyd = anyd ; self.anyw = anyw; self.anyt = anyt
    def __eq__(self,obj):
        return SyntacticEntityEqv(self,obj)
    def toName(self):
        retStr = ''
        if not self.anyd:
            retStr += str(self.d)
        if not self.anyw:
            retStr += ','+str(self.w)
        if not self.anyt:
            retStr += ','+str(self.t)
        return retStr

def SyntacticEntityEqv(e1,e2):
    if not ( e1.anyd == e2.anyd and e1.anyw == e2.anyw and e1.anyt == e2.anyt ):
        return False
    return  ( e1.anyd or ( str(e1.d) == str(e2.d) ) ) and \
            ( e1.anyw or ( str(e1.w) == str(e2.w) ) ) and \
            ( e1.anyt or ( str(e1.t) == str(e2.t) ) )

"""
class entity(object):
    def __init__(self,*args): # d,w,t, anyd = False, anyw = False, anyt = False
        assert len(args) >= 0 and len(args) <= 3
        self.d = args[0] if len(args) >= 1 else None
        self.w = args[1] if len(args) >= 2 else None
        self.t = args[2] if len(args) >= 3 else None
        anyd = False if len(args) >= 1 else True
        anyw = False if len(args) >= 2 else True
        anyt = False if len(args) >= 3 else True
        assert (not anyd) or anyw # anyd => anyw
        assert (not anyw) or anyt # anyw => anyt
        self.anyd = anyd ; self.anyw = anyw; self.anyt = anyt
    def __eq__(self,obj):
        assert obj.anyd == self.anyd and obj.anyw == self.anyw and obj.anyt == self.anyt
        retL = []
        if not self.anyd:
            retL.append( self.d == obj.d )
            if not self.anyw:
                retL.append( self.w == obj.w )
                if not self.anyt:
                    retL.append( self.t == obj.t )
        if retL:
            return z3.And( retL )
        return True

def SyntacticEntityEqv(e1,e2):
    if not ( e1.anyd == e2.anyd and e1.anyw == e2.anyw and e1.anyt == e2.anyt ):
        return False
    return  ( e1.anyd or ( str(e1.d) == str(e2.d) ) ) and \
            ( e1.anyw or ( str(e1.w) == str(e2.w) ) ) and \
            ( e1.anyt or ( str(e1.t) == str(e2.t) ) )

def SameWg(e1,e2):
    assert e1.anyd == e2.anyd and e1.anyw == e2.anyw and e1.anyt == e2.anyt
    retL = []
    if not self.anyd:
        retL.append( self.d == obj.d )
        if not self.anyw:
            retL.append( self.w == obj.w )
    if retL:
        return z3.And( retL )
    return True

def SameDv(e1,e2):
    assert e1.anyd == e2.anyd and e1.anyw == e2.anyw and e1.anyt == e2.anyt
    if not e1.anyd:
        return e1.d == e2.d
    return True
"""


vaidDict = {} # id -> ref
def varAddr(addr = None): # this is the factory function:
    vaid = str(addr)
    if vaid not in vaidDict:
        vaidDict[vaid] = vAddr(addr = addr)
    return vaidDict[vaid]

class vAddr(object):
    def __init__(self,addr = None):
        self.anyAddr = True if addr is None else False
        self.addr = addr
        self.vaid = str(addr) # to distinguish vas

    def __eq__(self,obj):
        if self.anyAddr or obj.anyAddr:
            return True
        return self.addr == obj.addr

    def __str__(self):
        return self.vaid
    def eval(self, model):
        if self.anyAddr : return ''
        if isinstance(self.addr, int) or isinstance(self.addr, str) or isinstance(self.addr, bool):
            return str(self.addr)
        return model.eval(self.addr)
 

def SyntacticAddrEqv(a1, a2):
    if a1.anyAddr != a2.anyAddr:
        return False
    if str(a1.addr) != str(a2.addr):
        return False
    return True

# ===============================================================

# instruction.py

#------------------------------
# AUX Func:

# the full state name will be "stateName@d,w,t"

dList = ['L2fifohead', 'L2fifotail' ]
dwList = ['L1fifohead' , 'L1fifotail' , 'rmwTd' , 'rmwTw' , 'rmwTt' , 'rmwed']
xdList = ['L2fr', 'L2hy' , 'L2val' , 'lockTd', 'lockTw' , 'lockTt' , 'locked' ]
xdwList = ['L1fr', 'L1hy' , 'L1val' ]
rdwtList = ['r']
xList = ['mem']

BoolValState = [ 'rmwed', 'L2fr', 'L2hy', 'locked','L1fr', 'L1hy'  ]
BVState = ['L2fifohead', 'L2fifotail','L1fifohead' , 'L1fifotail' , \
 'rmwTd' , 'rmwTw' , 'rmwTt' , 'L2val' , 'lockTd', 'lockTw' , 'lockTt', 'L1val', 'r']




def setAddr(sname, Eid, addr = None):
    """For a short state name: sname, it construct the right Eid and addr for it"""
    if sname in dList:
        assert not Eid.anyd 
        return varAddr(), entity(Eid.d)
    if sname in dwList:
        assert not Eid.anyd and not Eid.anyw 
        return varAddr(), entity(Eid.d, Eid.w)
    assert addr is not None or sname in ['L1fr'] # disallow invalidate for all address , L1 fr for all x
    if sname in xList:
        return varAddr(addr = addr), entity()
    if sname in xdList:
        assert not Eid.anyd
        return varAddr(addr = addr), entity(Eid.d)
    if sname in xdwList:
        assert not Eid.anyd and not Eid.anyw
        return varAddr(addr = addr), entity(Eid.d, Eid.w)
    if sname in rdwtList:
        assert not Eid.anyd and not Eid.anyw and not Eid.anyt
        return varAddr(addr = addr), entity(Eid.d, Eid.w, Eid.t)
    assert False

def setSname(sname, entity):
    """this extends the short name when given a right eid
    It should be used after using setAddr to get the proper Eid"""
    return sname+'@'+entity.toName()
def removeEntity(sname): 
    """This converts long name to a short name"""
    return sname.split('@')[0]
def getEntity(sname): 
    """ This gets the entity encoded in the form of  state@d,w,t$vaid  
    the $vaid part is only for an index to a ts's local map
    Okay to ignore $vaid in most cases """
    eid = ((sname.split('@')[1]).split('$')[0]).split(',')
    return entity( *eid )

#------------------------------

class Instruction(object):
    def __init__(self,name, decodeFunc):
        self.name = name
        self.decodeFunc = decodeFunc
        self.updateDict = {}    # statename -> (function, addr)

        self.tp = 'gpuInst'
    def setUpdateToState(self,stateName,func, addr = None, entity = None ):
        if entity is None:
            entity = self.Eid
        FullAddr,realE = setAddr(stateName, entity ,addr)
        FullName = setSname(stateName, realE)
        assert FullName not in self.updateDict # should not overwrite
        self.updateDict[FullName] = (func, FullAddr)
            
    def setEntity(self,Eid):
        self.Eid = Eid
    def recordAddr(self,addr):
        self.addr = addr

#------------------------------

class OpenCLInstruction(object):
    def __init__(self,name, decodeFunc):
        self.name = name
        self.decodeFunc = decodeFunc
        self.updateDict = {}    # statename -> (function, addr)
        self.wvop = None # will be re-assign by addAChain
        self.rvop = None 

    def setUpdateToState(self,stateName,func, addr = None, entity = None ):
        if entity is None:
            entity = self.Eid
        FullAddr = setAddr(stateName, entity ,addr)
        FullName = setSname(stateName, entity)
        assert FullName not in self.updateDict # should not overwrite
        self.updateDict[FullName] = (func, FullAddr)
            
    def setEntity(self,Eid):
        self.Eid = Eid
    def recordAddr(self,addr):
        self.addr = addr
#------------------------------
