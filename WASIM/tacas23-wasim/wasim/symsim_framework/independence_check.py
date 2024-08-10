# Check if a expression is independent of a var
# (namely, if var can be reduced in expression)

from pysmt.shortcuts import Symbol, Not, And, Or, Implies, Ite, BVAdd,BVOr, BVAnd, BV, EqualsOrIff, BVNot, BVSub, TRUE, is_sat, get_model
from pysmt.typing import BOOL, BVType

solver_name = 'z3'

def e_is_always_valid(e, assumptions = []):
  if e.is_bool_constant() or e.is_bool_op():
    assumptions.append(Not(e))
  elif e.is_bv_constant() or e.is_bv_op():
    assert (e.bv_width() == 1)
    assumptions.append(EqualsOrIff(e,BV(0,1)))
  return not(is_sat(And(assumptions), solver_name=solver_name))
  
def e_is_always_invalid(e, assumptions = []):
  if e.is_bool_constant() or e.is_bool_op():
    assumptions.append(e)
  elif e.is_bv_constant() or e.is_bv_op():
    assert (e.bv_width() == 1)
    assumptions.append(EqualsOrIff(e,BV(1,1)))
  return not(is_sat(And(assumptions), solver_name=solver_name))

def e_is_independent_of_v(e, v , assumptions = []):
  # make a copy of e(v1, ...) =/= e(v1', ...)
  w = v.bv_width()
  v1 = Symbol(str(v)+'1', BVType(w))
  v2 = Symbol(str(v)+'2', BVType(w))
  e1 = e.substitute({v:v1})
  e2 = e.substitute({v:v2})
  assumptionsSub = [Not(EqualsOrIff(e1,e2))]
  for a in assumptions:
    assumptionsSub.append( a.substitute({v:v1}) )
    assumptionsSub.append( a.substitute({v:v2}) )
  return not(is_sat(And(assumptionsSub), solver_name=solver_name))

def substitute_simplify(e, v, assumptions):
  m = get_model(And(assumptions))
  val = m.get_value(v)
  sub = {v:val}
  return e.substitute(sub).simplify()

def is_valid(e):
    return (not is_sat(Not(e), solver_name=solver_name))
  
  
  
# ----------------------------------------------------------

def test_btor_parsing():
  varA = Symbol("A", BVType(4)) # Default type is Boolean
  varB = Symbol("B", BVType(4))
  f = BVOr(varA, BVAnd(varA,varB))
  print(  e_is_independent_of_v (f, varA))
  print(  e_is_independent_of_v (f, varB))
  print(f)
  print(f.simplify())
  
  subf = substitute_simplify(f, varB, [])
  print (subf.serialize())


if __name__ == '__main__':
    test_btor_parsing()
