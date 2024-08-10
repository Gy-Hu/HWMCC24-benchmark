
# here we define the things that will be refer to 

# we need the mapping between timestamps and the states

ctr = 0
def uniqueName():
    global ctr
    ctr += 1
    return "ts"+str(ctr)

def newPiVar(stateName):
    return 'pi_'+stateName + '_' + uniqueName()

class CacheLine(object):
    def __init__(self, addr , PiVarList, entity, isL1):
        self.addr = addr
        self.PiVarList = PiVarList
        self.entity = entity
        self.isL1 = isL1
        self.varAddr = varAddr(entity, addr)
    @property
    def value(self): # create on demand

    @property
    def fr(self):
        pass
    @property
    def hy(self):
        pass

class FIFO(object):
    def __init__(self,PiVarList, entity):
        self.PiVarList = PiVarList
        self.entity = entity
        self.varAddr = varAddr(entity, addr=None, anyAddr = True)
    @property
    def head(self):
        pass
    @property
    def tail(self):
        pass

class lock(object):
    def __init__(self,  PiVarList, entity, addr = None):
        self.PiVarList = PiVarList
        self.addr = addr
        self.entity = entity
        self.varAddr = varAddr(entity, addr, False if addr else True )
    def ready(self,d,w,t):
        ???



class Cache(object):
    def __init__(self, isL1, PiVarList, entity):
        self.isL1 = isL1
        self.PiVarList = PiVarList
        self.fifo = FIFO(PiVarList = self.PiVarList, entity = entity)
        self.entity = entity

    def isL1():
        return self.isL1
    def isL2():
        return not self.isL1
    def __call__(self, x):
        return CacheLine(x, self.PiVarList, entity = entity)

# tackle the entity change
class DevState(object):
    def __init__(self,entity, PiVarList):
        self.entity = entity(d = entity.d, w = None, t = None, anyw = True, anyt = True)
        self.PiVarList = PiVarList
        self.L2 = Cache(isL1 = False, PiVarList = PiVarList)
        self.lockfile = lambda x:  return lock(PiVarList, entity = self.entity, addr = x)

class WgState(object):
    def __init__(self,entity, PiVarList):
        self.entity = entity(d = entity.d, w = entity.w, t = None, anyt = True)
        self.PiVarList = PiVarList
        self.L1 = Cache(isL1 = True, PiVarList = PiVarList)
        self.rmw = lock(PiVarList)

class ThreadState(object):
    def __init__(self,entity, PiVarList):
        self.entity = entity(d = entity.d, w = entity.w, t = entity.t)
        self.PiVarList = PiVarList
    def r(self,r):
        va = varAddr(entity = self.entity, addr = r)
        return ???




class Sys(object):
    def __init__(self,entity, PiVarList):
        self.entity = entity
        self.mem = lambda x: 0

    def __call__(self, *args):
        if len(args) == 1: # d
            return DevState()
        elif len(args) == 2: # d w

        elif len(args) == 3: # d w t 



        