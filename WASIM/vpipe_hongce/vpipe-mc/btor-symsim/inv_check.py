from pysmt.shortcuts import substitute, And, Not, Or, Implies, BVOne, BVZero, EqualsOrIff
from symtraverse import *
from state_simplify import state_simplify

def tobool(e):
    return EqualsOrIff(e,BVOne(1))

def is_valid(e):
    return (not is_sat(Not(e)))

def get_invalid_model(e):
    return (get_model(Not(e)))

def sort_model(m):
    mstr = str(m)
    return ('\n'.join(sorted(mstr.split('\n'))))
    
def del_dic_one(dic,string):
  for k, v in dic.items():
      if str(k) == string:
        dic.pop(k)
        break

def inv_check_one_step(flag):
  base_sv = {'wen_stage1', 'wen_stage2', 'stage1', 'stage2', 'stage3'}
  # name and width
  #oder1
  order = [ \
    TraverseBranchingNode(input_v=('rst', 1)),
    TraverseBranchingNode(signal_v=('stage1_go', 1)),
    TraverseBranchingNode(signal_v=('stage2_go', 1)),
    TraverseBranchingNode(signal_v=('stage3_go', 1))]

  # #oder2
  # order = [ \
  #   TraverseBranchingNode(input_v=('rst', 1)),
  #   TraverseBranchingNode(signal_v=('stage1_go', 1)),
  #   TraverseBranchingNode(signal_v=('stage3_go', 1)),
  #   TraverseBranchingNode(signal_v=('stage2_go', 1))]

  # # #oder3
  # order = [ \
  #   TraverseBranchingNode(input_v=('rst', 1)),
  #   TraverseBranchingNode(signal_v=('stage2_go', 1)),
  #   TraverseBranchingNode(signal_v=('stage1_go', 1)),
  #   TraverseBranchingNode(signal_v=('stage3_go', 1))]


  # #oder4
  # order = [ \
  #   TraverseBranchingNode(input_v=('rst', 1)),
  #   TraverseBranchingNode(signal_v=('stage2_go', 1)),
  #   TraverseBranchingNode(signal_v=('stage3_go', 1)),
  #   TraverseBranchingNode(signal_v=('stage1_go', 1))]

  # #oder5
  # order = [ \
  #   TraverseBranchingNode(input_v=('rst', 1)),
  #   TraverseBranchingNode(signal_v=('stage3_go', 1)),
  #   TraverseBranchingNode(signal_v=('stage1_go', 1)),
  #   TraverseBranchingNode(signal_v=('stage2_go', 1))]

  # #oder6
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
  executor.init(init_setting)


  
  
  if(flag=='tag0_0'):
    assumptions = [EqualsOrIff(executor.sv('stage1_go'),BV(0,1))]
    assump = EqualsOrIff(executor.sv('stage1_go'),BV(0,1))
  elif(flag=='tag0_1'):
    assumptions = [EqualsOrIff(executor.sv('stage1_go'),BV(1,1))]
  elif(flag=='tag1_1'):
    assumptions = [EqualsOrIff(executor.sv('stage1_go'),BV(0,1)),EqualsOrIff(executor.sv('stage2_go'),BV(0,1))]
  elif(flag=='tag1_2'):
    assumptions = [EqualsOrIff(executor.sv('stage2_go'),BV(1,1))]
  elif(flag=='tag2_2'):
    assumptions = [EqualsOrIff(executor.sv('stage2_go'),BV(0,1)),EqualsOrIff(executor.sv('stage3_go'),BV(0,1))]
  elif(flag=='tag2_3'):
    assumptions = [EqualsOrIff(executor.sv('stage3_go'),BV(1,1))]
  elif(flag=='tag3_3'):
    assumptions = [EqualsOrIff(executor.sv('stage3_go'),BV(0,1))]
  else:
    print ('<ERROR>: Wrong tag transition format!')
    assert False
  
  

  traverser = SymbolicTraverse(sts=sts, executor=executor, base_variable=[executor.sv(n) for n in base_sv])
  traverser.traverse(assumptions=assumptions, branching_point=order)

  print('l:',len(traverser.tracemgr.abs_state))
  for state in traverser.tracemgr.abs_state:
    state_simplify(state)
    state.print()
    state.print_assumptions()


  #init / trans
  #1:  sts.trans
  trans = sts.trans
  # init = sts.init
  print('inv-check !!!')
  # print('trans:',trans)

  var_to_nxt = {}
  for sv, var in init_setting.items():
    # print('sv',sv)
    # print('var',var)
    tp = BVType(var.bv_width())
    var_to_nxt[var] = Symbol(str(var)+"_next", tp)
    # print('var:', var)


  
  del_dic_one(var_to_nxt,'tag01')
  del_dic_one(var_to_nxt,'tag11')
  del_dic_one(var_to_nxt,'tag21')
  del_dic_one(var_to_nxt,'tag31')
  del_dic_one(var_to_nxt,'reg_v1')
  del_dic_one(var_to_nxt,'reg_v_comp1')
  # print('var_to_nxt:',var_to_nxt)


  expr_equal = []
  
  for var, var_nxt in var_to_nxt.items(): 
    expr_equal.append(EqualsOrIff(var_nxt, var))
    
  trans_nxt = And(expr_equal)
  
  trans_update = And(trans, trans_nxt)
  # print('trans_update:',trans_update)

  # 2.
  state_group=[]
  for state in traverser.tracemgr.abs_state:
    # print('new state!')
    # state.print()
    expr_equal2=[] 
    for state_var, expr in state.sv.items():
      expr_equal2.append(EqualsOrIff(state_var, expr))
    #### add assumptions
    asmpt_and = And(state.asmpt)
    print('asmpt:',asmpt_and)
    expr_and = And(expr_equal2)
    # state_group.append(And(expr_and,asmpt_and))
    state_group.append(expr_and)
    ####
  print('expr_equal2:',expr_equal2)
  print('state_group:',state_group)




  inv_new = Or(state_group)
  print('inv_new:',inv_new)
  # print('assump:',assump)


  inv_check = And(inv_new, assump, trans_update)
  
  # print('sts',sts.v2vprime)
  inv_new_prime = substitute(inv_new, sts.v2vprime)

  print('inv_new_prime:',inv_new_prime)

  # forall V, init(V) => inv(V)

  print (is_valid(Implies(inv_check, inv_new_prime)))
  cex = get_invalid_model(Implies(inv_check, inv_new_prime))
  

  print("counter example\n", sort_model(cex))

  # state_list = traverser.tracemgr.abs_state
  # valid = traverser.tracemgr.state_eq(state_list[0], state_list[1])
  # print('equal check:',valid)
  # state_list.pop()
  # print('state_list',state_list)


if __name__ == '__main__':
  flag='tag0_0'
  inv_check_one_step(flag)


