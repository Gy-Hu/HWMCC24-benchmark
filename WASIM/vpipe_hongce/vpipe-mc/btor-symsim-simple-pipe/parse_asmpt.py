from time import pthread_getcpuclockid
from inv_group_new import *
from cex_parser import cex_parser
from pysmt.rewritings import conjunctive_partition
from pysmt.shortcuts import BVComp, Ite

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

def scb_ite(con_v, con_w, rd, num_rd):
    con_rd = EqualsOrIff(BVComp(rd, num_rd), BV(1,1))
    ite3 = Ite(con_rd, BV(1,1), BV(0,1))
    ite2 = Ite(con_w, ite3, BV(0,1))
    ite1 = Ite(con_v, ite2, BV(0,1))
    return ite1

def substitue_state_asmpt(state_asmpt,symelement):
    v1, v2, w1, w2, inst, reg0, reg1, reg2, reg3, rd1, rd2 = symelement
    v1_bool, v2_bool, w1_bool, w2_bool= tobvcomp(v1), tobvcomp(v2), tobvcomp(w1), tobvcomp(w2)
    con_v1, con_v2, con_w1, con_w2 = EqualsOrIff(v1_bool,BV(1,1)), EqualsOrIff(v2_bool,BV(1,1)), EqualsOrIff(w1_bool,BV(1,1)), EqualsOrIff(w2_bool,BV(1,1))
    for k, v in state_asmpt.items():
        if(str(k.serialize()) == '__ILA_I_inst'):
            state_asmpt[k] = inst
        elif(str(k.serialize()) == "'RTL_scoreboard[0]'[1:1]"):
            state_asmpt[k] = scb_ite(con_v=con_v1, con_w=con_w1, rd=rd1, num_rd=BV(0,2))
        elif(str(k.serialize()) == "'RTL_scoreboard[0]'[0:0]"):
            state_asmpt[k] = scb_ite(con_v=con_v2, con_w=con_w2, rd=rd2, num_rd=BV(0,2))
        elif(str(k.serialize()) == "'RTL_scoreboard[1]'[1:1]"):
            state_asmpt[k] = scb_ite(con_v=con_v1, con_w=con_w1, rd=rd1, num_rd=BV(1,2))
        elif(str(k.serialize()) == "'RTL_scoreboard[1]'[0:0]"):
            state_asmpt[k] = scb_ite(con_v=con_v2, con_w=con_w2, rd=rd2, num_rd=BV(1,2))
        elif(str(k.serialize()) == "'RTL_scoreboard[2]'[1:1]"):
            state_asmpt[k] = scb_ite(con_v=con_v1, con_w=con_w1, rd=rd1, num_rd=BV(2,2))
        elif(str(k.serialize()) == "'RTL_scoreboard[2]'[0:0]"):
            state_asmpt[k] = scb_ite(con_v=con_v2, con_w=con_w2, rd=rd2, num_rd=BV(2,2))
        elif(str(k.serialize()) == "'RTL_scoreboard[3]'[1:1]"):
            state_asmpt[k] = scb_ite(con_v=con_v1, con_w=con_w1, rd=rd1, num_rd=BV(3,2))
        elif(str(k.serialize()) == "'RTL_scoreboard[3]'[0:0]"):
            state_asmpt[k] = scb_ite(con_v=con_v2, con_w=con_w2, rd=rd2, num_rd=BV(3,2))
        elif(str(k.serialize()) == '__auxvar0__recorder'):
            state_asmpt[k] = reg0
        elif(str(k.serialize()) == '__auxvar1__recorder'):
            state_asmpt[k] = reg1
        elif(str(k.serialize()) == '__auxvar2__recorder'):
            state_asmpt[k] = reg2
        elif(str(k.serialize()) == '__auxvar3__recorder'):
            state_asmpt[k] = reg3
        elif(str(k.serialize()) == 'ILA_r0'):
            state_asmpt[k] = reg0
        elif(str(k.serialize()) == 'ILA_r1'):
            state_asmpt[k] = reg1
        elif(str(k.serialize()) == 'ILA_r2'):
            state_asmpt[k] = reg2
        elif(str(k.serialize()) == 'ILA_r3'):
            state_asmpt[k] = reg3
    
    return state_asmpt
    

def tobvcomp(e):
    return BVComp(e,BV(1,1))

def main():
    file_name = "/home/fwj/vpipe-mc/btor-symsim-simple-pipe/branch_list_with_rst.pkl"
    open_file = open(file_name,"rb")
    branch_list = pickle.load(open_file)

    init_dict = {
    'RTL_id_ex_operand1':'oper1',
    'RTL_id_ex_operand2':'oper1',
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
    }
   
    btor_parser = BTOR2Parser()
    sts, _ = btor_parser.parse_file(Path("/home/fwj/vpipe-mc/btor-symsim-simple-pipe/problem.btor2"))
    executor = SymbolicExecutor(sts)

    #get free variable
    state_list_init =  branch_list[0]
    state_init = state_list_init[0]
    state_init.print()
    state_init.print_assumptions()

    state_expr_single = []
    for var,expr in state_init.sv.items():
        state_expr_single.append(EqualsOrIff(var, expr))
    state_expr = And(state_expr_single)
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
    if( (str(oper1)!='oper1') and (str(oper2)!='oper2') and (str(op)!='op') and (str(rd1)!='rd1') and (str(w1)!='w1') and \
        (str(ex_val)!='ex_val') and (str(rd2)!='rd2') and (str(w2)!='w2') and (str(v1)!='v1') and (str(v2)!='v2') and \
        (str(reg0)!='reg0') and (str(reg1)!='reg1') and (str(reg2)!='reg2') and (str(reg3)!='reg3') and (str(s0)!='s0') and \
        (str(s1)!='s1') and (str(s2)!='s2') and (str(s3)!='s3') and (str(inst)!='inst') and (str(inst_v)!='inst_v')    ):
        assert False


    symelement = [v1, v2, w1, w2, inst, reg0, reg1, reg2, reg3, rd1, rd2]
    # print(len(symelement))
    # print(symelement)
    start = tobool(executor.sv('__START__'))
    assume  = sts.assumption

    state_asmpt = {}
    arg_check(assume, state_asmpt)
    state_asmpt = substitue_state_asmpt(state_asmpt, symelement)
    print(state_asmpt)

    expr_list = []
    for k,v in state_asmpt.items():
        # if (str(k.serialize()) in str(list(state_init.sv))):
        # if(('ILA_r' not in str(k.serialize())) and ('__ILA_I_inst[6:7]' not in str(k.serialize()))):
        # if(('__ILA_I_inst[6:7]' not in str(k.serialize()))):
            expr = EqualsOrIff(k, v)
            expr_list.append(expr)
    asmpt_init = Implies(start, And(expr_list))
    print(asmpt_init)


    

    


    


if __name__ == '__main__':
  main()