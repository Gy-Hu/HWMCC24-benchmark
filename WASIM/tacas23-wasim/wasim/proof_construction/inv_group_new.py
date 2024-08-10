from pysmt.shortcuts import Symbol, Not, And, Or, Implies, Ite, BVAdd, BV, EqualsOrIff, BVNot, BVSub, TRUE
from pysmt.shortcuts import substitute, And, Not, Or, Implies, BVOne, BVZero, EqualsOrIff, get_free_variables, get_unsat_core, is_unsat, UnsatCoreSolver
from pysmt.parsing import parse
import os
from pysmt.printers import HRPrinter
from pysmt.rewritings import conjunctive_partition, disjunctive_partition
import sys
sys.path.append('/home/tacas23/wasim')
sys.path.append('/home/tacas23/wasim/symsim_framework')
from symsim_framework.symtraverse import *


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

def init_check_generic_func(inv, init, asmpt):
    LHS = And(init, asmpt)
    RHS = inv
    check_result = is_valid(Implies(LHS, RHS))
    print ('\n\ninit_check:',check_result)
    if(check_result == False):
        cex = get_invalid_model(Implies(LHS, RHS))
        print("counter example (inv check)\n", sort_model(cex))
        # conj = conjunctive_partition(RHS)
        # conj_list = list(conj)
        # for c in conj_list:
        #     val = cex.get_value(c)
        #     if str(val) == 'False':
        #       print('\n',c.serialize())
        #       print ('---------> False')
        #       args = list(c.args())
        #     #   conj_arg = conjunctive_partition(args[1])
        #       for c_arg in args:
        #             val_arg = cex.get_value(c_arg)
        #             if str(val_arg) == 'False':
        #                 print('\n',c)
        #                 print ('---------> False')
        #     else:
        #         print('\n',c)
        #         print ('---------> True')
        return check_result, cex
    else:
        print("counter example (inv check)\n", 'None')
        return check_result, None
    


def inv_check_generic_func(inv, \
                   trans_update, asmpt, sts):

    LHS = And([inv, asmpt, trans_update])
    RHS = substitute(inv, sts.v2vprime)
    check_result = is_valid(Implies(LHS, RHS))
    print ('\n\ninv_check:',check_result)
    if(check_result == False):
        cex = get_invalid_model(Implies(LHS, RHS))
        print("counter example (inv check)\n", sort_model(cex))
        return check_result, cex
    else:
        print("counter example (inv check)\n", 'None')
        return check_result, None
    

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
    if(check_result == False):
        cex = get_invalid_model(Implies(LHS, RHS))
        print("counter example (inv check)\n", sort_model(cex))
    else:
        print("counter example (inv check)\n", 'None')
    # sanity check: inv is compatible with asmpt
    assert is_sat(LHS)

def inv_check_func_c0(inv_l0,inv_l1,inv_l2,inv_l3,inv_l4,inv_l5,inv_l6,inv_group4_l4, inv_group5_l5, trans_update, asmpt, sts, prop,inv_addprop):
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

def inv_check_func_c1_2(inv_l0,inv_l1,inv_l2,inv_l3,inv_group2_l2, inv_group3_l3, trans_update, asmpt, sts, prop,inv_addprop):
    inv_tag0 = inv_l0
    inv_tag1 = inv_l1
    inv_tag2 = inv_l2
    inv_tag3 = inv_l3
    inv_property = []
    
    if(len(inv_group2_l2) == len(inv_group3_l3)):
        for idx in range(len(inv_group2_l2)):
            inv_property.append(And(inv_group2_l2[idx],inv_group3_l3[idx],inv_addprop[idx]))
    else:
        assert False
    
    inv_property_dedup = deduplicate(inv_property)
    inv_property_expr = Or(inv_property_dedup)

    inv = And(inv_tag0, inv_tag1, inv_tag2, inv_tag3, inv_property_expr)
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

def inv_check_func(inv_l0, inv_l1, inv_l2, inv_l3, inv_group3_l3, inv_group4_l4, inv_group5_l5, inv_ila_start_list0, inv_ila_start_list, inv_ila_started_list, trans_update, asmpt, sts):

    inv_start = inv_l0
    inv_ex = Or(inv_l1, inv_l2)
    inv_wb = inv_l3
    inv_wb_list0 = inv_group3_l3

    inv_wb_list = inv_group4_l4
    inv_finish_list = inv_group5_l5
    inv_ila_start_list = inv_ila_start_list
    inv_ila_started_list = inv_ila_started_list

    inv_property_list = []


    # if(len(inv_wb_list) == len(inv_finish_list) == len(inv_ila_start_list) == len(inv_ila_started_list)):
    #   for idx in range(len(inv_wb_list)):
    #     # inv_property_list.append(And(inv_wb_list1[idx], inv_wb_list2[idx], inv_finish_list[idx]))
    #     inv_property_list.append(And(Or(inv_wb_list0[idx], inv_wb_list[idx]), inv_finish_list[idx]\
    #     # ))
    #     , Or(inv_ila_start_list0[idx], inv_ila_start_list[idx]), inv_ila_started_list[idx]))
    # else:
    #   assert False
    # inv_property_expr = Or(inv_property_list)
    # inv = And(inv_start, inv_ex, inv_property_expr)

    if(len(inv_wb_list) == len(inv_finish_list) == len(inv_ila_start_list) == len(inv_ila_started_list)):
      for idx in range(len(inv_wb_list)):
        inv_property_list.append(And(inv_wb_list[idx], inv_finish_list[idx]\
        , inv_ila_start_list[idx], inv_ila_started_list[idx]))
    else:
      assert False    
    inv_property_expr = Or(inv_property_list)
    inv = And(inv_start, inv_ex, inv_wb, inv_property_expr)


    inv_asmpt = And(inv,asmpt)
    inv_check = And(inv_asmpt, trans_update)
    inv_prime = substitute(inv, sts.v2vprime)
    check_result = is_valid(Implies(inv_check, inv_prime))
    print ('\n\ninv_check:',check_result)
    cex = get_invalid_model(Implies(inv_check, inv_prime))
    print("counter example (inv check)\n", sort_model(cex))

    if(check_result == False):
        conj = conjunctive_partition(inv_prime)
        print(type(conj))
        conj_list = list(conj)
        # print(conj_list[0].serialize())

        for c in conj_list:
            print('\n',c)
            # print (c.serialize())
            print ('---------> ', cex.get_value(c))
            # input()
        

        print('new!\n\n')
        wb_conj = conj_list[1]
        disj = disjunctive_partition(wb_conj)

        for c in disj:
            print('\n',c)
            # print (c.serialize())
            print ('---------> ', cex.get_value(c))

        print('\n\nprop')
        prop = conj_list[0]
        prop_dis = list(disjunctive_partition(prop))
        s0 = prop_dis[1]
        s00 = conjunctive_partition(s0)

        for c in s00:
            print('\n',c)
            print (c.serialize())
            print ('---------> ', cex.get_value(c))


    # with open("/home/fwj/vpipe-mc/btor-symsim-simple-pipe/cex2waveform/cex.txt",'w') as f:
    #     f.write(sort_model(cex))

    # file = 'inv.txt'
    # with open(file,'w') as f:
    #     f.write(inv.serialize())
    # file = 'inv_prime.txt'
    # with open(file,'w') as f:
    #     f.write(inv_prime.serialize())

    return (check_result,cex,inv)

def inv_check_func_c4(inv_l0, inv_l1, inv_l2, inv_l3, inv_l4, inv_l5, inv_l6, inv_l7, trans_update, asmpt, sts):

    inv_start = inv_l0
    inv_id = Or(inv_l1, inv_l2)
    inv_ex = Or(inv_l3, inv_l4)
    inv_wb = Or(inv_l5, inv_l6)
    inv_finish = inv_l7

    inv = And(inv_start, inv_id, inv_ex, inv_wb, inv_finish)

    # inv = And(inv_start, inv_id, inv_ex)


    inv_asmpt = And(inv,asmpt)
    inv_check = And(inv_asmpt, trans_update)
    inv_prime = substitute(inv, sts.v2vprime)
    check_result = is_valid(Implies(inv_check, inv_prime))
    print ('\n\ninv_check:',check_result)
    cex = get_invalid_model(Implies(inv_check, inv_prime))
    print("counter example (inv check)\n", sort_model(cex))



    # file = 'inv.txt'
    # with open(file,'w') as f:
    #     f.write(inv.serialize())

    # if(check_result == False):
    #     conj = conjunctive_partition(inv_prime)
    #     conj_list = list(conj)

    #     disconj = disjunctive_partition(conj_list[1])
    #     for c in disconj:
    #         print('\n',c)
    #         # print (c.serialize())
    #         print ('---------> ', cex.get_value(c)) 



    return (check_result,cex,inv)

def inv_check_func_idex(inv_l0, inv_l1, inv_l2, inv_l3, inv_l4, trans_update, asmpt, sts):
    
    inv_start = inv_l0
    inv_id = Or(inv_l1, inv_l2)
    inv_ex = Or(inv_l3, inv_l4)

    # inv = And(inv_start, inv_id, inv_ex, inv_wb, inv_finish)

    inv = And(inv_start, inv_id, inv_ex)


    inv_asmpt = And(inv,asmpt)
    inv_check = And(inv_asmpt, trans_update)
    inv_prime = substitute(inv, sts.v2vprime)
    check_result = is_valid(Implies(inv_check, inv_prime))
    print ('\n\ninv_check:',check_result)
    cex = get_invalid_model(Implies(inv_check, inv_prime))
    print("counter example (inv check)\n", sort_model(cex))



    return (check_result,cex,inv)

def inv_check_func_c3(inv_l0, inv_l1, inv_l2, inv_l3, inv_l4, inv_l5, inv_l6, trans_update, asmpt, sts):

    inv_start = inv_l0
    inv_id = inv_l1
    inv_ex = Or(inv_l2, inv_l3)
    inv_wb = Or(inv_l4, inv_l5)
    inv_finish = inv_l6

    inv = And(inv_start, inv_id, inv_ex, inv_wb, inv_finish)
    # inv = And(inv_start, inv_id, inv_ex)


    inv_asmpt = And(inv,asmpt)
    inv_check = And(inv_asmpt, trans_update)
    inv_prime = substitute(inv, sts.v2vprime)
    check_result = is_valid(Implies(inv_check, inv_prime))
    print ('\n\ninv_check:',check_result)
    cex = get_invalid_model(Implies(inv_check, inv_prime))
    print("counter example (inv check)\n", sort_model(cex))

    return (check_result,cex,inv)

def test_ce(formula_list, cex):
    true_list = []
    for idx,inv_formula in enumerate(formula_list):
        print(idx)
        print (inv_formula)
        # print (inv_formula.serialize())
        print ('---------> %s \n' %cex.get_value(inv_formula))
        if(str(cex.get_value(inv_formula)) == 'True'):
            true_list.append(idx)
    print(true_list)
    return true_list

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

def partial_check_num(formula_list,num, cex, sts):
    for idx,inv_formula in enumerate(formula_list):
        if(num == idx):
            f_and = inv_formula.args()[1]
            f_and = substitute(f_and, sts.v2vprime)
            conj = conjunctive_partition(f_and)
            for c in conj:
                print('\n',c)
                # print (c.serialize())
                
                print ('---------> ', cex.get_value(c))
                if(str(cex.get_value(c)) == 'False'):
                    print(c.serialize())
            # print(inv_formula.serialize())
            print('state ', idx)
            




class InvGroup(object):
  def __init__(self, layer:int, tag, branch_list):
    self.layer = layer
    self.tag = tag
    self.branch_list = branch_list


    self.init = []
    self.inv_group = []  # list of (tag-> (sv1==?? /\ sv2==...))
    self.state_list = [] # list of (sv1==?? /\ sv2==...)
    self.inv_dedup = [] # deduplicate of inv_group
    self.state_dedup = [] # deduplicate of state_list
    self.state_update = []
    self.inv_update = []
    self.asmpt_group = []
    self.asmpt_group_for_inv = []
    self.asmpt_dedup = []
    self.unsat_core_cons = []

  def branch2state(self):
    state_group = []
    asmpt_group = []
    for state_list in self.branch_list:
        state_expr_single = [] 
        for var, expr in state_list[self.layer].sv.items():
          state_expr_single.append(EqualsOrIff(var, expr))
        state_expr = And(state_expr_single)

        asmpt = state_list[self.layer].asmpt
        asmpt_and = And(asmpt)
        

        state_group.append(state_expr)
        asmpt_group.append(asmpt_and)

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

    # TODO: do we need to do the same for assumptions?
    # stream = "asmpt_data.txt"
    # f = open(stream,"w")
    # hr_printer = HRPrinter(f)

    # for asmpt_list in asmpt_group:
    #     for asmpt_s in asmpt_list:
    #         hr_printer.printer(asmpt_s)
    #         f.write('\n')
    # f.close()

    # f = open(stream,"r")
    # lines = f.readlines()
    # for line in lines:
    #   asmpt_s = parse(line)
    #   self.asmpt_group_for_inv.append(asmpt_s)
    # f.close()

    # os.remove(stream)


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
        if inv in self.inv_dedup:
            continue
        self.inv_dedup.append(inv)
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

  def check_unsat_expr(self, truelist, cex_expr):
        ## IMPORTANT: modify the assumptions with cex_expr simultaneously
        for num in truelist:
            self.asmpt_group[num] = copy.copy(And(Not(cex_expr), self.asmpt_group[num]))

        truelist_new = []
        for num in truelist:
            asmpt_sat_check = And(self.asmpt_group[num], cex_expr)
            unsat_check = is_unsat(asmpt_sat_check)
            if(unsat_check == False):
                print('UNSAT check false!!\n\n')
                print(num)
                assert False
            else:
                truelist_new.append(num)
                # conj = conjunctive_partition(asmpt_sat_check)
                # ucore = get_unsat_core(conj,solver_name='btor')
                # for f in ucore:
                #     print(f.serialize())
        if(len(truelist)!=len(truelist_new)):
            print(truelist)
            print(truelist_new)
            input()
        return truelist_new

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

    assert len(inv_true_dedup) >= 1

    if(len(inv_true_dedup)>1):
        print('len of inv_true > 1\n\n')
        self.test_ce(cex)

    for inv_true_formula in inv_true_dedup:
        unsat_core_list = []
        self.unsat_core_cons.clear()
        self.state_update.clear()
        self.inv_update.clear()

        for idx in range(len(self.inv_group)):
            inv_formula = self.inv_group[idx]
            if(str(inv_formula.serialize()) == str(inv_true_formula.serialize())):
                asmpt_sat_check = And(self.asmpt_group[idx],And(constriants))
                unsat_check = is_unsat(asmpt_sat_check)
                if(unsat_check == False):
                    print('inv_formula:\n',inv_formula.serialize())
                    print('inv num:\n', idx)
                    print('UNSAT check false!!\n\n')
                    assert False
                else:
                    conj = conjunctive_partition(asmpt_sat_check)
                    ucore = get_unsat_core(conj,solver_name='btor')
                    for f in ucore:
                        unsat_core_list.append(f)
        unsat_core_dedup = []
        for f in unsat_core_list:
            if f in unsat_core_dedup:
                continue
            unsat_core_dedup.append(f)
        cons_list = []
        for f in unsat_core_dedup:
            print(f.serialize())
            for idx in range(len(old_cons_list)):
                if(str(f.serialize()) == old_cons_list[idx]):
                    self.unsat_core_cons.append(new_cons_list[idx])
                    for cons in constriants:
                        if(str(cons.serialize()) == old_cons_list[idx]):
                            continue
                        else:
                            cons_list.append(cons)
        print('len of constraints',len(cons_list))
        print('\nunsat_core_cons:')
        for f in self.unsat_core_cons:
            print(f)
        print('\n')
        # finish updating constraints


        # add updated constraints on the inv
        for idx in range(len(self.inv_group)):
            inv_formula = self.inv_group[idx]
            if(str(inv_formula.serialize()) == str(inv_true_formula.serialize())):
                state_formula_update = And(self.state_list[idx], Or(self.unsat_core_cons))
                self.state_update.append(state_formula_update)
            else:
                self.state_update.append(self.state_list[idx])
        
        for state in self.state_update:
            inv_single = Implies(self.tag,state)
            self.inv_update.append(inv_single)
        #test
        # print('\n\n--------------------------------------------------------------')
        # for inv in self.inv_update:
        #     print(inv.serialize())

        self.inv_group = copy.copy(self.inv_update)
        self.state_list = copy.copy(self.state_update)
    
    inv_update_nodedup = copy.copy(self.inv_group)
    self.inv_update = deduplicate(self.inv_update)
    return self.inv_update, inv_update_nodedup

  def test_ce(self, cex):
    if(len(self.inv_update)==0):
        inv_list = self.inv_dedup
    else:
        inv_list = self.inv_update
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

  def extract_prop(self, txt):
      extract_list = []
      for state_list in self.branch_list:
        for var, expr in state_list[self.layer].sv.items():
            if (str(var) == txt):
                extract_list.append(expr)
      return extract_list
  
  def extract_reg(self):
      extract_list = []
      extract_list_expr = []
      reg_list = []
      reg_list_expr = []
      for state_list in self.branch_list:
        for var, expr in state_list[self.layer].sv.items():
            if(str(var) == '\'RTL_registers[0]\''):
                reg0_expr = EqualsOrIff(var,expr)
                reg0 = expr
            elif(str(var) == '\'RTL_registers[1]\''):
                reg1_expr = EqualsOrIff(var,expr)
                reg1 = expr
            elif(str(var) == '\'RTL_registers[2]\''):
                reg2_expr = EqualsOrIff(var,expr)
                reg2 = expr
            elif(str(var) == '\'RTL_registers[3]\''):
                reg3_expr = EqualsOrIff(var,expr)
                reg3 = expr
        reg_list = [reg0_expr,reg1_expr,reg2_expr,reg3_expr]
        reg_list_expr = [reg0,reg1,reg2,reg3]
        if((reg_list[0]==None)or(reg_list[1]==None)or(reg_list[2]==None)or(reg_list[3]==None)):
            assert False
        else:
            reg_expr = And(reg_list)
        extract_list.append(reg_expr)
        extract_list_expr.append(reg_list_expr)
      return extract_list, extract_list_expr



  def extract_reg_for_ila(self,tag_ila):
      extract_list = []
      reg_list = []
      for state_list in self.branch_list:
        for var, expr in state_list[self.layer].sv.items():
            if(str(var) == '\'RTL_registers[0]\''):
                reg0_expr = EqualsOrIff(tag_ila[0],expr)
            elif(str(var) == '\'RTL_registers[1]\''):
                reg1_expr = EqualsOrIff(tag_ila[1],expr)
            elif(str(var) == '\'RTL_registers[2]\''):
                reg2_expr = EqualsOrIff(tag_ila[2],expr)
            elif(str(var) == '\'RTL_registers[3]\''):
                reg3_expr = EqualsOrIff(tag_ila[3],expr)
        reg_list = [reg0_expr,reg1_expr,reg2_expr,reg3_expr]
        if((reg_list[0]==None)or(reg_list[1]==None)or(reg_list[2]==None)or(reg_list[3]==None)):
            assert False
        else:
            reg_expr = And(reg_list)
        extract_list.append(reg_expr)
      return extract_list
  
  def inv_with_ila(self, ila_list):
      inv_list = []
      if(len(self.state_list) == len(ila_list)):
          for idx in range(len(ila_list)):
            inv_expr0 = And(self.state_list[idx], ila_list[idx])
            inv_expr = Implies(self.tag, inv_expr0)
            inv_list.append(inv_expr)
      else:
          assert False

      return inv_list
  
  def inv_with_ila2(self, ila):
      inv_list = []
      for state in self.state_list:
        inv_expr0 = And(state, ila)
        inv_expr = Implies(self.tag, inv_expr0)
        inv_list.append(inv_expr)
    

      return inv_list
  def add_unsat_asmpt(self, unsat_expr, num):
      state_new_list = []
      inv_new_list = []
      for idx, state in enumerate(self.state_list):
          if(idx == num):
              state_new = And(state, unsat_expr)
              state_new_list.append(state_new)
          else:
              state_new_list.append(state)
    
      for state in state_new_list:
            inv_single = Implies(self.tag,state)
            inv_new_list.append(inv_single)
      
      self.inv_group = copy.copy(inv_new_list)
      self.state_list = copy.copy(state_new_list)

      return self.inv_group

def add_unsat_asmpt_to_ila(ila_list, unsat_expr, num):
    ila_new_list = []
    for idx, ila in enumerate(ila_list):
        if(idx == num):
            ila_new = And(ila, unsat_expr)
            ila_new_list.append(ila_new)
        else:
            ila_new_list.append(ila)
    return ila_new_list
            



def make_pair_eq(l1, l2):
    assert len(l1) == len(l2)
    return And([EqualsOrIff(l1[idx], l2[idx]) for idx in range(len(l1))])

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


