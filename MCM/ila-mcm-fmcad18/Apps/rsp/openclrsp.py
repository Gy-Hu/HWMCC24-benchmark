# in this file, we define the MCM model
# state(d,w,t).r(?)
# state.mem(x)
from entity import *


# 3 views
#  wgview, devview
# LOAD = load_na_or_WG + load_DV_N + load_DV_R

# the read view operations must be enforced some where in the axioms (not here)
def CL_load_na_or_WG(r,x, Eid, state):
    inst = OpenCLInstruction('load_na_or_WG', True)
    inst.setEntity( Eid )
    inst.setUpdateToState('r', addr = r , func = state('mem', addr = x) )
    inst.relatedAxiom = """
    Axiom load_na_or_WG_SC
    forall l1:load_na_or_WG | forall l2:LOAD (~=l1) | ( HB[l1,l2] /\ SameWg[l1,l2] ) => HB[l1.rvop.WG, l2.rvop.WG]
    """ # no # same wg and HB
    # PO same thread and HB  
    # Define PO [a,b] := SameTh[a,b] /\ HB[a,b] ??
    return inst

def CL_load_DV_N(r,x, Eid, state):
    inst = OpenCLInstruction('load_DV_N', True)
    inst.setEntity( Eid )
    inst.setUpdateToState('r', addr = r , func = state('mem', addr = x) )
    inst.relatedAxiom = """
    Axiom load_DV_N_WG_SC
    forall l1:load_DV_N | forall l2:LOAD (~= l1) | ( HB[l1,l2] /\ SameWg[l1,l2] ) => HB[l1.rvop.WG, l2.rvop.WG]

    Axiom load_DV_N_WG_REL
    forall l1:load_DV_N | forall l2:LOAD (~= l1) | ( HB[l1.rvop.WG, l2.rvop.WG] /\ SameWg[l1,l2] ) => HBd[l1.rvop.DV, l2.rvop.DV] 

    # 
    """
    return inst

def CL_load_DV_R(r,x, Eid, state):
    inst = OpenCLInstruction('load_DV_R', True)
    inst.setEntity( Eid )
    inst.setUpdateToState('r', addr = r , func = state('mem', addr = x) )
    inst.relatedAxiom = """
    Axiom load_DV_R_WG_SC
    forall l1:load_DV_R | forall l2:LOAD (~= l1) | ( HB[l1,l2] /\ SameWg[l1,l2] ) => HB[l1.rvop.WG, l2.rvop.WG]

    Axiom load_DV_R_WG_REL
    forall l1:load_DV_R | forall l2:LOAD (~= l1) | ( HB[l1.rvop.WG, l2.rvop.WG] /\ SameWg[l1,l2] ) => HBd[l1.rvop.DV, l2.rvop.DV] 

    Axiom load_DV_R_RSP
    forall l1: load_DV_R | forall s1:STORE | ( SameDv[s1,l1] /\ RF[s1,l1] ) => (       ## SameDv and RF means RFDv ##
        forall s2: STORE (~=s1) | ( HB[s2.wvop.WG, s1.wvop.WG] /\ SameWg[ s1,s2 ] ) => HBd[s2.wvop.DV, l1.end] 
        )
    """
    return inst

def CL_store_na_or_WG(r,x, Eid, state):
    inst = OpenCLInstruction('store_na_or_WG', True)
    inst.setEntity( Eid )
    inst.setUpdateToState( 'mem', addr = x, func = state('r', addr = r) )
    inst.relatedAxiom = """
    Axiom store_na_or_WG_SC
    forall s1:store_na_or_WG | forall s2: STORE (~=s1) | ( HB[s2,s1] /\ SameWg[s2,s1] ) =>  HB[s2.wvop.WG , s1.wvop.WG]
    """ # None
    return inst

def CL_store_DV_N(r,x, Eid, state):
    inst = OpenCLInstruction('store_DV_N', True)
    inst.setEntity( Eid )
    inst.setUpdateToState( 'mem', addr = x, func = state('r', addr = r) )
    inst.relatedAxiom = """
    Axiom store_DV_N_SC
    forall s1: store_DV_N | forall s2: STORE (~=s1) | ( HB[s2,s1] /\ SameWg[s2,s1] ) =>  HB[s2.wvop.WG , s1.wvop.WG]

    Axiom store_DV_N_WG_DV
    forall s1: store_DV_N | forall s2: STORE (~=s1) | ( HB[s2.wvop.WG, s1.wvop.WG] /\ SameWg[ s1,s2 ] ) => HB[s2.wvop.DV, s1.wvop.DV]
    """
    return inst

def CL_store_DV_R(r,x, Eid, state):
    inst = OpenCLInstruction('store_DV_R', True)
    inst.setEntity( Eid )
    inst.setUpdateToState( 'mem', addr = x, func = state('r', addr = r) )
    inst.relatedAxiom = """
    Axiom store_DV_R_PO_WG
    forall s1: store_DV_R | forall s2: STORE (~=s1) | ( HB[s2,s1] /\ SameWg[s2,s1] ) =>  HB[s2.wvop.WG , s1.wvop.WG]

    Axiom store_DV_R_WG_DV
    forall s1: store_DV_R | forall s2: STORE (~=s1) | ( HB[s2.wvop.WG, s1.wvop.WG] /\ SameWg[ s1,s2 ] ) => HB[s2.wvop.DV, s1.wvop.DV]

    # this includes the indirect part #

    Axiom store_DV_R_RSP
    forall s1: store_DV_R | forall r: LOAD | ( RF[s1,r] /\ SameDv[s1,r] ) => (forall r2: LOAD (~=r) | ( HB[r.rvop.WG, r2.rvop.WG] /\ SameWg[r,r2] ) => HBd[s1.wvop.DV, r2.rvop.DV]   )

    Axiom store_DV_R_RSP_RMW
    forall s1: store_DV_R | forall rmw:RMW | HB[ rmw.rvop.DV , s1.wvop.DV ] => HB [rmw.wvop.DV, s1.wvop.DV ]
    # equivalent to: HB[ s1.wvop.DV , rmw.rvop.DV] \/ HB[ rmw.wvop.DV, s1.wvop.DV ]


    # rmw rvop.WG -->-- wvop.WG is unbreakable is guaranteed by itself
    # here we just guarantee that the

    # can be combined with  the RF_CO_FR axiom ?? 
    """
    return inst

def CL_fetch_inc_WG(r,x, Eid, state):
    inst = OpenCLInstruction('fetch_inc_WG', True)
    inst.setEntity( Eid )
    inst.setUpdateToState( 'mem', addr = x, func = state('r', addr = r) + 1 )
    inst.relatedAxiom = """
    Axiom fetch_inc_WG_to_LOAD
    forall rmw1: fetch_inc_WG | forall m: LOAD | SameWg[m,rmw1] => ( HB[ m.rvop.WG , rmw1.rvop.WG ] \/ HB[ rmw1.wvop.WG, m.rvop.WG ] )
    # LOAD includes rmw

    Axiom fetch_inc_WG_to_STORE
    forall rmw1: fetch_inc_WG | forall m: STORE | SameWg[m,rmw1] => ( HB[ m.wvop.WG , rmw1.rvop.WG ] \/ HB[ rmw1.wvop.WG, m.wvop.WG ] )
    # LOAD includes rmw
    """
    return inst

# other axioms

# FIXME: FETCH !!!
