from inv_group_new import *
from cex_parser import cex_parser, cex_parser_c1, cex_parser_c2
from copyreg import pickle
from pysmt.fnode import *
from pysmt.shortcuts import NotEquals
import pickle
import sys
sys.path.append('/home/tacas23/wasim')
sys.path.append('/home/tacas23/wasim/symsim_framework')
from symsim_framework.btorparser import *
from symsim_framework.symsim import *
import time


def main():
    start_time = time.perf_counter()
    file_name = "/home/tacas23/wasim/output/trace_simple_MAC_stall.pkl"
    open_file = open(file_name,"rb")
    branch_list = pickle.load(open_file)


    btor_parser = BTOR2Parser()
    sts, _ = btor_parser.parse_file(Path("/home/tacas23/wasim/design/simple_MAC_stall.btor2"))
    executor = SymbolicExecutor(sts)


    wen_stage1 = executor.sv('wen_stage1')
    wen_stage2 = executor.sv('wen_stage2')
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

    # tag0 = EqualsOrIff(executor.sv('tag0'),BV(1,1))
    # tag1 = EqualsOrIff(executor.sv('tag1'),BV(1,1))
    # tag2 = EqualsOrIff(executor.sv('tag2'),BV(1,1))
    # tag3 = EqualsOrIff(executor.sv('tag3'),BV(1,1))
    tag0, tag1, tag2, tag3 = tobool(executor.sv('tag0')), tobool(executor.sv('tag1')), tobool(executor.sv('tag2')), tobool(executor.sv('tag3'))
    rst = executor.sv('rst')



    #tag1 - tag2
    inv_group3 = InvGroup(layer=3,tag=tag2,branch_list=branch_list)
    inv_group3.branch2state()
    inv_dedup3 = inv_group3.inv_deduplicate()
    inv_l3 = Or(inv_dedup3)
    inv_l3_prop = inv_group3.extract_prop('stage3')

    #tag2 - tag2
    inv_group4 = InvGroup(layer=4,tag=tag2,branch_list=branch_list)
    inv_group4.branch2state()
    inv_group4_l4 = inv_group4.get_inv_group()
    inv_dedup4 = inv_group4.inv_deduplicate()
    inv_l4 = Or(inv_dedup4)
    inv_l4_prop = inv_group4.extract_prop('stage3')
    #tag2 - tag3
    inv_group5 = InvGroup(layer=5,tag=tag3,branch_list=branch_list)
    inv_group5.branch2state()
    inv_group5_l5 = inv_group5.get_inv_group()
    inv_dedup5 = inv_group5.inv_deduplicate()
    inv_l5 = Or(inv_dedup5)
    inv_l5_prop = inv_group5.extract_prop('stage3')
    #tag3 - tag3
    inv_group6 = InvGroup(layer=6,tag=tag3,branch_list=branch_list)
    inv_group6.branch2state()
    inv_dedup6 = inv_group6.inv_deduplicate()
    inv_l6 = Or(inv_dedup6)
    inv_l6_prop = inv_group6.extract_prop('stage3')

    pre_reg =  inv_l4_prop
    post_reg = inv_l5_prop 

    trans = sts.sv_update[reg_v_comp]


    pre_list = []
    for reg in pre_reg:
        eq_expr = EqualsOrIff(reg, reg_v)      
        pre_list.append(eq_expr)



    post_list = []
    for reg in post_reg:
        eq_expr = NotEquals(reg, trans)      
        post_list.append(eq_expr)
    
    sat_check_list = []
    for idx in range(len(pre_list)):
        assert(len(pre_list) == len(post_list))
        expr = And(pre_list[idx],post_list[idx])
        sat_check_list.append(expr)
    sat_check = Or(sat_check_list)
    check_result = is_sat(sat_check)
    # print(check_result)

    if(check_result == False):
        print('\n\nDirect Property Check Pass!')
    else:
        print('\n\nDirect Property Check Fail!')
        cex = get_invalid_model(sat_check)
        print("counter example (inv check)\n", sort_model(cex))

    end_time = time.perf_counter()
    print('Verification Time:%d(ms):  ' %int( round((end_time-start_time) * 1000) ))
    print('Verification Time:%d(s):  ' %round((end_time-start_time),2))
    
    
        

    

if __name__ == '__main__':
  main()