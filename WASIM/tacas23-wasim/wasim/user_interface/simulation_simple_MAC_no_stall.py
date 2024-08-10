from copyreg import pickle
import copy
from pysmt.fnode import *
import pickle
import time
import sys
sys.path.append('/home/tacas23/wasim')
sys.path.append('/home/tacas23/wasim/symsim_framework')
from symsim_framework.symtraverse import *

def symtraverse_all_step():
  start_time = time.perf_counter()
  base_sv = {'wen_stage1', 'wen_stage2', 'wen_stage3', 'stage1', 'stage2', 'stage3'}
  # name and width

  def abstract(s:StateAsmpt, base_var): # -> StateAsmpt
    # current policy: only keep those on base_var
    if len(base_var) == 0:
      print ("WARNING : set base_var first!")
    s2 = StateAsmpt(sv={}, asmpt=s.asmpt.copy(), assumption_interp=s.assumption_interp.copy())
    for s, v in s.sv.items():
      if str(s) in base_var:
        s2.sv[s] = v
    return s2

  order = [ \
    TraverseBranchingNode(input_v=('rst', 1)),
    TraverseBranchingNode(signal_v=('stage1_go', 1)),
    TraverseBranchingNode(signal_v=('stage2_go', 1)),
    TraverseBranchingNode(signal_v=('stage3_go', 1))]


  btor_parser = BTOR2Parser()
  sts, _ = btor_parser.parse_file(Path("/home/tacas23/wasim/design/simple_MAC_no_stall.btor2"))
  executor = SymbolicExecutor(sts)
  # #tag0->tag0 initialize
  init_setting = executor.convert({
      'wen_stage1':'v1',
      'wen_stage2':'v2',
      'wen_stage3':1,
      'stage1':'a',
      'stage2':'b',
      'stage3':'c'
      })
  executor.init(init_setting)

  rst = executor.sv('rst')
  wen_stage3 = executor.sv('wen_stage3')
  


  subst_map = {}
  subst_map[rst] = BV(0,1)
  subst_map[wen_stage3] = BV(1,1)

  def simplify_w_asmpt(state, subst_map):
    for var, expr in state.sv.items():
          expr_new = expr.substitute(subst_map).simplify()
          state.sv[var] = expr_new

  state_list = []    
  branch_list = []
  def sim_init():
    state_init = executor.get_curr_state()
    state_init = abstract(state_init, base_sv)
    simplify_w_asmpt(state_init, subst_map)
    state_init.print()
    # state_init.print_assumptions()

    state_list.append(state_init)

    return state_init

  def sim_next(state_pre):
    executor.set_current_state(state_pre, {})
    executor.sim_one_step_direct()
    state_post = executor.get_curr_state()
    state_post = abstract(state_post, base_sv)
    simplify_w_asmpt(state_post, subst_map)
    state_post.print()
    # state_post.print_assumptions()

    state_list.append(state_post)

    return state_post
  
  state_t0 = sim_init()

  state_t1 = sim_next(state_t0)

  state_t2 = sim_next(state_t1)

  state_t3 = sim_next(state_t2)

  # state_t4 = sim_next(state_t3)

  branch_list.append(state_list)

  end_time = time.perf_counter()


  file_name = "/home/tacas23/wasim/output/trace_simple_MAC_no_stall.pkl"
  open_file = open(file_name,"wb")
  pickle.dump(branch_list,open_file)
  open_file.close()

  print('program running Time:%d(ms):  ' %int( round((end_time-start_time) * 1000) ))
  print('program running time: %d(s):  ' %round((end_time-start_time),10))
  

if __name__ == '__main__':
  symtraverse_all_step()



