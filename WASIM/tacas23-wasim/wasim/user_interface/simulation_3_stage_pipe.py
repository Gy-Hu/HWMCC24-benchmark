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
  base_sv = {'RTL_id_ex_operand1','RTL_id_ex_operand2','RTL_id_ex_op','RTL_id_ex_rd','RTL_id_ex_reg_wen','RTL_ex_wb_val','RTL_ex_wb_rd','RTL_ex_wb_reg_wen','RTL_id_ex_valid','RTL_ex_wb_valid',\
    'RTL_registers[0]','RTL_registers[1]','RTL_registers[2]','RTL_registers[3]',\
      'RTL_scoreboard[0]','RTL_scoreboard[1]','RTL_scoreboard[2]','RTL_scoreboard[3]',\
        '__VLG_I_inst', '__VLG_I_inst_valid'}
       
  # name and width
  base_sv0 = base_sv
  order = [ \
    TraverseBranchingNode(input_v=('rst', 1)),
    TraverseBranchingNode(signal_v=('RTL_ex_go', 1)),
    TraverseBranchingNode(signal_v=('RTL_wb_go', 1)),
    ]

 

  btor_parser = BTOR2Parser()
  sts, _ = btor_parser.parse_file(Path("../design/3_stage_pipe_inst.btor2"))
  executor = SymbolicExecutor(sts)

  # #tag0->tag0 initialize
  init_setting = executor.convert({
      'RTL_id_ex_operand1':'oper1',
      'RTL_id_ex_operand2':'oper2',
      'RTL_id_ex_op':'op',
      'RTL_id_ex_rd':'rd1',
      'RTL_id_ex_reg_wen':'w1',
      'RTL_ex_wb_val':'ex_val',
      'RTL_ex_wb_rd':'rd2',
      'RTL_ex_wb_reg_wen':'w2',
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
      '__ILA_I_inst':'ila_inst',
      '__auxvar0__recorder_sn_condmet':0,
      '__auxvar1__recorder_sn_condmet':0,
      '__auxvar2__recorder_sn_condmet':0,
      '__auxvar3__recorder_sn_condmet':0,
      })
  executor.init(init_setting)


  def tag2asmpt(flag,executor_new):
    if(flag=='start-ex'): 
      return [And ( EqualsOrIff(executor_new.sv('rst'),BV(0,1)), EqualsOrIff(executor_new.sv('dummy_reset'),BV(0,1)) )]
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
      executor_temp = copy.copy(executor)
      d = executor_temp.convert(phase_marker)
      executor_temp.set_current_state(s, d)
      traverser_temp = SymbolicTraverse(sts=sts, executor= executor_temp, base_variable=[executor_temp.sv(n) for n in base_sv])
      traverser_temp.traverse_one_step(assumptions=tag2asmpt(flag=flag, executor_new=executor_temp), branching_point=order, s_init=s)
      print('number of state (%s): 1 --> %d' % (flag, len(traverser_temp.tracemgr.abs_state_one_step)))
      if(len(traverser_temp.tracemgr.abs_state_one_step) == 0):
        state_list_extended = copy.copy(state_list)
        state_list_extended.append(s)
        branch_list.append(state_list_extended)
      else:
        for nextstate in traverser_temp.tracemgr.abs_state_one_step:
            state_list_extended = copy.copy(state_list)
            state_list_extended.append(nextstate)
            branch_list.append(state_list_extended)
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
    start_num = len(branch_list_old)
    end_num = len(branch_list)
    print('number of state (%s) in total: %d --> %d' % (flag, len(branch_list_old), len(branch_list)))
    end_time = time.perf_counter()

    return (flag, start_num, end_num, end_time)

  #Step: start 
  print('Step: start')
  s_init = executor.get_curr_state()
  is_not_start = EqualsOrIff(executor.sv("__START__"), BV(0,1))
  is_not_start = executor.interpret_state_expr_on_curr_frame(is_not_start)
  assert not is_sat(And(s_init.asmpt + [is_not_start]))  # we expect __START__ to be 1 on the initial state
  pop_list = []
  base_sv_temp = {'RTL_id_ex_operand1','RTL_id_ex_operand2','RTL_id_ex_op','RTL_id_ex_rd','RTL_id_ex_reg_wen','RTL_ex_wb_val','RTL_ex_wb_rd','RTL_ex_wb_reg_wen','RTL_id_ex_valid','RTL_ex_wb_valid',\
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
  


  ##Step: start-ex
  print('Step: start-ex')
  (flag0, start_num0, end_num0, end_time0) = extend_branch_next_phase(branch_list, executor, sts, base_sv, flag='start-ex', phase_marker=\
    {'__START__': 1, 'ppl_stage_ex': 0, 'ppl_stage_wb': 0, 'ppl_stage_finish': 0})


  ##Step: ex-ex
  print('\n\n\nStep: ex-->ex')
  (flag1, start_num1, end_num1, end_time1) = extend_branch_same_phase(branch_list, executor, sts, base_sv=base_sv, flag='ex-ex', phase_marker=\
    {'__START__': 0, 'ppl_stage_ex': 1, 'ppl_stage_wb': 0, 'ppl_stage_finish': 0})

  ##Step: ex-wb
  print('\n\n\nStep: ex-->wb')
  (flag2, start_num2, end_num2, end_time2) = extend_branch_next_phase(branch_list, executor, sts, base_sv={'RTL_ex_wb_val','RTL_ex_wb_rd','RTL_ex_wb_reg_wen','RTL_ex_wb_valid',\
    'RTL_registers[0]','RTL_registers[1]','RTL_registers[2]','RTL_registers[3]'}, flag='ex-wb', phase_marker=\
    {'__START__': 0, 'ppl_stage_ex': 1, 'ppl_stage_wb': 0, 'ppl_stage_finish': 0})


  ##Step: wb-wb
  print('\n\n\nStep: wb-->wb')
  (flag3, start_num3, end_num3, end_time3) = extend_branch_same_phase(branch_list, executor, sts, base_sv={'RTL_ex_wb_val','RTL_ex_wb_rd','RTL_ex_wb_reg_wen','RTL_ex_wb_valid',\
    'RTL_registers[0]','RTL_registers[1]','RTL_registers[2]','RTL_registers[3]'}, flag='wb-wb', phase_marker=\
    {'__START__': 0, 'ppl_stage_ex': 0, 'ppl_stage_wb': 1, 'ppl_stage_finish': 0})

  ##Step: wb-finish
  print('\n\n\nStep: wb-->finish')
  (flag4, start_num4, end_num4, end_time4) = extend_branch_next_phase(branch_list, executor, sts, base_sv= {'RTL_registers[0]','RTL_registers[1]','RTL_registers[2]','RTL_registers[3]'}, \
    flag='wb-finish', phase_marker={'__START__': 0, 'ppl_stage_ex': 0, 'ppl_stage_wb': 1, 'ppl_stage_finish': 0})

  file_name = "../output/trace_3_stage_pipe_inst.pkl"
  open_file = open(file_name,"wb")
  pickle.dump(branch_list,open_file)
  open_file.close()


  def result_display(flag, num_old, num_new, end_time, start_time):
    print('-'*15)
    print('number of state (%s) in total: %d --> %d' % (flag, num_old, num_new))
    print('program running time: %d(s):  ' %round((end_time-start_time),2))
    print('program running time: %d(min):' %round((end_time-start_time)/60,2))

  flag_list = [flag0, flag1, flag2, flag3, flag4]
  num_old_list = [start_num0, start_num1, start_num2, start_num3, start_num4]
  num_new_list = [end_num0, end_num1, end_num2, end_num3, end_num4]
  end_time_list = [end_time0, end_time1, end_time2, end_time3, end_time4]

  print('\n\n\n\n\n--------------------------RESULT--------------------------\n')
  for idx in range(len(flag_list)):
    result_display(flag_list[idx], num_old_list[idx], num_new_list[idx], end_time_list[idx], start_time)


if __name__ == '__main__':
  symtraverse_all_step()