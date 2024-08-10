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
    file_name = "/home/tacas23/wasim/output/trace_simple_MAC_no_stall.pkl"
    open_file = open(file_name,"rb")
    branch_list = pickle.load(open_file)


    btor_parser = BTOR2Parser()
    sts, _ = btor_parser.parse_file(Path("/home/tacas23/wasim/design/simple_MAC_no_stall.btor2"))
    executor = SymbolicExecutor(sts)



    reg_v = executor.sv('reg_v')
    reg_v_comp = executor.sv('reg_v_comp')
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

    state_list_init =  branch_list[0]
    state_init = state_list_init[0]
    state_expr_single = []
    for var,expr in state_init.sv.items():
        state_expr_single.append(EqualsOrIff(var, expr))
    state_expr = And(state_expr_single)
    free_var = get_free_variables(state_expr)
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
    

    pre_reg =  inv_l2_prop
    post_reg = inv_l3_prop 

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
    asmpt = And(state_init.asmpt)
    check_result = is_sat(And(sat_check, asmpt))
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