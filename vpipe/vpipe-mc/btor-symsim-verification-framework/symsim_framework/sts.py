# state transition system
from pysmt.shortcuts import Symbol, Not, And, Or, Implies, Ite, BVAdd, BV, EqualsOrIff, BVNot, BVSub, TRUE
from pysmt.typing import BOOL, BVType

# assumptions
class StateAsmpt(object):
  def __init__(self, sv, asmpt, assumption_interp):
    """sv is var->assignment, asmpt is a list of assumptions"""
    assert (isinstance(sv, dict) and isinstance(asmpt, list))
    assert (len(assumption_interp) == len(asmpt))
    #sv:(state variable) dictionary(var->assignment), asmpt: list of assumptions
    self.sv = sv
    self.asmpt = asmpt
    self.assumption_interp = assumption_interp
  def print(self):
    prev_sv = self.sv
    print ('|%10s| %s' %( 'sv  ', 'rhs'))
    print ('|%10s|-%s' %( '-'*10, '-'*20))
    for sv, rhs in prev_sv.items():
      print ('|%10s| %s' %( str(sv), rhs.serialize()))
  def print_assumptions(self):
    for idx,a in enumerate(self.asmpt):
        print ('A%-2d:%s'%(idx,self.assumption_interp[idx]))
        print ('A%-2d:%s'%(idx,a.serialize()))

#transition system
class TransitionSystem(object):
    """Trivial representation of a Transition System."""
    def __init__(self, variables, prime_variables, init, trans):
        self.variables = variables
        self.prime_variables = prime_variables


        self.init = init
        self.trans = trans # T ->  # a formula or list (will need a final conversion)

        # var -> assign_list
        self.sv_update = dict() # state -> update function
        self.named_var = dict() # str -> var/expr
        self.state_var = set()
        self.input_var = set()
        self.output_var = set()
        self.wires = dict()
        self.assumption = TRUE
        self.assertion = TRUE
        self.sv_dependent_map = dict() # state_var -> state_var/input (prev cycle)
        self.sv_influence_map = dict() # state_var -> state_var (next cycle)

    @classmethod
    def get_prime(cls, v):
        """Returns the 'next' of the given variable"""
        return Symbol("%s_prime" % v.symbol_name(), v.symbol_type())
    @classmethod
    def get_primal(cls, v):
        """Returns the 'prev' of the given prime variable"""
        assert v.symbol_name().endswith("_prime")
        return Symbol("%s" % v.symbol_name()[:-6], v.symbol_type())

    def add_func_trans(self, trans):
        self.trans = trans

    def set_init(self, initexpr):
        self.init = initexpr 

    def add_output_var(self, v):
        self.output_var.add(v)
    def add_input_var(self, v):
        self.input_var.add(v)
    def add_state_var(self, v):
        self.state_var.add(v)
    def register_wire_name(self,v,e):
        if v in self.wires:
          print("WARNING: wire ", str(v), " redefined")
        self.wires[v] = e
    def set_assertion(self, a):
        self.assertion = a
    def set_assumption(self, a):
        self.assumption = a
    def finish_adding(self):
        self.variables = self.output_var.union(self.input_var.union(self.state_var))
        self.prime_variables = [TransitionSystem.get_prime(v) for v in self.variables]
        self.v2vprime = {v:TransitionSystem.get_prime(v) for v in self.variables}
        self.named_var = {v.symbol_name() : v for v in self.variables}
        # add wire name into that
        self.named_var.update(self.wires)
        
    def set_per_sv_update(self, primal_var, rhs):
        assert (primal_var not in self.sv_update)
        assert (primal_var in self.state_var)
        self.sv_update[primal_var] = rhs

    def record_dependent_sv(self, v, coiv):
        assert (isinstance(coiv, set))
        self.sv_dependent_map[v] = coiv
    def finish_record_dependent_sv(self):
        """will compute the influence set"""
        for pv, coiv in self.sv_dependent_map.items():
            for prev in coiv:
                if prev not in self.sv_influence_map:
                    self.sv_influence_map[prev] = set()
                self.sv_influence_map[prev].add(pv)
        for primal_v in self.state_var:
            if primal_v not in self.sv_update:
                print ('<W> %s is actually input' % str(primal_v))
                self.state_var.remove(primal_v)
                self.input_var.add(primal_v)
                

