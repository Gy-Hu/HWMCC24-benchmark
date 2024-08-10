from pysmt.shortcuts import Symbol, Not, And, Or, Implies, Ite, BVAdd, BV, EqualsOrIff, BVNot, BVSub, TRUE, is_sat, get_model, get_free_variables
from pysmt.typing import BOOL, BVType
from sts import StateAsmpt

class ChoiceItem(object):
  # This contains a set of assumptions and assignment to the input variables.
  # You need to first set assignment for the input variables,
  # before trying to interpret any constaints that contain input variables
  # UsedInSim is to make sure the last one in the list of history_choice
  # is a set of freshly-added assignment
  def __init__(self, assumptions, var_assign):
    self.assumptions = assumptions.copy()
    self.var_assign = var_assign.copy()
    self.UsedInSim = False
  def setSim(self):
    assert(not self.UsedInSim)
    self.UsedInSim = True
  def CheckSimed(self):
    assert(self.UsedInSim)
  def record_prev_assumption_len(self, l):
    self.assmpt_len=l
  def get_prev_assumption_len(self):
    return self.assmpt_len

class SymbolicExecutor(object):
  def __init__(self, ts):
    self.ts = ts # the transition system

    # input variables & state variables
    self.invar = ts.input_var
    self.svar  = ts.state_var

    self.trace = [] # list of state var assignment. A var assignemnt is a dict : v -> value
    self.history_choice = [] # list of choices
    self.history_assumptions = [] # list of list of assumptions
    self.history_assumptions_interp = [] # list of list of assumption interpretation

    self.name_cnt = {} # name -> counter, these counters are used to generated non-repeated names
    self.Xvar = set()  # a set of X-variables


  def tracelen(self):
    return len(self.trace)

  def all_assumptions(self): # get all assumptions
    return [c for l in self.history_assumptions for c in l]
  def all_assumption_interp(self):
    return [c for l in self.history_assumptions_interp for c in l]

  def sv(self, n: str):
    # n: name (string) , returns the variable/expression corresponds to this name
    return self.ts.named_var[n] # named_var also includes wire name
    
  def cur(self, n: str):
    # n: name (string), interpret var/expr n on the latest state
    sv_mapping = self.trace[-1]
    expr = self.sv(n)
    if not self._expr_only_sv(expr):
      assert(len(self.history_choice) != 0)
      assert(not self.history_choice[-1].UsedInSim)  # make sure we refer to input vars that are newly added
      iv_mapping = self.history_choice[-1].var_assign
      expr = expr.substitute({**sv_mapping, **iv_mapping})
    else:
      expr = expr.substitute(sv_mapping)  # if it does not use input variables, then we only need to substitute state variables
    return expr

  def _check_only_invar(self, vdict):
    # if all elements/keys is vdict are input variables
    for v in vdict:
      assert(v in self.invar)
      
  def _expr_only_sv(self, expr):
    # check if all variables in `expr` contains only the state variables
    varset = get_free_variables(expr)
    for v in varset:
      if v not in self.svar:
        return False
    return True

  def convert(self, vdict):
    # a helper function.
    # vdict should be like {"<string-for-state-var>" : integer/"var-name"}
    retdict = {}
    for v in vdict:
      value = vdict[v]
      if isinstance(v,str): #str-->sv(v)
        v = self.sv(v)
      if isinstance(value, int): #int-->bitvector
        value = BV(value,v.bv_width())
      elif isinstance(value, str): #str-->symbol
        value = Symbol(value, BVType(v.bv_width()))
      retdict[v] = value
    return retdict

  def backtrack(self):
    # return to the previous step
    assert (len(self.history_choice) != 0)
    del self.trace[-1]
    del self.history_assumptions[-1]
    del self.history_assumptions_interp[-1]
    self.history_choice[-1].UsedInSim = False

  def init(self, var_assignment={}) :
    # assign variables in the first step
    # you can (optionally) specify the assignment for init var in var_assignment
    
    # for those not set, we will create a variable internally
    for v in self.svar:
      if v not in var_assignment:
        var_assignment[v] = self.new_var(v.bv_width(), v, x=False )

    self.trace.append(var_assignment)
    
    self._expr_only_sv(self.ts.init) # make sure the initial constraint is only on the state variables
    init_constr = self.ts.init.substitute(var_assignment).simplify()  # initial predicate is
                                                                      # now a constraint
    self.history_assumptions.append([init_constr])  # add initial constraint
    self.history_assumptions_interp.append(['init'])

  def set_current_state(self, s:StateAsmpt, d) :
    # assign variables in the first step
    # you can (optionally) specify the assignment for init var in var_assignment
    
    # for those not set, we will create a variable internally
    self.trace = []
    var_assignment = {**s.sv.copy() , **d}
    for v in self.svar:
      if v not in var_assignment:
        var_assignment[v] = self.new_var(v.bv_width(), v, x=False)

    self.trace.append(var_assignment)

    self.history_assumptions = [s.asmpt.copy()]
    self.history_assumptions_interp = [s.assumption_interp.copy()]
    self.history_choice = []

  def print_current_step(self):
    prev_sv = self.trace[-1]
    print ('|%10s| %s' %( 'sv  ', 'rhs'))
    print ('|%10s|-%s' %( '-'*10, '-'*20))
    for sv, rhs in prev_sv.items():
      print ('|%10s| %s' %( str(sv), rhs.serialize()))
  def print_current_step_assumptions(self):
    for idx,l in enumerate(self.history_assumptions):
      for jdx, a in enumerate(l):
        interp = self.history_assumptions_interp[idx][jdx]
        print ('A%-2d,%-2d:%s'%(idx,jdx,interp))
        print ('A%-2d,%-2d:%s'%(idx,jdx,a.serialize()))

  def set_input(self, invar_assign, pre_assumptions):
    # invar_assign is a dictionary: invar -> expr
    # pre_assumption is on T(n-1), will be interpreted by input var given
    # will also interpret ts.assumption
    if len(self.history_choice) != 0:
      self.history_choice[-1].CheckSimed() 
    # the last choice has been used. Ensure usage: set_input -> sim_one_step -> set_input

    self._check_only_invar(invar_assign)
    prev_sv = self.trace[-1] # the last assignment
    for v in self.invar:
      if v in prev_sv:
        print("WARNING: ignore input assignment as assigned by prev-state,", str(v))
        invar_assign[v] = prev_sv[v]
      if v not in invar_assign: # if input variable is not set by input, then give it a new X variable
        invar_assign[v] = self.new_var(v.bv_width(), v, x=True) # create a (maybe) unconstrained variable
    c = ChoiceItem(assumptions=pre_assumptions, var_assign=invar_assign)
    self.history_choice.append(c)
    c.record_prev_assumption_len(len(self.history_assumptions[-1]))
    assert(len(self.history_assumptions) == len(self.history_assumptions_interp))
    assert(len(self.history_assumptions[-1]) == len(self.history_assumptions_interp[-1]))

    # this is to add to previous frame, interpret the assumptions
    assmpt = self.ts.assumption.substitute({**prev_sv, **invar_assign}).simplify()
    self.history_assumptions[-1].append(assmpt)
    self.history_assumptions_interp[-1].append('ts.asmpt @ ' + str(len(self.trace)-1))
    for assmpt in pre_assumptions:
      self.history_assumptions[-1].append(assmpt.substitute({**prev_sv, **invar_assign}).simplify())
      self.history_assumptions_interp[-1].append(str(assmpt) + '@' + str(len(self.trace) - 1))

  def undo_set_input(self):
    assert(len(self.history_choice) != 0)
    c= self.history_choice[-1]
    assert(not c.UsedInSim) # you cannot undo a simed input
    del self.history_choice[-1]
    l = c.get_prev_assumption_len()
    self.history_assumptions[-1] = self.history_assumptions[-1][0:l]
    self.history_assumptions_interp[-1]=self.history_assumptions_interp[-1][0:l]

  def interpret_state_expr_on_curr_frame(self, expr):
    # expr: list of / an expression contains only state variable
    if isinstance(expr, list):
      ret = []
      for e in expr:
        ret.append(self.interpret_state_expr_on_curr_frame(e))
      return ret
    prev_sv = self.trace[-1]
    if not self._expr_only_sv(expr):
      print ('expr should only contain only state variables')
      exit(1)
      return None
    return expr.substitute(prev_sv)

  def sim_one_step(self):
    assert(len(self.history_choice) != 0)

    c = self.history_choice[-1]
    c.setSim()

    invar_assign = c.var_assign
    prev_sv = self.trace[-1]
    svmap = {}
    for primal_v, rhs in self.ts.sv_update.items(): # update the value of state variables
      svmap[primal_v] = rhs.substitute({**invar_assign, **prev_sv}).simplify() # merge
    self.trace.append(svmap)
    self.history_assumptions.append([])
    self.history_assumptions_interp.append([])

  def get_Xs(self):
    return self.Xvar

  def new_var(self, bitwidth, vname = 'var', x = True):
    n = str(vname)+( 'X' if x else '')
    cnt =  self.name_cnt.get(n, 0) + 1
    self.name_cnt[n] = cnt
    symb = Symbol(n+str(cnt), BVType(bitwidth))
    if x:
      self.Xvar.add(symb)
    return symb
    
  def get_curr_state(self, assumptions=[]) -> StateAsmpt:
    need_to_push_input = False
    if len(self.history_choice) == 0 or self.history_choice[-1].UsedInSim:
      need_to_push_input=True
    if need_to_push_input:
      self.set_input({}, assumptions) # this will also make sure we interpret ts.assumption
    else:
      if len(assumptions) != 0:
        print ("WARNING: assumptions are not used in get_curr_state")
    # this is to add assumption to current state
    # however, assumptions could be on the inputs
    # so we need to give some inputs
    ret = StateAsmpt(sv=self.trace[-1], asmpt=self.all_assumptions(), assumption_interp=self.all_assumption_interp())
    if need_to_push_input:
      self.undo_set_input()
    return ret



def main():
  from pathlib import Path
  from btorparser import BTOR2Parser

  btor_parser = BTOR2Parser()
  sts, _ = btor_parser.parse_file(Path("example/pipe-no-stall.btor2"))
  executor = SymbolicExecutor(sts)

  executor.init(
    executor.convert({
      'wen_stage1':'v1',
      'wen_stage2':'v2',
      'wen_stage3':'v3',
      'stage1':'a',
      'stage2':'b',
      'stage3':'c'
      }))

  #init assumptions tag0
  executor.print_current_step() 
  executor.print_current_step_assumptions()

  #tag1
  executor.set_input(
    executor.convert({'rst':0}), [])
  executor.sim_one_step()

  print ()
  executor.print_current_step()
  executor.print_current_step_assumptions()

  #tag2
  executor.set_input(
    executor.convert({'rst':0}), [])
  executor.sim_one_step()

  print ()
  executor.print_current_step()
  executor.print_current_step_assumptions()

  #tag3
  executor.set_input(
    executor.convert({'rst':1}),[])
  executor.sim_one_step()

  print ()
  executor.print_current_step()
  executor.print_current_step_assumptions()


if __name__ == '__main__':
  main()
