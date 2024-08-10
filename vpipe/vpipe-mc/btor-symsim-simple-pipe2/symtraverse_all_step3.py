from cgitb import reset
from copyreg import pickle
from email.mime import base
from os import terminal_size
from readline import set_completion_display_matches_hook
from pysmt.shortcuts import substitute
from symtraverse import *
from state_simplify import state_simplify_ite
import copy
import operator
from sygus_simplify import sygus_simplify
from pysmt.type_checker import SimpleTypeChecker
from pysmt.operators import new_node_type,op_to_str,all_types
from pysmt.fnode import *
import pickle
from pysmt.fnode import FNode
import datetime
import time

def symtraverse_all_step():
  start_time = time.perf_counter()
  base_sv = {'RTL_if_id_inst','RTL_if_id_valid',\
            'RTL_id_ex_operand1','RTL_id_ex_operand2','RTL_id_ex_op','RTL_id_ex_rd','RTL_id_ex_reg_wen','RTL_id_ex_valid',\
            'RTL_ex_wb_val','RTL_ex_wb_rd','RTL_ex_wb_reg_wen','RTL_ex_wb_valid',\
            'RTL_registers[0]','RTL_registers[1]','RTL_registers[2]','RTL_registers[3]',\
            'RTL_scoreboard[0]','RTL_scoreboard[1]','RTL_scoreboard[2]','RTL_scoreboard[3]',\
            }
  

  order = [ \
    TraverseBranchingNode(input_v=('rst', 1)),
    TraverseBranchingNode(signal_v=('RTL_id_go', 1)),
    TraverseBranchingNode(signal_v=('RTL_ex_go', 1)),
    TraverseBranchingNode(signal_v=('RTL_wb_go', 1)),
    ]



  btor_parser = BTOR2Parser()
  sts, _ = btor_parser.parse_file(Path("/data/wenjifang//vpipe-mc/ILA-pipeline/ilang_simple_pipe/stall_vrecorder/verify/ADD/problem.btor2"))
  executor = SymbolicExecutor(sts)

  # #tag0->tag0 initialize
  init_setting = executor.convert({
      'RTL_if_id_inst':'inst_id',
      'RTL_id_ex_operand1':'oper1',
      'RTL_id_ex_operand2':'oper2',
      'RTL_id_ex_op':'op',
      'RTL_id_ex_rd':'rd1',
      'RTL_id_ex_reg_wen':'w1',
      'RTL_ex_wb_val':'ex_val',
      'RTL_ex_wb_rd':'rd2',
      'RTL_ex_wb_reg_wen':'w2',
      'RTL_if_id_valid':'v0',
      'RTL_id_ex_valid':'v1',
      'RTL_ex_wb_valid':'v2',
      'RTL_registers[0]':'reg0',
      'RTL_registers[1]':'reg1',
      'RTL_registers[2]':'reg2',
      'RTL_registers[3]':'reg3',
      'RTL_scoreboard[0]':'s0',
      'RTL_scoreboard[1]':'s1',
      'RTL_scoreboard[2]':'s2',
      'RTL_scoreboard[3]':'s3',
      '__VLG_I_inst': 'inst',
      '__VLG_I_inst_valid':'inst_v',
      '__ILA_I_inst':'ila_inst'
      })
  executor.init(init_setting)


  def tag2asmpt(flag,executor_new):
    if(flag=='start-id'): #tag0-1-1
      return [And ( EqualsOrIff(executor_new.sv('rst'),BV(0,1)), EqualsOrIff(executor_new.sv('dummy_reset'),BV(0,1)) )]
    elif(flag=='id-id'): 
      return [And (EqualsOrIff(executor_new.sv('RTL_id_go'),BV(0,1)) , EqualsOrIff(executor_new.sv('rst'),BV(0,1)), EqualsOrIff(executor_new.sv('dummy_reset'),BV(0,1)) )]
    elif(flag=='id-ex'):
      return [And (EqualsOrIff(executor_new.sv('RTL_id_go'),BV(1,1)) , EqualsOrIff(executor_new.sv('rst'),BV(0,1)), EqualsOrIff(executor_new.sv('dummy_reset'),BV(0,1)) )]
    elif(flag=='ex-ex'):
      return [And (EqualsOrIff(executor_new.sv('RTL_ex_go'),BV(0,1)) , EqualsOrIff(executor_new.sv('rst'),BV(0,1)), EqualsOrIff(executor_new.sv('dummy_reset'),BV(0,1)) )]
    elif(flag=='ex-wb'):
      return [And (EqualsOrIff(executor_new.sv('RTL_ex_go'),BV(1,1)) , EqualsOrIff(executor_new.sv('rst'),BV(0,1)), EqualsOrIff(executor_new.sv('dummy_reset'),BV(0,1)) )]
    elif(flag=='wb-wb'):
      return [And (EqualsOrIff(executor_new.sv('RTL_wb_go'),BV(0,1)) , EqualsOrIff(executor_new.sv('rst'),BV(0,1)), EqualsOrIff(executor_new.sv('dummy_reset'),BV(0,1)) )]
    elif(flag=='wb-finish'):
      return [And (EqualsOrIff(executor_new.sv('RTL_wb_go'),BV(1,1)) , EqualsOrIff(executor_new.sv('rst'),BV(0,1)), EqualsOrIff(executor_new.sv('dummy_reset'),BV(0,1)) )]
    else:
      print ('<ERROR>: Wrong tag transition format!')
      assert False

  def extend_branch_next_phase(branch_list, executor, sts, base_sv, flag, phase_marker):
    branch_list_old = copy.copy(branch_list)
    branch_list.clear()
    for state_list_old in branch_list_old:
      state_list = copy.copy(state_list_old)
      s = state_list[-1] # get the last state, and extend it by 1 step

      executor0_1 = copy.copy(executor)
      d = executor0_1.convert(phase_marker)
      executor0_1.set_current_state(s, d)
      traverser0_1 = SymbolicTraverse(sts=sts, executor= executor0_1, base_variable=[executor0_1.sv(n) for n in base_sv])
      traverser0_1.traverse_one_step(assumptions=tag2asmpt(flag=flag, executor_new=executor0_1), branching_point=order, s_init=s)
      print('number of state (%s): 1 --> %d' % (flag, len(traverser0_1.tracemgr.abs_state_one_step)))
      for nextstate in traverser0_1.tracemgr.abs_state_one_step:
          state_list_extended = copy.copy(state_list)
          state_list_extended.append(nextstate)
          branch_list.append(state_list_extended)
    print('number of state (%s) in total: %d --> %d' % (flag, len(branch_list_old), len(branch_list)))
    return (flag, len(branch_list_old), len(branch_list))

  def extend_branch_same_phase(branch_list, executor, sts, base_sv, flag, phase_marker):
    branch_list_old = copy.copy(branch_list)
    branch_list.clear()
    for state_list_old in branch_list_old:
      state_list = copy.copy(state_list_old)
      s = state_list[-1] # get the last state, and extend it by 1 step

      executor0_1 = copy.copy(executor)
      d = executor0_1.convert(phase_marker)
      executor0_1.set_current_state(s, d)
      traverser0_1 = SymbolicTraverse(sts=sts, executor= executor0_1, base_variable=[executor0_1.sv(n) for n in base_sv])
      traverser0_1.traverse(assumptions=tag2asmpt(flag=flag, executor_new=executor0_1), branching_point=order, s_init=s)
      print('number of state (%s): 1 --> %d' % (flag, len(traverser0_1.tracemgr.abs_state)))
      for nextstate in traverser0_1.tracemgr.abs_state: # HZ: note here abs_state contains the original state `s`
          state_list_extended = copy.copy(state_list)
          state_list_extended.append(nextstate)
          branch_list.append(state_list_extended)
    print('number of state (%s) in total: %d --> %d' % (flag, len(branch_list_old), len(branch_list)))
    return (flag, len(branch_list_old), len(branch_list))

  #Step: start 
  print('Step: start')
  s_init = executor.get_curr_state()
  is_not_start = EqualsOrIff(executor.sv("__START__"), BV(0,1))
  is_not_start = executor.interpret_state_expr_on_curr_frame(is_not_start)
  assert not is_sat(And(s_init.asmpt + [is_not_start]))  # we expect __START__ to be 1 on the initial state
  pop_list = []
  base_sv_temp = {'RTL_if_id_inst','RTL_if_id_valid',\
                  'RTL_id_ex_operand1','RTL_id_ex_operand2','RTL_id_ex_op','RTL_id_ex_rd','RTL_id_ex_reg_wen','RTL_id_ex_valid',\
                  'RTL_ex_wb_val','RTL_ex_wb_rd','RTL_ex_wb_reg_wen','RTL_ex_wb_valid',\
                  '\'RTL_registers[0]\'','\'RTL_registers[1]\'','\'RTL_registers[2]\'','\'RTL_registers[3]\'',\
                  '\'RTL_scoreboard[0]\'','\'RTL_scoreboard[1]\'','\'RTL_scoreboard[2]\'','\'RTL_scoreboard[3]\'',\
                  '__VLG_I_inst', '__VLG_I_inst_valid'}
  for s, v in s_init.sv.items():
    print(str(s.serialize()))
    if (str(s.serialize()) not in base_sv_temp):
    #   # if(str(s.serialize() != b_sv)):
      pop_list.append(s)
  result = 'RTL_registers[0]' in base_sv
  print(result)

  print(pop_list)
  for s in pop_list:
    s_init.sv.pop(s)
  branch_list = [[s_init]]

  s_init.print()
  


  ##Step: start-id
  print('Step: start-id')
  (flag0, num_old0, num_new0) = extend_branch_next_phase(branch_list, executor, sts, base_sv=base_sv, flag='start-id', phase_marker=\
    {'__START__': 1, 'stage_tracker_if_id_iuv': 0, 'stage_tracker_id_ex_iuv': 0, 'stage_tracker_ex_wb_iuv': 0, 'stage_tracker_wb_iuv': 0})
  end_time0 = time.perf_counter()
  print('program running time: %d(s):  ' %round((end_time0-start_time),2))
  print('program running time: %d(min):' %round((end_time0-start_time)/60,2))

  ##Step: id-id
  print('\n\n\nStep: id-->id')
  (flag1, num_old1, num_new1) = extend_branch_same_phase(branch_list, executor, sts, base_sv=base_sv, flag='id-id', phase_marker=\
    {'__START__': 0, 'stage_tracker_if_id_iuv': 1, 'stage_tracker_id_ex_iuv': 0, 'stage_tracker_ex_wb_iuv': 0, 'stage_tracker_wb_iuv': 0})
  end_time1 = time.perf_counter()
  print('program running time: %d(s):  ' %round((end_time1-start_time),2))
  print('program running time: %d(min):' %round((end_time1-start_time)/60,2))


  base_sv = {'RTL_id_ex_operand1','RTL_id_ex_operand2','RTL_id_ex_op','RTL_id_ex_rd','RTL_id_ex_reg_wen','RTL_id_ex_valid',\
            'RTL_ex_wb_val','RTL_ex_wb_rd','RTL_ex_wb_reg_wen','RTL_ex_wb_valid',\
            'RTL_registers[0]','RTL_registers[1]','RTL_registers[2]','RTL_registers[3]'}
  ##Step: id-ex
  print('Step: id-ex')
  (flag2, num_old2, num_new2) = extend_branch_next_phase(branch_list, executor, sts, base_sv=base_sv, flag='id-ex', phase_marker=\
    {'__START__': 0, 'stage_tracker_if_id_iuv': 1, 'stage_tracker_id_ex_iuv': 0, 'stage_tracker_ex_wb_iuv': 0, 'stage_tracker_wb_iuv': 0})
  end_time2 = time.perf_counter()
  print('program running time: %d(s):  ' %round((end_time2-start_time),2))
  print('program running time: %d(min):' %round((end_time2-start_time)/60,2))
  
  
  ##Step: ex-ex
  print('\n\n\nStep: ex-->ex')
  (flag3, num_old3, num_new3) = extend_branch_same_phase(branch_list, executor, sts, base_sv=base_sv, flag='ex-ex', phase_marker=\
    {'__START__': 0, 'stage_tracker_if_id_iuv': 0, 'stage_tracker_id_ex_iuv': 1, 'stage_tracker_ex_wb_iuv': 0, 'stage_tracker_wb_iuv': 0})
  end_time3 = time.perf_counter()
  print('program running time: %d(s):  ' %round((end_time3-start_time),2))
  print('program running time: %d(min):' %round((end_time3-start_time)/60,2))

  base_sv = {'RTL_ex_wb_val','RTL_ex_wb_rd','RTL_ex_wb_reg_wen','RTL_ex_wb_valid',\
    'RTL_registers[0]','RTL_registers[1]','RTL_registers[2]','RTL_registers[3]'}

  # file_name = "branch_list_idex.pkl"
  # open_file = open(file_name,"wb")
  # pickle.dump(branch_list,open_file)
  # open_file.close()
  # exit()
  ##Step: ex-wb
  print('\n\n\nStep: ex-->wb')
  (flag4, num_old4, num_new4) = extend_branch_next_phase(branch_list, executor, sts, base_sv=base_sv, flag='ex-wb', phase_marker=\
    {'__START__': 0, 'stage_tracker_if_id_iuv': 0, 'stage_tracker_id_ex_iuv': 1, 'stage_tracker_ex_wb_iuv': 0, 'stage_tracker_wb_iuv': 0})
  end_time4 = time.perf_counter()
  print('program running time: %d(s):  ' %round((end_time4-start_time),2))
  print('program running time: %d(min):' %round((end_time4-start_time)/60,2))

  ##Step: wb-wb
  print('\n\n\nStep: wb-->wb')
  (flag5, num_old5, num_new5) = extend_branch_same_phase(branch_list, executor, sts, base_sv=base_sv, flag='wb-wb', phase_marker=\
    {'__START__': 0, 'stage_tracker_if_id_iuv': 0, 'stage_tracker_id_ex_iuv': 0, 'stage_tracker_ex_wb_iuv': 1, 'stage_tracker_wb_iuv': 0})
  end_time5 = time.perf_counter()
  print('program running time: %d(s):  ' %round((end_time5-start_time),2))
  print('program running time: %d(min):' %round((end_time5-start_time)/60,2))

  base_sv = {'RTL_registers[0]','RTL_registers[1]','RTL_registers[2]','RTL_registers[3]'}
  ##Step: wb-finish
  print('\n\n\nStep: wb-->finish')
  (flag6, num_old6, num_new6) = extend_branch_next_phase(branch_list, executor, sts, base_sv=base_sv, flag='wb-finish', phase_marker=\
    {'__START__': 0, 'stage_tracker_if_id_iuv': 0, 'stage_tracker_id_ex_iuv': 0, 'stage_tracker_ex_wb_iuv': 1, 'stage_tracker_wb_iuv': 0})
  end_time6 = time.perf_counter()
  print('program running time: %d(s):  ' %round((end_time6-start_time),2))
  print('program running time: %d(min):' %round((end_time6-start_time)/60,2))

  file_name = "branch_list_c3_0613.pkl"
  open_file = open(file_name,"wb")
  pickle.dump(branch_list,open_file)
  open_file.close()

  def result_display(flag, num_old, num_new, end_time, start_time):
    print('-'*15)
    print('number of state (%s) in total: %d --> %d' % (flag, num_old, num_new))
    print('program running time: %d(s):  ' %round((end_time-start_time),2))
    print('program running time: %d(min):' %round((end_time-start_time)/60,2))

  flag_list = [flag0, flag1, flag2, flag3, flag4, flag5, flag6]
  num_old_list = [num_old0, num_old1, num_old2, num_old3, num_old4, num_old5, num_old6]
  num_new_list = [num_new0, num_new1, num_new2, num_new3, num_new4, num_new5, num_new6]
  end_time_list = [end_time0, end_time1, end_time2, end_time3, end_time4, end_time5, end_time6]

  print('\n\n\n\n\n--------------------------RESULT--------------------------\n')
  for idx in range(len(flag_list)):
    result_display(flag_list[idx], num_old_list[idx], num_new_list[idx], end_time_list[idx], start_time)



if __name__ == '__main__':
  symtraverse_all_step()



