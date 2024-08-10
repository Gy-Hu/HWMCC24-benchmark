from entity import *

# instruction centric modeling
# instruction centric checking

# parameterized model

"""
state
    d w t : r
    d w   : L1 L1.fifo.head L1.fifo.tail lock (single)
    d     : L2 L2.fifo.head L2.fifo.tail lock (addr-> lock)
"""
# make sure you only read once

"""

                    state(d).L2.isL2()
L2fr x,entity(d)    state(d).L2(x).fr
L2hy x,entity(d)    state(d).L2(x).hy
L2val x,entity(d)   state(d).L2(x).value
L2fifohead entity(d)    state(d).L2.fifo.head
L2fifotail entity(d)    state(d).L2.fifo.tail
lockTd  x,entity(d)     state(d).lockfile(x).ready(d,w,t) := lock(d,w,t)
lockTw  x,entity(d)
lockTt  x,entity(d)
locked  x,entity(d)

L1fr x,entity(d,w)      state(d,w).L1(x).fr
L1hy x,entity(d,w)      state(d,w).L1(x).hy
L1val x, entity(d,w)    state(d,w).L1(x).value   __call__
L1fifohead entity(d,w)  state(d,w).L1.fifo.head
L1fifotail entity(d,w)  state(d,w).L1.fifo.tail
                        state(d,w).L1.isL1()                       
rmwTd  entity(d,w)
rmwTw  entity(d,w)
rmwTt  entity(d,w)
rmwed  entity(d,w)

r r,entity(d,w,t)



forallDev( lambda )
forallWg( d , lambda )

rlViewInfo  = 
    ( None, d, w   , num  ) : marker : L1 flush
    ( None, d, None, num  ) : marker : L2 flush
    ( x   , d, None, num  ) : L2 x
    ( x   , d, w   , num  ) : L1 x

"""


DIRTY = True
CLEAN = False
VALID = True
INVALID = False
FLUSH_MARKER = None

def newVariable(name, varname):  # it uses name, is it okay? 
    stateName = removeEntity(name)
    if stateName in BoolValState:
        return z3.Bool(varname)
    if stateName in BVState:
        return z3.Int(varname)
    assert False


def L1Enqueue(state, inst): 
    inst.setUpdateToState( 'L1fifohead', state('L1fifohead') + 1 )
def L1Dequeue(state, inst):
    inst.setUpdateToState( 'L1fifotail', state('L1fifotail') + 1 )

def L2Enqueue(state, inst):
    inst.setUpdateToState( 'L2fifohead', state('L2fifohead') + 1)
def L2Dequeue(state, inst):
    inst.setUpdateToState( 'L2fifotail', state('L2fifotail') + 1 )

def lockRMW(inst,state, entity = None): # you can overwrite overWriteVA to write to a larger group!
    inst.setUpdateToState( 'rmwed' , True , entity = entity)
    inst.setUpdateToState( 'rmwTd' , inst.Eid.d , entity = entity)
    inst.setUpdateToState( 'rmwTw' , inst.Eid.w , entity = entity)
    inst.setUpdateToState( 'rmwTt' , inst.Eid.t , entity = entity)

def unlockRMW(inst,state, entity = None):
    inst.setUpdateToState( 'rmwed' , False , entity = entity)

def readyRMW(state, fullEntity, entity = None):
    assert not fullEntity.anyd and not fullEntity.anyw and not fullEntity.anyt
    return z3.Or( z3.Not( state('rmwed' ,  entity = entity) ), 
            z3.And( [
                state('rmwTd' ,  entity = entity) == fullEntity.d ,
                state('rmwTw' ,  entity = entity) == fullEntity.w ,
                state('rmwTt' ,  entity = entity) == fullEntity.t ] ) )

def locklockfile(inst,x,state):
    inst.setUpdateToState( 'locked' , True ,       addr = x)
    inst.setUpdateToState( 'lockTd' , inst.Eid.d , addr = x)
    inst.setUpdateToState( 'lockTw' , inst.Eid.w , addr = x)
    inst.setUpdateToState( 'lockTt' , inst.Eid.t , addr = x)

def unlocklockfile(inst,x,state):
    inst.setUpdateToState( 'locked' , False ,       addr = x)


def readylockfile(x, state , fullEntity):
    assert not fullEntity.anyd and not fullEntity.anyw and not fullEntity.anyt
    return z3.Or( z3.Not( state('locked', addr = x) ), 
            z3.And( [
                state('lockTd', addr = x) == fullEntity.d ,
                state('lockTw', addr = x) == fullEntity.w ,
                state('lockTt', addr = x) == fullEntity.t ] ) )


def storeL1(  x ,v , inst , state):
    inst.setUpdateToState( 'L1val'  , v , addr = x)
    inst.setUpdateToState( 'L1fr'    , VALID , addr = x)
    inst.setUpdateToState( 'L1hy'    , DIRTY , addr = x)
    L1Enqueue(state, inst)

def storeL2( x , v , inst, state ):
    inst.setUpdateToState( 'L2val'  , v , addr = x)
    inst.setUpdateToState( 'L2fr'    , VALID , addr = x)
    inst.setUpdateToState( 'L2hy'    , DIRTY , addr = x)
    L2Enqueue(state, inst)

    # TODO: create dequeue child must need

# the record info must be read at the time of the instruction

# invlidate forall x



#------------------------------



# May have env trans
def inst_LD(x, r,  Eid, state, **useless):
    # TODO: create rd ? 
    # No : may not need
    inst = Instruction('LD', state('L1fr',addr = x) == VALID ) 
    inst.setEntity( Eid )
    inst.setUpdateToState( 'r' , state('L1val', addr = x), addr = r )
    inst.recordAddr( x )
    return inst



# has env trans
def inst_ST(x, r,  Eid, state, **useless):
    inst = Instruction('ST', True ) 
    inst.setEntity( Eid )
    storeL1( x, state('r' , addr = r ) , inst , state = state) # TODO: create dequeue child must need
    #store(  state(d,w).L1, x, state(d,w,t).r(r) , inst ) 
    inst.recordAddr( x )
    return inst


# has env trans
def inst_INC_L1(x, r , Eid,state, **useless):
    inst = Instruction('INC_L1' , z3.And( readyRMW(state, Eid) , state('L1fr', addr = x) == VALID ) )
    inst.setEntity( Eid )
    inst.setUpdateToState( 'r', state('L1val', addr = x ), addr = r )
    storeL1( x, state('L1val', addr = x) + 1, inst , state = state)
    inst.recordAddr( x )
    return inst


# has env trans
def inst_INC_L2(x, r , Eid, state , num_dev,  **useless): # will need to  give a function

    decode = z3.And([ \
        readyRMW(state, Eid),
        state('L1hy', addr = x) != DIRTY,
        readylockfile(x, state, Eid),
        state('L2fr', addr = x) == VALID
    ])

    inst = Instruction('INC_L2' , decode )
    inst.setEntity( Eid )
    
    inst.setUpdateToState( 'L1fr', INVALID, addr = x) #invalidate( state(d,w).L1, inst  )
    inst.setUpdateToState( 'r', state('L2val', addr = x ) , addr = x ) 
    for devIdx in range(num_dev):
        if devIdx == Eid.d: continue
        inst.setUpdateToState( 'L2fr', INVALID, addr = x, entity = entity( devIdx ) )
    storeL2( x, state('L2val', addr = x) + 1 , inst , state = state) # contains L2fr


    inst.recordAddr( x )
    return inst

# add unflush block by axioms (?? or states??)
# has env trans
def inst_FLU_L1_WG(Eid, state, **useless): 
    inst = Instruction('FLU_L1_WG' , True )
    inst.setEntity( Eid )
    L1Enqueue(state,inst)

    return inst

def inst_FLU_L1_DV(Eid, state, num_wg, **useless):
    inst = Instruction('FLU_L1_DV', True )
    inst.setEntity( Eid ) 

    for wgId in range(num_wg):
        inst.setUpdateToState('L1fifohead',  
            state('L1fifohead', entity = entity(Eid.d,wgId) ) + 1 , entity = entity(Eid.d, wgId) )
        # for all wg in the same device, enqueue a flush marker

    return inst


def inst_FLU_L2_DV(Eid, state, **useless):
    inst = Instruction('FLU_L2_DV', True )
    inst.setEntity( Eid )
    L2Enqueue(state, inst)
    return inst


# ------------------------------
# the above need additional 
# ------------------------------

# purly axiomatic
def inst_INV_L1_WG(Eid, state,  **useless):
    inst = Instruction('INV_L1_WG', True)
    inst.setEntity( Eid )
    inst.setUpdateToState( 'L1fr' , INVALID ,  addr = None ) # will not set addr = x
    return inst

# purly axiomatic
def inst_INV_L1_DV(Eid, state,  num_wg, **useless):
    inst = Instruction('INV_L1_DV', True)
    inst.setEntity( Eid )
    for wgId in range(num_wg):
        inst.setUpdateToState('L1fr', INVALID, addr = None , entity = entity(Eid.d, wgId) ) # will not set addr = x
    return inst

# same work group should be interpreted as w == w' and d == d'

"""
Axiom INV_L1_WG
forall inv:INV_L1_WG | forall l:LOAD | SameWg[inv,l] /\ HB[inv,l] => HB[inv , l.fetch ]
??? l.fetch ???

Axiom INV_L1_DV
forall inv:INV_L1_DV | forall l:LOAD | SameDv[inv,l] /\ HB[inv,l] => HB[inv , l.fetch]
??? l.fetch ???

"""

"""
def inst_INV_L1_SY(d,w,t, state):
    inst = Instruction('INV_L1_SY', )
    inst.setEntity( entity(d,w,t) )
    return inst
"""

def inst_LK_L2(x, Eid, state, **useless):
    inst = Instruction('LK_L2',  readylockfile(x, state , Eid) )
    inst.setEntity( Eid )
    locklockfile(inst,x,state)
    inst.recordAddr( x )
    return inst

def inst_UL_L2(x, Eid, state, **useless):
    inst = Instruction('UL_L2', True )
    inst.setEntity( Eid )
    unlocklockfile(inst,x,state)
    inst.recordAddr( x )
    return inst

def inst_LK_rmw_DV(Eid, state,  num_wg, **useless):
    decode = z3.And(
        [ readyRMW( state , Eid, entity = entity(Eid.d, wgId) )  \
            for wgId in range(num_wg)  ]  )
    
    inst = Instruction('LK_rmw_DV', decode )
    inst.setEntity( Eid )
    for wgId in range(num_wg):
        lockRMW(inst, state, entity = entity(Eid.d, wgId) )  # not including w
    #forallWg( d, lambda w2: inst.setUpdateToState( state(d,w2).rmw , lock(d,w,t) ) )
    return inst

def inst_UL_rmw_DV(Eid, state, num_wg,  **useless):
    inst = Instruction('UL_rmw_DV', True )
    inst.setEntity( Eid )
    for wgId in range(num_wg):
        unlockRMW(inst, state, entity = entity(Eid.d, wgId) ) 
    return inst



# decode may need to chain 

# instantiate the above instructions and give the state() 
# need to take care of time and value. maybe register the pi_var?

# try not to model evict!

def ev_FLUSH_L1(x,Eid,state, num_dev, **useless):
    inst = Instruction('FLUSH_L1', z3.And( state('L1hy', addr = x)  == DIRTY, readylockfile(x, state, Eid)  )  )
    inst.setEntity( Eid )
    for devIdx in range(num_dev):
        if devIdx == Eid.d: continue
        inst.setUpdateToState( 'L2fr' , INVALID ,addr = x, entity = entity(devIdx) ) # write to all device at x
    #forallDev(lambda d2: if d2 != d : inst.setUpdateToState( state(d2).L2(x).fr , INVALID ) )
    storeL2(x , state('L1val', addr = x) , inst , state = state)
    #store( state(d).L2, x, state(d,w).L1(x).value , inst )  # but one for L2fr
    inst.setUpdateToState(  'L1hy', CLEAN,  addr = x )   
    #inst.setUpdateToState( state(d,w).L1(x).hy , CLEAN )    # 
    inst.recordAddr( x )
    inst.tp = 'gpuEnvTrans'
    return inst

"""
def ev_FLUSH_L2(x, d,w,t, state):
    inst = Instruction('FLUSH_L2', z3.And( state(d).L2(x).hy == DIRTY , state(d).lockfile(x).ready(d,w,t) ) )

"""

# we need to make L2 all valid for the same dv?

def ev_FETCH_L1(x, Eid, state, **useless):
    decode = z3.And( [ state('L1hy', addr = x) == CLEAN,  # z3.Or( state('L1fr', addr = x) == INVALID , state('L1hy', addr = x) == CLEAN ),  
        state('L2fr', addr = x) == VALID,
        readylockfile(x, state, Eid) 
        ])
    inst = Instruction('FETCH_L1', decode)
    inst.setEntity( Eid )
    inst.setUpdateToState( 'L1val', state('L2val', addr = x), addr = x )
    inst.setUpdateToState( 'L1fr' , VALID, addr = x )
    inst.setUpdateToState( 'L1hy' , CLEAN, addr = x )
    inst.recordAddr( x )
    inst.tp = 'gpuEnvTrans'
    return inst    


"""
def ev_FETCH_L2(x, d,w,t, state):
    pass
"""

"""
for different instruction, these will be instantiated when necessary (given a matching template)

"""

# the slot must be read at the time of instruction
# value & when

def ev_DEQLOC_L1(x, slot, Eid, state, **useless):
    decode = z3.And( z3.Or( state('L1fr', addr = x) == INVALID , state('L1hy', addr = x) == CLEAN ) , state('L1fifotail')  == slot )
    inst = Instruction('DEQLOC_L1'  , decode )
    inst.setEntity( Eid )
    inst.setUpdateToState('L1fifotail', state('L1fifotail') + 1)
    #dequeue( state(d,w).L1.fifo, inst ) # seperate time
    inst.recordAddr( x )
    inst.tp = 'gpuEnvTrans'
    return inst


def ev_DEQLOC_L2(x, slot,Eid, state, **useless):
    decode = z3.And( z3.Or( state('L2fr', addr = x) == INVALID , state('L2hy', addr = x) == CLEAN ) , state('L2fifotail')  == slot )
    inst = Instruction('DEQLOC_L2'  , decode )
    inst.setEntity( Eid )
    inst.setUpdateToState('L2fifotail', state('L2fifotail') + 1)
    #dequeue( state(d).L2.fifo, inst ) # seperate time
    inst.recordAddr( x )
    inst.tp = 'gpuEnvTrans'
    return inst

def ev_DEQMARKER_L1(slot, Eid,state, **useless):
    inst = Instruction('DEQMARKER_L1' , state('L1fifotail') == slot  )
    inst.setEntity( Eid )
    inst.setUpdateToState('L1fifotail', state('L1fifotail') + 1)
    inst.tp = 'gpuEnvTrans'
    return inst

def ev_DEQMARKER_L2(slot, Eid,state, **useless):
    inst = Instruction('DEQMARKER_L2' , state('L2fifotail') == slot )
    inst.setEntity( Eid )
    inst.setUpdateToState('L2fifotail', state('L2fifotail') + 1)
    inst.tp = 'gpuEnvTrans'
    return inst






# ------------------------------
# Summary instructions
# ------------------------------

# they won't exist, they are just a summary of several instructions
