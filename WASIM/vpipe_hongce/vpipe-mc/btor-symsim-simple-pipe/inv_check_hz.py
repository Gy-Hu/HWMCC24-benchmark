from ast import Eq
from lib2to3.pgen2.token import RPAR
from operator import le
from time import pthread_getcpuclockid
from inv_group_new import *
from cex_parser import cex_parser
from pysmt.rewritings import conjunctive_partition
from parse_asmpt import *

def ila_trans():
    btor_parser = BTOR2Parser()
    sts, _ = btor_parser.parse_file(Path("/data/wenjifang/vpipe-mc/ILA-pipeline/ilang_simple_pipe/stall_short_vrecorder/verify/ADD/problem.btor2"))
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
    pre = executor.get_curr_state()

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
    file_name = "/data/wenjifang/vpipe-mc/btor-symsim-simple-pipe/branch_list_with_rst2.pkl"
    open_file = open(file_name,"rb")
    branch_list = pickle.load(open_file)


    btor_parser = BTOR2Parser()
    sts, _ = btor_parser.parse_file(Path("/data/wenjifang/vpipe-mc/ILA-pipeline/ilang_simple_pipe/stall_short_vrecorder/verify/ADD/problem.btor2"))
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
      '__ILA_I_inst':'ila_inst'
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

    for sv, val in init_setting.items():
       if str(val) == 'v1':
           v1 = val
       elif str(val) == 'v2':
           v2 = val

    start, ppl_stage_ex, ppl_stage_wb, ppl_stage_finish = tobool(executor.sv('__START__')), tobool(executor.sv('ppl_stage_ex')), tobool(executor.sv('ppl_stage_wb')), tobool(executor.sv('ppl_stage_finish'))
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
    

    #get free variable
    state_list_init =  branch_list[0]
    state_init = state_list_init[0]
    state_init.print()
    state_init.print_assumptions()
    state_asmpt_init = And(state_init.asmpt)
    asmpt_init = state_init.asmpt[1] # HZ: this is the assumption on symbolic values
    

    a0 = EqualsOrIff(v1, BV(0,1))
    a1 = And(EqualsOrIff(v1, BV(0,1)), EqualsOrIff(v2, BV(1,1)))
    a2 = And(EqualsOrIff(v1, BV(0,1)), EqualsOrIff(v2, BV(1,1)))
    a3 = EqualsOrIff(v1, BV(1,1))
    a4 = EqualsOrIff(v1, BV(1,1))
    all_asmpt_simplified = [a0,a1,a2,a3,a4]


    #layer0 -- init (start)
    inv_group0 = InvGroup(layer=0,tag=start,branch_list=branch_list)
    inv_group0.branch2state([])
    inv_start = Or(inv_group0.inv_group)

    #layer1 -- start-ex
    inv_group1 = InvGroup(layer=1,tag=ppl_stage_ex,branch_list=branch_list)
    inv_group1.branch2state(all_asmpt_simplified)
    inv_start2ex = Or(inv_group1.inv_group)

    #layer2 -- ex-ex
    inv_group2 = InvGroup(layer=2,tag=ppl_stage_ex,branch_list=branch_list)
    inv_group2.branch2state(all_asmpt_simplified)
    inv_ex2ex = Or(inv_group2.inv_group)

    #layer3 -- ex-wb
    inv_group3 = InvGroup(layer=3,tag=ppl_stage_wb,branch_list=branch_list)
    inv_group3.branch2state(all_asmpt_simplified)
    inv_ex2wb = Or(inv_group3.inv_group)
    
    #layer4 -- wb-wb
    inv_group4 = InvGroup(layer=4,tag=ppl_stage_wb,branch_list=branch_list)
    inv_group4.branch2state(all_asmpt_simplified)
    inv_wb2wb = Or(inv_group4.inv_group)

    #layer5 -- wb-finish
    inv_group5 = InvGroup(layer=5,tag=ppl_stage_finish,branch_list=branch_list)
    inv_group5.branch2state(all_asmpt_simplified)
    inv_wb2finish = Or(inv_group5.inv_group)

    inv_ex = Or(inv_start2ex, inv_ex2ex)
    inv_wb = Or(inv_ex2wb, inv_wb2wb)

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
    # HZ: assumption: start |-> init_setting_left == init_setting_right
    asmpt_start_cond = Implies(start, And([EqualsOrIff(sv, symbolic_val) for sv, symbolic_val in init_setting.items()]))

    asmpt_no_rst = And(EqualsOrIff(rst,BV(0,1)), EqualsOrIff(dummy_reset,BV(0,1)), EqualsOrIff(reseted,BV(1,1)))
 
    one_hot_element = [start,ppl_stage_ex,ppl_stage_wb,ppl_stage_finish]
    ll = len(one_hot_element)
    one_hot_list = []
    for i in range(0,ll):
      for j in range(i+1, ll):
        one_hot_list.append(Not(And(one_hot_element[i], one_hot_element[j])))


    asmpt_tag = And(
        And(one_hot_list), Not(And(start, started)), Or(start,started),
        Not(And(ppl_stage_ex, ended)), Not(And(ppl_stage_ex, ended2)), Not(And(ppl_stage_wb, ended)),
        Implies(ppl_stage_ex, started), Implies(ppl_stage_wb, started), Implies(ppl_stage_finish, started), Implies(ended, started), Implies(ended2, started))

    

    free_var_test = get_free_variables(asmpt_init) # HZ: this is the assumption on symbolic values
    for var in free_var_test:
        if str(var) == '__RESETED__1':
            reseted1 = var
        elif str(var) == '__START__1':
            start1 = var
        elif str(var) == 'ppl_stage_wb1':
            ppl_stage_wb1 = var
        elif str(var) == 'dummy_resetX1':
            dummy_resetX1 = var
    tag_cons = And(EqualsOrIff(reseted1,BV(1,1)), EqualsOrIff(start1,BV(1,1)), EqualsOrIff(ppl_stage_wb1,BV(0,1)), EqualsOrIff(dummy_resetX1,BV(0,1)))
    asmpt_init = And(tag_cons, asmpt_init)

    aux_and = And(EqualsOrIff(aux0_cm, BV(0,1)), EqualsOrIff(aux1_cm, BV(0,1)), EqualsOrIff(aux2_cm, BV(0,1)), EqualsOrIff(aux3_cm, BV(0,1)))
    aux_and_one = And(EqualsOrIff(aux0_cm, BV(1,1)), EqualsOrIff(aux1_cm, BV(1,1)), EqualsOrIff(aux2_cm, BV(1,1)), EqualsOrIff(aux3_cm, BV(1,1)))
    asmpt_aux = And(Implies(start, aux_and), Implies(ppl_stage_ex, aux_and), Implies(ppl_stage_wb, aux_and), Implies(ppl_stage_finish, aux_and_one))
    asmpt_aux_eq = make_pair_eq(extracted_list[0:4], extracted_list[4:8])
    # asmpt_aux = aux_and
    
    # asmpt = And(asmpt_rst, asmpt_tag)
    asmpt = And(asmpt_start_cond, asmpt_no_rst, asmpt_tag, asmpt_init, asmpt_aux, asmpt_aux_eq)
    # asmpt = And(asmpt_rst, asmpt_tag, asmpt_init, asmpt_aux)

    # -------------------------------------------------
    # TEST rtl inv w. assumptions

    # inv_rtl = And([inv_start, inv_ex,  inv_wb, inv_wb2finish])
    # cex = inv_check_generic_func(inv_rtl, trans_update, asmpt, sts)
    # 
    
    # -------------------------------------------------
    #inv_finish = inv_wb2finish
    
    # (check_result,cex,inv) = inv_check_func0(inv_start, inv_start2ex, inv_ex2ex, inv_ex2wb, inv_wb2wb, inv_wb2finish, trans_update, asmpt, sts)

    all_pairs, all_asmpt = extract_pair_of_regval_from_branch_list(branch_list, 4, 5 )
    ila_var_list = [ILA_r0, ILA_r1, ILA_r2, ILA_r3]
    aux_var_list = [aux0, aux1, aux2, aux3]


    start_or_list = []
    ex_or_list = []
    wb_or_list = []
    finish_or_list = []
    for pair_no in range(len(all_pairs)):
        pair0 = all_pairs[pair_no]
        pair0_pre = pair0[0]
        pair0_post = pair0[1]
        v0_v1_asmpt = all_asmpt_simplified[pair_no]
        start2sv = And([make_pair_eq(pair0_pre, ila_var_list ), make_pair_eq(pair0_pre, aux_var_list), v0_v1_asmpt])
        ex2sv = And([make_pair_eq(ila_var_list, pair0_post ), make_pair_eq(aux_var_list, pair0_pre), v0_v1_asmpt])
        wb2sv = And([make_pair_eq(ila_var_list, pair0_post ), make_pair_eq(aux_var_list, pair0_pre), v0_v1_asmpt])
        finish2sv = And([make_pair_eq(ila_var_list, pair0_post), make_pair_eq(aux_var_list, pair0_pre), v0_v1_asmpt])

        start_or_list.append(start2sv)
        ex_or_list.append(ex2sv)
        wb_or_list.append(wb2sv)
        finish_or_list.append(finish2sv)

    # start_implies_sv = Implies(start, Or(start_or_list))
    # ex_implies_sv = Implies(ppl_stage_ex, Or(ex_or_list))
    # wb_implies_sv = Implies(ppl_stage_wb, Or(wb_or_list))
    # finish_implies_sv = Implies(ppl_stage_finish, Or(finish_or_list))

    assert len(inv_group5.state_list) == len(finish_or_list) == 5
    inv_finish_ila_rtl= Implies(ppl_stage_finish, \
                        Or( \
                            [And(inv_group5.state_list[idx],finish_or_list[idx]) \
                             for idx in range(len(finish_or_list))]))

    ila_start =  Implies(start , And(make_pair_eq(ila_var_list,  extracted_list[0:4]), make_pair_eq(aux_var_list, extracted_list[4:8]))) #

    ex_wb = And([make_pair_eq(ila_var_list,  sv_extracted_list), make_pair_eq(aux_var_list, extracted_list[4:8])])
    ila_ex = Implies(ppl_stage_ex , ex_wb)
    ila_wb = Implies(ppl_stage_wb , ex_wb)


    # inv_ila_rtl = And(inv_start, inv_ex, inv_wb, inv_finish_ila_rtl, start_implies_sv, ex_implies_sv, wb_implies_sv)
    inv_ila_rtl = And(inv_start, inv_ex, inv_wb, inv_finish_ila_rtl, ila_start, ila_ex, ila_wb)

    #inv_ila = And([start_implies_sv, ex_implies_sv, wb_implies_sv, finish_implies_sv])

    #inv_ila_rtl = And([inv_ila, inv_rtl])
    # print (sts_init_extended.serialize())
    # print (ila_start.serialize())
    
    init_check_generic_func(inv_ila_rtl, sts_init_extended)
    inv_check_generic_func(inv_ila_rtl, trans_update, asmpt, sts)
    property_check_generic_func(inv_ila_rtl, sts_assertion, asmpt)
    
    # print ('---- in cex -----')
    # for ridx, rexpr in enumerate([ILA_r0, ILA_r1, ILA_r2, ILA_r3]):
    #     rexpr_prime = substitute(rexpr, sts.v2vprime)
    #     print ('ILA r',ridx, cex.get_value(rexpr_prime))

    # for ridx, rexpr in enumerate([aux0, aux1, aux2, aux3]):
    #     rexpr_prime = substitute(rexpr, sts.v2vprime)
    #     print ('aux r',ridx, cex.get_value(rexpr_prime))

    # print ('---- rtl side ----')
    # for sv_eq in inv_group5.state_list:
    #     sv_eq_prime = substitute(sv_eq, sts.v2vprime)
    #     print (cex.get_value(sv_eq_prime))
    # print ('---- ila side ----')
    # for sv_eq in finish_or_list:
    #     sv_eq_prime = substitute(sv_eq, sts.v2vprime)
    #     print (cex.get_value(sv_eq_prime))
    # for pair_no in range(len(all_pairs)):
    #     pair0 = all_pairs[pair_no]
    #     pair0_post = pair0[1]
    #     v0_v1_asmpt = all_asmpt_simplified[pair_no]
    #     print ('condition : ', pair_no)
    #     for ridx, rexpr in enumerate(pair0_post):
    #         rexpr_prime = substitute(rexpr, sts.v2vprime)
    #         print ('r',ridx, cex.get_value(rexpr_prime))



if __name__ == '__main__':
  extracted_list, sv_extracted_list = ila_trans()
  main(extracted_list, sv_extracted_list)

""" HZ: NOTE

1. assumption : asmpt_start_cond = Implies(start, And([EqualsOrIff(sv, symbolic_val) for sv, symbolic_val in init_setting.items()]))
2. cegar on ILA_trans

0 v1 == 0
1 (v2 == 1) && (v1==0 )
2 (v2 == 1) && (v1==0 )
3 v1 == 1
4 v1 == 1



Question to think about : init condition ?

"""