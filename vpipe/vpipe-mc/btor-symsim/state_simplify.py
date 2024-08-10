from pysmt.shortcuts import And, is_sat, substitute, TRUE, FALSE, EqualsOrIff
from pysmt.fnode import FNode
from sts import StateAsmpt

def is_reducible(expr:FNode, assumptions): # -> 0: always 0 /1/ None
  if not is_sat(And([EqualsOrIff(expr, TRUE())] + assumptions)):
    return 0
  if not is_sat(And([EqualsOrIff(expr, FALSE())] + assumptions)):
    return 1
  return None

def expr_simplify(expr:FNode, assumptions):
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
      reducible = is_reducible(cond, assumptions)
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

def state_simplify(s:StateAsmpt):
  for var, expr in s.sv.items():
    s.sv[var] = expr_simplify(expr,s.asmpt)


def state_simplify_one_step(s:StateAsmpt,add_asmpt):
  if(add_asmpt!=None):
    new_asmpt = s.asmpt.append(list(add_asmpt))
  for var, expr in s.sv.items():
    s.sv[var] = expr_simplify(expr, new_asmpt)