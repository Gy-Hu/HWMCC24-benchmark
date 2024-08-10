from lib2to3.pgen2.token import NOTEQUAL
from tabnanny import check
from inv_group import *
from cex_parser import cex_parser
from pysmt.shortcuts import NotEquals

def main():
    #parse ILA_rx update function uf()
    btor_parser_uf = BTOR2Parser()
    sts_uf, _ = btor_parser_uf.parse_file(Path("/home/fwj/vpipe-mc/ILA-pipeline/ilang_simple_pipe/ILA_instr/ADD.btor2"))
    executor_uf = SymbolicExecutor(sts_uf)

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
    ILA_r0, ILA_r1, ILA_r2, ILA_r3 = executor.sv('ILA_r0'),  executor.sv('ILA_r1'), executor.sv('ILA_r2'), executor.sv('ILA_r3')
    
    tag_ila = [ILA_r0, ILA_r1, ILA_r2, ILA_r3]

    r0, r1, r2, r3 = executor_uf.sv('r0'), executor_uf.sv('r1'), executor_uf.sv('r2'), executor_uf.sv('r3')

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


    wb_state_list = []
    wb_list = []
    for reg_expr_list in inv_reg4:
        for idx in range(len(reg_expr_list)):
            assert(len(reg_expr_list) == len(tag_ila))
            eq_expr = EqualsOrIff(reg_expr_list[idx],tag_ila[idx])
            wb_state_list.append(eq_expr)
        wb_state = And(wb_state_list)
        wb_list.append(wb_state)
    # wb = Or(wb_list)


    uf = []
    for k,v in sts_uf.named_var.items():
        if(str(k) == 'r0_next'):
            uf0 = v
        elif(str(k) == 'r1_next'):
            uf1 = v
        elif(str(k) == 'r2_next'):
            uf2 = v
        elif(str(k) == 'r3_next'):
            uf3 = v
    uf = [uf0, uf1, uf2, uf3]
    assert(len(uf) == 4)
    uf_new = []
    uf_substitute = {r0:ILA_r0, r1:ILA_r1, r2:ILA_r2, r3:ILA_r3}
    for ufx in uf:
        ufx_new = substitute(ufx, uf_substitute)
        uf_new.append(ufx_new)


    finish_state_list = []
    finish_list = []
    for reg_expr_list in inv_reg5:
        for idx in range(len(reg_expr_list)):
            assert(len(reg_expr_list) == len(uf_new))
            eq_expr = NotEquals(reg_expr_list[idx],uf_new[idx])
            finish_state_list.append(eq_expr)
        finish_state = And(finish_state_list)
        finish_list.append(finish_state)
    # finish = Or(finish_list)


    sat_check_list = []
    for idx in range(len(wb_list)):
        assert(len(wb_list) == len(finish_list))
        expr = And(wb_list[idx],finish_list[idx])
        sat_check_list.append(expr)
    sat_check = Or(sat_check_list)
    check_result = is_sat(sat_check)
    print(check_result)



    



    
if __name__ == '__main__':
  main()