import string
from pysmt.shortcuts import And, is_sat, substitute, TRUE, FALSE, EqualsOrIff, BV, get_free_variables
from pysmt.fnode import FNode
from sts import StateAsmpt
from typing import Set


def is_reducible_bool(expr:FNode, assumptions): # -> 0: always 0 /1/ None
  # print('start reduce!')
  if not is_sat(And([EqualsOrIff(expr, TRUE())] + assumptions)):
    return 0
  if not is_sat(And([EqualsOrIff(expr, FALSE())] + assumptions)):
    return 1
  # print('finish reduce!')
  return None

def is_reducible_bv_width1(expr:FNode, assumptions): # -> 0: always 0 /1/ None
  if not is_sat(And([EqualsOrIff(expr, BV(1,1))] + assumptions)):
    return 0
  if not is_sat(And([EqualsOrIff(expr, BV(0,1))] + assumptions)):
    return 1
  return None

def expr_simplify_ite(expr:FNode, assumptions, set_of_xvar:Set[FNode]):
  """for all ite(c, x , y) , check if its condition is fixed under assumptions"""
  # print('running state simplify!')
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
  # print('state simplify finish!')
  
  return expr.substitute(subst_map).simplify()

def expr_simplify_ite_new(expr:FNode, assumptions, set_of_xvar:Set[FNode]):
  """for all ite(c, x , y) , check if its condition is fixed under assumptions"""
  # print('running state simplify!')
  cond_list = []
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
      # if((cond not in cond_list) and ('X' in str(cond.serialize())) ):
      if(cond not in cond_list):

        reducible = is_reducible_bool(cond, assumptions)
        if reducible == 0:
          cond_list.append(cond)
          subst_map[cond] = F
          # queue = queue + list(children[1:])
          queue = queue + [children[2]]
        elif reducible == 1:
          cond_list.append(cond)
          subst_map[cond] = T
          # queue = queue + list(children[1:])
          queue = queue + [children[1]]
        else:
          queue = queue + list(children)
      else:
        # print(cond)
        pass
    else:
      queue = queue + list(node.args())
  # print('state simplify finish!')
  
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

def get_xvar_sub(assumptions, set_of_xvar:Set[FNode], free_var):
  xvar_sub = {}
  bv1_list =[]
  for xvar in set_of_xvar:
    if((xvar.bv_width() == 1) and (xvar in free_var)):
      bv1_list.append(xvar)
      reducible = is_reducible_bv_width1(xvar, assumptions)
      if reducible == 0:
        xvar_sub[xvar] = BV(0,1)
      elif reducible == 1:
        xvar_sub[xvar] = BV(1,1)
  stall_list = []
  for xvar in set_of_xvar:
    if('stall' in str(xvar.serialize())):
      stall_list.append(xvar)

  
  return xvar_sub

def usr_info_sub(usr_str:string, usr_bv:BV, set_of_xvar:Set[FNode], free_var):
  usr_sub = {}
  for xvar in set_of_xvar:
    if((usr_str in str(xvar.serialize())) and (xvar.bv_width() == 1) and (xvar in free_var)):
      usr_sub[xvar] = usr_bv
  
  return usr_sub


def state_simplify_ite(s:StateAsmpt, set_of_xvar:Set[FNode]):
  for var, expr in s.sv.items():
    s.sv[var] = expr_simplify_ite(expr, s.asmpt, set_of_xvar)

def state_simplify_bv_width1(s:StateAsmpt, set_of_xvar:Set[FNode]):
  for var, expr in s.sv.items():
    s.sv[var] = expr_simplify_bv_width1(expr, s.asmpt, set_of_xvar)

def state_simplify_xvar(s:StateAsmpt, set_of_xvar:Set[FNode]):
  # print(set_of_xvar)
  # input()
  eq_list = []
  for var, expr in s.sv.items():
    eq = EqualsOrIff(var, expr)
    eq_list.append(eq)
  state_and = And(eq_list)
  free_var = get_free_variables(state_and)

  # usr_sub = usr_info_sub('dummy_reset', BV(0,1), set_of_xvar, free_var)
  usr_sub = {}
  # if (len(usr_sub)>1):
  #   print(usr_sub)
  #   input()
  for var, expr in s.sv.items():
    expr_new = expr.substitute(usr_sub).simplify()
    s.sv[var] = expr_new
  xvar_sub = get_xvar_sub(s.asmpt, set_of_xvar, free_var)
  
  for var, expr in s.sv.items():
    expr_new = expr.substitute(xvar_sub).simplify()
    # s.sv[var] = expr_new
    s.sv[var] = expr_simplify_ite_new(expr_new, s.asmpt, set_of_xvar)
