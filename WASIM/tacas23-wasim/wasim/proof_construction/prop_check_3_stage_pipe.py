from lib2to3.pgen2.token import NOTEQUAL
from re import sub
from tabnanny import check
from inv_group_new import *
from cex_parser import cex_parser
from pysmt.shortcuts import NotEquals
from inv_group_new import *
from cex_parser import cex_parser
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
    file_name = "/home/tacas23/wasim/output/trace_3_stage_pipe_inst.pkl"
    open_file = open(file_name,"rb")
    branch_list = pickle.load(open_file)

    btor_parser = BTOR2Parser()
    sts, _ = btor_parser.parse_file(Path("/home/tacas23/wasim/design/3_stage_pipe_inst.btor2"))
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
    '__VLG_I_inst_valid':'inst_v',
    '__ILA_I_inst':'inst'
    })

    for k,v in init_setting.items():
        if(str(k) == '__ILA_I_inst'):
            inst = v
    start, ppl_stage_ex, ppl_stage_wb, ppl_stage_finish = executor.sv('__START__'), tobool(executor.sv('ppl_stage_ex')), tobool(executor.sv('ppl_stage_wb')), tobool(executor.sv('ppl_stage_finish'))
    ILA_r0, ILA_r1, ILA_r2, ILA_r3 = executor.sv('ILA_r0'),  executor.sv('ILA_r1'), executor.sv('ILA_r2'), executor.sv('ILA_r3')
    rst = executor.sv('rst')
    inst_ila = executor.sv('__ILA_I_inst')
    
    tag_ila = [ILA_r0, ILA_r1, ILA_r2, ILA_r3]



    #layer4 -- wb-wb
    inv_group4 = InvGroup(layer=4,tag=ppl_stage_wb,branch_list=branch_list)
    inv_group4.branch2state()
    inv_group4_l4 = inv_group4.get_inv_group()
    _, inv_reg4 = inv_group4.extract_reg()


    #layer5 -- wb-finish
    inv_group5 = InvGroup(layer=5,tag=ppl_stage_finish,branch_list=branch_list)
    inv_group5.branch2state()
    inv_group5_l5 = inv_group5.get_inv_group()
    inv_group5.inv_deduplicate()
    _, inv_reg5 = inv_group5.extract_reg()


    ## get transition relations
    trans_r0 = sts.sv_update[ILA_r0]
    trans_r1 = sts.sv_update[ILA_r1]
    trans_r2 = sts.sv_update[ILA_r2]
    trans_r3 = sts.sv_update[ILA_r3]
    trans_list = [trans_r0, trans_r1, trans_r2, trans_r3]


    r_sub = {rst:BV(0,1), start:BV(1,1)}
    trans_new_list = []
    for trans in trans_list:
        trans_new = substitute(trans, r_sub).simplify()
        trans_new = substitute(trans_new, {inst_ila:inst})
        trans_new_list.append(trans_new)


    wb_state_list = []
    wb_list = []
    for reg_expr_list in inv_reg4:
        for idx in range(len(reg_expr_list)):
            assert(len(reg_expr_list) == len(tag_ila))
            eq_expr = EqualsOrIff(reg_expr_list[idx],tag_ila[idx])
            wb_state_list.append(eq_expr)
        wb_state = And(wb_state_list)
        wb_list.append(wb_state)


    finish_state_list = []
    finish_list = []
    for reg_expr_list in inv_reg5:
        for idx in range(len(reg_expr_list)):
            assert(len(reg_expr_list) == len(trans_new_list))
            eq_expr = NotEquals(reg_expr_list[idx],trans_new_list[idx])
            finish_state_list.append(eq_expr)
        finish_state = And(finish_state_list)
        finish_list.append(finish_state)



    sat_check_list = []
    for idx in range(len(wb_list)):
        assert(len(wb_list) == len(finish_list))
        expr = And(wb_list[idx],finish_list[idx])
        sat_check_list.append(expr)
    sat_check = Or(sat_check_list)
    check_result = is_sat(sat_check)
    # print(check_result)

    if(check_result == False):
        print('\n\nDirect Property Check Pass!')
    else:
        print('\n\nDirect Property Check Fail!')
    
    # sat_check = substitute(sat_check, sts.v2vprime)
    # print(sat_check.serialize())
    end_time = time.perf_counter()
    print('Verification Time:%d(ms):  ' %int( round((end_time-start_time) * 1000) ))
    print('Verification Time:%d(s):  ' %round((end_time-start_time),5))
    



    
if __name__ == '__main__':
  main()
