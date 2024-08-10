import z3
    
def SameWg(i1,i2):
    e1 = i1.Eid ; e2 = i2.Eid
    assert e1.anyd == e2.anyd and e1.anyw == e2.anyw and e1.anyt == e2.anyt
    retL = True
    if not e1.anyd:
        retL = retL and ( e1.d == e2.d )
        if not e1.anyw:
            retL = retL and ( e1.w == e2.w )
    return retL

def SameDv(i1,i2):
    e1 = i1.Eid ; e2 = i2.Eid
    assert e1.anyd == e2.anyd and e1.anyw == e2.anyw and e1.anyt == e2.anyt
    if not e1.anyd:
        return e1.d == e2.d
    return True


def HB(a,b):
    return a.timestamp < b.timestamp

def HBd(a,b):
    return z3.Implies( z3.And( a.inst.decodeFunc, b.inst.decodeFunc), a.timestamp < b.timestamp )


def either_or(a,b):
    return ( a and not b ) or (b and not a)

def SameAddr(i1,i2):
    assert either_or(i1.wvop is None , i1.rvop is None)
    assert either_or(i2.wvop is None , i2.rvop is None)
    addr1 = i1.wvop.addr if i1.wvop is not None else i1.rvop.addr
    addr2 = i2.wvop.addr if i2.wvop is not None else i2.rvop.addr
    return addr1 == addr2

def SameData(i1,i2):
    assert either_or(i1.wvop is None , i1.rvop is None)
    assert either_or(i2.wvop is None , i2.rvop is None)
    val1 = i1.wvop.value if i1.wvop is not None else i1.rvop.value
    val2 = i2.wvop.value if i2.wvop is not None else i2.rvop.value
    return val1 == val2


def LAnd(l):
    if len(l) == 0:
        print '<W> Axiom Scenario does not exist'
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

def PO2Axioms(obj):
        # ----- AXIOM load_na_or_WG_SC BEGIN -----
    var4_L = []
    for l1 in obj.load_na_or_WG_list:  # forall l1 : obj.load_na_or_WG_list
        var2_L = []
        for l2 in obj.LOAD_list:  # forall l2 : obj.LOAD_list
            if  l2 is l1: continue 
            var1 = z3.Implies( True , z3.Implies( ( z3.And( HB ( l1 , l2 )  , SameWg ( l1 , l2 )  )  ) , HB ( l1.rvop.WG , l2.rvop.WG )  )  )
            var2_L.append( var1)
        var3 = LAnd( var2_L)
        var4_L.append( var3)
    var5 = LAnd( var4_L)
    obj.runProp.append(  z3.simplify( var5 ) )
    # ----- AXIOM load_na_or_WG_SC END -----
    # ----- AXIOM load_DV_N_WG_SC BEGIN -----
    var9_L = []
    for l1 in obj.load_DV_N_list:  # forall l1 : obj.load_DV_N_list
        var7_L = []
        for l2 in obj.LOAD_list:  # forall l2 : obj.LOAD_list
            if  l2 is l1: continue 
            var6 = z3.Implies( True , z3.Implies( ( z3.And( HB ( l1 , l2 )  , SameWg ( l1 , l2 )  )  ) , HB ( l1.rvop.WG , l2.rvop.WG )  )  )
            var7_L.append( var6)
        var8 = LAnd( var7_L)
        var9_L.append( var8)
    var10 = LAnd( var9_L)
    obj.runProp.append(  z3.simplify( var10 ) )
    # ----- AXIOM load_DV_N_WG_SC END -----
    # ----- AXIOM load_DV_N_WG_REL BEGIN -----
    var14_L = []
    for l1 in obj.load_DV_N_list:  # forall l1 : obj.load_DV_N_list
        var12_L = []
        for l2 in obj.LOAD_list:  # forall l2 : obj.LOAD_list
            if  l2 is l1: continue 
            var11 = z3.Implies( True , z3.Implies( ( z3.And( HB ( l1.rvop.WG , l2.rvop.WG )  , SameWg ( l1 , l2 )  )  ) , HBd ( l1.rvop.DV , l2.rvop.DV )  )  )
            var12_L.append( var11)
        var13 = LAnd( var12_L)
        var14_L.append( var13)
    var15 = LAnd( var14_L)
    obj.runProp.append(  z3.simplify( var15 ) )
    # ----- AXIOM load_DV_N_WG_REL END -----
    # ----- AXIOM load_DV_R_WG_SC BEGIN -----
    var19_L = []
    for l1 in obj.load_DV_R_list:  # forall l1 : obj.load_DV_R_list
        var17_L = []
        for l2 in obj.LOAD_list:  # forall l2 : obj.LOAD_list
            if  l2 is l1: continue 
            var16 = z3.Implies( True , z3.Implies( ( z3.And( HB ( l1 , l2 )  , SameWg ( l1 , l2 )  )  ) , HB ( l1.rvop.WG , l2.rvop.WG )  )  )
            var17_L.append( var16)
        var18 = LAnd( var17_L)
        var19_L.append( var18)
    var20 = LAnd( var19_L)
    obj.runProp.append(  z3.simplify( var20 ) )
    # ----- AXIOM load_DV_R_WG_SC END -----
    # ----- AXIOM load_DV_R_WG_REL BEGIN -----
    var24_L = []
    for l1 in obj.load_DV_R_list:  # forall l1 : obj.load_DV_R_list
        var22_L = []
        for l2 in obj.LOAD_list:  # forall l2 : obj.LOAD_list
            if  l2 is l1: continue 
            var21 = z3.Implies( True , z3.Implies( ( z3.And( HB ( l1.rvop.WG , l2.rvop.WG )  , SameWg ( l1 , l2 )  )  ) , HBd ( l1.rvop.DV , l2.rvop.DV )  )  )
            var22_L.append( var21)
        var23 = LAnd( var22_L)
        var24_L.append( var23)
    var25 = LAnd( var24_L)
    obj.runProp.append(  z3.simplify( var25 ) )
    # ----- AXIOM load_DV_R_WG_REL END -----
    # ----- AXIOM store_na_or_WG_SC BEGIN -----
    var29_L = []
    for s1 in obj.store_na_or_WG_list:  # forall s1 : obj.store_na_or_WG_list
        var27_L = []
        for s2 in obj.STORE_list:  # forall s2 : obj.STORE_list
            if  s2 is s1: continue 
            var26 = z3.Implies( True , z3.Implies( ( z3.And( HB ( s2 , s1 )  , SameWg ( s2 , s1 )  )  ) , HB ( s2.wvop.WG , s1.wvop.WG )  )  )
            var27_L.append( var26)
        var28 = LAnd( var27_L)
        var29_L.append( var28)
    var30 = LAnd( var29_L)
    obj.runProp.append(  z3.simplify( var30 ) )
    # ----- AXIOM store_na_or_WG_SC END -----
    # ----- AXIOM store_DV_N_SC BEGIN -----
    var34_L = []
    for s1 in obj.store_DV_N_list:  # forall s1 : obj.store_DV_N_list
        var32_L = []
        for s2 in obj.STORE_list:  # forall s2 : obj.STORE_list
            if  s2 is s1: continue 
            var31 = z3.Implies( True , z3.Implies( ( z3.And( HB ( s2 , s1 )  , SameWg ( s2 , s1 )  )  ) , HB ( s2.wvop.WG , s1.wvop.WG )  )  )
            var32_L.append( var31)
        var33 = LAnd( var32_L)
        var34_L.append( var33)
    var35 = LAnd( var34_L)
    obj.runProp.append(  z3.simplify( var35 ) )
    # ----- AXIOM store_DV_N_SC END -----
    # ----- AXIOM store_DV_N_WG_DV BEGIN -----
    var39_L = []
    for s1 in obj.store_DV_N_list:  # forall s1 : obj.store_DV_N_list
        var37_L = []
        for s2 in obj.STORE_list:  # forall s2 : obj.STORE_list
            if  s2 is s1: continue 
            var36 = z3.Implies( True , z3.Implies( ( z3.And( HB ( s2.wvop.WG , s1.wvop.WG )  , SameWg ( s1 , s2 )  )  ) , HB ( s2.wvop.DV , s1.wvop.DV )  )  )
            var37_L.append( var36)
        var38 = LAnd( var37_L)
        var39_L.append( var38)
    var40 = LAnd( var39_L)
    obj.runProp.append(  z3.simplify( var40 ) )
    # ----- AXIOM store_DV_N_WG_DV END -----
    # ----- AXIOM store_DV_R_PO_WG BEGIN -----
    var44_L = []
    for s1 in obj.store_DV_R_list:  # forall s1 : obj.store_DV_R_list
        var42_L = []
        for s2 in obj.STORE_list:  # forall s2 : obj.STORE_list
            if  s2 is s1: continue 
            var41 = z3.Implies( True , z3.Implies( ( z3.And( HB ( s2 , s1 )  , SameWg ( s2 , s1 )  )  ) , HB ( s2.wvop.WG , s1.wvop.WG )  )  )
            var42_L.append( var41)
        var43 = LAnd( var42_L)
        var44_L.append( var43)
    var45 = LAnd( var44_L)
    obj.runProp.append(  z3.simplify( var45 ) )
    # ----- AXIOM store_DV_R_PO_WG END -----
    # ----- AXIOM store_DV_R_WG_DV BEGIN -----
    var49_L = []
    for s1 in obj.store_DV_R_list:  # forall s1 : obj.store_DV_R_list
        var47_L = []
        for s2 in obj.STORE_list:  # forall s2 : obj.STORE_list
            if  s2 is s1: continue 
            var46 = z3.Implies( True , z3.Implies( ( z3.And( HB ( s2.wvop.WG , s1.wvop.WG )  , SameWg ( s1 , s2 )  )  ) , HB ( s2.wvop.DV , s1.wvop.DV )  )  )
            var47_L.append( var46)
        var48 = LAnd( var47_L)
        var49_L.append( var48)
    var50 = LAnd( var49_L)
    obj.runProp.append(  z3.simplify( var50 ) )
    # ----- AXIOM store_DV_R_WG_DV END -----


def store_dv_r_3(obj):
    def RF(s,l): # read-from s --> load 
        if not SameDv(s,l): return True # this is no use: dummy True

        var1_L = []
        for sother in obj.STORE_list: # forall stores (~=s)
            if sother is s: continue
            var2 = z3.Or( CO(sother,s) , FR(l, sother) )
            var1_L.append(var2)
        var3 = z3.And( var1_L )

        ## SameWg(s,l) ,  z3.And( [var3, SameAddr(s,l), SameData(s,l) , HBd(s.wvop.WG, l.rvop.WG) ] )
        if SameWg(s,l): # this is not made dynamic
            return z3.And( [var3, SameAddr(s,l), SameData(s,l) , HBd(s.wvop.WG, l.rvop.WG) ] )
        # else: SameDv(s,l):
        return z3.And( [var3, SameAddr(s,l), SameData(s,l) , HB(s.wvop.DV, l.rvop.DV), s.wvop.DV.inst.decodeFunc, l.rvop.DV.inst.decodeFunc ] )

    def FR(l,s):
        if not SameDv(s,l): return True
        if SameWg(s,l):
            return z3.Implies( SameAddr(s,l) ,  HBd(l.rvop.WG, s.wvop.WG ) )
        return z3.Implies( SameAddr(s,l) ,  HBd(l.rvop.DV, s.wvop.DV ) )

    def CO(s1,s2):
        if not SameDv(s1,s2): return True
        if SameWg(s1,s2):
            return z3.Implies( SameAddr(s1,s2) ,  HB(s1.wvop.WG, s2.wvop.WG ) )
        return z3.Implies( SameAddr(s1,s2) ,  HB(s1.wvop.DV, s2.wvop.DV ) )
    # ----- AXIOM store_DV_R_RSP BEGIN -----
    var6_L = []
    for s1 in obj.store_DV_R_list:  # forall s1 : obj.store_DV_R_list
        var4_L = []
        for r in obj.LOAD_list:  # forall r : obj.LOAD_list
            var2_L = []
            for r2 in obj.LOAD_list:  # forall r2 : obj.LOAD_list
                if  r2 is r: continue 
                var1 = z3.Implies( True , z3.Implies( ( z3.And( HB ( r.rvop.WG , r2.rvop.WG )  , z3.BoolVal( SameWg ( r , r2 ) )  )  ) , HBd ( s1.wvop.DV , r2.rvop.DV )  )  )
                var2_L.append( var1)

            var3 = LAnd( var2_L)
            var4_L.append( z3.Implies( z3.And( z3.BoolVal( SameDv ( s1,r) ),  RF ( s1 , r ) ) , ( var3 ) ) )
        var5 = LAnd( var4_L)
        var6_L.append( var5)
    var7 = LAnd( var6_L)
    obj.runProp.append(  z3.simplify( var7 ) ) #
    # ----- AXIOM store_DV_R_RSP END -----

def load_dv_r_3(obj):
    def RF(s,l): # read-from s --> load 
        if not SameDv(s,l): return True # this is no use: dummy True

        var1_L = []
        for sother in obj.STORE_list: # forall stores (~=s)
            if sother is s: continue
            var2 = z3.Or( CO(sother,s) , FR(l, sother) )
            var1_L.append(var2)
        var3 = z3.And( var1_L )

        ## SameWg(s,l) ,  z3.And( [var3, SameAddr(s,l), SameData(s,l) , HBd(s.wvop.WG, l.rvop.WG) ] )
        if SameWg(s,l): # this is not made dynamic
            return z3.And( [var3, SameAddr(s,l), SameData(s,l) , HBd(s.wvop.WG, l.rvop.WG) ] )
        # else: SameDv(s,l): # we must make sure they read from the way we define
        return z3.And( [var3, SameAddr(s,l), SameData(s,l) , HB(s.wvop.DV, l.rvop.DV), s.wvop.DV.inst.decodeFunc, l.rvop.DV.inst.decodeFunc ] )

    def FR(l,s):
        if not SameDv(s,l): return True
        if SameWg(s,l):
            return z3.Implies( SameAddr(s,l) ,  HBd(l.rvop.WG, s.wvop.WG ) )
        return z3.Implies( SameAddr(s,l) ,  HBd(l.rvop.DV, s.wvop.DV ) )

    def CO(s1,s2):
        if not SameDv(s1,s2): return True
        if SameWg(s1,s2):
            return z3.Implies( SameAddr(s1,s2) ,  HB(s1.wvop.WG, s2.wvop.WG ) )
        return z3.Implies( SameAddr(s1,s2) ,  HB(s1.wvop.DV, s2.wvop.DV ) )
    # ----- AXIOM load_DV_R_RSP BEGIN -----
    var6_L = []
    for l1 in obj.load_DV_R_list:  # forall l1 : obj.load_DV_R_list
        var4_L = []
        for s1 in obj.STORE_list:  # forall s1 : obj.STORE_list
            var2_L = []
            for s2 in obj.STORE_list:  # forall s2 : obj.STORE_list
                if  s2 is s1: continue 
                var1 = z3.Implies( True , z3.Implies( ( z3.And( HB ( s2.wvop.WG , s1.wvop.WG )  , z3.BoolVal( SameWg ( s1 , s2 ) ) )  ) , HBd ( s2.wvop.DV , l1.end )  )  )
                var2_L.append( var1)
            var3 = LAnd( var2_L)
            var4_L.append( z3.Implies( ( z3.And( z3.BoolVal( SameDv ( s1 , l1 ) )  , RF ( s1 , l1 )  )  ) , ( var3 ) ) )
        var5 = LAnd( var4_L)
        var6_L.append( var5)
    var7 = LAnd( var6_L)
    obj.runProp.append(  z3.simplify( var7 ) )
    # ----- AXIOM load_DV_R_RSP END -----