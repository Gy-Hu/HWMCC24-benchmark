from time import pthread_getcpuclockid
from inv_group import *
from cex_parser import cex_parser
from pysmt.rewritings import conjunctive_partition



def main():
    file_name = "/home/fwj/vpipe-mc/btor-symsim-simple-pipe/branch_list_with_rst.pkl"
    open_file = open(file_name,"rb")
    branch_list = pickle.load(open_file)


    btor_parser = BTOR2Parser()
    sts, _ = btor_parser.parse_file(Path("/home/fwj/vpipe-mc/btor-symsim-simple-pipe/problem.btor2"))
    executor = SymbolicExecutor(sts)

    init_setting = executor.convert({
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
    '__VLG_I_inst_valid':'inst_v'
    })

    start, ppl_stage_ex, ppl_stage_wb, ppl_stage_finish = tobool(executor.sv('__START__')), tobool(executor.sv('ppl_stage_ex')), tobool(executor.sv('ppl_stage_wb')), tobool(executor.sv('ppl_stage_finish'))
    started = tobool(executor.sv('__STARTED__'))
    startedn = EqualsOrIff(executor.sv('__STARTED__'), BV(0,1)) 
    ended = tobool(executor.sv('__ENDED__'))
    ended2 = tobool(executor.sv('__2ndENDED__'))
    rst = executor.sv('rst')
    dummy_reset = executor.sv('dummy_reset')
    reseted =  executor.sv('__RESETED__')
    ILA_r0, ILA_r1, ILA_r2, ILA_r3 = executor.sv('ILA_r0'),  executor.sv('ILA_r1'), executor.sv('ILA_r2'), executor.sv('ILA_r3'),
    tag_ila = [ILA_r0, ILA_r1, ILA_r2, ILA_r3]

    __ILA_I_inst = executor.sv('__ILA_I_inst')
    __VLG_I_inst = executor.sv('__VLG_I_inst')

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

    for var in free_var:
        if(str(var) == 'v1'):
            v1 = var
        elif(str(var) == 'v2'):
            v2 = var
    
    if( (str(v1)!='v1') and (str(v2)!='v2')):
        assert False

    #layer0 -- init (start)
    inv_group0 = InvGroup(layer=0,tag=start,branch_list=branch_list)
    inv_group0.branch2state()
    inv_dedup0 = inv_group0.inv_deduplicate()
    inv_l0 = Or(inv_dedup0)


    #layer1 -- start-ex
    inv_group1 = InvGroup(layer=1,tag=ppl_stage_ex,branch_list=branch_list)
    inv_group1.branch2state()
    inv_dedup1 = inv_group1.inv_deduplicate()
    inv_l1 = Or(inv_dedup1)


    #layer2 -- ex-ex
    inv_group2 = InvGroup(layer=2,tag=ppl_stage_ex,branch_list=branch_list)
    inv_group2.branch2state()
    inv_dedup2 = inv_group2.inv_deduplicate()
    inv_l2 = Or(inv_dedup2)


    #layer3 -- ex-wb
    inv_group3 = InvGroup(layer=3,tag=ppl_stage_wb,branch_list=branch_list)
    inv_group3.branch2state()
    inv_group3_l3 = inv_group3.get_inv_group()

    inv_reg3_ila = inv_group3.extract_reg_for_ila(tag_ila)
    inv_ila_start_list1 = []
    for reg_expr in inv_reg3_ila:
        inv_single = Implies(startedn,reg_expr)
        inv_ila_start_list1.append(inv_single)


    #layer4 -- wb-wb
    inv_group4 = InvGroup(layer=4,tag=ppl_stage_wb,branch_list=branch_list)
    inv_group4.branch2state()
    inv_group4_l4 = inv_group4.get_inv_group()

    inv_reg4_ila = inv_group4.extract_reg_for_ila(tag_ila)
    inv_ila_start_list2 = []
    for reg_expr in inv_reg4_ila:
        inv_single = Implies(startedn,reg_expr)
        inv_ila_start_list2.append(inv_single)


    #layer5 -- wb-finish
    inv_group5 = InvGroup(layer=5,tag=ppl_stage_finish,branch_list=branch_list)
    inv_group5.branch2state()
    inv_group5_l5 = inv_group5.get_inv_group()

    inv_reg5_ila = inv_group5.extract_reg_for_ila(tag_ila)
    inv_ila_started_list = []
    for reg_expr in inv_reg5_ila:
        inv_single = Implies(started,reg_expr)
        inv_ila_started_list.append(inv_single)


    ###inv check
    #1:  sts.trans
    trans = sts.trans
    file = 'trans.txt'
    # with open (file,'w') as f:
    #     f.write(trans.serialize())
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
    asmpt_rst = And(EqualsOrIff(rst,BV(0,1)), EqualsOrIff(dummy_reset,BV(0,1)), EqualsOrIff(reseted,BV(0,1)),\
      EqualsOrIff(substitute(rst,sts.v2vprime),BV(0,1)), EqualsOrIff(substitute(dummy_reset,sts.v2vprime),BV(0,1)), EqualsOrIff(substitute(reseted,sts.v2vprime),BV(0,1)))
    
    one_hot_element = [start,ppl_stage_ex,ppl_stage_wb,ppl_stage_finish]
    ll = len(one_hot_element)
    one_hot_list = []
    for i in range(0,ll):
      for j in range(i+1, ll):
        one_hot_list.append(Not(And(one_hot_element[i], one_hot_element[j])))

    asmpt_inst = EqualsOrIff(__VLG_I_inst, __ILA_I_inst)
 
    asmpt_tag = And(And(one_hot_list), Not(And(start,started)),  Not(And(ppl_stage_ex,ended)), Not(And(start,ended2)))
    # asmpt_tag = And(one_hot_list)
    asmpt = And(asmpt_rst, asmpt_tag, asmpt_inst)
    # asmpt = And(asmpt_rst, asmpt_inst)
    
    
    (check_result,cex,inv_prop) = inv_check_func(inv_l0, inv_l1, inv_l2, inv_group3_l3, inv_group4_l4, inv_group5_l5, inv_ila_start_list1, inv_ila_start_list2, inv_ila_started_list, trans_update, asmpt, sts)
    
    i = 0
    
    tag_record_list = []
    while(i!=0):
        i = i-1
    # while(check_result == False):
    #     i = i+1
        (v_cons,n_tag0,n_tag1,n_tag2,n_tag3) = cex_parser(cex)

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
                
        old_cons_list = ['(v1 = 0_1)','(v1 = 1_1)','(v2 = 0_1)','(v2 = 1_1)']
        new_cons_list = [EqualsOrIff(v1,BV(1,1)),EqualsOrIff(v1,BV(0,1)),EqualsOrIff(v2,BV(1,1)),EqualsOrIff(v2,BV(0,1))]

        ### inv update
        if(n_tag0 == 1):
            print('start:',n_tag0)
            ce_constr = copy.copy(ce_constr_v)
            inv_dedup0 = inv_group0.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
            print('\n\n',inv_dedup0)
            input()
            inv_l0 = Or(inv_dedup0)
            tag_record_list.append('start')
        elif(n_tag1 == 1):
            print('ppl_stage_ex:',n_tag1)
            ce_constr = copy.copy(ce_constr_v)
            inv_dedup1 = inv_group1.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
            inv_l1 = Or(inv_dedup1)
            inv_dedup2 = inv_group2.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
            inv_l2 = Or(inv_dedup2)
            tag_record_list.append('ppl_stage_ex')
        elif(n_tag2 == 1):
            pass
        elif(n_tag3 == 1):
            pass
        
        ##inv check
        (check_result,cex,inv_prop) = inv_check_func(inv_l0, inv_l1, inv_l2, inv_group3_l3, inv_group4_l4, inv_group5_l5, inv_ila_start_list1, inv_ila_start_list2, inv_ila_started_list, trans_update, asmpt, sts)
        
        
    
    inv_group5.inv_deduplicate()
    # inv_group4.test_ce(cex)
    # print('\n\n')
    # inv_group5.test_ce_prime(cex,sts)
    # print('\n\n')
    # inv_group2.test_ce_prime(cex,sts)

    print('\n\n\n\nfinish! Find inv!')
    print('number of ilterations:',i)
    print('cex tag record:',tag_record_list)



if __name__ == '__main__':
  main()


