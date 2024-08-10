from ast import Eq
from operator import le
from time import pthread_getcpuclockid
from inv_group_new import *
from cex_parser import cex_parser
from pysmt.rewritings import conjunctive_partition
from parse_asmpt import *

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
    file_name = "/home/fwj/vpipe-mc/btor-symsim-simple-pipe/branch_list_with_rst.pkl"
    file_name = "/home/fwj/vpipe-mc/btor-symsim-simple-pipe/branch_list_with_rst2.pkl"
    open_file = open(file_name,"rb")
    branch_list = pickle.load(open_file)


    btor_parser = BTOR2Parser()
    sts, _ = btor_parser.parse_file(Path("/home/fwj/vpipe-mc/btor-symsim-simple-pipe/problem.btor2"))
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
      '__auxvar0__recorder':'ar0',
      '__auxvar1__recorder':'ar1',
      '__auxvar2__recorder':'ar2',
      '__auxvar3__recorder':'ar3',
      'ILA_r0':'ila_reg0',
      'ILA_r1':'ila_reg1',
      'ILA_r2':'ila_reg2',
      'ILA_r3':'ila_reg3',
      }
    init_setting = executor.convert(init_dict)

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


    

    __ILA_I_inst = executor.sv('__ILA_I_inst')
    __VLG_I_inst = executor.sv('__VLG_I_inst')

    #get free variable
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
        if(str(var) == 'oper1'):
            oper1 = var
        elif(str(var) == 'oper2'):
            oper2 = var
        elif(str(var) == 'op'):
            op = var
        elif(str(var) == 'rd1'):
            rd1 = var
        elif(str(var) == 'w1'):
            w1 = var
        elif(str(var) == 'ex_val'):
            ex_val = var
        elif(str(var) == 'rd2'):
            rd2 = var
        elif(str(var) == 'w2'):
            w2 = var
        elif(str(var) == 'v1'):
            v1 = var
        elif(str(var) == 'v2'):
            v2 = var
        elif(str(var) == 'reg0'):
            reg0 = var
        elif(str(var) == 'reg1'):
            reg1 = var
        elif(str(var) == 'reg2'):
            reg2 = var
        elif(str(var) == 'reg3'):
            reg3 = var
        elif(str(var) == 's0'):
            s0 = var
        elif(str(var) == 's1'):
            s1 = var
        elif(str(var) == 's2'):
            s2 = var
        elif(str(var) == 's3'):
            s3 = var
        elif(str(var) == 'inst'):
            inst = var
        elif(str(var) == 'inst_v'):
            inst_v = var
        elif(str(var) == 'ila_inst'):
            ila_inst = var
        elif(str(var) == 'ar0'):
            ar0 = var
        elif(str(var) == 'ar1'):
            ar1 = var
        elif(str(var) == 'ar2'):
            ar2 = var
        elif(str(var) == 'ar3'):
            ar3 = var
        # elif(str(var) == 'ila_reg0'):
        #     ila_reg0 = var
        # elif(str(var) == 'ila_reg1'):
        #     ila_reg1 = var
        # elif(str(var) == 'ila_reg2'):
        #     ila_reg2 = var
        # elif(str(var) == 'ila_reg3'):
        #     ila_reg3 = var
    if( (str(oper1)!='oper1') and (str(oper2)!='oper2') and (str(op)!='op') and (str(rd1)!='rd1') and (str(w1)!='w1') and \
        (str(ex_val)!='ex_val') and (str(rd2)!='rd2') and (str(w2)!='w2') and (str(v1)!='v1') and (str(v2)!='v2') and \
        (str(reg0)!='reg0') and (str(reg1)!='reg1') and (str(reg2)!='reg2') and (str(reg3)!='reg3') and (str(s0)!='s0') and \
        (str(s1)!='s1') and (str(s2)!='s2') and (str(s3)!='s3') and (str(inst)!='inst') and (str(inst_v)!='inst_v')    ):
        assert False
    


    # #layer0 -- init (start)
    # inv_group0 = InvGroup(layer=0,tag=start,branch_list=branch_list)
    # inv_group0.branch2state()
    # inv_dedup0 = inv_group0.inv_deduplicate()
    # inv_l0 = Or(inv_dedup0)

    # #layer1 -- start-ex
    # inv_group1 = InvGroup(layer=1,tag=ppl_stage_ex,branch_list=branch_list)
    # inv_group1.branch2state()
    # inv_dedup1 = inv_group1.inv_deduplicate()
    # inv_l1 = Or(inv_dedup1)


    # #layer2 -- ex-ex
    # inv_group2 = InvGroup(layer=2,tag=ppl_stage_ex,branch_list=branch_list)
    # inv_group2.branch2state()
    # inv_dedup2 = inv_group2.inv_deduplicate()
    # inv_l2 = Or(inv_dedup2)


    # #layer3 -- ex-wb
    # inv_group3 = InvGroup(layer=3,tag=ppl_stage_wb,branch_list=branch_list)
    # inv_group3.branch2state()
    # inv_group_l3 = inv_group3.get_inv_group()
    


    # inv_reg3_ila = inv_group3.extract_reg_for_ila(tag_ila)
    # inv_ila_start_list0 = []
    # for reg_expr in inv_reg3_ila:
    #     inv_single = Implies(start,reg_expr)
    #     inv_ila_start_list0.append(inv_single)

    # inv_dedup3 = inv_group3.inv_deduplicate()
    # inv_l3 = Or(inv_dedup3)


    # #layer4 -- wb-wb
    # inv_group4 = InvGroup(layer=4,tag=ppl_stage_wb,branch_list=branch_list)
    # inv_group4.branch2state()
    # inv_group4_l4 = inv_group4.get_inv_group()


    # inv_reg4_ila = inv_group4.extract_reg_for_ila(tag_ila)
    # aux_list = inv_group4.extract_reg_for_ila(tag_aux)
    # inv_ila_start_list = []
    # ila_list = inv_reg4_ila
    # for reg_expr in inv_reg4_ila:
    #     inv_single = Implies(start,reg_expr)
    #     inv_ila_start_list.append(inv_single)

    
    # inv_dedup4 = inv_group4.inv_deduplicate()
    # inv_l4 = Or(inv_dedup4)

    # ila_aux_list = []
    # for idx in range(len(ila_list)):
    #     expr = And(ila_list[idx], aux_list[idx])
    #     ila_aux_list.append(expr)
    

    # #layer5 -- wb-finish
    # inv_group5 = InvGroup(layer=5,tag=ppl_stage_finish,branch_list=branch_list)
    # inv_group5.branch2state()
    # inv_group5_l5 = inv_group5.get_inv_group()

    # inv_reg5_ila = inv_group5.extract_reg_for_ila(tag_ila)
    # aux_prime_list = inv_group5.extract_reg_for_ila(tag_aux)
    # inv_ila_started_list = []
    # ila_prime_list = inv_reg5_ila
    # for reg_expr in inv_reg5_ila:
    #     inv_single = Implies(And(started, ppl_stage_finish),reg_expr)
    #     inv_ila_started_list.append(inv_single)
    
    # inv_dedup5 = inv_group5.inv_deduplicate()
    # inv_l5 = Or(inv_dedup5)

    # ila_aux_prime_list = []
    # for idx in range(len(ila_prime_list)):
    #     expr = And(ila_prime_list[idx], aux_prime_list[idx])
    #     ila_aux_prime_list.append(expr)


    
    
    
    
    #layer0 -- init (start)
    inv_group0 = InvGroup(layer=0,tag=start,branch_list=branch_list)
    inv_group0.branch2state()
    inv_list0 = inv_group0.get_inv_group()
    inv_l0 = Or(inv_list0)

    #layer1 -- start-ex
    inv_group1 = InvGroup(layer=1,tag=ppl_stage_ex,branch_list=branch_list)
    inv_group1.branch2state()
    inv_list1 = inv_group1.get_inv_group()
    inv_l1 = Or(inv_list1)

    #layer2 -- ex-ex
    inv_group2 = InvGroup(layer=2,tag=ppl_stage_ex,branch_list=branch_list)
    inv_group2.branch2state()
    inv_list2 = inv_group2.get_inv_group()
    inv_l2 = Or(inv_list2)

    #layer3 -- ex-wb
    inv_group3 = InvGroup(layer=3,tag=ppl_stage_wb,branch_list=branch_list)
    inv_group3.branch2state()
    inv_list3 = inv_group3.get_inv_group()
    inv_l3 = Or(inv_list3)

    #layer4 -- wb-wb
    inv_group4 = InvGroup(layer=4,tag=ppl_stage_wb,branch_list=branch_list)
    inv_group4.branch2state()
    inv_list4 = inv_group4.get_inv_group()
    inv_l4 = Or(inv_list4)

    #layer5 -- wb-wb
    inv_group5 = InvGroup(layer=5,tag=ppl_stage_finish,branch_list=branch_list)
    inv_group5.branch2state()
    inv_list5 = inv_group5.get_inv_group()
    inv_l5 = Or(inv_list5)
    

    ###inv check
    #1:  sts.trans
    trans = sts.trans
    assume  = sts.assumption
    assertion = sts.assertion
    trans = And(trans,assume,substitute(assume,sts.v2vprime))

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

    #additional assumptions
    asmpt_rst = And(EqualsOrIff(rst,BV(0,1)), EqualsOrIff(dummy_reset,BV(0,1)), EqualsOrIff(reseted,BV(1,1)))
 
    one_hot_element = [start,ppl_stage_ex,ppl_stage_wb,ppl_stage_finish]
    ll = len(one_hot_element)
    one_hot_list = []
    for i in range(0,ll):
      for j in range(i+1, ll):
        one_hot_list.append(Not(And(one_hot_element[i], one_hot_element[j])))


    asmpt_tag = And(
        And(one_hot_list), Not(And(start, started)),  Not(And(ppl_stage_ex, ended)), Not(And(ppl_stage_ex, ended2)), Not(And(ppl_stage_wb, ended)),
        Implies(ppl_stage_ex, started), Implies(ppl_stage_wb, started), Implies(ppl_stage_finish, started), Implies(ended, started), Implies(ended2, started))

    

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
        elif(str(var) == 'ila_reg1'):
            ila_reg1 = var
    tag_cons = And(EqualsOrIff(reseted1,BV(1,1)), EqualsOrIff(start1,BV(1,1)), EqualsOrIff(ppl_stage_wb1,BV(0,1)), EqualsOrIff(dummy_resetX1,BV(0,1)))
    asmpt_init = And(tag_cons,asmpt_init)

    asmpt = And(asmpt_rst, asmpt_tag, asmpt_init)

    
    (check_result,cex,inv) = inv_check_func0(inv_l0, inv_l1, inv_l2, inv_l3, inv_l4, inv_l5, trans_update, asmpt, sts)
    # (check_result,cex,inv) = inv_check_func(inv_l0, inv_l1, inv_l2, inv_l3, inv_group_l3, inv_group4_l4, inv_group5_l5, inv_ila_start_list0, inv_ila_start_list, inv_ila_started_list, trans_update, asmpt, sts)
    inv_asmpt = And(inv, asmpt)
    exit()

    # 2. init check
    init = sts.init
    init_eq_list = []
    for k,v in init_dict.items():
        if ('ILA_r' not in str(k)):
            k_sv = executor.sv(str(k))
            for var in free_var:
                if(str(var) == str(v)):
                    v_sv = var
            eq_expr = EqualsOrIff(k_sv, v_sv)
            init_eq_list.append(eq_expr)

    init_new = And([init, And(init_eq_list), 
    EqualsOrIff(executor.sv('rst'),BV(0,1)), EqualsOrIff(executor.sv('dummy_reset'),BV(0,1))
    ])
   

    print('\n\ninit:',init_new.serialize())
    # input()
    ### forall V, init(V) => inv(V)
    init_check = Implies(init_new, inv)
    print ('init_check:',is_valid(init_check))
    cex_init = get_invalid_model(init_check)
    print("counter example (init check):\n", sort_model(cex_init))
    print('\n\n')

    if(is_valid(init_check) == False):
        conj = conjunctive_partition(inv)
        print(type(conj))
        conj_list = list(conj)
        # print(conj_list[0].serialize())

        for c in conj_list:
            print('\n',c)
            # print (c.serialize())
            print ('---------> ', cex_init.get_value(c))
            # input()


    # 3. property check
    assertion  = sts.assertion
    inv_asmpt_test = And(inv, asmpt_tag, asmpt_rst)
    prop_check = Implies(inv_asmpt,assertion)
    print('\n\nproperty:',assertion.serialize())
    print ('prop_check:',is_valid(prop_check))
    cex_prop = get_invalid_model(prop_check)
    print("counter example (prop check):\n", sort_model(cex_prop))

    if(is_valid(prop_check) == False):
        conj = conjunctive_partition(assertion)
        print(type(conj))
        conj_list = list(conj)
        # print(conj_list[0].serialize())

        for c in conj_list:
            print('\n',c)
            # print (c.serialize())
            print ('---------> ', cex_prop.get_value(c))
            input()

    # i = 0
    
    # tag_record_list = []
    # while(i!=0):
    #     i = i-1
    # # while(check_result == False):
    # #     i = i+1
    #     (v_cons,n_tag0,n_tag1,n_tag2,n_tag3) = cex_parser(cex)

    #     ce_constr_v = []
    #     v1_cons_0 = EqualsOrIff(v1,BV(0,1))
    #     v1_cons_1 = EqualsOrIff(v1,BV(1,1))
    #     v2_cons_0 = EqualsOrIff(v2,BV(0,1))
    #     v2_cons_1 = EqualsOrIff(v2,BV(1,1))

    #     if(v_cons == 0):
    #         ce_constr_v = [v1_cons_0,v2_cons_0]
    #     elif(v_cons == 1):
    #         ce_constr_v = [v1_cons_0,v2_cons_1]
    #     elif(v_cons == 2):
    #         ce_constr_v = [v1_cons_1,v2_cons_0]
    #     elif(v_cons == 3):
    #         ce_constr_v = [v1_cons_1,v2_cons_1]
    #     print(ce_constr_v)
                
    #     old_cons_list = ['(v1 = 0_1)','(v1 = 1_1)','(v2 = 0_1)','(v2 = 1_1)']
    #     new_cons_list = [EqualsOrIff(v1,BV(1,1)),EqualsOrIff(v1,BV(0,1)),EqualsOrIff(v2,BV(1,1)),EqualsOrIff(v2,BV(0,1))]

    #     ### inv update
    #     if(n_tag0 == 1):
    #         print('start:',n_tag0)
    #         ce_constr = copy.copy(ce_constr_v)
    #         inv_dedup0 = inv_group0.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
    #         print('\n\n',inv_dedup0)
    #         inv_l0 = Or(inv_dedup0)
    #         tag_record_list.append('start')
    #     elif(n_tag1 == 1):
    #         print('ppl_stage_ex:',n_tag1)
    #         ce_constr = copy.copy(ce_constr_v)
    #         inv_dedup1 = inv_group1.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
    #         inv_l1 = Or(inv_dedup1)
    #         inv_dedup2 = inv_group2.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
    #         inv_l2 = Or(inv_dedup2)
    #         tag_record_list.append('ppl_stage_ex')
    #     elif(n_tag2 == 1):
    #         print('ppl_stage_wb:',n_tag2)
    #         ce_constr = copy.copy(ce_constr_v)
    #         inv_dedup3 = inv_group3.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
    #         inv_l3 = Or(inv_dedup3)

    #         _, inv_group4_l4 = inv_group3.update_inv(cex,ce_constr,old_cons_list,new_cons_list)

    #         inv_reg4_ila = inv_group4.extract_reg_for_ila(tag_ila)
    #         inv_ila_start_list = []
    #         for reg_expr in inv_reg4_ila:
    #             inv_single = Implies(start,reg_expr)
    #             inv_ila_start_list.append(inv_single)

    #         tag_record_list.append('ppl_stage_wb')
    #     elif(n_tag3 == 1):
    #         pass
        
    #     ##inv check
    #     (check_result,cex,inv_prop) = inv_check_func(inv_l0, inv_l1, inv_l2, inv_l3, inv_group4_l4, inv_group5_l5, inv_ila_start_list, inv_ila_started_list, trans_update, asmpt, sts)
        
        
    




if __name__ == '__main__':
  main()


