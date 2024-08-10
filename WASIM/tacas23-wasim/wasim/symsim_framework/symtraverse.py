import copy
from pysmt.shortcuts import FALSE, BVZExt, get_free_variables
from symsim import Symbol, Not, And, Or, Implies, Ite, BVAdd, BV, EqualsOrIff, BVNot, BVSub, TRUE, is_sat, get_model
from symsim import BOOL, BVType
from symsim import SymbolicExecutor
from tracemgr import TraceManager
from pathlib import Path
from btorparser import BTOR2Parser
from sts import TransitionSystem, StateAsmpt
from typing import Tuple, Sequence, List
from state_simplify import state_simplify_xvar
from sygus_simplify import sygus_simplify, expr_contains_X
import multiprocessing
from functools import partial

def simplify_process(state, xvar):
  """Perform two steps of simplification processes:
      1. state simplify
      2. sygus simplify
    
    Args:
        state: the state under simplification
        set_of_xvar: set of the X variables
    """
  state_simplify_xvar(state, xvar)
  sygus_simplify(state, xvar)

class SearchTreeNode(object):
  def __init__(self, current_state:StateAsmpt , child_state_nodes:List, parent_node):
    self.current_state = current_state
    self.child_state_nodes = child_state_nodes
    self.parent_node = parent_node

class TraverseBranchingNode(object):
  """Class of branch and nodes for symbolic traverse

  Attributes:
      branch_on_inputvar: whether the input varriables are assigned 
      v_name: name of the variable
      v_width: bitwidth of the variable
      value: value to record search
  """
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
  """Class of state stack for symbolic traverse search

  Attributes:
      stack: list of the TraverseBranchingNode class
      ptr: pointer to the stack
      branching_point: branch point for stack search
      no_next_choice: there is no other choice of the current stack
      simulator: symbolic simulator
  """
  def __init__(self, branching_point: Sequence[TraverseBranchingNode], simulator: SymbolicExecutor):
    self.stack: List[TraverseBranchingNode] = []
    self.ptr = 0 
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
  """Class to performa the symbolic traverse

  Attributes:
      sts: state transition system
      executor: symbolic simulator
      tracemgr: trace manager
      base_sv: the base variables selected to represent the new state
      new_state_list: list of a set of child states simulated from a parent state
      list_of_state_list: list of the state list from all parent states
  """
  def __init__(self, sts:TransitionSystem, executor:SymbolicExecutor, base_variable):
    self.sts = sts
    self.executor = executor
    self.tracemgr = TraceManager(sts)
    self.base_sv = base_variable
    # self.s_concrete = {}
    self.new_state_list = []
    self.list_of_state_list = []
    # self.parent_id_list = []
    
    self.tracemgr.record_base_var(base_variable)
  
  def traverse_one_step(self, assumptions, branching_point: Sequence[TraverseBranchingNode], s_init = []):
    """Perform symbolic traverse for one clock cycle (without stall) and collect new states"""
    # the current state should be reachable /\ concrete enough /\ a new state
    state = self.executor.get_curr_state(assumptions)
    state_init = copy.copy(state)
    reachable = self.tracemgr.check_reachable(state)  # also include the assumption on current step
    if(not reachable):
    
      self.tracemgr.abs_state_one_step.append(s_init)
      # self.tracemgr.abs_state.append(state)
      assert len(self.tracemgr.abs_state_one_step) == 1
      print('not reachable! skip!')
      print ('================================')
      print ('Finished!')
      print ('Get #state:', len(self.tracemgr.abs_state_one_step))

      abs_state = self.tracemgr.abs_state_one_step[0]
      state_simplify_xvar(abs_state, self.executor.get_Xs())
      sygus_simplify(abs_state, self.executor.get_Xs())
      # state_init.print()
      # s_init.print()
      input()
      return 0
    # assert reachable
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
      state = self.executor.get_curr_state()  # this add assumptions on the state after the prev sim : no need
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
        state = self.executor.get_curr_state()
        state.print()
        assert False
      
      is_new_state = self.tracemgr.record_state_w_asmpt(
        state,
        self.executor.get_Xs())
      
      print ('New state!' if is_new_state else 'Already Exists ')
      if is_new_state:
        self.tracemgr.record_state_w_asmpt_one_step(state)

      init_choice.next_choice()
      self.executor.backtrack()
      self.executor.undo_set_input()
    print ('================================')
    print ('Finished!')
    print ('Get #state:', len(self.tracemgr.abs_state_one_step))

    for idx in range(len(self.tracemgr.abs_state_one_step)):
      abs_state_one_step = self.tracemgr.abs_state_one_step[idx]
      state_simplify_xvar(abs_state_one_step, self.executor.get_Xs())
      sygus_simplify(abs_state_one_step, self.executor.get_Xs())


  def traverse_all_states(self, assumptions, branching_fun, abs_fun, ref_fun):
    """Perform symbolic traverse with pluggable abstraction refinment fuction interface"""
    # ADD one layer of abstraction!
    # TODO: let's complete this and the example in abs_ref.py
    state = self.executor.get_curr_state(assumptions)
    state_init = abs_fun(state)
    reachable = self.tracemgr.check_reachable(state)
    if not reachable:
      return []
    search_tree_root = SearchTreeNode(current_state=state_init, child_state_nodes=[], parent_node=None)
    queue = [search_tree_root]
    all_states = []
    while len(queue) != 0:
      node_to_explore = queue[-1]
      del queue[-1]
      self.executor.set_current_state(node_to_explore.current_state, {})
      branching_fun.set_way_point(search_tree_root, queue, node_to_explore)
      all_states.append(node_to_explore.current_state)
      while branching_fun.has_valid_choice():
        iv, asmpt = branching_fun.get_inputvar_asmpt(assumptions) # TODO
        self.executor.set_input(iv, asmpt)
        self.executor.sim_one_step()

        state = self.executor.get_curr_state()
        if not self.tracemgr.check_reachable(state):
            continue
        
        abs_state = abs_fun(state)
        reachable = self.tracemgr.check_reachable(abs_state)
        
        if abs_fun.abs_eq(abs_state, node_to_explore.current_state):
          continue

        ancestor = node_to_explore.parent_node
        found_same_state = False
        while ancestor is not None:
          if abs_fun.abs_eq(ancestor.current_state, abs_state):
            found_same_state = True
            break
          ancestor = ancestor.parent_node
        if found_same_state:
          continue  # if it is not a new state, then we don't need to further explore

        if ref_fun.needs_refinement(abs_state):
          abs_state = ref_fun(node_to_explore, abs_state, iv, asmpt)
        
        # now add the new state to the queue
        
        new_child_node = SearchTreeNode(current_state=abs_state, child_state_nodes=[], parent_node=node_to_explore)
        node_to_explore.child_state_nodes.append(new_child_node)
        queue.append(new_child_node)
        all_states.append(abs_state)
    
    return all_states


  def traverse(self, assumptions, branching_point: Sequence[TraverseBranchingNode], s_init = []):
    """Perform symbolic traverse for stall situation and collect new states"""
    # the current state should be reachable /\ concrete enough /\ a new state
    state = self.executor.get_curr_state(assumptions)
    state_init = copy.copy((self.tracemgr.abstract(state)))
    # state.print()
    # state.print_assumptions()
    reachable = self.tracemgr.check_reachable(state) # also include the assumption on current step
    if(not reachable):

      self.tracemgr.abs_state.append(s_init)
      # self.tracemgr.abs_state.append(state)
      assert len(self.tracemgr.abs_state) == 1
      print('not reachable! skip!')
      print ('================================')
      print ('Finished!')
      print ('Get #state:', len(self.tracemgr.abs_state))

      abs_state = self.tracemgr.abs_state[0]
      state_simplify_xvar(abs_state, self.executor.get_Xs())
      sygus_simplify(abs_state, self.executor.get_Xs())
      # state_init.print()
      # s_init.print()
      # input()
      return 0
    # assert reachable
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
        state = self.executor.get_curr_state()
        state.print()
        for s,v in state.sv.items():
          if expr_contains_X(v, self.executor.get_Xs()):  #  ('X' in str(v.serialize()))
            print(v.serialize())
            # input()
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
        self.executor.get_Xs())  # check if `state` in `state_list`


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
      state_simplify_xvar(abs_state, self.executor.get_Xs())
      sygus_simplify(abs_state, self.executor.get_Xs())

