# inv group
from re import S
from pysmt.shortcuts import Symbol, Not, And, Or, Implies, Ite, BVAdd, BV, EqualsOrIff, BVNot, BVSub, TRUE
from pysmt.typing import BOOL, BVType
from copyreg import pickle
import imp
from click import open_file
from pysmt.shortcuts import substitute, And, Not, Or, Implies, BVOne, BVZero, EqualsOrIff, get_free_variables, get_unsat_core, is_unsat, UnsatCoreSolver
from symtraverse import *
from state_simplify import state_simplify_ite
import pickle
from pysmt.parsing import parse
import os
from pysmt.printers import HRPrinter
from pysmt.rewritings import conjunctive_partition, disjunctive_partition
from pysmt.solvers import z3,msat,btor
from pysmt.shortcuts import Solver
import re

def deduplicate(l):
    return list(set(l))

def tobool(e): # return (e == 1)
    return EqualsOrIff(e,BVOne(1))

def is_valid(e):
    return (not is_sat(Not(e)))

def get_invalid_model(e):
    return (get_model(Not(e)))

def sort_model(m):
    mstr = str(m)
    return ('\n'.join(sorted(mstr.split('\n'))))
    
def del_dic_one(dic,string):
    for k, v in dic.items():
        if str(k) == string:
          dic.pop(k)
          break

def inv_check(inv_l0):
    inv_tag0 = inv_l0
    print(type(inv_tag0))


# (inv_start, inv_start2ex, inv_ex2ex, inv_ex2wb, inv_wb2wb, inv_wb2finish, trans_update, asmpt, sts):

def debug_RHS(cex, RHS):
    # recursively go down the RHS AST, if we encounter an AND, trace into the first False element
    # if we get to an OR, trace into all False element 
    pass

def init_check_generic_func(inv, init):

    LHS = init
    RHS = inv
    check_result = is_valid(Implies(LHS, RHS))
    print ('\n\ninit_check:',check_result)
    cex = get_invalid_model(Implies(LHS, RHS))
    print("counter example (inv check)\n", sort_model(cex))
    return cex


def inv_check_generic_func(inv, \
                   trans_update, asmpt, sts):

    LHS = And([inv, asmpt, trans_update])
    RHS = substitute(inv, sts.v2vprime)
    check_result = is_valid(Implies(LHS, RHS))
    print ('\n\ninv_check:',check_result)
    cex = get_invalid_model(Implies(LHS, RHS))
    print("counter example (inv check)\n", sort_model(cex))
    return cex

    # if not check_result:
    #     conj = conjunctive_partition(RHS)
    #     conj_list = list(conj)

    #     for c in conj_list:
    #         val = cex.get_value(c)
    #         if str(val) == 'False':
    #           print('\n',c.serialize())
    #           print ('---------> False')
    # return cex

def property_check_generic_func(inv, prop, asmpt):
    LHS = And([inv, asmpt])
    RHS = prop
    check_result = is_valid(Implies(LHS, RHS))
    print ('\n\nprop_check:',check_result)
    cex = get_invalid_model(Implies(LHS, RHS))
    print("counter example (inv check)\n", sort_model(cex))
    # sanity check: inv is compatible with asmpt
    assert is_sat(LHS)

        

def inv_check_func(inv_start, inv_start2ex, inv_ex2ex, inv_ex2wb, inv_wb2wb, inv_wb2finish, \
                   inv_ila_start_list0, inv_ila_start_list, inv_ila_started_list, \
                   trans_update, asmpt, sts):

    inv_ex = Or(inv_start2ex, inv_ex2ex)
    inv_wb = Or(inv_ex2wb, inv_wb2wb)
    inv_finish = inv_wb2finish

    inv = And(inv_start, inv_ex, inv_wb, inv_finish)

    LHS = And([inv, asmpt, trans_update])
    RHS = substitute(inv, sts.v2vprime)
    check_result = is_valid(Implies(LHS, RHS))
    print ('\n\ninv_check:',check_result)
    cex = get_invalid_model(Implies(LHS, RHS))
    print("counter example (inv check)\n", sort_model(cex))


    # inv_ex = Or(inv_start2ex, inv_ex2ex)
    # inv_wb = inv_l3
    # inv_wb_list0 = inv_group3_l3

    # inv_wb_list = inv_group4_l4
    # inv_finish_list = inv_group5_l5
    # inv_ila_start_list = inv_ila_start_list
    # inv_ila_started_list = inv_ila_started_list

    # inv_property_list = []


    # # if(len(inv_wb_list) == len(inv_finish_list) == len(inv_ila_start_list) == len(inv_ila_started_list)):
    # #   for idx in range(len(inv_wb_list)):
    # #     # inv_property_list.append(And(inv_wb_list1[idx], inv_wb_list2[idx], inv_finish_list[idx]))
    # #     inv_property_list.append(And(Or(inv_wb_list0[idx], inv_wb_list[idx]), inv_finish_list[idx]\
    # #     # ))
    # #     , Or(inv_ila_start_list0[idx], inv_ila_start_list[idx]), inv_ila_started_list[idx]))
    # # else:
    # #   assert False
    # # inv_property_expr = Or(inv_property_list)
    # # inv = And(inv_start, inv_ex, inv_property_expr)

    # if len(inv_wb_list) == len(inv_finish_list) == len(inv_ila_start_list) == len(inv_ila_started_list):
    #   for idx in range(len(inv_wb_list)):
    #     inv_property_list.append(And(inv_wb_list[idx], inv_finish_list[idx],\
    #     inv_ila_start_list[idx], inv_ila_started_list[idx]))
    # else:
    #   assert False    
    # inv_property_expr = Or(inv_property_list)
    # inv = And(inv_start, inv_ex, inv_wb, inv_property_expr)


    # inv_asmpt = And(inv,asmpt)
    # inv_check = And(inv_asmpt, trans_update)
    # inv_prime = substitute(inv, sts.v2vprime)
    # check_result = is_valid(Implies(inv_check, inv_prime))
    # print ('\n\ninv_check:',check_result)
    # cex = get_invalid_model(Implies(inv_check, inv_prime))
    # print("counter example (inv check)\n", sort_model(cex))

    # if(check_result == False):
    #     conj = conjunctive_partition(inv_prime)
    #     print(type(conj))
    #     conj_list = list(conj)
    #     # print(conj_list[0].serialize())

    #     for c in conj_list:
    #         print('\n',c)
    #         # print (c.serialize())
    #         print ('---------> ', cex.get_value(c))
    #         # input()
        

    #     print('new!\n\n')
    #     wb_conj = conj_list[1]
    #     disj = disjunctive_partition(wb_conj)

    #     for c in disj:
    #         print('\n',c)
    #         # print (c.serialize())
    #         print ('---------> ', cex.get_value(c))

    #     print('\n\nprop')
    #     prop = conj_list[0]
    #     prop_dis = list(disjunctive_partition(prop))
    #     s0 = prop_dis[1]
    #     s00 = conjunctive_partition(s0)

    #     for c in s00:
    #         print('\n',c)
    #         print (c.serialize())
    #         print ('---------> ', cex.get_value(c))


    # with open("/home/fwj/vpipe-mc/btor-symsim-simple-pipe/cex2waveform/cex.txt",'w') as f:
    #     f.write(sort_model(cex))

    # file = 'inv.txt'
    # with open(file,'w') as f:
    #     f.write(inv.serialize())
    # file = 'inv_prime.txt'
    # with open(file,'w') as f:
    #     f.write(inv_prime.serialize())

    return (check_result,cex,inv)

def inv_check_func0(inv_start, inv_start2ex, inv_ex2ex, inv_ex2wb, inv_wb2wb, inv_wb2finish, trans_update, asmpt, sts):

    inv_ex = Or(inv_start2ex, inv_ex2ex)
    inv_wb = Or(inv_ex2wb, inv_wb2wb)
    inv_finish = inv_wb2finish

    inv = And(inv_start, inv_ex, inv_wb, inv_finish)
    inv = And(inv_start)


    LHS = And([inv, asmpt, trans_update])
    RHS = substitute(inv, sts.v2vprime)
    check_result = is_valid(Implies(LHS, RHS))
    print ('\n\ninv_check:',check_result)
    cex = get_invalid_model(Implies(LHS, RHS))
    print("counter example (inv check)\n", sort_model(cex))



    return (check_result,cex,inv)

def test_ce(formula_list, cex):
    for inv_formula in formula_list:
        print (inv_formula)
        # print (inv_formula.serialize())
        print ('---------> ', cex.get_value(inv_formula))

def test_ce_prime(formula_list, cex, sts): 
    for inv_formula in formula_list:
        inv_formula_sub = substitute(inv_formula, sts.v2vprime)
        print (inv_formula_sub)
        # print (inv_formula_sub.serialize())
        print ('---------> ', cex.get_value(inv_formula_sub))

def partial_check(formula_list, cex, sts):
    idx = 0
    for inv_formula in formula_list:
        f_and = inv_formula.args()[1]
        f_and = substitute(f_and, sts.v2vprime)
        conj = conjunctive_partition(f_and)
        for c in conj:
            print('\n',c)
            # print (c.serialize())
            print ('---------> ', cex.get_value(c))
        # print(inv_formula.serialize())
        print('state ', idx)
        
        idx = idx + 1
        input()

def Fnode_sequence_to_str(l) -> str:
  """this will use Fnode.serialize() instead of str(Fnode)"""
  if isinstance(l, list):
    return '['+( ','.join([Fnode_sequence_to_str(e) for e in l]) ) + ']'
  if isinstance(l, tuple):
    return '('+( ','.join([Fnode_sequence_to_str(e) for e in l]) ) + ')'
  # we hope it has a serialize method
  return l.serialize()

def extract_rtl_regval_from_state_list(state_list, layer):
    """ get values of RTL_registers[0..3] , and return list( tag_ila[0..3]== ...)
    """
    extract_list = [None]*4
    for var, expr in state_list[layer].sv.items():
        if str(var) == '\'RTL_registers[0]\'':
          extract_list[0] = expr
        elif str(var) == '\'RTL_registers[1]\'':
          extract_list[1] = expr
        elif str(var) == '\'RTL_registers[2]\'':
          extract_list[2] = expr
        elif str(var) == '\'RTL_registers[3]\'':
          extract_list[3] = expr
    for e in extract_list:
      assert e is not None
    return extract_list

def extract_pair_of_regval_from_branch_list(branch_list, layer1, layer2):
  """Example of pair_dedup: [ ( [r0pre, r1pre, r2pre, r3pre],  [r0post, r1post, r2post, r3post] ), ...  ] """
  all_pair = []
  assumptions = []
  # pair_dedup = []
  # pair_dedup_str = set()

  for branch in branch_list:
    pre_state = extract_rtl_regval_from_state_list(state_list=branch, layer=layer1) # list of 4
    post_state= extract_rtl_regval_from_state_list(state_list=branch, layer=layer2) # list of 4
    assert len(pre_state) == len(post_state)
    pair = (pre_state, post_state)
    all_pair.append(pair)
    assumptions.append(And(branch[layer2].asmpt))
    # str_of_pair = Fnode_sequence_to_str(pair)
    # if str_of_pair not in pair_dedup_str:
    #   pair_dedup_str.add(str_of_pair)
    #   pair_dedup.append(pair)
  return all_pair, assumptions

def make_pair_eq(l1, l2):
  assert len(l1) == len(l2)
  return And([EqualsOrIff(l1[idx], l2[idx]) for idx in range(len(l1))])


def is_cex_consistent_w_asmpt(cex, asmpt, sub_list_var):
  assert len(sub_list_var) != 0

  eqs = And([EqualsOrIff(s, cex.get_value(s)) for s in sub_list_var])
  print ('cex v1 v2:', eqs.serialize())
  return is_sat(And(eqs, asmpt))

class InvGroup(object):
  def __init__(self, layer:int, tag, branch_list):
    self.layer = layer
    self.tag = tag
    self.branch_list = branch_list


    self.init = []
    self.inv_group = []  # list of (tag-> (sv1==?? /\ sv2==...))
    self.state_list = [] # list of (sv1==?? /\ sv2==...)
    self.inv_dedup = [] # remove repeated elements from inv_group
    self.state_dedup = [] # remove repeated elements from state_list
    self.state_update = []

    self.unsat_core_cons = []

  def branch2state(self, asmpt_list):
    state_group = []
    assert len(asmpt_list) == len(self.branch_list) or len(asmpt_list) == 0 or asmpt_list is None  # asumption per each branch
    for state_list in self.branch_list:
        state_expr_single = [] 
        for var, expr in state_list[self.layer].sv.items():
          state_expr_single.append(EqualsOrIff(var, expr))
        state_expr = And(state_expr_single)

        # asmpt = state_list[self.layer].asmpt
        # asmpt_and = And(asmpt)
        

        state_group.append(state_expr)

    # we write the expressions and re-parse them to make sure
    # the variables with the same names are actually the same variables
    stream = "state_data.txt"
    f = open(stream,"w")
    hr_printer = HRPrinter(f)

    for state in state_group:
      hr_printer.printer(state)
      f.write('\n')
    f.close()

    f = open(stream,"r")
    lines = f.readlines()
    for line in lines:
      state = parse(line)
      self.state_list.append(state)
    f.close()

    os.remove(stream)
    
    for branchidx, state_eq_conj in enumerate(self.state_list):
        # state.print()
        if asmpt_list:
            state_eq_conj = And(state_eq_conj, asmpt_list[branchidx])
        inv_single = Implies(self.tag, state_eq_conj)
        self.inv_group.append(inv_single)
    
    # deduplicate of asmptions
    for state in self.state_list:
        if state in self.state_dedup:
            continue
        self.state_dedup.append(state)

    # deduplicate of inv_group
    for inv in self.inv_group:
        if inv in self.inv_dedup:
            continue
        self.inv_dedup.append(inv)


  
  def inv_with_ila(self, ila_list):
    """ return List of ( tag -> RTL.sv1 == ... /\\ RTL.sv2 == /\\ ... /\\ ila_list[]... ) """
    assert len(self.state_list) == len(ila_list)

    inv_list = []
    for idx in range(len(ila_list)):
      inv_expr0 = And(self.state_list[idx], ila_list[idx])
      inv_expr = Implies(self.tag, inv_expr0)
      inv_list.append(inv_expr)
  
    return inv_list


#-------------------------------------------------------------
# DEBUG related functions
#-------------------------------------------------------------

  def test_ce(self, cex):
    inv_list = self.inv_dedup
    for idx in range(len(inv_list)):
        inv_formula = inv_list[idx]
        # print(inv_formula)
        print (inv_formula.serialize())
        print ('---------> ', cex.get_value(inv_formula))

  def test_ce_prime(self, cex, sts): 
    for idx in range(len(self.inv_dedup)):
        inv_formula = self.inv_dedup[idx]
        inv_formula_sub = substitute(inv_formula, sts.v2vprime)
        # print(inv_formula_sub)
        print (inv_formula_sub.serialize())
        print ('---------> ', cex.get_value(inv_formula_sub))
       
