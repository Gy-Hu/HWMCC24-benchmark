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

def branch2state(layer,tag):
    state_group = []
    for state_list in branch_list:
        # state_list[layer].print()
        state_expr_single = [] 
        for var, expr in state_list[layer].sv.items():
          state_expr_single.append(EqualsOrIff(var, expr))
        state_expr = And(state_expr_single)

        state_group.append(state_expr)
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
    state_list = []
    for line in lines:
      state = parse(line)
      state_list.append(state)
    f.close()

    os.remove(stream)
    
    inv_group = []
    for state in state_list:
        inv_single = Implies(tag,state)
        inv_group.append(inv_single)
    return (inv_group,state_list)

      



file_name = "branch_list.pkl"
open_file = open(file_name,"rb")
branch_list = pickle.load(open_file)





btor_parser = BTOR2Parser()
sts, _ = btor_parser.parse_file(Path("example/pipe-with-stall.btor2"))
executor = SymbolicExecutor(sts)

init_setting = executor.convert({
      'wen_stage1':'v1',
      'wen_stage2':'v2',
      'stage1':'a',
      'stage2':'b',
      'stage3':'c'
      })





###############################################################################

tag0 = EqualsOrIff(executor.sv('tag0'),BV(1,1))
tag1 = EqualsOrIff(executor.sv('tag1'),BV(1,1))
tag2 = EqualsOrIff(executor.sv('tag2'),BV(1,1))
tag3 = EqualsOrIff(executor.sv('tag3'),BV(1,1))



(inv_l0_group,state_l0) = branch2state(layer=0,tag=tag0)



#deduplicate
deduplicate = []
for constraint in state_l0:
  # str_constr = constraint.serialize()
  if constraint in deduplicate:
    continue
  deduplicate.append(constraint)
  # print (constraint.serialize())

deduplicate_inv = []
for constraint2 in inv_l0_group:
  str_constr2 = constraint2.serialize()
  if constraint2 in deduplicate_inv:
    continue
  deduplicate_inv.append(constraint2)
  # print (constraint.serialize())

for expr in deduplicate_inv:
  print(expr)
# input()
#end

#add constraints


state_group = []
for state_list in branch_list:
  state_group.append(state_list[0])
asmpt_test = And(state_group[280].asmpt)
free_var = get_free_variables(asmpt_test)

for var in free_var:
  if(str(var) == 'v1'):
    v1 = var
  elif(str(var) == 'v2'):
    v2 = var


v1_cons = EqualsOrIff(v1,BV(1,1))
v2_cons = EqualsOrIff(v2,BV(1,1))

print(type(deduplicate[-1]))


new = Implies(tag0,And(deduplicate[-1],v1_cons,v2_cons))
new = Implies(tag0,And(deduplicate[-1]))
del deduplicate_inv[-1]
deduplicate_inv.append(new)
inv_l0_group = deduplicate_inv
print(new)
#end

for inv in inv_l0_group:
  print(inv)

# input()

inv_tag0 = Or(inv_l0_group)


#tag1
(inv_l1_group,_) = branch2state(layer=1,tag=tag1)
(inv_l2_group,_) = branch2state(layer=2,tag=tag1)

inv_tag1_group = inv_l1_group + inv_l2_group

inv_tag1 = Or(inv_tag1_group)

#tag21 tag1-->tag2
(inv_l3_group,_) = branch2state(layer=3,tag=tag2)
inv_tag2_p1 = Or(inv_l3_group)


inv_property = []
#tag22 tag2-->tag2 and tag31 tag2-->tag3
(inv_l4_group,_) = branch2state(layer=4,tag=tag2)
(inv_l5_group,_) = branch2state(layer=5,tag=tag3)

if(len(inv_l4_group) == len(inv_l5_group)):
  for idx in range(len(inv_l4_group)):
    inv_property.append(And(inv_l4_group[idx],inv_l5_group[idx]))
inv_property_expr = Or(inv_property)
  



#tag32 tag3-->tag3
(inv_l6_group,_) = branch2state(layer=6,tag=tag3)
inv_tag3_p2 = Or(inv_l6_group)

#add assumption: tag cannot be 1 at the same time
asmpt = And(Not(And(tag0,tag1)), Not(And(tag0,tag2)), Not(And(tag0,tag3)), Not(And(tag1,tag2)), Not(And(tag1,tag3)), Not(And(tag2,tag3)))

assumption = EqualsOrIff(executor.sv('rst'),BV(0,1))
inv = And(inv_tag0, inv_tag1, inv_tag2_p1, inv_tag3_p2, inv_property_expr)






###inv check
#1:  sts.trans
trans = sts.trans
# init = sts.init
print('inv-check !!!')
# print('trans:',trans)

var_to_nxt = {}
for sv, var in init_setting.items():
  # print('sv',sv)
  # print('var',var)
  tp = BVType(var.bv_width())
  var_to_nxt[var] = Symbol(str(var)+"_next", tp)
  # print('var:', var)

  
  
del_dic_one(var_to_nxt,'tag01')
del_dic_one(var_to_nxt,'tag11')
del_dic_one(var_to_nxt,'tag21')
del_dic_one(var_to_nxt,'tag31')
del_dic_one(var_to_nxt,'reg_v1')
del_dic_one(var_to_nxt,'reg_v_comp1')

expr_equal = []

for var, var_nxt in var_to_nxt.items(): 
  expr_equal.append(EqualsOrIff(var_nxt, var))
  
trans_nxt = And(expr_equal)

trans_update = And(trans, trans_nxt)


inv_check = And(inv, trans_update, assumption)
inv_prime = substitute(inv, sts.v2vprime)

print (is_valid(Implies(inv_check, inv_prime)))
cex = get_invalid_model(Implies(inv_check, inv_prime))

print(type(sort_model(cex)))


print("counter example\n", sort_model(cex))

deduplicate = set()
for constraint in inv_l1_group:
  str_constr = constraint.serialize()
  if str_constr in deduplicate:
    continue
  deduplicate.add(str_constr)
  print (str_constr)
  constr_sub = substitute(constraint, sts.v2vprime)
  print (constr_sub.serialize())
  print ('---------> ', cex.get_value(constr_sub))
  
print('------------------------------------')
deduplicate = set()
for constraint in inv_l0_group:
  str_constr = constraint.serialize()
  if str_constr in deduplicate:
    continue
  deduplicate.add(str_constr)
  print (constraint.serialize())
  print ('---------> ', cex.get_value(constraint))

print(sts.v2vprime)
#inv_tag2_p1_prime = substitute(inv_tag2_p1, sts.v2vprime)
#print(cex.get_value(inv_tag2_p1_prime))

state_group = []
for state_list in branch_list:
  state_group.append(state_list[0])

l = len(state_group)
print("len:",l)

state_group[280].print()
state_group[280].print_assumptions()

expr_asmpt_and = And(state_group[280].asmpt)
print(expr_asmpt_and)

# expr_constr_list = []
# expr_constr_list.append( EqualsOrIff('v1',BV(0,1) ))
# print(expr_constr_list[0])

asmpt_test = And(state_group[280].asmpt)
# asmpt_test = asmpt_test.serialize()
free_var = get_free_variables(asmpt_test)
print(free_var)
print(type(free_var))

for var in free_var:
  if(str(var) == 'v1'):
    v1 = var
  elif(str(var) == 'v2'):
    v2 = var
print(type(v1))
  # test = EqualsOrIff(var,BV(0,1))
print(v1)
print(v2)

v1_cons = EqualsOrIff(v1,BV(0,1))
v2_cons = EqualsOrIff(v2,BV(0,1))

expr_sat_check = And(expr_asmpt_and,v1_cons,v2_cons)
# expr_sat_check = And(expr_asmpt_and)

print(expr_sat_check)

sat_check_result = is_unsat(expr_sat_check)
print(sat_check_result)


conj = conjunctive_partition(expr_sat_check)
print(type(conj))
ucore = get_unsat_core(conj,solver_name='msat')
print('UNSAT core size',len(ucore))
for f in ucore:
  print(f.serialize())

# slv = UnsatCoreSolver(name='msat')







