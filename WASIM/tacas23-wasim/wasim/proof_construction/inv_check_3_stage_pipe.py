from inv_group_new import *
from cex_parser import cex_parser, cex_parser_c2
from copyreg import pickle
from pysmt.fnode import *
import pickle
import sys
sys.path.append('/home/tacas23/wasim')
sys.path.append('/home/tacas23/wasim/symsim_framework')
from symsim_framework.btorparser import *
from symsim_framework.symsim import *
import time



def arg_check(formula, state_asmpt:dict):
    f_d1 = formula.args()
    for f_arg in f_d1:
        f_d2 = f_arg.args()
        if(len(f_d2) == 0):
            continue
        elif(f_arg.is_bv_comp()):
            state_asmpt[f_d2[0]] = f_d2[1]
        else:
            arg_check(f_arg, state_asmpt)


def ila_trans():
    btor_parser = BTOR2Parser()
    sts, _ = btor_parser.parse_file(Path("/home/tacas23/wasim/design/3_stage_pipe_inst.btor2"))
    executor = SymbolicExecutor(sts)
    init_dict = {
        'ILA_r0' : 'x0',
        'ILA_r1' : 'x1',
        'ILA_r2' : 'x2',
        'ILA_r3' : 'x3',
        '__auxvar0__recorder' : 'aux0',
        '__auxvar1__recorder' : 'aux1',
        '__auxvar2__recorder' : 'aux2',
        '__auxvar3__recorder' : 'aux3',
        '__START__': 1
    }
    input_dict = {'__ILA_I_inst':'ila_inst', 'rst':0}

    init_setting = executor.convert(init_dict)
    input_dict   = executor.convert(input_dict)

    executor.init(init_setting)

    # print (pre.asmpt[1].serialize())
    executor.set_input(input_dict,[])
    executor.sim_one_step()
    state = executor.get_curr_state()
    extract_list = ['x0','x1','x2','x3','aux0','aux1','aux2','aux3']
    extracted_list = [None] * len(extract_list)
    sv_extract_list = ['ILA_r0','ILA_r1','ILA_r2','ILA_r3']
    sv_extracted_list = [None] * len(sv_extract_list)

    for sv,expr in init_setting.items():
        for idx,sn in enumerate(extract_list):
            if str(expr) == sn:
                extracted_list[idx] = expr

    for sv,expr in state.sv.items():
        for idx,sn in enumerate(sv_extract_list):
            if str(sv) == sn:
                sv_extracted_list[idx] = expr


    return extracted_list, sv_extracted_list


def main(extracted_list, sv_extracted_list):
    start_time = time.perf_counter()
    file_name = "/home/tacas23/wasim/output/trace_3_stage_pipe_inst.pkl"
    open_file = open(file_name,"rb")
    branch_list = pickle.load(open_file)
    num_layer = 5




    btor_parser = BTOR2Parser()
    sts, _ = btor_parser.parse_file(Path("/home/tacas23/wasim/design/3_stage_pipe_inst.btor2"))
    executor = SymbolicExecutor(sts)

    init_dict = {
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
      }


    ila_init_dict = {
        'ILA_r0' : 'x0',
        'ILA_r1' : 'x1',
        'ILA_r2' : 'x2',
        'ILA_r3' : 'x3',
        '__auxvar0__recorder' : 'aux0',
        '__auxvar1__recorder' : 'aux1',
        '__auxvar2__recorder' : 'aux2',
        '__auxvar3__recorder' : 'aux3' }

    init_setting = executor.convert(init_dict)
    ila_init_dict = executor.convert(ila_init_dict)

    tag_start = tobool(executor.sv('__START__'))
    tag_ex = tobool(executor.sv('ppl_stage_ex'))
    tag_wb = tobool(executor.sv('ppl_stage_wb'))
    tag_finish = tobool(executor.sv('ppl_stage_finish'))
    started = tobool(executor.sv('__STARTED__'))
    startn = EqualsOrIff(executor.sv('__START__'), BV(0,1))
    startedn = EqualsOrIff(executor.sv('__STARTED__'), BV(0,1))
    ended = tobool(executor.sv('__ENDED__'))
    ended2 = tobool(executor.sv('__2ndENDED__'))
    rst = executor.sv('rst')
    dummy_reset = executor.sv('dummy_reset')
    reseted =  executor.sv('__RESETED__')
    ILA_r0, ILA_r1, ILA_r2, ILA_r3 = executor.sv('ILA_r0'),  executor.sv('ILA_r1'), executor.sv('ILA_r2'), executor.sv('ILA_r3')
    tag_ila = [ILA_r0, ILA_r1, ILA_r2, ILA_r3]
    aux0, aux1, aux2, aux3 = executor.sv('__auxvar0__recorder'), executor.sv('__auxvar1__recorder'), executor.sv('__auxvar2__recorder'), executor.sv('__auxvar3__recorder')
    tag_aux = [aux0, aux1, aux2, aux3]
    aux0_cm, aux1_cm, aux2_cm, aux3_cm = executor.sv('__auxvar0__recorder_sn_condmet'), executor.sv('__auxvar1__recorder_sn_condmet'), executor.sv('__auxvar2__recorder_sn_condmet'), executor.sv('__auxvar3__recorder_sn_condmet')
    id_go = executor.sv('RTL_id_go')

    state_list_init =  branch_list[0]
    state_init = state_list_init[0]
    state_init.print()
    state_init.print_assumptions()
    state_asmpt_init = And(state_init.asmpt)
    asmpt_init = state_init.asmpt[1]
    
    state_expr_single = []
    for var,expr in state_init.sv.items():
        state_expr_single.append(EqualsOrIff(var, expr))
    state_expr = And(And(state_expr_single), state_asmpt_init)
    free_var = get_free_variables(state_expr)

    for var in free_var:
        if(str(var) == 'v1'):
            v1 = var
        elif(str(var) == 'v2'):
            v2 = var
    
    
    #layer0 -- init (start)
    inv_group0 = InvGroup(layer=0,tag=tag_start,branch_list=branch_list)
    inv_group0.branch2state()
    inv_list0 = inv_group0.get_inv_group()
    inv_l0 = Or(inv_list0)

    #layer1 -- start-ex
    inv_group1 = InvGroup(layer=1,tag=tag_ex,branch_list=branch_list)
    inv_group1.branch2state()
    inv_list1 = inv_group1.get_inv_group()
    # inv_list1 = inv_group1.inv_with_ila(ila_prime_list)
    inv_l1 = Or(inv_list1)

    #layer2 -- ex-ex
    inv_group2 = InvGroup(layer=2,tag=tag_ex,branch_list=branch_list)
    inv_group2.branch2state()
    inv_list2 = inv_group2.get_inv_group()
    # inv_list1 = inv_group1.inv_with_ila(ila_prime_list)
    inv_l2 = Or(inv_list2)

    #layer3 -- ex-wb
    inv_group3 = InvGroup(layer=3,tag=tag_wb,branch_list=branch_list)
    inv_group3.branch2state()
    inv_list3 = inv_group3.get_inv_group()
    # inv_list2 = inv_group2.inv_with_ila(ila_prime_list)
    inv_l3 = Or(inv_list3)

     #layer4 -- wb-wb
    inv_group4 = InvGroup(layer=4,tag=tag_wb,branch_list=branch_list)
    inv_group4.branch2state()
    inv_list4 = inv_group4.get_inv_group()
    # inv_list2 = inv_group2.inv_with_ila(ila_prime_list)
    inv_l4 = Or(inv_list4)

    #layer5 -- wb-finish
    inv_group5 = InvGroup(layer=5,tag=tag_finish,branch_list=branch_list)
    inv_group5.branch2state()
    inv_list5 = inv_group5.get_inv_group()
    # inv_list3 = inv_group3.inv_with_ila(ila_prime_list)
    inv_l5 = Or(inv_list5)
    


    ### inv check
    #1:  sts.trans
    sts_init = sts.init
    trans = sts.trans
    sts_assume  = sts.assumption
    sts_assertion = sts.assertion
    trans_with_asumpt = And(trans, sts_assume, substitute(sts_assume, sts.v2vprime))

    print('\n\n',substitute(sts_assume,sts.v2vprime).serialize())



    print('inv-check !!!')
    var_to_nxt = { symbolic_val: Symbol(str(symbolic_val)+"_next", \
                                        BVType(symbolic_val.bv_width())) \
                  for sv, symbolic_val in init_setting.items()}  # for example, {a : a_next, b : b_next , ...}

    init_symbolic_var_result = And([EqualsOrIff(sv, symbolic_val) for sv, symbolic_val in init_setting.items()])
    init_symbolic_var_ila = And([EqualsOrIff(sv, symbolic_val) for sv, symbolic_val in ila_init_dict.items()])
    sts_init_extended = And(sts_init, init_symbolic_var_result, init_symbolic_var_ila)

    trans_symbolic_var_not_changing = \
        [EqualsOrIff(var_nxt, symbolic_val) \
          for symbolic_val, var_nxt in var_to_nxt.items()] # for example, [a_next := a, b_next := b, ...]

    trans_update = And(trans_with_asumpt, And(trans_symbolic_var_not_changing))

    ### additional assumptions
    asmpt_rst = And(EqualsOrIff(rst,BV(0,1)), EqualsOrIff(dummy_reset,BV(0,1)), EqualsOrIff(reseted,BV(1,1)))
 
    one_hot_element = [tag_start, tag_ex, tag_wb, tag_finish]
    ll = len(one_hot_element)
    one_hot_list = []
    for i in range(0,ll):
      for j in range(i+1, ll):
        one_hot_list.append(Not(And(one_hot_element[i], one_hot_element[j])))


    asmpt_tag = And(
        And(one_hot_list), Not(And(tag_start, started)), Not(And(tag_ex, ended)), Not(And(tag_ex, ended2)), Not(And(tag_wb, ended)),
        Implies(tag_ex, started), Implies(tag_wb, started), Implies(tag_finish, started), Implies(ended, started), Implies(ended2, started))

    

    free_var_test = get_free_variables(asmpt_init)
    for var in free_var_test:
        if(str(var) == '__RESETED__1'):
            reseted1 = var
        elif(str(var) == '__START__1'):
            start1 = var
        elif(str(var) == 'ppl_stage_wb1'):
            ppl_stage_wb1 = var
        elif(str(var) == 'dummy_resetX1'):
            dummy_resetX1 = var
    print(asmpt_init.serialize())

    tag_cons = And(EqualsOrIff(reseted1,BV(1,1)), EqualsOrIff(start1,BV(1,1)), EqualsOrIff(ppl_stage_wb1,BV(0,1)), EqualsOrIff(dummy_resetX1,BV(0,1)))
    asmpt_init = And(tag_cons,asmpt_init)

    aux_and = And(EqualsOrIff(aux0_cm, BV(0,1)), EqualsOrIff(aux1_cm, BV(0,1)), EqualsOrIff(aux2_cm, BV(0,1)), EqualsOrIff(aux3_cm, BV(0,1)))
    aux_and_one = And(EqualsOrIff(aux0_cm, BV(1,1)), EqualsOrIff(aux1_cm, BV(1,1)), EqualsOrIff(aux2_cm, BV(1,1)), EqualsOrIff(aux3_cm, BV(1,1)))
    asmpt_aux = And(Implies(tag_start, aux_and), Implies(tag_ex, aux_and), Implies(tag_wb, aux_and),Implies(tag_finish, aux_and_one))
    asmpt_aux_eq = make_pair_eq(extracted_list[0:4], extracted_list[4:8])


    asmpt_start_cond = Implies(tag_start, And([EqualsOrIff(sv, symbolic_val) for sv, symbolic_val in init_setting.items()]))

    

    asmpt = And(asmpt_start_cond, asmpt_rst, asmpt_tag, asmpt_init, asmpt_aux, asmpt_aux_eq)


    
    ila_var_list = [ILA_r0, ILA_r1, ILA_r2, ILA_r3]
    aux_var_list = [aux0, aux1, aux2, aux3]

    all_pairs,_ = extract_pair_of_regval_from_branch_list(branch_list, num_layer-1, num_layer)

    finish_or_list = []
    for pair_no in range(len(all_pairs)):
        pair0 = all_pairs[pair_no]
        pair0_pre = pair0[0]
        pair0_post = pair0[1]
        finish2sv = And([make_pair_eq(ila_var_list, pair0_post), make_pair_eq(aux_var_list, pair0_pre)])
        finish_or_list.append(finish2sv)

    assert len(inv_group5.state_list) == len(finish_or_list)
    inv_finish_ila_rtl= Implies(tag_finish, \
                        Or( \
                            [And(inv_group5.state_list[idx],finish_or_list[idx]) \
                             for idx in range(len(finish_or_list))]))

    ila_start =  Implies(tag_start , And(make_pair_eq(ila_var_list,  extracted_list[0:4]), make_pair_eq(aux_var_list, extracted_list[4:8]))) #

    id_ex_wb = And([make_pair_eq(ila_var_list,  sv_extracted_list), make_pair_eq(aux_var_list, extracted_list[4:8])])
    # ila_id = Implies(tag_id , id_ex_wb)
    ila_ex = Implies(tag_ex , id_ex_wb)
    ila_wb = Implies(tag_wb , id_ex_wb)

    inv_start = inv_l0
    inv_ex = Or(inv_l1, inv_l2)
    inv_wb = Or(inv_l3, inv_l4)
    inv_ila_rtl = And(inv_start, inv_ex, inv_wb, inv_finish_ila_rtl, ila_start, ila_ex, ila_wb)

    (check_result_init, cex_init) = init_check_generic_func(inv_ila_rtl, sts_init_extended, asmpt)
    (check_result, cex) = inv_check_generic_func(inv_ila_rtl, trans_update, asmpt, sts)
    property_check_generic_func(inv_ila_rtl, sts_assertion, asmpt)



    
    # i = 0
    
    tag_record_list = []
    unsat_expr_list = []
    # while(i!=0):
    #     i = i-1
    while(check_result == False):
        i = i+1
        (v_cons,n_tag0,n_tag1,n_tag2,n_tag3) = cex_parser_c2(cex)

        ce_constr_v = []
        v1_cons_0 = EqualsOrIff(v1,BV(0,1))
        v1_cons_1 = EqualsOrIff(v1,BV(1,1))
        v2_cons_0 = EqualsOrIff(v2,BV(0,1))
        v2_cons_1 = EqualsOrIff(v2,BV(1,1))

        if(v_cons == 0):
            ce_constr_v = [v1_cons_0,v2_cons_0]
        elif(v_cons == 1):
            ce_constr_v = [v1_cons_0,v2_cons_1]
        elif(v_cons == 2):
            ce_constr_v = [v1_cons_1,v2_cons_0]
        elif(v_cons == 3):
            ce_constr_v = [v1_cons_1,v2_cons_1]
        print(ce_constr_v)


        ### inv update
        cex_expr = And(ce_constr_v)
        unsat_expr = Not(cex_expr)
        unsat_expr_list.append(unsat_expr)
        if(n_tag0 == 1):
            print('start:',n_tag0)
            truelist = test_ce(inv_list0, cex)
            truelist = inv_group0.check_unsat_expr(truelist, cex_expr)   
            tag_record_list.append('start')
        elif(n_tag1 == 1):
            print('ppl_stage_ex:',n_tag1)
            list_1 = test_ce(inv_list1, cex)
            list_1 = inv_group1.check_unsat_expr(list_1, cex_expr)   
            list_2 = test_ce(inv_list2, cex)
            list_2 = inv_group2.check_unsat_expr(list_2, cex_expr)   
            truelist = list_1 + list_2
            tag_record_list.append('ppl_stage_ex')
        elif(n_tag2 == 1):
            print('ppl_stage_wb:',n_tag2)
            list_1 = test_ce(inv_list3, cex)
            list_1 = inv_group3.check_unsat_expr(list_1, cex_expr)   
            list_2 = test_ce(inv_list4, cex)
            list_2 = inv_group4.check_unsat_expr(list_2, cex_expr)   
            truelist = list_1 + list_2
            tag_record_list.append('ppl_stage_wb')
        elif(n_tag3 == 1):
            print('ppl_stage_finish:',n_tag3)
            truelist = test_ce(inv_list5, cex)
            truelist = inv_group5.check_unsat_expr(truelist, cex_expr)               
            tag_record_list.append('ppl_stage_finish')
        
        for idx in truelist:
                inv_list0 = inv_group0.add_unsat_asmpt(unsat_expr, idx)
                inv_list1 = inv_group1.add_unsat_asmpt(unsat_expr, idx)
                inv_list2 = inv_group2.add_unsat_asmpt(unsat_expr, idx)
                inv_list3 = inv_group3.add_unsat_asmpt(unsat_expr, idx)
                inv_list4 = inv_group4.add_unsat_asmpt(unsat_expr, idx)
                inv_list5 = inv_group5.add_unsat_asmpt(unsat_expr, idx)
        inv_l0 = Or(inv_list0)
        inv_l1 = Or(inv_list1)
        inv_l2 = Or(inv_list2)
        inv_l3 = Or(inv_list3)
        inv_l4 = Or(inv_list4)
        inv_l5 = Or(inv_list5)

        for idx in truelist:
            finish_or_list = add_unsat_asmpt_to_ila(finish_or_list, unsat_expr, idx)


        assert len(inv_group5.state_list) == len(finish_or_list)
        inv_finish_ila_rtl= Implies(tag_finish, \
                            Or( \
                                [And(inv_group5.state_list[idx],finish_or_list[idx]) \
                                for idx in range(len(finish_or_list))]))


        inv_start = inv_l0
        inv_ex = Or(inv_l1, inv_l2)
        inv_wb = Or(inv_l3, inv_l4)
        inv_ila_rtl = And(inv_start, inv_ex, inv_wb, inv_finish_ila_rtl, ila_start, ila_ex, ila_wb)

        (check_result, cex) = inv_check_generic_func(inv_ila_rtl, trans_update, asmpt, sts)


    print('num of iteration:',i)
    print('tag record list',tag_record_list)

    print('\n\n\n')
    print('-'*15, 'CHECK RESULT', '-'*15)
    asmpt_unsat =  And(unsat_expr_list)
    init_check_generic_func(inv_ila_rtl, sts_init_extended, And(asmpt, asmpt_unsat))
    inv_check_generic_func(inv_ila_rtl, trans_update, asmpt, sts)
    property_check_generic_func(inv_ila_rtl, sts_assertion, asmpt)

    end_time = time.perf_counter()
    print('Verification Time:%d(ms):  ' %int( round((end_time-start_time) * 1000) ))
    print('Verification Time:%d(s):  ' %round((end_time-start_time),2))
    


if __name__ == '__main__':
  extracted_list, sv_extracted_list = ila_trans()
  main(extracted_list, sv_extracted_list)


