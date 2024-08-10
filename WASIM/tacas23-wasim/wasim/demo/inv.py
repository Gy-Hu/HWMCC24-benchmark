import sys
sys.path.append('/home/tacas23/wasim')
sys.path.append('/home/tacas23/wasim/symsim_framework')

from pathlib import Path
import copy
from symsim_framework.symtraverse import *
from pysmt.shortcuts import substitute, BVOne


def is_valid(e):
    return (not is_sat(Not(e)))

def tobool(e):
    return EqualsOrIff(e,BVOne(1))

def abstract(s:StateAsmpt, base_var): # -> StateAsmpt
# current policy: only keep those on base_var
    if len(base_var) == 0:
        print ("WARNING : set base_var first!")
    s_new = StateAsmpt(sv={}, asmpt=s.asmpt.copy(), assumption_interp=s.assumption_interp.copy())
    for s, v in s.sv.items():
        if str(s) in base_var:
            s_new.sv[s] = v
    return s_new

btor_parser = BTOR2Parser()
sts, _ = btor_parser.parse_file(Path("/home/tacas23/wasim/design/simple_MAC_no_stall.btor2"))
executor = SymbolicExecutor(sts)

init_setting = executor.convert({
    'wen_stage1':'v1',
    'wen_stage2':'v2',
    'wen_stage3': 1,
    'stage1':'a',
    'stage2':'b',
    'stage3':'c'
  })

executor.init(init_setting)


wen_stage1,wen_stage2,wen_stage3,stage1,stage2,stage3,rst = \
  executor.sv('wen_stage1'),executor.sv('wen_stage2'),executor.sv('wen_stage3'),executor.sv('stage1'),executor.sv('stage2'),executor.sv('stage3'),executor.sv('rst')

tag0,tag1,tag2,tag3 = tobool(executor.sv('tag0')), tobool(executor.sv('tag1')), tobool(executor.sv('tag2')), tobool(executor.sv('tag3'))

reg_v,reg_v_comp = executor.sv('reg_v'), executor.sv('reg_v_comp')
base_sv = {'wen_stage1', 'wen_stage2', 'wen_stage3', 'stage1', 'stage2', 'stage3'}

s0 = executor.get_curr_state()
s0 = abstract(s0,base_sv)
executor.set_input(
    executor.convert({'rst':0, 'wen_stage3':1}), [])
executor.sim_one_step()
s1 = executor.get_curr_state()
s1 = abstract(s1,base_sv)

executor.set_input(
    executor.convert({'rst':0, 'wen_stage3':1}), [])
executor.sim_one_step()
s2 = executor.get_curr_state()
s2 = abstract(s2,base_sv)

executor.set_input(
    executor.convert({'rst':0, 'wen_stage3':1}), [])
executor.sim_one_step()
s3 = executor.get_curr_state()
s3 = abstract(s3,base_sv)

state_expr_single = []
for var,expr in s0.sv.items():
    state_expr_single.append(EqualsOrIff(var, expr))
state_expr = And(state_expr_single)
free_var = get_free_variables(state_expr)

for var in free_var:
        if(str(var) == 'v1'):
            v1 = var
        elif(str(var) == 'v2'):
            v2 = var
        elif(str(var) == 'a'):
            a = var
        elif(str(var) == 'b'):
            b = var
        elif(str(var) == 'c'):
            c = var

init = And([sts.init,     
    EqualsOrIff(v1,wen_stage1), EqualsOrIff(v2,wen_stage2), EqualsOrIff(BV(1,1),wen_stage3),
    EqualsOrIff(a,stage1), EqualsOrIff(b,stage2), EqualsOrIff(c,stage3), EqualsOrIff(rst, BV(0,1)), sts.assumption])
    
inv = And([Implies(tag, 
          And([EqualsOrIff(v,val) for v, val in s.sv.items()])) \
                for tag,s in [(tag0,s0),(tag1,s1),(tag2,s2),(tag3,s3)]] + \
      [ Implies(EqualsOrIff(v2,BV(1,1)), EqualsOrIff(v1,BV(1,1))), \
        Implies(Or(tag2,tag3), EqualsOrIff(reg_v,(Ite(tobool(v1),2*a+1,c)))), \
        Implies(Or(tag1,tag2,tag3), EqualsOrIff(reg_v_comp,reg_v*2+1))])
inv_prime = substitute(inv, sts.v2vprime)

prop = sts.assertion
prop_prime = substitute(prop, sts.v2vprime)

trans = And(sts.trans,sts.assumption,\
            substitute(sts.assumption ,sts.v2vprime), \
            EqualsOrIff(rst, BV(0,1)),\
            EqualsOrIff(wen_stage3, BV(1,1)))

print ('\n\n')
print ('Init_check:', is_valid(Implies(init, inv)))
print ('Inv_check: ', is_valid(Implies(And(trans,inv), inv_prime)))
print ('Prop_check: ', is_valid(Implies(inv, prop)))
print ('Indective invariant:\n', inv)
print ('\n\n')

#m=get_model(Not(Implies(And(trans,inv), inv_prime)))


#invf1 = substitute(And([Implies(tag, 
#          And([EqualsOrIff(v,val) for v, val in s.sv.items()])) \
#                for tag,s in [(tag0,s0),(tag1,s1),(tag2,s2),(tag3,s3)]]), sts.v2vprime)
#print (m.get_value(invf1))


