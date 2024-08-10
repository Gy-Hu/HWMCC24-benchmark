from pysmt.shortcuts import Symbol, Not, And, Or, Implies, Ite, BVAdd, BV, EqualsOrIff, BVNot, BVSub, TRUE, is_sat, get_model, get_free_variables, Interpolator
from pysmt.typing import BOOL, BVType
from pysmt.logics import QF_BV

class BMC(object):
  def __init__(self, ts):
    self.ts = ts # the transition system

    # input variables & state variables
    self.invar = ts.input_var
    self.svar  = ts.state_var
    
    self.timed_var = dict() # t -> (v -> v)
    self.trans_rels = []
    self.constraint = []

  def _get_var(self, v, t: int):
    assert t>=0
    if t in self.timed_var:
      if v in self.timed_var[t]:
        return self.timed_var[t][v] 
    n = str(v)
    bitwidth = v.bv_width()
    symb = Symbol(n+'_'+str(t), BVType(bitwidth))
    if t not in self.timed_var:
      self.timed_var[t] = dict()
    self.timed_var[t][v] = symb    
    return symb
    
  def get_varset_at(self, t: int):
    # t is the time t >= 0
    if t in self.timed_var:
      return self.timed_var[t]
    allvars = self.invar.union(self.svar)
    for v in allvars:
      self._get_var(v, t)
    return self.timed_var[t]
  
  def varmap_to_prime(self, vmap):
    retvmap = {}
    for v, timev in vmap.items():
      primev = self.ts.get_prime(v)
      retvmap[primev] = timev
    return retvmap
  
  def sv(self, n: str):
    # n: name (string) , returns the variable/expression corresponds to this name
    return self.ts.named_var[n] # named_var also includes wire name
    
  def sv_at(self, n: str, t: int):
    # n: name (string) , returns the variable/expression corresponds to this name
    vmap = self.get_varset_at(t)
    v = self.ts.named_var[n]
    if v in vmap: # it may be an variable
      return vmap[v]
    return v.substitue(vmap) # named_var also includes wire name
    
  def interpret_expr_at(self, expr, t: int):
    vmap = self.get_varset_at(t)
    return expr.substitute(vmap)
  
  def init_step(self):
    vmap = self.get_varset_at(0)
    initconstr = self.ts.init.substitute(vmap)
    self.constraint = [initconstr]
    
  def unroll_onestep(self):
    prevIdx = len(self.trans_rels)          # suppose prevIdx == 1
    prevmap = self.get_varset_at(prevIdx)   # e.g., v --> v_1
    postmap = self.get_varset_at(prevIdx+1) # e.g., v --> v_2
    postmap = self.varmap_to_prime(postmap) #       v'--> v_2
    
    tran_rel = self.ts.trans.substitute({**prevmap, **postmap})
    self.trans_rels.append(tran_rel)
    self.constraint.append( self.ts.assumption.substitute(prevmap) )
  
  def get_constr(self):
    k = len(self.trans_rels)
    return self.constraint + self.trans_rels + [self.interpret_expr_at(self.ts.assumption, k)]
    
  def get_constr_seq(self):
    # we want   (init /\ init assumpt) /\ (T01 /\ constr1) /\ (T12 /\ constr2)
    k = len(self.trans_rels)
    constr = self.constraint + [self.interpret_expr_at(self.ts.assumption, k)]
    trans = self.trans_rels
    
    retl = [ And(constr[0:2]) ]
    assert (len(trans) == len(constr)-2)
    for kt in range(2, len(constr)):
      retl.append ( And(trans[kt-2], constr[kt]) )
    return retl
    


def main():
  from pathlib import Path
  from btorparser import BTOR2Parser

  btor_parser = BTOR2Parser()
  sts, prop = btor_parser.parse_file(Path("example/pipe-no-stall.btor2"))
  prop = And([p[2] for p in prop])
  bmc = BMC(sts)
  cover = EqualsOrIff(bmc.sv('tag3'), BV(1,1)) # tag3 == 1
  
  bmc.init_step()
  prop0 = bmc.interpret_expr_at(prop, 0)
  cover0 = bmc.interpret_expr_at(cover, 0)
  cnstr = bmc.get_constr()
  
  print ('0 SAT:', is_sat(And(cnstr + [Not(prop0)])), 'Cover:', is_sat(And(cnstr + [cover0])))
  
  for k in range(1,10):
    bmc.unroll_onestep()
    propK = bmc.interpret_expr_at(prop, k)
    coverK = bmc.interpret_expr_at(cover, k)
    cnstr = bmc.get_constr()
    res = is_sat(And(cnstr + [Not(propK)]))
    res2 = is_sat(And(cnstr + [coverK]))
    
    print ( k , 'SAT:', res, "Cover:", res2)
    assert res == False
    if res2:
      constr_sep = bmc.get_constr_seq()
      constr_sep.append(Not(propK))
      itp_solver = Interpolator(logic=QF_BV)
      itps = itp_solver.sequence_interpolant(constr_sep)
      #for sep in constr_sep:
      #  print (sep.serialize())
      for itp in itps:
        print (itp.serialize())
      print ('----------------')
      
    # see if converge?
      
      
    
   
  #for c in cnstr:
  #  print (c.serialize())
  #print (propK.serialize())
  


if __name__ == '__main__':
  main()
