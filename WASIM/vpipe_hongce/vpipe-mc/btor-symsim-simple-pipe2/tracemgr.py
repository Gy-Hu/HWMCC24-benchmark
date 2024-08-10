from pysmt.shortcuts import Symbol, Not, And, Or, Implies, Ite, BVAdd, BV, EqualsOrIff, BVNot, BVSub, TRUE, is_sat, get_model, get_free_variables, is_valid
from pysmt.typing import BOOL, BVType
from yaml import serialize
from independence_check import e_is_always_valid, e_is_independent_of_v, substitute_simplify
from sts import StateAsmpt

class TraceManager(object):
  def __init__(self, ts):
    self.ts = ts # the transition system

    # input variables / state variables
    self.invar = set(ts.input_var)
    self.svar  = set(ts.state_var)
    self.Xvar = set()

    self.base_var = set()
    self.abs_state = [] # a list of abstracted state
    self.abs_state_one_step = []
    self.simp_state = [] # a list of simplified state
    self.prev_state_list = []
    self.curr_state_list = []

  def record_x_var(self, var): #?
    # a list of/set of/ X variables
    if isinstance(var,list):
      self.Xvar.update(set(var))
    elif isinstance(var, set):
      self.Xvar.update(var)
    else: # if it is a single variable
      self.Xvar.add(var)
    #add --> add a single element to the set
    #update --> add multiple elements to the set

  def record_base_var(self, var):
    # var : the symbolic values that can be regarded as fixed
    # not the input in the middle
    if isinstance(var, list):
      self.base_var.update(set(var))
    elif isinstance(var, set):
      self.base_var.update(var)
    else:
      self.base_var.add(var)
  
  def remove_base_var(self,var):
    self.base_var.remove(var)

  def record_state_w_asmpt(self, state: StateAsmpt, Xvar):
    # 1. test if input state can be subsumed by some existing one
    self.record_x_var(Xvar)

    for s in self.abs_state:
      if self.abs_eq(s_abs=s, s2=state):  # if the given state can be regarded as the same as some state before
        return False
    # o.w. , record this state
    self.abs_state.append(self.abstract(state))
    return True


  def record_state_w_asmpt3(self, new_state_list, state: StateAsmpt, Xvar):
    """ Check if `state` is one of `new_state_list`, if not record in `self.abs_state` """
    self.record_x_var(Xvar)

    for s in new_state_list:
      if self.abs_eq(s_abs=self.abstract(s), s2=state):  # if the given state can be regarded as the same as some state before
        return False
    # o.w. , record this state
    self.abs_state.append(self.abstract(state))
    return True

  
  def compare_record_state_w_asmpt(self, prev_state:StateAsmpt,curr_state:StateAsmpt, Xvar):
    # print('len_of_abs_state',len(self.abs_state))
    # self.record_x_var(Xvar)
    # if self.abs_eq(s_abs=self.abs_state[0],s2=prev_state):
    #   print('0')
    #   return False

    

    # for i in range(len(self.prev_state_list)):
    #   if self.abs_eq(s_abs=self.abstract(prev_state),s2=self.prev_state_list[i]):
    #     if self.abs_eq(s_abs=self.abstract(curr_state),s2=self.curr_state_list[i]):
    #       print('1')
    #       print('i =',i)
    #       self.prev_state_list.append(self.abstract(prev_state))
    #       self.curr_state_list.append(self.abstract(curr_state))
    #       print('len = ',len(self.curr_state_list))
    #       return False

    # self.prev_state_list.append(self.abstract(prev_state))
    # self.curr_state_list.append(self.abstract(curr_state))
    # print('len = ',len(self.curr_state_list))
    

    if self.abs_eq(s_abs=self.abstract(prev_state), s2=curr_state):
      # print('2')
      # del self.prev_state_list[-1]
      # del self.curr_state_list[-1]
      return False
    else:
      # print('before:',len(self.abs_state))
      self.abs_state.append(self.abstract(curr_state))
      return True

  def determine_new_state(self,state_list,parent_id_list,state):
    pass

   

  def record_state_w_asmpt_one_step(self, state: StateAsmpt):
    self.abs_state_one_step.append(self.abstract(state))
    return True


  def _debug_abs_check(self, expr, assumptions):
    print ('-----------------')
    print ('expr:', expr.serialize())
    for idx,a in enumerate(assumptions):
      print ('* a'+ str(idx) + ':', a.serialize())
    print ('-----------------')

  def abs_eq(self, s_abs: StateAsmpt, s2: StateAsmpt) -> bool:
    # check if s2 is abstractly equal to an abstract state: s_abs
    expr = TRUE()
    for s, v in s_abs.sv.items():
      if not (s in s2.sv):
        return False
      v2 = s2.sv[s]
      expr = And(expr, EqualsOrIff(v, v2))

    assumptions = s_abs.asmpt + s2.asmpt
    if not is_sat(And(assumptions)):  # a sanity check to make sure assumptions are compatible
      return False
    # self._debug_abs_check(expr, assumptions)
    valid = e_is_always_valid(expr, assumptions)  # expr:  And( v1==v1' , v2==v2' , ... )
    return valid
    
  
  # def state_eq(self, state1: StateAsmpt,state2: StateAsmpt) -> bool:
  #   for s1, v1 in state1.sv.items():
  #       if not (s1 in state1.sv):
  #         return False
  #       v2 = state2.sv[s1]
  #       if(v1 != v2):
  #         return False
  #   if (len(state1.asmpt) != len(state2.asmpt)):
  #     return False
  #   else:
  #     for i in range(len(state1.asmpt)):
  #       if(state1.asmpt[i] != state2.asmpt[i]):
  #         return False
  #       else:
  #         return True

  # def add_state(self, state, flag_list):
  #   if(flag_list == 'prv'):
  #     self.prv_state.append(state)
  #   elif(flag_list == 'cur'):
  #     self.cur_state.append(state)

  # def del_state(self,flag_list):
  #   if(flag_list == 'prv'):
  #     self.prv_state.pop()
  #   elif(flag_list == 'cur'):
  #     self.cur_state.pop()

  def _debug_concrete_check(self, Xs, E, As):
    print ('='*20)
    print ('expr:', E.serialize())
    for idx,a in enumerate(As):
      print ('* a'+ str(idx) + ':', a.serialize())
    print ('Xs:', Xs)
    print ('='*20)

  def concretize(self, s_in:StateAsmpt, Xs) -> StateAsmpt:
    self.record_x_var(Xs)

    asmpt = s_in.asmpt.copy()
    asmpt_interp = s_in.assumption_interp.copy()
    ret_sv = dict()
    m = get_model(And(asmpt))
    print(m)

    for s,v in s_in.sv.items():
      allv_in_v = get_free_variables(v)
      allv_in_v = allv_in_v.intersection(self.Xvar)

      expr = v
      for X in allv_in_v:
        ind = e_is_independent_of_v(e=expr, v=X, assumptions=asmpt)
        if ind:
          val = m.get_value(X)
          sub = {X:val}
          expr = expr.substitute(sub).simplify()
          # expr = substitute_simplify(e=expr, v=X, assumptions=asmpt)
      ret_sv[s] = expr

    return StateAsmpt(sv=ret_sv, asmpt=asmpt, assumption_interp=asmpt_interp)

  def check_reachable(self, s_in: StateAsmpt) -> bool:
    asmpt = s_in.asmpt
    current_asmpt_sat = is_sat(And(asmpt))
    # if (current_asmpt_sat == False):
    #   print(asmpt)
    #   for a in asmpt:
    #     print(a.serialize())
    #     check_sat = is_sat(a)
    #     if(check_sat == False):
    #       print('check false!!',a.serialize())
    return current_asmpt_sat

  def check_concrete_enough(self, s_in: StateAsmpt, Xs):
    # check if s is semantically concrete enough?
    #  if s contains no X on the base_vars
    self.record_x_var(Xs)
    
    if len(self.base_var) == 0:
      print ("WARNING : set base_var first!")

    for s, v in s_in.sv.items():
      if s not in self.base_var:
        continue
      allv_in_v = get_free_variables(v)
      allv_in_v = allv_in_v.intersection(self.Xvar)
      # for all the X variables appearing in v, check if X affecting the output
      # if not, the Xs can actually be eliminated.
      for X in allv_in_v:
        ind = e_is_independent_of_v(e=v, v=X, assumptions=s_in.asmpt)
        if not ind:
          return False
        # print('e:',v.serialize())
        # print('x:',X)
        # if v.bv_width() == 1:
        #   print (is_sat(And([EqualsOrIff(v, BV(0,1) )]+s_in.asmpt)))
        #   print (is_sat(And([EqualsOrIff(v, BV(1,1) )]+s_in.asmpt)))

        # otherwise it is independent of X
        # we can replace (eliminate) it actually
    return True

  def abstract(self, s:StateAsmpt): # -> StateAsmpt
    # current policy: only keep those on base_var
    if len(self.base_var) == 0:
      print ("WARNING : set base_var first!")
    s2 = StateAsmpt(sv={}, asmpt=s.asmpt.copy(), assumption_interp=s.assumption_interp.copy())
    for s, v in s.sv.items():
      if s in self.base_var:
        s2.sv[s] = v
    return s2

  