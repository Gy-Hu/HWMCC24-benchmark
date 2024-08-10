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
	self.runProp.append(  z3.simplify( var5 ) )
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
	self.runProp.append(  z3.simplify( var10 ) )
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
	self.runProp.append(  z3.simplify( var15 ) )
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
	self.runProp.append(  z3.simplify( var20 ) )
	# ----- AXIOM load_DV_R_WG_SC END -----
	# ----- AXIOM load_DV_R_WG_REL BEGIN -----
	var24_L = []
	for l1 in obj.load_DV_R_list:  # forall l1 : obj.load_DV_R_list
		var22_L = []
		for l2 in obj.LOAD_list:  # forall l2 : obj.LOAD_list
			if  l2 is l1: continue 
			var21 = z3.Implies( True , z3.Implies( ( z3.And( HB ( l1.rvop.WG , l2.rvop.WG )  , SameWg ( l1 , l2 )  )  ) , HB ( l1.rvop.DV , l2.rvop.DV )  )  )
			var22_L.append( var21)
		var23 = LAnd( var22_L)
		var24_L.append( var23)
	var25 = LAnd( var24_L)
	self.runProp.append(  z3.simplify( var25 ) )
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
	self.runProp.append(  z3.simplify( var30 ) )
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
	self.runProp.append(  z3.simplify( var35 ) )
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
	self.runProp.append(  z3.simplify( var40 ) )
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
	self.runProp.append(  z3.simplify( var45 ) )
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
	self.runProp.append(  z3.simplify( var50 ) )
	# ----- AXIOM store_DV_R_WG_DV END -----