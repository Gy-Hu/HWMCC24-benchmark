import sys
sys.path.append('/home/tacas23/wasim')
sys.path.append('/home/tacas23/wasim/symsim_framework')

from pathlib import Path
import copy
from symsim_framework.symtraverse import *

btor_parser = BTOR2Parser()
sts, _ = btor_parser.parse_file(Path("/home/tacas23/wasim/design/simple_MAC_no_stall.btor2"))
executor = SymbolicExecutor(sts)


  # name and width

def abstract(s:StateAsmpt, base_var): # -> StateAsmpt
# current policy: only keep those on base_var
    if len(base_var) == 0:
        print ("WARNING : set base_var first!")
    s_new = StateAsmpt(sv={}, asmpt=s.asmpt.copy(), assumption_interp=s.assumption_interp.copy())
    for s, v in s.sv.items():
        if str(s) in base_var:
            s_new.sv[s] = v
    return s_new

executor.init(
  executor.convert({
    'wen_stage1':'v1',
    'wen_stage2':'v2',
    'wen_stage3':1,
    'stage1':'a',
    'stage2':'b',
    'stage3':'c'
  }))


s0 = executor.get_curr_state()

executor.set_input(
    executor.convert({'rst':0, 'wen_stage3':1}), [])
executor.sim_one_step()
s1 = executor.get_curr_state()

executor.set_input(
    executor.convert({'rst':0, 'wen_stage3':1}), [])
executor.sim_one_step()
s2 = executor.get_curr_state()

executor.set_input(
    executor.convert({'rst':0, 'wen_stage3':1}), [])
executor.sim_one_step()
s3 = executor.get_curr_state()

base_sv = {'wen_stage1', 'wen_stage2', 'wen_stage3', 'stage1', 'stage2', 'stage3'}

print('\n\n\n')
print('Properties under verification: ', sts.assertion.serialize())
for s in [s0,s1,s2,s3]:
    # s.print()
    # s.print_assumptions()
    if is_sat( \
        And([Not(sts.assertion)] + 
            [EqualsOrIff(v,val) for v, val in s.sv.items()] + 
            s.asmpt)):
        print ('Direct Property Check Fail!')
        assert(False)

print('Direct Property Check Pass!')
print('\n\n\n')



# print(sts.assertion.serialize())
      




