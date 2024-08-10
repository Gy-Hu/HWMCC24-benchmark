from inv_group import *

# def inv_check(inv_l0,inv_l1,inv_l2,inv_l3,inv_group4_l4,inv_group5_l5,inv_l6,trans_update,asmpt,sts,inv_group):
# def inv_check(inv_l0):
#     inv_tag0 = inv_l0
    # inv_tag1 = Or(inv_l1,inv_l2)
    # inv_tag2_p1 = inv_l3
    # inv_tag3_p2 = inv_l6
    # inv_property = []
    # if(len(inv_group4_l4) == len(inv_group5_l5)):
    #     for idx in range(len(inv_group4_l4)):
    #         inv_property.append(And(inv_group4_l4[idx],inv_group5_l5[idx]))
    # else:
    #     assert False
    
    # inv_property_dedup = deduplicate(inv_property)
    # inv_property_expr = Or(inv_property_dedup)
    # print(inv_property_expr)


    # inv = And(inv_tag0, inv_tag1, inv_tag2_p1, inv_tag3_p2, inv_property_expr)
    # inv_check = And(inv, trans_update, asmpt)
    # inv_prime = substitute(inv, sts.v2vprime)
    # print (is_valid(Implies(inv_check, inv_prime)))
    # cex = get_invalid_model(Implies(inv_check, inv_prime))
    # print(type(cex))

    # print("counter example\n", sort_model(cex))
    # inv_group.test_ce(cex)
    # return cex

def main():
    file_name = "/home/fwj/vpipe-mc/btor-symsim/branch_list.pkl"
    open_file = open(file_name,"rb")
    branch_list = pickle.load(open_file)





    btor_parser = BTOR2Parser()
    sts, _ = btor_parser.parse_file(Path("/home/fwj/vpipe-mc/btor-symsim/pipe-with-stall.btor2"))
    executor = SymbolicExecutor(sts)

    init_setting = executor.convert({
        'wen_stage1':'v1',
        'wen_stage2':'v2',
        'stage1':'a',
        'stage2':'b',
        'stage3':'c'
        })





    ###############################################################################

    tag0 = EqualsOrIff(executor.sv('tag0'),BV(1,1))
    tag1 = EqualsOrIff(executor.sv('tag1'),BV(1,1))
    tag2 = EqualsOrIff(executor.sv('tag2'),BV(1,1))
    tag3 = EqualsOrIff(executor.sv('tag3'),BV(1,1))

    #get free variable
    state_list_init =  branch_list[0]
    state_init = state_list_init[0]
    state_init.print()
    state_init.print_assumptions()
    asmpt_init = And(state_init.asmpt)
    # asmpt_test = asmpt_test.serialize()
    free_var = get_free_variables(asmpt_init)
    print(free_var)
    print(type(free_var))

    for var in free_var:
        if(str(var) == 'v1'):
            v1 = var
        elif(str(var) == 'v2'):
            v2 = var
    
    if( (str(v1)!='v1') and (str(v2)!='v2')):
        assert False
    print(type(v1))
    # test = EqualsOrIff(var,BV(0,1))
    print(v1)
    print(v2)




    #tag0 - tag0
    inv_group0 = InvGroup(layer=0,tag=tag0,branch_list=branch_list)
    inv_group0.branch2state()
    state_list0 = inv_group0.get_state_list()
    inv_dedup0 = inv_group0.inv_deduplicate()
    inv_l0 = Or(inv_dedup0)

    print('old:\n',inv_l0.serialize())
    print('\n\n')



    inv_list0 = inv_group0.get_inv_group()
    inv_l0 = Or(inv_list0)
    inv_l0 = inv_l0.simplify()

    print('new:\n',(inv_l0).serialize())
    print('\n\n')
    
    # print(len(inv_dedup0))
    # print(len(inv_list0))
    # input(0)

    state_dedup = inv_group0.state_deduplicate()

    # print(len(inv_dedup0))
    # # print('len of inv',len(inv_l0_group))
    # # print('len of state',len(state_l0))
    # for expr in inv_dedup0:
    #     print(expr)
    
    #tag0 - tag1
    inv_group1 = InvGroup(layer=1,tag=tag1,branch_list=branch_list)
    inv_group1.branch2state()
    inv_dedup1 = inv_group1.inv_deduplicate()
    inv_l1 = Or(inv_dedup1)

    # inv_list1 = inv_group1.get_inv_group()
    # inv_l1 = Or(inv_list1)
    # print(len(inv_dedup1))
    # print(len(inv_list1))
    # input(1)
    

    #tag1 - tag1
    inv_group2 = InvGroup(layer=2,tag=tag1,branch_list=branch_list)
    inv_group2.branch2state()
    inv_dedup2 = inv_group2.inv_deduplicate()
    inv_l2 = Or(inv_dedup2)

    # inv_list2 = inv_group2.get_inv_group()
    # inv_l2 = Or(inv_list2)
    # print(len(inv_dedup2))
    # print(len(inv_list2))
    # input(2)


    #tag1 - tag2
    inv_group3 = InvGroup(layer=3,tag=tag2,branch_list=branch_list)
    inv_group3.branch2state()
    inv_dedup3 = inv_group3.inv_deduplicate()
    inv_l3 = Or(inv_dedup3)

    # inv_list3 = inv_group3.get_inv_group()
    # inv_l3 = Or(inv_list3)
    # print(len(inv_dedup3))
    # print(len(inv_list3))
    # input(3)

    
    

    #tag2 - tag2
    inv_group4 = InvGroup(layer=4,tag=tag2,branch_list=branch_list)
    inv_group4.branch2state()
    inv_group4_l4 = inv_group4.get_inv_group()
    inv_dedup4 = inv_group4.inv_deduplicate()
    inv_l4 = Or(inv_dedup4)

    
    
    

    #tag2 - tag3
    inv_group5 = InvGroup(layer=5,tag=tag3,branch_list=branch_list)
    inv_group5.branch2state()
    inv_group5_l5 = inv_group5.get_inv_group()
    inv_dedup5 = inv_group5.inv_deduplicate()
    inv_l5 = Or(inv_dedup5)
    

    #tag3 - tag3
    inv_group6 = InvGroup(layer=6,tag=tag3,branch_list=branch_list)
    inv_group6.branch2state()
    inv_dedup6 = inv_group6.inv_deduplicate()
    inv_l6 = Or(inv_dedup6)
    
    # inv_list6 = inv_group6.get_inv_group()
    # inv_l6 = Or(inv_list6)
    # print(len(inv_dedup6))
    # print(len(inv_list6))
    # input(6)
    


    #inv
    inv_tag0 = inv_l0
    inv_tag1 = Or(inv_l1,inv_l2)
    inv_tag2_p1 = inv_l3
    inv_tag3_p2 = inv_l6
    inv_tag2 = Or(inv_l3,inv_l4)
    inv_tag3 = Or(inv_l5,inv_l6)
    
    inv_property = []
    if(len(inv_group4_l4) == len(inv_group5_l5)):
        for idx in range(len(inv_group4_l4)):
            inv_property.append(And(inv_group4_l4[idx],inv_group5_l5[idx]))
    else:
        assert False
    
    inv_property_dedup = deduplicate(inv_property)
    inv_property_expr = Or(inv_property_dedup)
    # inv_property_expr = Or(inv_property)
    
    # print(len(inv_property_dedup))
    # print(len(inv_property))
    # input(6)

    # print(inv_property_expr)

    
    inv = And(inv_tag0, inv_tag1, inv_tag2_p1, inv_tag3_p2, inv_property_expr)
    # inv = And(inv_tag0, inv_tag1, inv_tag2, inv_tag3)

    # print(inv_tag0)
    # input()
    # print(inv_tag1)
    # input()
    # print(inv_tag2_p1)
    # input()
    # print(inv_tag3_p2)
    # input()
    # print(inv_property_expr)
    # input()



    

    ###inv check
    #1:  sts.trans
    trans = sts.trans
    print('inv-check !!!')


    var_to_nxt = {}
    for sv, var in init_setting.items():
        tp = BVType(var.bv_width())
        var_to_nxt[var] = Symbol(str(var)+"_next", tp)

    
    
    del_dic_one(var_to_nxt,'tag01')
    del_dic_one(var_to_nxt,'tag11')
    del_dic_one(var_to_nxt,'tag21')
    del_dic_one(var_to_nxt,'tag31')
    del_dic_one(var_to_nxt,'reg_v1')
    del_dic_one(var_to_nxt,'reg_v_comp1')

    expr_equal = []

    for var, var_nxt in var_to_nxt.items(): 
        expr_equal.append(EqualsOrIff(var_nxt, var))
    
    trans_nxt = And(expr_equal)

    trans_update = And(trans, trans_nxt)

    #additional assumptions
    
    asmpt_rst = EqualsOrIff(executor.sv('rst'),BV(0,1))
    asmpt_tag = And(Not(And(tag0,tag1)), Not(And(tag0,tag2)), Not(And(tag0,tag3)), Not(And(tag1,tag2)), Not(And(tag1,tag3)), Not(And(tag2,tag3)))
    asmpt = And(asmpt_rst,asmpt_tag)
    # asmpt = asmpt_rst
    inv_check = And(inv, trans_update, asmpt)

    inv_prime = substitute(inv, sts.v2vprime)

    print (is_valid(Implies(inv_check, inv_prime)))
    cex = get_invalid_model(Implies(inv_check, inv_prime))

    print(type(cex))


    print("counter example\n", sort_model(cex))


    #counter example feedback
    ce_constr = []
    v1_cons = EqualsOrIff(v1,BV(0,1))
    v2_cons = EqualsOrIff(v2,BV(0,1))
    # ce_constr = [EqualsOrIff(v1,BV(0,1)),EqualsOrIff(v2,BV(0,1))]

    
    
    old_cons_list = ['(v1 = 0_1)','(v1 = 1_1)','(v2 = 0_1)','(v2 = 1_1)']
    new_cons_list = [EqualsOrIff(v1,BV(1,1)),EqualsOrIff(v1,BV(0,1)),EqualsOrIff(v2,BV(1,1)),EqualsOrIff(v2,BV(0,1))]

###update1
    ce_constr = [EqualsOrIff(v1,BV(0,1)),EqualsOrIff(v2,BV(0,1))]
    inv_dedup1 = inv_group1.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
    inv_l1 = Or(inv_dedup1)

    ce_constr = [EqualsOrIff(v1,BV(0,1)),EqualsOrIff(v2,BV(0,1))]
    inv_dedup2 = inv_group2.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
    inv_l2 = Or(inv_dedup2)
    

    
##inv check1
    inv_tag0 = inv_l0
    inv_tag1 = Or(inv_l1,inv_l2)
    inv_tag2_p1 = inv_l3
    inv_tag3_p2 = inv_l6
    inv_property = []
    if(len(inv_group4_l4) == len(inv_group5_l5)):
        for idx in range(len(inv_group4_l4)):
            inv_property.append(And(inv_group4_l4[idx],inv_group5_l5[idx]))
    else:
        assert False
    
    inv_property_dedup = deduplicate(inv_property)
    inv_property_expr = Or(inv_property_dedup)
    print(inv_property_expr)


    inv = And(inv_tag0, inv_tag1, inv_tag2_p1, inv_tag3_p2, inv_property_expr)
    # inv = And(inv_tag0, inv_tag1, inv_tag2, inv_tag3)
    
    inv_check = And(inv, trans_update, asmpt)
    inv_prime = substitute(inv, sts.v2vprime)
    print (is_valid(Implies(inv_check, inv_prime)))
    cex = get_invalid_model(Implies(inv_check, inv_prime))
    print(type(cex))

    print("counter example\n", sort_model(cex))
    inv_group3.test_ce(cex)
    print('\n\nprime:')
    inv_group3.test_ce_prime(cex, sts)


    

# ###update2
#     ce_constr = [EqualsOrIff(v1,BV(0,1)),EqualsOrIff(v2,BV(0,1))]
#     inv_dedup1 = inv_group1.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
#     inv_l1 = Or(inv_dedup1)

#     ce_constr = [EqualsOrIff(v1,BV(0,1)),EqualsOrIff(v2,BV(0,1))]
#     inv_dedup2 = inv_group2.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
#     inv_l2 = Or(inv_dedup2)
    
    
# ###inv check2
#     inv_tag0 = inv_l0
#     inv_tag1 = Or(inv_l1,inv_l2)
#     inv_tag2_p1 = inv_l3
#     inv_tag3_p2 = inv_l6
#     inv_property = []
#     if(len(inv_group4_l4) == len(inv_group5_l5)):
#         for idx in range(len(inv_group4_l4)):
#             inv_property.append(And(inv_group4_l4[idx],inv_group5_l5[idx]))
#     else:
#         assert False
    
#     inv_property_dedup = deduplicate(inv_property)
#     inv_property_expr = Or(inv_property_dedup)
#     print(inv_property_expr)


#     inv = And(inv_tag0, inv_tag1, inv_tag2_p1, inv_tag3_p2, inv_property_expr)
#     inv_check = And(inv, trans_update, asmpt)
#     inv_prime = substitute(inv, sts.v2vprime)
#     print (is_valid(Implies(inv_check, inv_prime)))
#     cex = get_invalid_model(Implies(inv_check, inv_prime))
#     print(type(cex))

#     print("counter example\n", sort_model(cex))
#     inv_group0.test_ce(cex)


# ###update3
#     ce_constr = [EqualsOrIff(v1,BV(0,1)),EqualsOrIff(v2,BV(0,1))]
#     inv_dedup0 = inv_group0.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
#     inv_l0 = Or(inv_dedup0)

    
    
# ###inv check3
#     inv_tag0 = inv_l0
#     inv_tag1 = Or(inv_l1,inv_l2)
#     inv_tag2_p1 = inv_l3
#     inv_tag3_p2 = inv_l6
#     inv_property = []
#     if(len(inv_group4_l4) == len(inv_group5_l5)):
#         for idx in range(len(inv_group4_l4)):
#             inv_property.append(And(inv_group4_l4[idx],inv_group5_l5[idx]))
#     else:
#         assert False
    
#     inv_property_dedup = deduplicate(inv_property)
#     inv_property_expr = Or(inv_property_dedup)
#     print(inv_property_expr)


#     inv = And(inv_tag0, inv_tag1, inv_tag2_p1, inv_tag3_p2, inv_property_expr)
#     inv_check = And(inv, trans_update, asmpt)
#     inv_prime = substitute(inv, sts.v2vprime)
#     print (is_valid(Implies(inv_check, inv_prime)))
#     cex = get_invalid_model(Implies(inv_check, inv_prime))
#     print(type(cex))

#     print("counter example\n", sort_model(cex))
#     inv_group0.test_ce(cex)

# ##update4
#     ce_constr = [EqualsOrIff(v1,BV(0,1)),EqualsOrIff(v2,BV(1,1))]
#     inv_dedup0 = inv_group0.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
#     inv_l0 = Or(inv_dedup0)

    
    
# ###inv check4
#     inv_tag0 = inv_l0
#     inv_tag1 = Or(inv_l1,inv_l2)
#     inv_tag2_p1 = inv_l3
#     inv_tag3_p2 = inv_l6
#     inv_property = []
#     if(len(inv_group4_l4) == len(inv_group5_l5)):
#         for idx in range(len(inv_group4_l4)):
#             inv_property.append(And(inv_group4_l4[idx],inv_group5_l5[idx]))
#     else:
#         assert False
    
#     inv_property_dedup = deduplicate(inv_property)
#     inv_property_expr = Or(inv_property_dedup)
#     print(inv_property_expr)


#     inv = And(inv_tag0, inv_tag1, inv_tag2_p1, inv_tag3_p2, inv_property_expr)
#     inv_check = And(inv, trans_update, asmpt)
#     inv_prime = substitute(inv, sts.v2vprime)
#     print (is_valid(Implies(inv_check, inv_prime)))
#     cex = get_invalid_model(Implies(inv_check, inv_prime))
#     print(type(cex))

#     print("counter example\n", sort_model(cex))
#     inv_group0.test_ce(cex)

# ##update5
#     ce_constr = [EqualsOrIff(v1,BV(1,1)),EqualsOrIff(v2,BV(0,1))]
#     inv_dedup0 = inv_group0.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
#     inv_l0 = Or(inv_dedup0)

    
    
# ###inv check5
#     inv_tag0 = inv_l0
#     inv_tag1 = Or(inv_l1,inv_l2)
#     inv_tag2_p1 = inv_l3
#     inv_tag3_p2 = inv_l6
#     inv_property = []
#     if(len(inv_group4_l4) == len(inv_group5_l5)):
#         for idx in range(len(inv_group4_l4)):
#             inv_property.append(And(inv_group4_l4[idx],inv_group5_l5[idx]))
#     else:
#         assert False
    
#     inv_property_dedup = deduplicate(inv_property)
#     inv_property_expr = Or(inv_property_dedup)
#     print(inv_property_expr)


#     inv = And(inv_tag0, inv_tag1, inv_tag2_p1, inv_tag3_p2, inv_property_expr)
#     inv_check = And(inv, trans_update, asmpt)
#     inv_prime = substitute(inv, sts.v2vprime)
#     print (is_valid(Implies(inv_check, inv_prime)))
#     cex = get_invalid_model(Implies(inv_check, inv_prime))
#     print(type(cex))

#     print("counter example\n", sort_model(cex))
#     inv_group0.test_ce(cex)

# ##update6
#     ce_constr = [EqualsOrIff(v1,BV(0,1)),EqualsOrIff(v2,BV(1,1))]
#     inv_dedup0 = inv_group0.update_inv(cex,ce_constr,old_cons_list,new_cons_list)
#     inv_l0 = Or(inv_dedup0)

    
    
# ###inv check6
#     inv_tag0 = inv_l0
#     inv_tag1 = Or(inv_l1,inv_l2)
#     inv_tag2_p1 = inv_l3
#     inv_tag3_p2 = inv_l6
#     inv_property = []
#     if(len(inv_group4_l4) == len(inv_group5_l5)):
#         for idx in range(len(inv_group4_l4)):
#             inv_property.append(And(inv_group4_l4[idx],inv_group5_l5[idx]))
#     else:
#         assert False
    
#     inv_property_dedup = deduplicate(inv_property)
#     inv_property_expr = Or(inv_property_dedup)
#     print(inv_property_expr)


#     inv = And(inv_tag0, inv_tag1, inv_tag2_p1, inv_tag3_p2, inv_property_expr)
#     inv_check = And(inv, trans_update, asmpt)
#     inv_prime = substitute(inv, sts.v2vprime)
#     print (is_valid(Implies(inv_check, inv_prime)))
#     cex = get_invalid_model(Implies(inv_check, inv_prime))
#     print(type(cex))

#     print("counter example\n", sort_model(cex))
#     inv_group1.test_ce(cex)




    

if __name__ == '__main__':
  main()