from os import terminal_size
from cupshelpers import Printer
from pysmt.shortcuts import substitute, get_free_variables, read_smtlib
from pysmt.smtlib.printers import to_smtlib
from pysmt.smtlib.parser import SmtLibParser
from pysmt.logics import get_closer_smtlib_logic
from pysmt.type_checker import SimpleTypeChecker
from pysmt.fnode import FNode
from symtraverse import *
from state_simplify import state_simplify
import copy
import operator
from six import StringIO
from sygus_simplify import sygus_simplify
import pickle
from pysmt.printers import HRPrinter



# from io import StringIO

def test_stall():
  base_sv = {'wen_stage1', 'wen_stage2', 'stage1', 'stage2', 'stage3'}
  # name and width
  #oder0
  order = [ \
    TraverseBranchingNode(input_v=('rst', 1)),
    TraverseBranchingNode(signal_v=('stage1_go', 1)),
    TraverseBranchingNode(signal_v=('stage2_go', 1)),
    TraverseBranchingNode(signal_v=('stage3_go', 1))]

  #oder1
  # order = [ \
  #   TraverseBranchingNode(input_v=('rst', 1)),
  #   TraverseBranchingNode(signal_v=('stage2_go', 1)),
  #   TraverseBranchingNode(signal_v=('stage3_go', 1)),
  #   TraverseBranchingNode(signal_v=('stage1_go', 1))]

  # order = [ \
  #   TraverseBranchingNode(input_v=('rst', 1)),
  #   TraverseBranchingNode(signal_v=('stage3_go', 1)),
  #   TraverseBranchingNode(signal_v=('stage2_go', 1)),
  #   TraverseBranchingNode(signal_v=('stage1_go', 1))]


  btor_parser = BTOR2Parser()
  sts, _ = btor_parser.parse_file(Path("example/pipe-with-stall.btor2"))
  executor = SymbolicExecutor(sts)

  # #tag0->tag0
  init_setting = executor.convert({
      'wen_stage1':'v1',
      'wen_stage2':'v2',
      'stage1':'a',
      'stage2':'b',
      'stage3':'c'
      })
  # init_setting = executor.convert({
  #     'wen_stage1':'v1',
  #     'wen_stage2':0,
  #     'stage1':'a',
  #     'stage2':'b',
  #     'stage3':'b'
  #     })
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


  
  
  #Step: tag0-->tag0\
  print('Step: tag0-->tag0')
  traverser0_0 = SymbolicTraverse(sts=sts, executor=executor, base_variable=[executor.sv(n) for n in base_sv])
  traverser0_0.traverse(assumptions=tag2asmpt('tag0_0'), branching_point=order)
  print('number of state (tag0-->tag0):', len(traverser0_0.tracemgr.abs_state))

  
  executor0_1 = copy.copy(executor)
  s0_0 = traverser0_0.tracemgr.abs_state

  prev_list = traverser0_0.tracemgr.prev_state_list
  curr_list = traverser0_0.tracemgr.curr_state_list


  print('number of state (tag0-->tag0):',len(s0_0))
  for idx in range(len(s0_0)):
    s0_0[idx].print()
    s0_0[idx].print_assumptions()

  # s0_0[4].print()
  # s0_0[4].print_assumptions()

  

  



  # sygus_simplify(s0_0[4])

  def state2hrstring(stream,state_list):
    f = open(stream,"a")
    hr_printer = HRPrinter(f)

    state_list_new = []
    for state in state_list:
      state_expr_single = []
      for var, expr in state.sv.items():
        state_expr_single.append(EqualsOrIff(var, expr))
      state_expr = And(state_expr_single)
      state_list_new.append(state_expr)

    for state in state_list_new:
      print(state)
      hr_printer.printer(state)
      f.write('\n')
    
    f.close()

  # exit()

  # s = Printer()

  # for state in new_state_list:
  #   print(state)
  
  # f.close

  # # input()

  # file_name = "test.pkl"

  # open_file = open(file_name,"wb")
  # pickle.dump(new_state_list,open_file)
  # open_file.close()
  


  print('\n\n\n\n\n\n\nResults Statistics:')
  print('number of state (tag0-->tag0):',len(s0_0))
  # print('number of state (tag0-->tag1):',len(s0_1))
  # print('number of state (tag1-->tag1):',len(s1_1))
  # print('number of state (tag1-->tag2):',len(s1_2))
  # print('number of state (tag2-->tag2):',len(s2_2))
  # print('number of state (tag2-->tag3):',len(s2_3))
  # print('number of state (tag3-->tag3):',len(s3_3))










if __name__ == '__main__':
  test_stall()



