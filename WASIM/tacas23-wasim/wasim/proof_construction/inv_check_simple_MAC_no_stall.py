from inv_group_new import *
from cex_parser import cex_parser, cex_parser_c1, cex_parser_c2
from copyreg import pickle
from pysmt.fnode import *
import pickle
import sys
sys.path.append('/home/tacas23/wasim')
sys.path.append('/home/tacas23/wasim/symsim_framework')
from symsim_framework.btorparser import *
from symsim_framework.symsim import *
import time



def main():
    start_time = time.perf_counter()
    file_name = "/home/tacas23/wasim/output/trace_simple_MAC_no_stall.pkl"
    open_file = open(file_name,"rb")
    branch_list = pickle.load(open_file)


    btor_parser = BTOR2Parser()
    sts, _ = btor_parser.parse_file(Path("/home/tacas23/wasim/design/simple_MAC_no_stall.btor2"))
    executor = SymbolicExecutor(sts)


    wen_stage1 = executor.sv('wen_stage1')
    wen_stage2 = executor.sv('wen_stage2')
    wen_stage3 = executor.sv('wen_stage3')
    reg_v = executor.sv('reg_v')
    reg_v_comp = executor.sv('reg_v_comp')
    stage1 = executor.sv('stage1')
    stage2 = executor.sv('stage2')
    stage3 = executor.sv('stage3')


    print(type(reg_v))
    print(type(reg_v_comp))
    print(type(stage3))

    

    init_setting = executor.convert({
        'wen_stage1':'v1',
        'wen_stage2':'v2',
        'stage1':'a',
        'stage2':'b',
        'stage3':'c'
        })

    


    ###############################################################################
    tag0, tag1, tag2, tag3 = tobool(executor.sv('tag0')), tobool(executor.sv('tag1')), tobool(executor.sv('tag2')), tobool(executor.sv('tag3'))
    rst = executor.sv('rst')

    

    #get free variable
    state_list_init =  branch_list[0]
    state_init = state_list_init[0]
    state_init.print()
    state_init.print_assumptions()
    asmpt_init = And(state_init.asmpt)
    state_expr_single = []
    for var,expr in state_init.sv.items():
        state_expr_single.append(EqualsOrIff(var, expr))
    state_expr = And(state_expr_single)
    free_var = get_free_variables(state_expr)

    # asmpt_test = asmpt_test.serialize()
    # free_var = get_free_variables(asmpt_init)
    print(free_var)
    print(type(free_var))

    for var in free_var:
        if(str(var) == 'v1'):
            v1 = var
        elif(str(var) == 'v2'):
            v2 = var
        elif(str(var) == 'a'):
            a = var
        elif(str(var) == 'b'):
            b = var
        elif(str(var) == 'c'):
            c = var
    
    if( (str(v1)!='v1') and (str(v2)!='v2')):
        assert False
    print(type(v1))
    print(type(a))
    print(v1)
    print(v2)




    #tag0
    inv_group0 = InvGroup(layer=0,tag=tag0,branch_list=branch_list)
    inv_group0.branch2state()
    state_list0 = inv_group0.get_state_list()
    inv_dedup0 = inv_group0.inv_deduplicate()
    inv_l0 = Or(inv_dedup0)

       
    #tag1
    inv_group1 = InvGroup(layer=1,tag=tag1,branch_list=branch_list)
    inv_group1.branch2state()
    inv_dedup1 = inv_group1.inv_deduplicate()
    inv_l1 = Or(inv_dedup1)
    #tag2
    inv_group2 = InvGroup(layer=2,tag=tag2,branch_list=branch_list)
    inv_group2.branch2state()
    inv_group2_l2 = inv_group2.get_inv_group()
    inv_dedup2 = inv_group2.inv_deduplicate()
    inv_l2 = Or(inv_dedup2)
    inv_l2_prop = inv_group2.extract_prop('stage3')
    #tag3
    inv_group3 = InvGroup(layer=3,tag=tag3,branch_list=branch_list)
    inv_group3.branch2state()
    inv_group3_l3 = inv_group3.get_inv_group()
    inv_dedup3 = inv_group3.inv_deduplicate()
    inv_l3 = Or(inv_dedup3)
    inv_l3_prop = inv_group3.extract_prop('stage3')


    ###inv check
    #1:  sts.trans
    trans = sts.trans
    assume  = sts.assumption 
    # trans = And(trans,assume,substitute(assume,sts.v2vprime))
    trans = And(trans,assume)
    print('inv-check !!!')
    var_to_nxt = {}
    for sv, var in init_setting.items():
        tp = BVType(var.bv_width())
        var_to_nxt[var] = Symbol(str(var)+"_next", tp)
    del_dic_one(var_to_nxt,'tag01')
    del_dic_one(var_to_nxt,'tag11')
    del_dic_one(var_to_nxt,'tag21')
    del_dic_one(var_to_nxt,'tag31')
    # del_dic_one(var_to_nxt,'reg_v1')
    # del_dic_one(var_to_nxt,'reg_v_comp1')
    
    expr_equal = []
    for var, var_nxt in var_to_nxt.items(): 
        expr_equal.append(EqualsOrIff(var_nxt, var))
    
    trans_nxt = And(expr_equal)
    trans_update = And(trans, trans_nxt)

    #additional assumptions
    asmpt_rst = And(EqualsOrIff(rst,BV(0,1)), EqualsOrIff(substitute(rst,sts.v2vprime),BV(0,1)))
    asmpt_tag = And(Not(And(tag0,tag1)), Not(And(tag0,tag2)), Not(And(tag0,tag3)), Not(And(tag1,tag2)), Not(And(tag1,tag3)), Not(And(tag2,tag3)))
    asmpt = And(asmpt_rst,asmpt_tag)
    # asmpt = asmpt_rst

    # 0.complete inv with properties
    prop1 = Implies(tag3, EqualsOrIff(reg_v_comp,reg_v*2+1))

    prop = EqualsOrIff(BV(1,1),BV(1,1))
    inv_addprop = []
    for addprop in inv_l2_prop:
        inv_addprop.append(Implies(tag3,EqualsOrIff(reg_v,addprop)))

    # prop = Implies(tag3,EqualsOrIff(reg_v_comp,stage3))

    #init inv check
    (check_result,cex,inv_prop) = inv_check_func_c1_2(inv_l0,inv_l1,inv_l2,inv_l3,inv_group2_l2, inv_group3_l3, trans_update, asmpt, sts, prop1,inv_addprop)


    print('-'*20)
    # 1.init check
    init = sts.init
    init_new = And([init, 
    EqualsOrIff(v1,wen_stage1), EqualsOrIff(v2,wen_stage2), EqualsOrIff(BV(1,1),wen_stage3),
    EqualsOrIff(a,stage1), EqualsOrIff(b,stage2), EqualsOrIff(c,stage3),
    EqualsOrIff(rst, BV(0,1)), EqualsOrIff(substitute(rst,sts.v2vprime), BV(0,1))
    ])

    print('\n\ninit:',init_new.serialize())
    ### forall V, init(V) => inv(V)
    init_check = Implies(init_new, inv_prop)
    print ('init_check:',is_valid(init_check))
    print('\n\n')


    # 2.inv check
    # print('inv:',inv_prop.serialize())
    ### forall V V', trans(V,V') /\ inv(V) => inv(V')
    inv_prop_prime = substitute(inv_prop, sts.v2vprime)
    inv_check_result = Implies(And(trans,inv_prop), inv_prop_prime)
    print ('inv_check:',is_valid(inv_check_result))
    # print ('inv_check:',check_result)
    # print('\n\n')


    # 3.property check
    assertion  = sts.assertion
    prop_check = Implies(And(inv_prop, And(state_init.asmpt)),assertion)
    print('\n\nproperty:',assertion.serialize())
    print ('prop_check:',is_valid(prop_check))
    print("counter example (prop check):\n", sort_model(get_invalid_model(prop_check)))

    end_time = time.perf_counter()
    print('Verification Time:%d(ms):  ' %int( round((end_time-start_time) * 1000) ))
    print('Verification Time:%d(s):  ' %round((end_time-start_time),2))
    


    



    

if __name__ == '__main__':
  main()