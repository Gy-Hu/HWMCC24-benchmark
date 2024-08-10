from pysmt.shortcuts import And, is_sat, substitute, TRUE, FALSE, EqualsOrIff, BV
from pysmt.fnode import FNode
from sts import StateAsmpt
from typing import Set

def is_reducible_bool(expr:FNode, assumptions): # -> 0: always 0 /1/ None
  if not is_sat(And([EqualsOrIff(expr, TRUE())] + assumptions)):
    return 0
  if not is_sat(And([EqualsOrIff(expr, FALSE())] + assumptions)):
    return 1
  return None

def is_reducible_bv_width1(expr:FNode, assumptions): # -> 0: always 0 /1/ None
  if not is_sat(And([EqualsOrIff(expr, BV(1,1))] + assumptions)):
    return 0
  if not is_sat(And([EqualsOrIff(expr, BV(0,1))] + assumptions)):
    return 1
  return None

def expr_simplify_ite(expr:FNode, assumptions, set_of_xvar:Set[FNode]):
  """for all ite(c, x , y) , check if its condition is fixed under assumptions"""
  queue = [expr]
  T = TRUE()
  F = FALSE()
  subst_map = {}
  while len(queue) != 0:
    node = queue[0]
    del queue[0]
    if node.is_ite():
      children = node.args()
      cond = children[0]
      reducible = is_reducible_bool(cond, assumptions)
      if reducible == 0:
        subst_map[cond] = F
        queue = queue + list(children[1:])
      elif reducible == 1:
        subst_map[cond] = T
        queue = queue + list(children[1:])
      else:
        queue = queue + list(children)
    else:
      queue = queue + list(node.args())
  
  return expr.substitute(subst_map).simplify()

def expr_simplify_bv_width1(expr:FNode, assumptions, set_of_xvar:Set[FNode]):
  """for bitvector variable `expr` with width 1, check if its value is fixed to 1_1/0_1 under the assumptions,
  we only check the case when `expr` is an X variable.
  """
  subst_map = {}
  arg = expr.args()
  if len(arg)==0 and (expr in set_of_xvar) and expr.bv_width() == 1:  # HZ: this is not safe: 'X' in str(expr.serialize())
    print(expr)
    reducible = is_reducible_bv_width1(expr, assumptions)
    if reducible == 0:
      subst_map[expr] = BV(0,1)
    elif reducible == 1:
      subst_map[expr] = BV(1,1)
    print(expr.substitute(subst_map).simplify())
  
  return expr.substitute(subst_map).simplify()

def state_simplify_ite(s:StateAsmpt, set_of_xvar:Set[FNode]):
  for var, expr in s.sv.items():
    s.sv[var] = expr_simplify_ite(expr, s.asmpt, set_of_xvar)

def state_simplify_bv_width1(s:StateAsmpt, set_of_xvar:Set[FNode]):
  for var, expr in s.sv.items():
    s.sv[var] = expr_simplify_bv_width1(expr, s.asmpt, set_of_xvar)