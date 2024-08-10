from copyreg import pickle
import imp
from os import terminal_size
from click import open_file
from pysmt.shortcuts import substitute
from symtraverse import *
from state_simplify import state_simplify
import copy
import operator
from sygus_simplify import sygus_simplify
from pysmt.type_checker import SimpleTypeChecker
from pysmt.operators import new_node_type,op_to_str,all_types
from pysmt.fnode import *
import pickle
from pysmt.printers import HRPrinter
import os


def symtraverse_all_step():
  base_sv = {'wen_stage1', 'wen_stage2', 'stage1', 'stage2', 'stage3'}
  # name and width

  order = [ \
    TraverseBranchingNode(input_v=('rst', 1)),
    TraverseBranchingNode(signal_v=('stage1_go', 1)),
    TraverseBranchingNode(signal_v=('stage2_go', 1)),
    TraverseBranchingNode(signal_v=('stage3_go', 1))]



  btor_parser = BTOR2Parser()
  sts, _ = btor_parser.parse_file(Path("example/pipe-with-stall.btor2"))

  executor = SymbolicExecutor(sts)


  # #tag0->tag0 initialize
  init_setting = executor.convert({
      'wen_stage1':'v1',
      'wen_stage2':'v2',
      'stage1':'a',
      'stage2':'b',
      'stage3':'c'
      })
  pickle1 = copy.copy(init_setting)
  executor.init(init_setting)


  
  def tag2asmpt(flag):
    if(flag=='tag0_0'):
      return [EqualsOrIff(executor.sv('stage1_go'),BV(0,1))]
    elif(flag=='tag1'):
      return [EqualsOrIff(executor.sv('stage1_go'),BV(1,1))]
    elif(flag=='tag1_1'):
      return [EqualsOrIff(executor.sv('stage1_go'),BV(0,1)),EqualsOrIff(executor.sv('stage2_go'),BV(0,1))]
    elif(flag=='tag2'):
      return [EqualsOrIff(executor.sv('stage2_go'),BV(1,1))]
    elif(flag=='tag2_2'):
      return [EqualsOrIff(executor.sv('stage2_go'),BV(0,1)),EqualsOrIff(executor.sv('stage3_go'),BV(0,1))]
    elif(flag=='tag3'):
      return [EqualsOrIff(executor.sv('stage3_go'),BV(1,1))]
    elif(flag=='tag3_3'):
      return [EqualsOrIff(executor.sv('stage3_go'),BV(0,1))]
    else:
      print ('<ERROR>: Wrong tag transition format!')
      assert False

    

  state_list = []
  branch_list = []
  branch_list_temp = []
  
  
  #Step: tag0-->tag0
  print('Step: tag0-->tag0')
  traverser0_0 = SymbolicTraverse(sts=sts, executor=executor, base_variable=[executor.sv(n) for n in base_sv])
  traverser0_0.traverse(assumptions=tag2asmpt('tag0_0'), branching_point=order)
  print('number of state (tag0-->tag0):',len(traverser0_0.tracemgr.abs_state))

  
  executor0_1 = copy.copy(executor)
  s0_0 = traverser0_0.tracemgr.abs_state


  print('number of state (tag0-->tag0):',len(s0_0))

  print('state of tag0-->tag0')
  for idx in range(len(s0_0)):
    s0_0[idx].print()
  # input()
    # state_list.append(s0_0[idx])




  #Step: tag0-->tag1
  executor_copy0_0 = copy.copy(executor)
  print('\n\n\nStep: tag0-->tag1')
  s0_1 = []
  state_list = []
  
  for idx0_0 in range(len(s0_0)):
      s00 = s0_0[idx0_0]
      print('prev_state')
      s00.print()
      executor0_1 = executor_copy0_0
      d = executor0_1.convert({'tag0':1, 'tag1':0, 'tag2':0, 'tag3':0})
      executor0_1.set_current_state(s00, d)
      traverser0_1 = SymbolicTraverse(sts=sts, executor= executor0_1, base_variable=[executor0_1.sv(n) for n in base_sv])
      traverser0_1.traverse_one_step(assumptions=tag2asmpt('tag1'), branching_point=order,tag_flag= 'tag1')

      for state in traverser0_1.tracemgr.abs_state_one_step:
        state_list.append(s00)
        state_list.append(state)
        branch_list.append(copy.copy(state_list))
        state_list = []
      s0_1 = s0_1 + traverser0_1.tracemgr.abs_state_one_step

  print('number of state (tag0-->tag1):',len(s0_1))
  print('len of branch_list',len(branch_list))
  print('len of state list ',len(branch_list[0])) ##len = 2

  print('state of tag0-->tag1')
  print('state_list')
  for state_list in branch_list:
    state_list[1].print()
  print('s0_1')
  for idx in range(len(s0_1)):
    s0_1[idx].print()
  

  # #Step: tag1-->tag1
  # executor_copy0_1 = copy.copy(executor0_1)
  # print('\n\n\nStep: tag1-->tag1')
  # s1_1 = []
  # branch_list_temp = copy.copy(branch_list)
  # branch_list.clear()
  # # state_list.clear()
  # for state_list_temp in branch_list_temp:
  # # for idx in range(len(s0_1)):
  #   state_list = copy.copy(state_list_temp)
  #   # print(len(state_list_temp))
  #   # input()
  #   s01 = state_list[-1]
  #   print('prev_state')
  #   s01.print()
  #   # s01 = s0_1[idx]
  #   executor1_1 = executor_copy0_1
  #   # input()

  #   d = executor1_1.convert({'tag0':0, 'tag1':1, 'tag2':0, 'tag3':0})
  #   executor1_1.set_current_state(s01, d)
  #   traverser1_1 = SymbolicTraverse(sts=sts, executor= executor1_1, base_variable=[executor1_1.sv(n) for n in base_sv])
  #   traverser1_1.traverse(assumptions=tag2asmpt('tag1_1'), branching_point=order)

  #   for state in traverser1_1.tracemgr.abs_state:
  #     state_list = copy.copy(state_list_temp)
  #     # print(len(state_list))
  #     # input()
  #     state_list.append(state)
  #     branch_list.append(copy.copy(state_list))
  #     state_list.clear()

  #   s1_1 = s1_1 + traverser1_1.tracemgr.abs_state
  #   # input()
  # print('number of state (tag1-->tag1):',len(s1_1))
  # print('len of branch_list',len(branch_list))
  # print('len of state list ',len(branch_list[0]))

  # print('state of tag1-->tag1')
  # print('state_list')
  # for idx in range(len(branch_list)):
  #   state_list = branch_list[idx]
  #   state_list[2].print()
  #   s1_1[idx].print()
  #   print('111111\n')
  




  # #Step: tag1-->tag2
  # executor_copy1_1 = copy.copy(executor1_1)
  # print('\n\n\nStep: tag1-->tag2')
  # s1_2 = []
  # branch_list_temp = copy.copy(branch_list)
  # branch_list.clear()
  # for state_list_temp in branch_list_temp:
  #   state_list = copy.copy(state_list_temp)
  #   s12 = state_list[-1]
  #   print('prev_state')
  #   s12.print()
  # # for idx in range(len(s1_1)):
  #   # s12 = s1_1[idx]
  #   executor1_2 = executor_copy1_1
  #   d = executor1_2.convert({'tag0':0, 'tag1':1, 'tag2':0, 'tag3':0})
  #   executor1_2.set_current_state(s12, d)
  #   traverser1_2 = SymbolicTraverse(sts=sts, executor= executor1_2, base_variable=[executor1_2.sv(n) for n in base_sv])
  #   traverser1_2.traverse_one_step(assumptions=tag2asmpt('tag2'), branching_point=order,tag_flag= 'tag2')

  #   for state in traverser1_2.tracemgr.abs_state_one_step:
  #     state_list = copy.copy(state_list_temp)
  #     # print(len(state_list))
  #     # input()
  #     state_list.append(state)
  #     branch_list.append(copy.copy(state_list))
  #     state_list.clear()

  #   s1_2 = s1_2 + traverser1_2.tracemgr.abs_state_one_step
  # print('number of state (tag1-->tag2):',len(s1_2))
  # print('len of branch_list',len(branch_list))
  # print('len of state list ',len(branch_list[0]))

  # print('state of tag1-->tag2')
  # print('state_list')
  # for idx in range(len(branch_list)):
  #   state_list = branch_list[idx]
  #   state_list[3].print()
  #   s1_2[idx].print()
  #   print('111111\n')


  # # #Step: tag2-->tag2
  # executor_copy1_2 = copy.copy(executor1_2)
  # print('\n\n\nStep: tag2-->tag2')
  # s2_2 = []
  # branch_list_temp = copy.copy(branch_list)
  # branch_list.clear()
  # for state_list_temp in branch_list_temp:
  #   state_list = copy.copy(state_list_temp)
  #   s22 = state_list[-1]
  #   print('prev_state')
  #   s22.print()
  # # for idx in range(len(s1_2)):
  #   # s22 = s1_2[idx]
  #   executor2_2 = executor_copy1_2
  #   d = executor2_2.convert({'tag0':0, 'tag1':0, 'tag2':1, 'tag3':0})
  #   executor2_2.set_current_state(s22, d)
  #   traverser2_2 = SymbolicTraverse(sts=sts, executor= executor2_2, base_variable=[executor2_2.sv(n) for n in base_sv])
  #   traverser2_2.traverse(assumptions=tag2asmpt('tag2_2'), branching_point=order)

  #   for state in traverser2_2.tracemgr.abs_state:
  #     state_list = copy.copy(state_list_temp)
  #     # print(len(state_list))
  #     # input()
  #     state_list.append(state)
  #     branch_list.append(copy.copy(state_list))
  #     state_list.clear()

  #   s2_2 = s2_2 + traverser2_2.tracemgr.abs_state
  # print('number of state (tag2-->tag2):',len(s2_2))
  # print('len of branch_list',len(branch_list))
  # print('len of state list ',len(branch_list[0]))


  # # #Step: tag2-->tag3
  # executor_copy2_2 = copy.copy(executor2_2)
  # print('\n\n\nStep: tag2-->tag3')
  # s2_3 = []
  # branch_list_temp = copy.copy(branch_list)
  # branch_list.clear()
  # for state_list_temp in branch_list_temp:
  #   state_list = copy.copy(state_list_temp)
  #   s23 = state_list[-1]
  #   print('prev_state')
  #   s23.print()
  # # for idx in range(len(s2_2)):
  #   # s23 = s2_2[idx]
  #   executor2_3 = executor_copy2_2
  #   d = executor2_3.convert({'tag0':0, 'tag1':0, 'tag2':1, 'tag3':0})
  #   executor2_3.set_current_state(s23, d)
  #   traverser2_3 = SymbolicTraverse(sts=sts, executor= executor2_3, base_variable=[executor2_3.sv(n) for n in base_sv])
  #   traverser2_3.traverse_one_step(assumptions=tag2asmpt('tag3'), branching_point=order,tag_flag= 'tag3')


  #   for state in traverser2_3.tracemgr.abs_state_one_step:
  #     state_list = copy.copy(state_list_temp)
  #     # print(len(state_list))
  #     # input()
  #     state_list.append(state)
  #     branch_list.append(copy.copy(state_list))
  #     state_list.clear()

  #   s2_3 = s2_3 + traverser2_3.tracemgr.abs_state_one_step
  # print('number of state (tag2-->tag3):',len(s2_3))
  # print('len of branch_list',len(branch_list))
  # print('len of state list ',len(branch_list[0]))


  # # #Step: tag3-->tag3
  # executor_copy2_3 = copy.copy(executor2_3)
  # print('\n\n\nStep: tag2-->tag2')
  # s3_3 = []
  # branch_list_temp = copy.copy(branch_list)
  # branch_list.clear()

  # for state_list_temp in branch_list_temp:
  #   state_list = copy.copy(state_list_temp)
  #   s33 = state_list[-1]
  #   print('prev_state')
  #   s33.print()
  # # for idx in range(len(s2_3)):
  #   # s33 = s2_3[idx]
  #   executor3_3 = executor_copy2_3
  #   d = executor3_3.convert({'tag0':0, 'tag1':0, 'tag2':0, 'tag3':1})
  #   executor3_3.set_current_state(s33, d)
  #   traverser3_3 = SymbolicTraverse(sts=sts, executor= executor3_3, base_variable=[executor3_3.sv(n) for n in base_sv])
  #   traverser3_3.traverse(assumptions=tag2asmpt('tag3_3'), branching_point=order)


  #   for state in traverser3_3.tracemgr.abs_state:
  #     state_list = copy.copy(state_list_temp)
  #     # print(len(state_list))
  #     # input()
  #     state_list.append(state)
  #     branch_list.append(copy.copy(state_list))
  #     state_list.clear()


  #   s3_3 = s3_3 + traverser3_3.tracemgr.abs_state
  # print('number of state (tag3-->tag3):',len(s3_3))
  # print('len of branch_list',len(branch_list))
  # print('len of state list ',len(branch_list[0]))

  # for idx in range(len(s3_3)):
  #   for s, v in s3_3[idx].sv.items():
  #     if('X' in str(v.serialize())):
  #       input('X here')
  #     else:
  #       pass
  #       # print('No X in states')
  #   # s3_3[idx].print()




  print('\n\n\n\n\n\n\nResults Statistics:')
  print('number of state (tag0-->tag0):',len(s0_0))
  print('number of state (tag0-->tag1):',len(s0_1))
  # print('number of state (tag1-->tag1):',len(s1_1))
  # print('number of state (tag1-->tag2):',len(s1_2))
  # print('number of state (tag2-->tag2):',len(s2_2))
  # print('number of state (tag2-->tag3):',len(s2_3))
  # print('number of state (tag3-->tag3):',len(s3_3))
  # print('len of final branch list',len(branch_list))
  # print('len of final state list ',len(branch_list[0]))


  # file_name = "branch_list.pkl"
  # open_file = open(file_name,"wb")
  # pickle.dump(branch_list,open_file)
  # open_file.close()


      

  


  

  return (branch_list,executor,sts)



  





if __name__ == '__main__':
  symtraverse_all_step()



