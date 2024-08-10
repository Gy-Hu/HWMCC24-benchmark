from time import pthread_getcpuclockid
from inv_group import *
from cex_parser import cex_parser



def main():
    file_name = "/home/fwj/vpipe-mc/btor-symsim-simple-pipe/branch_list_with_rst.pkl"
    open_file = open(file_name,"rb")
    branch_list = pickle.load(open_file)


    btor_parser = BTOR2Parser()
    sts, _ = btor_parser.parse_file(Path("/home/fwj/vpipe-mc/btor-symsim-simple-pipe/problem.btor2"))
    executor = SymbolicExecutor(sts)

    


    # wen_stage1 = executor.sv('wen_stage1')
    # wen_stage2 = executor.sv('wen_stage2')
    # reg_v = executor.sv('reg_v')
    # reg_v_comp = executor.sv('reg_v_comp')
    # stage1 = executor.sv('stage1')
    # stage2 = executor.sv('stage2')
    # stage3 = executor.sv('stage3')

    

    # init_setting = executor.convert({
    #     'wen_stage1':'v1',
    #     'wen_stage2':'v2',
    #     'stage1':'a',
    #     'stage2':'b',
    #     'stage3':'c'
    #     })

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
      '__VLG_I_inst_valid':'inst_v',
      # 'dummy_reset':0,
      # '__START__': '1'
      })

    


    ###############################################################################

    start, ppl_stage_ex, ppl_stage_wb, ppl_stage_finish = tobool(executor.sv('__START__')), tobool(executor.sv('ppl_stage_ex')), tobool(executor.sv('ppl_stage_wb')), tobool(executor.sv('ppl_stage_finish'))
    rst = executor.sv('rst')
    dummy_reset = executor.sv('dummy_reset')

    

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

    # for var in free_var:
    #     if(str(var) == 'v1'):
    #         v1 = var
    #     elif(str(var) == 'v2'):
    #         v2 = var
    #     elif(str(var) == 'a'):
    #         a = var
    #     elif(str(var) == 'b'):
    #         b = var
    #     elif(str(var) == 'c'):
    #         c = var
    
    # if( (str(v1)!='v1') and (str(v2)!='v2')):
    #     assert False
    # print(type(v1))
    # print(type(a))
    # print(v1)
    # print(v2)




    #tag0 - tag0
    inv_group0 = InvGroup(layer=0,tag=start,branch_list=branch_list)
    inv_group0.branch2state()
    state_list0 = inv_group0.get_state_list()
    inv_dedup0 = inv_group0.inv_deduplicate()
    inv_l0 = Or(inv_dedup0)

       
    # #tag0 - tag1
    # inv_group1 = InvGroup(layer=1,tag=start,branch_list=branch_list)
    # inv_group1.branch2state()
    # inv_dedup1 = inv_group1.inv_deduplicate()
    # inv_l1 = Or(inv_dedup1)
    # #tag1 - tag1
    # inv_group2 = InvGroup(layer=2,tag=ppl_stage_ex,branch_list=branch_list)
    # inv_group2.branch2state()
    # inv_dedup2 = inv_group2.inv_deduplicate()
    # inv_l2 = Or(inv_dedup2)
    # #tag1 - tag2
    # inv_group3 = InvGroup(layer=3,tag=ppl_stage_wb,branch_list=branch_list)
    # inv_group3.branch2state()
    # inv_dedup3 = inv_group3.inv_deduplicate()
    # inv_l3 = Or(inv_dedup3)
    # #tag2 - tag2
    # inv_group4 = InvGroup(layer=4,tag=ppl_stage_wb,branch_list=branch_list)
    # inv_group4.branch2state()
    # inv_group4_l4 = inv_group4.get_inv_group()
    # inv_dedup4 = inv_group4.inv_deduplicate()
    # inv_l4 = Or(inv_dedup4)
    # inv_l4_prop = inv_group4.extract_prop('stage3')
    # #tag2 - tag3
    # inv_group5 = InvGroup(layer=5,tag=ppl_stage_finish,branch_list=branch_list)
    # inv_group5.branch2state()
    # inv_group5_l5 = inv_group5.get_inv_group()
    # inv_dedup5 = inv_group5.inv_deduplicate()
    # inv_l5 = Or(inv_dedup5)


    


    ###inv check
    #1:  sts.trans
    trans = sts.trans
    assume  = sts.assumption
    assertion = sts.assertion
    print('trans:\n\n',trans.serialize())
    print('assume:\n\n',assume.serialize())
    print('assertion:\n\n',assertion.serialize())
    # trans = And(trans,assume,substitute(assume,sts.v2vprime))
    # print('inv-check !!!')
    # var_to_nxt = {}
    # for sv, var in init_setting.items():
    #     tp = BVType(var.bv_width())
    #     var_to_nxt[var] = Symbol(str(var)+"_next", tp)
    # # del_dic_one(var_to_nxt,'tag01')
    # # del_dic_one(var_to_nxt,'tag11')
    # # del_dic_one(var_to_nxt,'tag21')
    # # del_dic_one(var_to_nxt,'tag31')
    # # del_dic_one(var_to_nxt,'reg_v1')
    # # del_dic_one(var_to_nxt,'reg_v_comp1')
    
    # expr_equal = []
    # for var, var_nxt in var_to_nxt.items(): 
    #     expr_equal.append(EqualsOrIff(var_nxt, var))
    
    # trans_nxt = And(expr_equal)
    # trans_update = And(trans, trans_nxt)

    # #additional assumptions
    # asmpt_rst = And(EqualsOrIff(rst,BV(0,1)), EqualsOrIff(dummy_rst,BV(0,1)),EqualsOrIff(substitute(rst,sts.v2vprime),BV(0,1)),EqualsOrIff(substitute(dummy_rst,sts.v2vprime),BV(0,1)))
    # asmpt_tag = And(Not(And(start,ppl_stage_ex)), Not(And(ppl_stage_ex,ppl_stage_wb)), Not(And(ppl_stage_wb,ppl_stage_finish)))
    # asmpt = And(asmpt_rst,asmpt_tag)
    # # asmpt = asmpt_rst

    # # 0.complete inv with properties
    #             # prop1 = Implies(tag3, EqualsOrIff(reg_v_comp,reg_v*2+1))

    #             # prop = EqualsOrIff(BV(1,1),BV(1,1))
    #             # inv_addprop = []
    #             # for addprop in inv_l4_prop:
    #             #     inv_addprop.append(Implies(tag3,EqualsOrIff(reg_v,addprop)))

    # # prop = Implies(tag3,EqualsOrIff(reg_v_comp,stage3))

    # #init inv check
    # (check_result,cex,inv_prop) = inv_check_func(inv_l0,inv_l1,inv_l2,inv_l3,inv_l4,inv_l5,inv_l6,inv_group4_l4, inv_group5_l5, trans_update, asmpt, sts, prop1,inv_addprop)

    # i = 1
    
    # tag_record_list = []
    # # while(i!=0):
    # #     i = i-1
    # while(check_result == False):
    #     i = i+1
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
    #         print('tag0:',n_tag0)
    #         # input('tag')
    #         ce_constr = copy.copy(ce_constr_v)
    #         inv_dedup0 = inv_group0.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
    #         inv_l0 = Or(inv_dedup0)
    #         tag_record_list.append('tag0')
    #     elif(n_tag1 == 1):
    #         print('tag1:',n_tag1)
    #         # input('tag')
    #         ce_constr = copy.copy(ce_constr_v)
    #         inv_dedup1 = inv_group1.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
    #         inv_l1 = Or(inv_dedup1)

    #         ce_constr = copy.copy(ce_constr_v)
    #         inv_dedup2 = inv_group2.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
    #         inv_l2 = Or(inv_dedup2)
    #         tag_record_list.append('tag1')
    #     elif(n_tag2 == 1):
    #         pass
    #     elif(n_tag3 == 1):
    #         pass
        
    #     ##inv check
    #     (check_result,cex,inv_prop) = inv_check_func(inv_l0,inv_l1,inv_l2,inv_l3,inv_l4,inv_l5,inv_l6,inv_group4_l4, inv_group5_l5, trans_update, asmpt, sts, prop1,inv_addprop)

        
    #     # inv_group0.test_ce(cex)
    #     # inv_group0.test_ce_prime(cex,sts)
        
    #     # input()
    # print('\n\n\n\nfinish! Find inv!')
    # print('number of ilterations:',i)
    # print('cex tag record:',tag_record_list)

    
    # # inv_prop = And(inv_asmpt,prop)
    # # inv_prop = inv_asmpt
    # # inv_prop = And(inv_prop,prop3)


    # 1.init check
    init = sts.init
    # init_new = And([init, 
    # EqualsOrIff(v1,wen_stage1), EqualsOrIff(v2,wen_stage2),
    # EqualsOrIff(a,stage1), EqualsOrIff(b,stage2), EqualsOrIff(c,stage3),
    # EqualsOrIff(rst, BV(0,1)), EqualsOrIff(substitute(rst,sts.v2vprime), BV(0,1))
    # ])

    # print('\n\ninit:',init_new.serialize())
    # ### forall V, init(V) => inv(V)
    # init_check = Implies(init_new, inv_prop)
    # print ('init_check:',is_valid(init_check))
    # print('\n\n')


    # # 2.inv check
    # # print('inv:',inv_prop.serialize())
    # ### forall V V', trans(V,V') /\ inv(V) => inv(V')
    # inv_prop_prime = substitute(inv_prop, sts.v2vprime)
    # inv_check_result = Implies(And(trans,inv_prop), inv_prop_prime)
    # print ('inv_check:',is_valid(inv_check_result))
    # # print ('inv_check:',check_result)
    # print('\n\n')


    # # 3.property check
    
    # assertion  = sts.assertion
    
    # print(assume)
    # print(trans)
    # prop_check = Implies(inv_prop,assertion)
    # print('\n\nproperty:',assertion.serialize())
    # print ('prop_check:',is_valid(prop_check))
    # print("counter example (prop check):\n", sort_model(get_invalid_model(prop_check)))


    



    

if __name__ == '__main__':
  main()