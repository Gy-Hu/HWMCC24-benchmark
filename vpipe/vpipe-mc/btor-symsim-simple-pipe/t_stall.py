from symsim import Symbol, Not, And, Or, Implies, Ite, BVAdd, BV, EqualsOrIff, BVNot, BVSub, TRUE, is_sat, get_model
from symsim import BOOL, BVType
from symsim import SymbolicExecutor
from tracemgr import TraceManager
from pathlib import Path
from btorparser import BTOR2Parser

def test_stall():
  btor_parser = BTOR2Parser()
  sts, _ = btor_parser.parse_file(Path("example/pipe-with-stall.btor2"))
  executor = SymbolicExecutor(sts)
  tm = TraceManager(sts)

  executor.init(
    executor.convert({
      'wen_stage1':'v1',
      'wen_stage2':'v2',
      'stage1':'a',
      'stage2':'b',
      'stage3':'c'
      }))

  # executor.set_current_state(
  #   executor.convert({
  #     'wen_stage1':'v1',
  #     'wen_stage2':'v2',
  #     'stage1':'a',
  #     'stage2':'b',
  #     'stage3':'c'
  #     }),
  #     [EqualsOrIff(executor.sv('stage1_go'),BV(0,1))]
  #   )

  # executor.set_input( 
  #   executor.convert( {'rst':0 } ), 
  #   [EqualsOrIff(executor.sv('stage1_go'),BV(1,1))])
  executor.set_current_state()
  executor.sim_one_step()
  executor.print_current_step()

  executor.get_curr_state()


  # executor.print_current_step_assumptions()

  # tm.record_base_var({
  #   executor.sv('wen_stage1'),
  #   executor.sv('wen_stage2'),
  #   executor.sv('stage1'),
  #   executor.sv('stage2'),
  #   executor.sv('stage3')})


  
  # current branching policy : rst -> stage1_go -> stage2_go -> stage3_go
  # current merging policy : on var stage0,1,2, wen_stage1,2
  
  # executor.set_input( 
  #   executor.convert( {'rst':0 } ), 
  #   [ \
  #       EqualsOrIff(sts.named_var['stage1_go'],BV(1,1))])
  #       #EqualsOrIff(sts.named_var['stage2_go'],BV(1,1)),
  #       #EqualsOrIff(sts.named_var['stage3_go'],BV(1,1))])
  # executor.sim_one_step()
  # executor.print_current_step()
  # executor.print_current_step_assumptions()
  # exit(1)


  # executor.set_input( 
  #   executor.convert( {'rst':0 } ), 
  #   [ \
  #       EqualsOrIff(sts.named_var['stage1_go'],BV(0,1)),
  #       EqualsOrIff(sts.named_var['stage2_go'],BV(1,1))])
  # executor.sim_one_step()


  # executor.set_input( 
  #   executor.convert( {'rst':0 } ), 
  #   [ \
  #       EqualsOrIff(sts.named_var['stage1_go'],BV(0,1)),
  #       EqualsOrIff(sts.named_var['stage2_go'],BV(1,1))])
  # executor.sim_one_step()

  # #executor.print_current_step()
  # #executor.print_current_step_assumptions()
  # state = executor.get_curr_state()
  # state.print_assumptions() 
  # print(tm.check_reachable(state))
  exit(1)
  
  # below are garbage
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  executor.print_current_step()
  executor.print_current_step_assumptions()
  state = executor.get_curr_state()
  concrete_enough = tm.check_concrete_enough(state, executor.get_Xs())
  print ('1.rst concrete enough',  concrete_enough)
  is_new_state = tm.record_state_w_asmpt(
    state,
    executor.get_Xs())
  assert(not is_new_state)

  executor.backtrack()
  executor.undo_set_input()

  executor.set_input( 
    executor.convert( {'rst':0 } ), 
    [
      EqualsOrIff(sts.named_var['stage1_go'],BV(0,1))
    ])
  executor.sim_one_step()
  executor.print_current_step()
  executor.print_current_step_assumptions()
  state = executor.get_curr_state()
  concrete_enough = tm.check_concrete_enough(state, executor.get_Xs())
  print ('1.rst0st1go concrete enough', concrete_enough) # False


  executor.backtrack()
  executor.undo_set_input()

  executor.set_input( 
    executor.convert( {'rst':0 } ), 
    [
      EqualsOrIff(sts.named_var['stage1_go'],BV(0,1)),
      EqualsOrIff(sts.named_var['stage2_go'],BV(0,1)),
      EqualsOrIff(sts.named_var['stage3_go'],BV(0,1))
    ])
  executor.sim_one_step()
  executor.print_current_step()
  executor.print_current_step_assumptions()
  state = executor.get_curr_state()
  concrete_enough = tm.check_concrete_enough(state, executor.get_Xs())
  
  if concrete_enough:
    snew = tm.concretize(state, Xs = executor.get_Xs())
    print ()
    print ('-----------OLD-------------')
    state.print()
    state.print_assumptions()
    print ('-----------NEW-------------')
    snew.print()
    snew.print_assumptions()
    print ('-----------END-------------')
    print ()
    state=snew

  print ('2. concrete enough',  concrete_enough)
  exit(1)
  is_new_state = tm.record_state_w_asmpt(
    state,
    executor.get_Xs())
  assert(not is_new_state)

if __name__ == '__main__':
	test_stall()


"""

  executor.backtrack()
  executor.undo_set_input()
  
  executor.set_input( 
    executor.convert( {'rst':0 } ), 
    [
      EqualsOrIff(sts.named_var['stage1_go'],BV(0,1)),
      EqualsOrIff(sts.named_var['stage2_go'],BV(0,1)),
      EqualsOrIff(sts.named_var['stage3_go'],BV(1,1))
    ])
  executor.sim_one_step()
  executor.print_current_step()
  executor.print_current_step_assumptions()
  state = executor.get_curr_state()
  concrete_enough = tm.check_concrete_enough(state, executor.get_Xs())

  if concrete_enough:
    snew = tm.concretize(state, Xs = executor.get_Xs())
    print ()
    print ('-----------OLD-------------')
    state.print()
    state.print_assumptions()
    print ('-----------NEW-------------')
    snew.print()
    snew.print_assumptions()
    print ('-----------END-------------')
    print ()
    state=snew

  print ('3. concrete enough',  concrete_enough)
  is_new_state = tm.record_state_w_asmpt(
    state,
    executor.get_Xs())
  assert(is_new_state)

"""
