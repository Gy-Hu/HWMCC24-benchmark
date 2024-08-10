from pysmt.shortcuts import Symbol, Not, And, Or, Implies, Ite, BVAdd,BVOr, BVAnd, BV, EqualsOrIff, BVNot, BVSub, TRUE, is_sat, get_model
from pysmt.typing import BOOL, BVType

solver_name = 'z3'

def e_is_valid(e, assumptions = []):
  local_assumptions = assumptions[:]
  local_assumptions.append(Not(e))
  return not(is_sat(And(local_assumptions), solver_name=solver_name))
  
def e_is_invalid(e, assumptions = []):
  local_assumptions = assumptions[:]
  local_assumptions.append(e)
  return not(is_sat(And(local_assumptions), solver_name=solver_name))
