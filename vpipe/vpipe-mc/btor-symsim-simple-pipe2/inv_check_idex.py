from ast import Eq
from lib2to3.pgen2.token import RPAR
from operator import le
from time import pthread_getcpuclockid
from inv_group_new import *
from cex_parser import cex_parser
from pysmt.rewritings import conjunctive_partition
from parse_asmpt import *
from pysmt.shortcuts import get_env
from pysmt.formula import FormulaManager

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


def main():
    file_name = "/data/wenjifang/vpipe-mc/btor-symsim-simple-pipe2/branch_list_idex.pkl"
    open_file = open(file_name,"rb")
    branch_list = pickle.load(open_file)




    btor_parser = BTOR2Parser()
    sts, _ = btor_parser.parse_file(Path("/data/wenjifang/vpipe-mc/ILA-pipeline/ilang_simple_pipe/stall_vrecorder/verify/ADD/problem.btor2"))
    executor = SymbolicExecutor(sts)

    init_dict = {
      'RTL_if_id_inst':'inst_id',
      'RTL_id_ex_operand1':'oper1',
      'RTL_id_ex_operand2':'oper2',
      'RTL_id_ex_op':'op',
      'RTL_id_ex_rd':'rd1',
      'RTL_id_ex_reg_wen':'w1',
      'RTL_ex_wb_val':'ex_val',
      'RTL_ex_wb_rd':'rd2',
      'RTL_ex_wb_reg_wen':'w2',
      'RTL_if_id_valid':'v0',
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
    init_setting = executor.convert(init_dict)

    tag_start = tobool(executor.sv('__START__'))
    tag_id = tobool(executor.sv('stage_tracker_if_id_iuv'))
    tag_ex = tobool(executor.sv('stage_tracker_id_ex_iuv'))
    tag_wb = tobool(executor.sv('stage_tracker_ex_wb_iuv'))
    tag_finish = tobool(executor.sv('stage_tracker_wb_iuv'))
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
        elif(str(var) == 'v0'):
            v0 = var
    
    
    #layer0 -- init (start)
    inv_group0 = InvGroup(layer=0,tag=tag_start,branch_list=branch_list)
    inv_group0.branch2state()
    inv_list0 = inv_group0.get_inv_group()
    inv_l0 = Or(inv_list0)

    #layer1 -- start-id
    inv_group1 = InvGroup(layer=1,tag=tag_id,branch_list=branch_list)
    inv_group1.branch2state()
    inv_list1 = inv_group1.get_inv_group()
    # inv_list1 = inv_group1.inv_with_ila(ila_prime_list)
    inv_l1 = Or(inv_list1)

    #layer2 -- id-id
    inv_group2 = InvGroup(layer=2,tag=tag_id,branch_list=branch_list)
    inv_group2.branch2state()
    inv_list2 = inv_group2.get_inv_group()
    # inv_list1 = inv_group1.inv_with_ila(ila_prime_list)
    inv_l2 = Or(inv_list2)

    #layer3 -- id-ex
    inv_group3 = InvGroup(layer=3,tag=tag_ex,branch_list=branch_list)
    inv_group3.branch2state()
    inv_list3 = inv_group3.get_inv_group()
    # inv_list2 = inv_group2.inv_with_ila(ila_prime_list)
    inv_l3 = Or(inv_list3)

    #layer4 -- ex-ex
    inv_group4 = InvGroup(layer=4,tag=tag_ex,branch_list=branch_list)
    inv_group4.branch2state()
    inv_list4 = inv_group4.get_inv_group()
    # inv_list2 = inv_group2.inv_with_ila(ila_prime_list)
    inv_l4 = Or(inv_list4)

    ### inv check
    #1:  sts.trans
    trans = sts.trans
    assume  = sts.assumption
    assertion = sts.assertion
    trans = And(trans,assume,substitute(assume,sts.v2vprime))

    file = 'trans.txt'
    with open(file,'w') as f:
        f.write(trans.serialize())

    print('\n\n',substitute(assume,sts.v2vprime).serialize())


    print('inv-check !!!')
    var_to_nxt = {}
    for sv, var in init_setting.items():
        tp = BVType(var.bv_width())
        var_to_nxt[var] = Symbol(str(var)+"_next", tp)
    
    expr_equal = []
    for var, var_nxt in var_to_nxt.items(): 
        expr_equal.append(EqualsOrIff(var_nxt, var))
    
    trans_nxt = And(expr_equal)
    trans_update = And(trans, trans_nxt)

    ### additional assumptions
    asmpt_rst = And(EqualsOrIff(rst,BV(0,1)), EqualsOrIff(dummy_reset,BV(0,1)), EqualsOrIff(reseted,BV(1,1)))
 
    one_hot_element = [tag_start, tag_id, tag_ex, tag_wb, tag_finish]
    ll = len(one_hot_element)
    one_hot_list = []
    for i in range(0,ll):
      for j in range(i+1, ll):
        one_hot_list.append(Not(And(one_hot_element[i], one_hot_element[j])))


    asmpt_tag = And(
        And(one_hot_list), Not(And(tag_start, started)),  Not(And(tag_id, ended)), Not(And(tag_ex, ended)), Not(And(tag_ex, ended2)), Not(And(tag_wb, ended)),
        Implies(tag_id, started), Implies(tag_ex, started), Implies(tag_wb, started), Implies(tag_finish, started), Implies(ended, started), Implies(ended2, started))

    

    free_var_test = get_free_variables(asmpt_init)
    for var in free_var_test:
        if(str(var) == '__RESETED__1'):
            reseted1 = var
        elif(str(var) == '__START__1'):
            start1 = var
        elif(str(var) == 'stage_tracker_ex_wb_iuv1'):
            stage_tracker_ex_wb_iuv1 = var
        elif(str(var) == 'dummy_resetX1'):
            dummy_resetX1 = var
    print(asmpt_init.serialize())

    tag_cons = And(EqualsOrIff(reseted1,BV(1,1)), EqualsOrIff(start1,BV(1,1)), EqualsOrIff(stage_tracker_ex_wb_iuv1,BV(0,1)), EqualsOrIff(dummy_resetX1,BV(0,1)))
    asmpt_init = And(tag_cons,asmpt_init)

    aux_and = And(EqualsOrIff(aux0_cm, BV(0,1)), EqualsOrIff(aux1_cm, BV(0,1)), EqualsOrIff(aux2_cm, BV(0,1)), EqualsOrIff(aux3_cm, BV(0,1)))
    aux_and_one = And(EqualsOrIff(aux0_cm, BV(1,1)), EqualsOrIff(aux1_cm, BV(1,1)), EqualsOrIff(aux2_cm, BV(1,1)), EqualsOrIff(aux3_cm, BV(1,1)))
    # asmpt_aux = And(Implies(start, aux_and), Implies(ppl_stage_ex, aux_and), Implies(ppl_stage_wb, aux_and), Implies(ppl_stage_finish, aux_and_one))
    # asmpt_aux = aux_and
    # asmpt_id = Implies(tag_id ,EqualsOrIff(id_go, BV(1,1)))
    
    asmpt = And(asmpt_rst, asmpt_tag, asmpt_init, )
    # asmpt = And(asmpt_rst, asmpt_tag, asmpt_init, asmpt_id)


    # asmpt = And(asmpt_rst, asmpt_tag, asmpt_init, asmpt_aux)
    

    
    (check_result,cex,inv) = inv_check_func_idex(inv_l0, inv_l1, inv_l2, inv_l3, inv_l4, trans_update, asmpt, sts)
    test_ce(inv_list2, cex)
    partial_check_num(inv_list3, 0, cex, sts)
    exit()
     
    # # inv_asmpt = And(inv, asmpt)
    # # inv_list4 = deduplicate(inv_list4)
    test_ce(inv_list1, cex)
    # test_ce(inv_list2, cex)
    # test_ce_prime(inv_list3, cex, sts)

    # partial_check_num(inv_list3, 1, cex, sts)
    i = 3
    
    tag_record_list = []
    while(i!=0):
        i = i-1
    # while(check_result == False):
    #     i = i+1
        (v_cons,n_tag0,n_tag1,n_tag2,n_tag3) = cex_parser(cex)

        ce_constr_v = []
        v0_cons_0 = EqualsOrIff(v0,BV(0,1))
        v0_cons_1 = EqualsOrIff(v0,BV(1,1))
        v1_cons_0 = EqualsOrIff(v1,BV(0,1))
        v1_cons_1 = EqualsOrIff(v1,BV(1,1))
        v2_cons_0 = EqualsOrIff(v2,BV(0,1))
        v2_cons_1 = EqualsOrIff(v2,BV(1,1))

        if(v_cons == 0):
            ce_constr_v = [v0_cons_0,v1_cons_0,v2_cons_0]
        elif(v_cons == 1):
            ce_constr_v = [v0_cons_0,v1_cons_0,v2_cons_1]
        elif(v_cons == 2):
            ce_constr_v = [v0_cons_0,v1_cons_1,v2_cons_0]
        elif(v_cons == 3):
            ce_constr_v = [v0_cons_0,v1_cons_1,v2_cons_1]
        elif(v_cons == 4):
            ce_constr_v = [v0_cons_1,v1_cons_0,v2_cons_0]
        elif(v_cons == 5):
            ce_constr_v = [v0_cons_1,v1_cons_0,v2_cons_1]
        elif(v_cons == 6):
            ce_constr_v = [v0_cons_1,v1_cons_1,v2_cons_0]
        elif(v_cons == 7):
            ce_constr_v = [v0_cons_1,v1_cons_1,v2_cons_1]
        print(ce_constr_v)
                
        old_cons_list = ['(v0 = 0_1)','(v0 = 1_1)','(v1 = 0_1)','(v1 = 1_1)','(v2 = 0_1)','(v2 = 1_1)']
        new_cons_list = [EqualsOrIff(v0,BV(1,1)),EqualsOrIff(v0,BV(0,1)),EqualsOrIff(v1,BV(1,1)),EqualsOrIff(v1,BV(0,1)),EqualsOrIff(v2,BV(1,1)),EqualsOrIff(v2,BV(0,1))]

        ### inv update
        if(n_tag0 == 1):
            print('start:',n_tag0)
            ce_constr = copy.copy(ce_constr_v)
            _,inv_dedup0 = inv_group0.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
            print('\n\n',inv_dedup0)
            inv_l0 = Or(inv_dedup0)
            tag_record_list.append('start')
        elif(n_tag1 == 1):
            print('ppl_stage_id:',n_tag1)
            ce_constr = copy.copy(ce_constr_v)
            _,inv_dedup1 = inv_group1.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
            inv_l1 = Or(inv_dedup1)
            _,inv_dedup2 = inv_group2.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
            inv_l2 = Or(inv_dedup2)
            
            tag_record_list.append('ppl_stage_id')
        elif(n_tag2 == 1):
            print('ppl_stage_ex:',n_tag2)
            ce_constr = copy.copy(ce_constr_v)
            _,inv_dedup3 = inv_group3.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
            inv_l3 = Or(inv_dedup3)
            _,inv_dedup4 = inv_group4.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
            inv_l4 = Or(inv_dedup4)

            tag_record_list.append('ppl_stage_ex')
        elif(n_tag3 == 1):
            print('ppl_stage_wb:',n_tag3)
            ce_constr = copy.copy(ce_constr_v)
            _,inv_dedup5 = inv_group5.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
            inv_l5 = Or(inv_dedup5)
            _,inv_dedup6 = inv_group6.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
            inv_l6 = Or(inv_dedup6)

            tag_record_list.append('ppl_stage_wb')
            
        
    #     ##inv check
        # (check_result,cex,inv_prop) = inv_check_func(inv_l0, inv_l1, inv_l2, inv_l3, inv_group4_l4, inv_group5_l5, inv_ila_start_list, inv_ila_started_list, trans_update, asmpt, sts)
        (check_result,cex,inv) = inv_check_func_c4(inv_l0, inv_l1, inv_l2, inv_l3, inv_l4, inv_l5, inv_l6, inv_l7, trans_update, asmpt, sts)
        test_ce(inv_dedup1, cex)
        input()
    print(tag_record_list)
        
    




if __name__ == '__main__':
  main()


