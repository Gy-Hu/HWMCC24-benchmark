import copy
from pysmt.shortcuts import FALSE, BVZExt
from symsim import Symbol, Not, And, Or, Implies, Ite, BVAdd, BV, EqualsOrIff, BVNot, BVSub, TRUE, is_sat, get_model
from symsim import BOOL, BVType
from symsim import SymbolicExecutor
from tracemgr import TraceManager
from pathlib import Path
from btorparser import BTOR2Parser
from sts import TransitionSystem, StateAsmpt
from typing import Tuple, Sequence, List
from state_simplify import state_simplify, state_simplify_one_step
from sygus_simplify import sygus_simplify


class TraverseBranchingNode(object):
  def __init__(self, input_v :Tuple[str,int] = None, signal_v :Tuple[str,int] = None):
    assert (input_v is None or signal_v is None)
    assert (not (input_v is None and signal_v is None))
    iv_tuple = input_v if input_v is not None else signal_v
    self.branch_on_inputvar = input_v is not None
    self.v_name = iv_tuple[0]
    self.v_width = iv_tuple[1]
    self.value = 0
  def next(self) -> bool:
    self.value += 1
    if self.value == 2**self.v_width:
      return False
    return True
  def getnode(self):
    iv_tuple=(self.v_name, self.v_width)
    if self.branch_on_inputvar:
      tmp = TraverseBranchingNode(input_v=iv_tuple)
    else:
      tmp = TraverseBranchingNode(signal_v=iv_tuple)
    return tmp
  def __repr__(self):
    return self.v_name + '==' + str(self.value)

class PerStateStack(object):
  def __init__(self, branching_point: Sequence[TraverseBranchingNode], simulator: SymbolicExecutor):
    self.stack: List[TraverseBranchingNode] = []
    self.ptr = 0 #what is ptr?
    self.branching_point = branching_point
    self.no_next_choice = False
    self.simulator = simulator
    #print('Sequence!!:',branching_point)
  def __repr__(self):
    return str(self.stack) + " ptr: " + str(self.ptr) + ('  (END)' if self.no_next_choice else '')

  def has_valid_choice(self):
    return not self.no_next_choice

  def get_iv_asmpt(self, assumptions):
    iv = {}
    asmpt = []
    for branch_node in self.stack:
      d = self.simulator.convert({branch_node.v_name: branch_node.value})
      if branch_node.branch_on_inputvar:
        iv.update(d)
      else:
        l = list(d.items())
        assert len(l) == 1
        asmpt.append( EqualsOrIff(l[0][0], l[0][1]) )  # variable == ...
    asmpt = asmpt + assumptions
    return iv, asmpt

  def next_choice(self):
    succ = False
    while not succ:
      if len(self.stack) == 0:
        self.no_next_choice = True
        return False
      succ = self.stack[-1].next()
      if not succ:
        self.ptr -= 1
        del self.stack[-1]
    return True

  def deeper_choice(self) -> bool:
    if self.ptr == len(self.branching_point):
      return False
    branch_node = self.branching_point[self.ptr]
    self.stack.append(branch_node.getnode())
    self.ptr += 1
    return True

  def check_stack(self):
    # print('curr_state_stack',self)
    # return True
    count = 0
    for node in self.stack:
      if(node.value == 1):
        count += 1

    if(count > 1):
      return False
    else:
      return True 

# lattice 


class SymbolicTraverse(object):
  def __init__(self, sts:TransitionSystem, executor:SymbolicExecutor, base_variable):
    self.sts = sts
    self.executor = executor
    self.tracemgr = TraceManager(sts)
    self.base_sv = base_variable
    self.s_concrete = {}
    self.new_state_list = []
    self.list_of_state_list = []
    self.parent_id_list = []
    
    self.tracemgr.record_base_var(base_variable)
  
  def traverse_one_step(self, assumptions, branching_point: Sequence[TraverseBranchingNode], tag_flag):
    # the current state should be reachable /\ concrete enough /\ a new state
    state = self.executor.get_curr_state(assumptions)
    reachable = self.tracemgr.check_reachable(state)  # also include the assumption on current step
    assert reachable
    concrete_enough = self.tracemgr.check_concrete_enough(state,  self.executor.get_Xs())
    assert concrete_enough
    is_new_state = self.tracemgr.record_state_w_asmpt(
      state,
      self.executor.get_Xs())
    assert is_new_state

    init_choice = PerStateStack(branching_point, self.executor)
    while init_choice.has_valid_choice():
      print(init_choice, end='')
      iv, asmpt = init_choice.get_iv_asmpt(assumptions) 
      self.executor.set_input(iv, asmpt)
      self.executor.sim_one_step()
      state = self.executor.get_curr_state() # this add assumptions on the state after the prev sim : no need
      reachable = self.tracemgr.check_reachable(state)
      # reachable = (self.tracemgr.check_reachable(state)) and (init_choice.check_stack())

      if not reachable:
        print(' not reachable.')
        init_choice.next_choice()
        self.executor.backtrack()
        self.executor.undo_set_input()
        continue


      concrete_enough = self.tracemgr.check_concrete_enough(state, self.executor.get_Xs())
      if not concrete_enough:
        print(' not concrete. Retry with deeper choice.')
        succ = init_choice.deeper_choice()
        if succ:  # incr input_concretize_ptr; backtrack and undo input
          self.executor.backtrack()
          self.executor.undo_set_input()
          continue
        # else: failed
        print ('<ERROR>: cannot reach a concrete state even if all choices are made. Future work.')
        assert False
      
      is_new_state = self.tracemgr.record_state_w_asmpt(
        state,
        self.executor.get_Xs())
      
      print ('New state!' if is_new_state else 'Already Exists ')

      for k,v in state.sv.items():
          if((str(k)==tag_flag)and(str(v)=='0_1')):
            pass
            # print('Not new tag state!')
          elif(str(k)==tag_flag):
            expr = state.sv[k]
            assumpt = state.asmpt
            assumpt_and = And(assumpt)
            expr_equal = EqualsOrIff(expr, BV(0,1))
            sat_check =  And(expr_equal, assumpt_and)
            sat_check_result = is_sat(sat_check)
            # print('sat_check_result:',sat_check_result)
            if(sat_check_result == False):
              # print('New tag state!')
              self.tracemgr.record_state_w_asmpt_one_step(state)
            else:
              pass
              # print ('Not new tag state!')

      init_choice.next_choice()
      self.executor.backtrack()
      self.executor.undo_set_input()
    print ('================================')
    print ('Finished!')
    print ('Get #state:', len(self.tracemgr.abs_state_one_step))
    for idx in range(len(self.tracemgr.abs_state_one_step)):
      abs_state_one_step = self.tracemgr.abs_state_one_step[idx]
      state_simplify(abs_state_one_step)
      sygus_simplify(abs_state_one_step)
      print ('--------------------------------')
      abs_state_one_step.print() 
      # abs_state_one_step.print_assumptions()
      print('\n')
    # return add_asmpt

  def traverse(self, assumptions, branching_point: Sequence[TraverseBranchingNode]):
    
    
    # the current state should be reachable /\ concrete enough /\ a new state
    state = self.executor.get_curr_state(assumptions)
    state.print()
    state.print_assumptions()
    reachable =  self.tracemgr.check_reachable(state) # also include the assumption on current step
    assert reachable
    concrete_enough = self.tracemgr.check_concrete_enough(state,  self.executor.get_Xs())
    assert concrete_enough
    is_new_state = self.tracemgr.record_state_w_asmpt(
      state,
      self.executor.get_Xs())
    assert is_new_state
    
    # extend state
    init_stack = PerStateStack(branching_point, self.executor)
    stack_per_state = [init_stack]  # List of PerStateStack
    print('init stack per state:',init_stack)
    print('init tracelen:', self.executor.tracelen())
    init_tracelen = self.executor.tracelen()-1 # --> len(stack) == 1
    

    # init state --> state_list[0]
    self.new_state_list.append(state)


    tree_branch_num = 0
    branch_end_flag = 0
    while stack_per_state: # while not empty
      
      state = self.executor.get_curr_state()

      current_state_stack = stack_per_state[-1]
      print ('Trace:', self.executor.tracelen()-init_tracelen, 'Stack:', len(stack_per_state))
      print('>> ', stack_per_state, end=' : ')
      # print('curr_state_stack:',current_state_stack)
      if not current_state_stack.has_valid_choice(): #backtrack-->previous state
        print (' no new choices, back to prev state')
        del stack_per_state[-1]
        if (stack_per_state):
          self.executor.backtrack()
          self.executor.undo_set_input()
          # parent_id = self.parent_id_list[-2]
          state_list_temp = copy.deepcopy(self.new_state_list)
          self.list_of_state_list.append(state_list_temp)
          tree_branch_num = tree_branch_num + 1
          del self.new_state_list[-1]
          branch_end_flag = 1
          # parent_id_cnt = parent_id_cnt - 1
        continue

      iv, asmpt = current_state_stack.get_iv_asmpt(assumptions)  # this add assumptions on the state before the sim
      self.executor.set_input(iv, asmpt)
      self.executor.sim_one_step()
      # state = self.executor.get_curr_state(assumptions) # this add assumptions on the state after the prev sim
      state = self.executor.get_curr_state()
      curr_state = state



      reachable = self.tracemgr.check_reachable(state)
      # reachable = (self.tracemgr.check_reachable(state)) and (current_state_stack.check_stack())

      if not reachable:
        print(' not reachable.')
        current_state_stack.next_choice()
        self.executor.backtrack()
        self.executor.undo_set_input()
        continue

      concrete_enough = self.tracemgr.check_concrete_enough(state, self.executor.get_Xs())
      if not concrete_enough:
        print(' not concrete. Retry with deeper choice.')
        succ = current_state_stack.deeper_choice()
        if succ:  # incr input_concretize_ptr; backtrack and undo input
          self.executor.backtrack()
          self.executor.undo_set_input()
          continue
        # else: failed
        print ('<ERROR>: cannot reach a concrete state even if all choices are made. Future work.')
        assert False

      if(branch_end_flag == 1):
        branch_end_flag = 0
        state_list = self.list_of_state_list[tree_branch_num-1]
      else:
        state_list = self.new_state_list


      is_new_state = self.tracemgr.record_state_w_asmpt3(
        state_list,
        state,
        self.executor.get_Xs())


      # record and check
      if is_new_state:
        print('A new state!')
        self.new_state_list.append(curr_state)

        # current_state_stack.next_choice()  # okay, the current choice has been explored
        stack_per_state.append(PerStateStack(branching_point, self.executor))
        # push stack - input_concretize_ptr
        # continue to extend on new state


      else:
        print(' not new state. Go back. Try next.')

        current_state_stack.next_choice()
        self.executor.backtrack()
        self.executor.undo_set_input()
        


    print ('================================')
    print ('Finished!')
    print ('Get #state:', len(self.tracemgr.abs_state))
    for idx in range(len(self.tracemgr.abs_state)):
      abs_state = self.tracemgr.abs_state[idx]
      state_simplify(abs_state)
      sygus_simplify(abs_state)

      # print ('--------------------------------')
      abs_state.print() 
      # abs_state.print_assumptions()
      # print('\n')
    
