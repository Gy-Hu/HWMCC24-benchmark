# inv group
from re import S
from pysmt.shortcuts import Symbol, Not, And, Or, Implies, Ite, BVAdd, BV, EqualsOrIff, BVNot, BVSub, TRUE
from pysmt.typing import BOOL, BVType
from copyreg import pickle
import imp
from click import open_file
from pysmt.shortcuts import substitute, And, Not, Or, Implies, BVOne, BVZero, EqualsOrIff, get_free_variables, get_unsat_core, is_unsat, UnsatCoreSolver
from symtraverse import *
from state_simplify import state_simplify
from symtraverse_all_step import symtraverse_all_step
import pickle
from pysmt.parsing import parse
import os
from pysmt.printers import HRPrinter
from pysmt.rewritings import conjunctive_partition
from pysmt.solvers import z3,msat,btor
from pysmt.shortcuts import Solver

def deduplicate(list):
    dedup = []
    for state in list:
        if state in dedup:
            continue
        dedup.append(state)
    return dedup

def tobool(e):
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

def inv_check_func(inv_l0,inv_l1,inv_l2,inv_l3,inv_l4,inv_l5,inv_l6,inv_group4_l4, inv_group5_l5, trans_update, asmpt, sts, prop,inv_addprop):
    inv_tag0 = inv_l0
    inv_tag1 = Or(inv_l1,inv_l2)
    inv_tag2_p1 = inv_l3
    inv_tag3_p2 = inv_l6
    inv_tag2 = Or(inv_l3,inv_l4)
    inv_tag3 = Or(inv_l5,inv_l6)
    inv_property = []
    
    if(len(inv_group4_l4) == len(inv_group5_l5)):
        for idx in range(len(inv_group4_l4)):
            inv_property.append(And(inv_group4_l4[idx],inv_group5_l5[idx],inv_addprop[idx]))
    else:
        assert False
    
    inv_property_dedup = deduplicate(inv_property)
    inv_property_expr = Or(inv_property_dedup)

    inv = And(inv_tag0, inv_tag1, inv_tag2_p1, inv_tag3_p2, inv_property_expr)
    # inv = And(inv_tag0, inv_tag1, inv_tag2, inv_tag3)
    inv_asmpt0 = And(inv,asmpt)
    inv_asmpt = And(inv_asmpt0,prop)
    inv_check = And(inv_asmpt0, trans_update)
    inv_prime = substitute(inv_asmpt, sts.v2vprime)
    check_result = is_valid(Implies(inv_check, inv_prime))
    print ('\n\ninv_check:',check_result)
    cex = get_invalid_model(Implies(inv_check, inv_prime))
    print("counter example (inv check)\n", sort_model(cex))

    return (check_result,cex,inv_asmpt)

class InvGroup(object):
  def __init__(self, layer, tag, branch_list):
    self.layer = layer
    self.tag = tag
    self.branch_list = branch_list

    self.inv_group = []
    self.state_list = []
    self.inv_dedup = []
    self.state_dedup = []
    self.state_update = []
    self.inv_update = []
    self.asmpt_group = []
    self.asmpt_dedup = []
    self.unsat_core_cons = []
  def branch2state(self):
    state_group = []
    asmpt_group = []
    for state_list in self.branch_list:
        # state_list[layer].print()
        state_expr_single = [] 
        for var, expr in state_list[self.layer].sv.items():
          state_expr_single.append(EqualsOrIff(var, expr))
        state_expr = And(state_expr_single)

        asmpt = state_list[self.layer].asmpt
        asmpt_and = And(asmpt)
        

        state_group.append(state_expr)
        asmpt_group.append(asmpt_and)

    stream = "state_data"
    f = open(stream,"w")
    hr_printer = HRPrinter(f)

    for state in state_group:
      # print(state)
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


    self.asmpt_group = asmpt_group
    for asmpt in self.asmpt_group:
        if asmpt in self.asmpt_dedup:
            continue
        self.asmpt_dedup.append(asmpt)
    
    
    for state in self.state_list:
        # state.print()
        inv_single = Implies(self.tag,state)
        self.inv_group.append(inv_single)
    # return (self.inv_group,self.state_list)
    for state in self.state_list:
        if state in self.state_dedup:
            continue
        self.state_dedup.append(state)
  def get_inv_group(self):
    return self.inv_group

  def get_state_list(self):
    return self.state_list

  def inv_deduplicate(self):
    for inv in self.inv_group:
        # str_inv = inv.serialize()
        if inv in self.inv_dedup:
            continue
        self.inv_dedup.append(inv)
    # inv_dedup = self.inv_dedup
    # for expr in self.inv_dedup:
    #     print(expr)
    return self.inv_dedup

  def state_deduplicate(self):
    for state in self.state_list:
        if state in self.state_dedup:
            continue
        self.state_dedup.append(state)
    return self.state_dedup

  def asmpt_deduplicate(self):
    for asmpt in self.asmpt_list:
        if asmpt in self.asmpt_dedup:
            continue
        self.asmpt_dedup.append(asmpt)
    return self.asmpt_dedup

  def ce2constraints(self,cex):
      pass

  def update_inv(self, cex, constriants, old_cons_list, new_cons_list): # get constraints from the counterexample --> unsat core --> new constraints
    #1. from counterexamples get unsat_core constraints
    print('\n\nbegin to update inv!')


    inv_true = []
    inv_true2 = []
    for inv_formula in self.inv_dedup:
        if(str(cex.get_value(inv_formula)) == 'True'):
            inv_true.append(inv_formula)

    for inv_formula in self.inv_group:
        if(str(cex.get_value(inv_formula)) == 'True'):
            inv_true2.append(inv_formula)
    inv_true_dedup = deduplicate(inv_true2)

    


    if(len(inv_true_dedup)>1):
        print('len of inv_true > 1\n\n')
        self.test_ce(cex)
        # assert False
        # input()


    


    for inv_true_formula in inv_true_dedup:
        unsat_core_list = []
        self.unsat_core_cons.clear()
        self.state_update.clear()
        self.inv_update.clear()

        for idx in range(len(self.inv_group)):
            inv_formula = self.inv_group[idx]
            # print(inv_formula)
            # print (inv_formula.serialize())
            # print ('---------> ', cex.get_value(inv_formula))
            if(str(inv_formula.serialize()) == str(inv_true_formula.serialize())):
            # if(str(cex.get_value(inv_formula)) == 'True'):
                # print(len(self.inv_group))
                # print(len(self.asmpt_group))
                asmpt_sat_check = And(self.asmpt_group[idx],And(constriants))
                # print(asmpt_sat_check)
                unsat_check = is_unsat(asmpt_sat_check)
                # print(unsat_check)
                if(unsat_check == False):
                    print('inv_formula:',inv_formula.serialize())
                    print('UNSAT check false!!\n\n')
                    assert False
                else:
                    conj = conjunctive_partition(asmpt_sat_check)
                    # print(type(conj))
                    ucore = get_unsat_core(conj,solver_name='z3')
                    # print('UNSAT core')
                    for f in ucore:
                        unsat_core_list.append(f)
                        # print(type(f))
                        # print(f.serialize())
                        # input(1)
        # unsat_core_list deduplicate
        unsat_core_dedup = []
        for f in unsat_core_list:
            if f in unsat_core_dedup:
                continue
            unsat_core_dedup.append(f)
        # print(len(unsat_core_dedup))
        cons_list = []
        for f in unsat_core_dedup:
            print(f.serialize())
            
            for idx in range(len(old_cons_list)):
                if(str(f.serialize()) == old_cons_list[idx]):
                    self.unsat_core_cons.append(new_cons_list[idx])
                    # print(f.serialize())
                    # print(f_not.serialize())
                    for cons in constriants:
                        if(str(cons.serialize()) == old_cons_list[idx]):
                            continue
                        else:
                            cons_list.append(cons)

        
        print('len of constraints',len(cons_list))
        # self.unsat_core_cons.extend(cons_list)
        print('\nunsat_core_cons:')
        for f in self.unsat_core_cons:
            print(f)
        print('\n')
        # finish updating constraints


        # add updated constraints on the inv
        for idx in range(len(self.inv_group)):
            inv_formula = self.inv_group[idx]
            # print (inv_formula.serialize())
            # print ('---------> ', cex.get_value(inv_formula))
            # if(str(cex.get_value(inv_formula)) == 'True'):
            if(str(inv_formula.serialize()) == str(inv_true_formula.serialize())):
                state_formula_update = And(self.state_list[idx],Or(self.unsat_core_cons))
                # print(inv_formula_update)
                self.state_update.append(state_formula_update)
            else:
                self.state_update.append(self.state_list[idx])
        
        for state in self.state_update:
            # state.print()
            inv_single = Implies(self.tag,state)
            self.inv_update.append(inv_single)
        #test
        # print('\n\n--------------------------------------------------------------')
        for inv in self.inv_update:
            print(inv.serialize())



        self.inv_group = copy.copy(self.inv_update)
        self.state_list = copy.copy(self.state_update)


    return self.inv_update

  def test_ce(self, cex): 
    for idx in range(len(self.inv_dedup)):
        inv_formula = self.inv_dedup[idx]
        print(inv_formula)
        print (inv_formula.serialize())
        print ('---------> ', cex.get_value(inv_formula))

  def test_ce_prime(self, cex, sts): 
    for idx in range(len(self.inv_dedup)):
        inv_formula = self.inv_dedup[idx]
        inv_formula_sub = substitute(inv_formula, sts.v2vprime)
        print(inv_formula_sub)
        print (inv_formula_sub.serialize())
        print ('---------> ', cex.get_value(inv_formula_sub))

  def extract_prop(self, txt):
      extract_list = []
      for state_list in self.branch_list:
        for var, expr in state_list[self.layer].sv.items():
            if (str(var) == txt):
                extract_list.append(expr)
      return extract_list


       
