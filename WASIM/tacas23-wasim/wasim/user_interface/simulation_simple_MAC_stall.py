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
  base_sv = {'wen_stage1', 'wen_stage2', 'stage1', 'stage2', 'stage3'}
  # name and width

  order = [ \
    TraverseBranchingNode(input_v=('rst', 1)),
    TraverseBranchingNode(signal_v=('stage1_go', 1)),
    TraverseBranchingNode(signal_v=('stage2_go', 1)),
    TraverseBranchingNode(signal_v=('stage3_go', 1))]


  btor_parser = BTOR2Parser()
  sts, _ = btor_parser.parse_file(Path("/home/tacas23/wasim/design/simple_MAC_stall.btor2"))
  executor = SymbolicExecutor(sts)
  # #tag0->tag0 initialize
  init_setting = executor.convert({
      'wen_stage1':'v1',
      'wen_stage2':'v2',
      'stage1':'a',
      'stage2':'b',
      'stage3':'c'
      })
  executor.init(init_setting)
  
  def tag2asmpt(flag, executor_new):
    if(flag=='tag0_0'):
      return [EqualsOrIff(executor_new.sv('stage1_go'),BV(0,1))]
    elif(flag=='tag0_1'):
      return [EqualsOrIff(executor_new.sv('stage1_go'),BV(1,1))]
    elif(flag=='tag1_1'):
      return [EqualsOrIff(executor_new.sv('stage1_go'),BV(0,1)),EqualsOrIff(executor_new.sv('stage2_go'),BV(0,1))]
    elif(flag=='tag1_2'):
      return [EqualsOrIff(executor_new.sv('stage2_go'),BV(1,1))]
    elif(flag=='tag2_2'):
      return [EqualsOrIff(executor_new.sv('stage2_go'),BV(0,1)),EqualsOrIff(executor_new.sv('stage3_go'),BV(0,1))]
    elif(flag=='tag2_3'):
      return [EqualsOrIff(executor_new.sv('stage3_go'),BV(1,1))]
    elif(flag=='tag3_3'):
      return [EqualsOrIff(executor_new.sv('stage3_go'),BV(0,1))]
    else:
      print ('<ERROR>: Wrong tag transition format!')
      assert False
  
  def extend_branch_init(branch_list, executor, sts, base_sv, flag):
    branch_list_old = copy.copy(branch_list)
    branch_list.clear()
    executor_temp = copy.copy(executor)
    traverser_temp = SymbolicTraverse(sts=sts, executor= executor_temp, base_variable=[executor_temp.sv(n) for n in base_sv])
    traverser_temp.traverse(assumptions=tag2asmpt(flag=flag, executor_new=executor_temp), branching_point=order)
    print('number of state (%s): 1 --> %d' % (flag, len(traverser_temp.tracemgr.abs_state)))
    for nextstate in traverser_temp.tracemgr.abs_state: # HZ: note here abs_state contains the original state `s`
        state_list_extended = copy.copy(state_list)
        state_list_extended.append(nextstate)
        branch_list.append(state_list_extended)
        nextstate.print()
        # nextstate.print_assumptions()
    start_num = len(branch_list_old)
    end_num = len(branch_list)
    print('number of state (%s) in total: %d --> %d' % (flag, len(branch_list_old), len(branch_list)))
    end_time = time.perf_counter()

    return (flag, start_num, end_num, end_time)

  def extend_branch_next_phase(branch_list, executor, sts, base_sv, flag, phase_marker):
    branch_list_old = copy.copy(branch_list)
    branch_list.clear()
    for state_list_old in branch_list_old:
      state_list = copy.copy(state_list_old)
      s = state_list[-1] # get the last state, and extend it by 1 step
      executor_temp = copy.copy(executor)
      d = executor_temp.convert(phase_marker)
      executor_temp.set_current_state(s, d)
      traverser_temp = SymbolicTraverse(sts=sts, executor= executor_temp, base_variable=[executor_temp.sv(n) for n in base_sv])
      traverser_temp.traverse_one_step(assumptions=tag2asmpt(flag=flag, executor_new=executor_temp), branching_point=order, s_init=s)
      print('number of state (%s): 1 --> %d' % (flag, len(traverser_temp.tracemgr.abs_state_one_step)))
      for nextstate in traverser_temp.tracemgr.abs_state_one_step:
          state_list_extended = copy.copy(state_list)
          state_list_extended.append(nextstate)
          branch_list.append(state_list_extended)
          nextstate.print()
          nextstate.print_assumptions()
    start_num = len(branch_list_old)
    end_num = len(branch_list)
    print('number of state (%s) in total: %d --> %d' % (flag, len(branch_list_old), len(branch_list)))
    end_time = time.perf_counter()

    return (flag, start_num, end_num, end_time)

  def extend_branch_same_phase(branch_list, executor, sts, base_sv, flag, phase_marker):
    branch_list_old = copy.copy(branch_list)
    branch_list.clear()
    for state_list_old in branch_list_old:
      state_list = copy.copy(state_list_old)
      s = state_list[-1] # get the last state, and extend it by 1 step
      executor_temp = copy.copy(executor)
      d = executor_temp.convert(phase_marker)
      executor_temp.set_current_state(s, d)
      traverser_temp = SymbolicTraverse(sts=sts, executor= executor_temp, base_variable=[executor_temp.sv(n) for n in base_sv])
      traverser_temp.traverse(assumptions=tag2asmpt(flag=flag, executor_new=executor_temp), branching_point=order, s_init=s)
      print('number of state (%s): 1 --> %d' % (flag, len(traverser_temp.tracemgr.abs_state)))
      for nextstate in traverser_temp.tracemgr.abs_state: # HZ: note here abs_state contains the original state `s`
          state_list_extended = copy.copy(state_list)
          state_list_extended.append(nextstate)
          branch_list.append(state_list_extended)
          nextstate.print()
          nextstate.print_assumptions()
    start_num = len(branch_list_old)
    end_num = len(branch_list)
    print('number of state (%s) in total: %d --> %d' % (flag, len(branch_list_old), len(branch_list)))
    end_time = time.perf_counter()

    return (flag, start_num, end_num, end_time)
  
  

  state_list = []
  branch_list = []
  branch_list_temp = []
  
  
  #Step: tag0-->tag0
  print('Step: tag0-->tag0')
  (flag0, start_num0, end_num0, end_time0) = extend_branch_init(branch_list, executor, sts, base_sv, flag='tag0_0')

  #Step: tag0-->tag1
  print('\n\n\nStep: tag0-->tag1')
  (flag1, start_num1, end_num1, end_time1) = extend_branch_next_phase(branch_list, executor, sts, base_sv, flag='tag0_1', phase_marker=\
   {'tag0':1, 'tag1':0, 'tag2':0, 'tag3':0})
  
  #Step: tag1-->tag1
  print('\n\n\nStep: tag1-->tag1')
  (flag2, start_num2, end_num2, end_time2) = extend_branch_same_phase(branch_list, executor, sts, base_sv, flag='tag1_1', phase_marker=\
   {'tag0':0, 'tag1':1, 'tag2':0, 'tag3':0})
  
  #Step: tag1-->tag2
  print('\n\n\nStep: tag1-->tag2')
  (flag3, start_num3, end_num3, end_time3) = extend_branch_next_phase(branch_list, executor, sts, base_sv, flag='tag1_2', phase_marker=\
   {'tag0':0, 'tag1':1, 'tag2':0, 'tag3':0})


  # #Step: tag2-->tag2
  (flag4, start_num4, end_num4, end_time4) = extend_branch_same_phase(branch_list, executor, sts, base_sv, flag='tag2_2', phase_marker=\
   {'tag0':0, 'tag1':0, 'tag2':1, 'tag3':0})


  # #Step: tag2-->tag3
  print('\n\n\nStep: tag2-->tag3')
  (flag5, start_num5, end_num5, end_time5) = extend_branch_next_phase(branch_list, executor, sts, base_sv, flag='tag2_3', phase_marker=\
   {'tag0':0, 'tag1':0, 'tag2':1, 'tag3':0})

  # #Step: tag3-->tag3
  print('\n\n\nStep: tag3-->tag3')
  (flag6, start_num6, end_num6, end_time6) = extend_branch_same_phase(branch_list, executor, sts, base_sv, flag='tag3_3', phase_marker=\
   {'tag0':0, 'tag1':0, 'tag2':0, 'tag3':1})

  file_name = "/home/tacas23/wasim/output/trace_simple_MAC_stall.pkl"
  open_file = open(file_name,"wb")
  pickle.dump(branch_list,open_file)
  open_file.close()

  def result_display(flag, num_old, num_new, end_time, start_time):
      print('-'*15)
      print('number of state (%s) in total: %d --> %d' % (flag, num_old, num_new))
      print('program running time: %d(s):  ' %round((end_time-start_time),2))
      print('program running time: %d(min):' %round((end_time-start_time)/60,2))

  flag_list = [flag0, flag1, flag2, flag3, flag4, flag5, flag6]
  num_old_list = [start_num0, start_num1, start_num2, start_num3, start_num4, start_num5, start_num6]
  num_new_list = [end_num0, end_num1, end_num2, end_num3, end_num4, end_num5, end_num6]
  end_time_list = [end_time0, end_time1, end_time2, end_time3, end_time4, end_time5, end_time6]

  print('\n\n\n\n\n--------------------------RESULT--------------------------\n')
  for idx in range(len(flag_list)):
    result_display(flag_list[idx], num_old_list[idx], num_new_list[idx], end_time_list[idx], start_time)

if __name__ == '__main__':
  symtraverse_all_step()



