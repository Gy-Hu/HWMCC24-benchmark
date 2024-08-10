from asyncore import write
from re import S
from pysmt.operators import all_types, op_to_str
from pysmt.shortcuts import substitute, get_free_variables, serialize, Ite, BV, EqualsOrIff, get_type, BVConcat, And, Or, BVNot, BVComp
from pysmt.shortcuts import *
from pysmt.smtlib.printers import to_smtlib
from pysmt.smtlib.parser import SmtLibParser
from symsim import And
import os, linecache
from six import StringIO
from pysmt.smtlib.script import SmtLibCommand
from pysmt.type_checker import SimpleTypeChecker
import re, copy
from ast import arg
import threading
import time

import subprocess
import os
import signal
 
def run_cmd(cmd_string, timeout):
    p = subprocess.Popen(cmd_string, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True, close_fds=True,
                         preexec_fn=os.setsid)
    try:
        (msg, errs) = p.communicate(timeout=timeout)
        ret_code = p.poll()
        if ret_code:
            code = 1
            msg = "[Error]Called Error : " + str(msg.decode('utf-8'))
        else:
            code = 0
            msg = str(msg.decode('utf-8'))
    except subprocess.TimeoutExpired:
        p.kill()
        p.terminate()
        os.killpg(p.pid, signal.SIGTERM)
 
        
        # (outs, errs) = p.communicate()
        # print(outs.decode('utf-8'))
 
        code = 1
        msg = "[ERROR]Timeout Error : Command '" + cmd_string + "' timed out after " + str(timeout) + " seconds"
        timeout_flag = 111
        print(msg)
        # input()
    except Exception as e:
        code = 1
        msg = "[ERROR]Unknown Error : " + str(e)
        print(msg)
        # input()
 
    return code, msg
# class MyThread(threading.Thread):
#   def __init__(self, func, args0, args1, args2, args3, args4, args5):
#     super(MyThread, self).__init__()
#     self.func = func
#     self.args0 = args0
#     self.args1 = args1
#     self.args2 = args2
#     self.args3 = args3
#     self.args4 = args4
#     self.args5 = args5

#   def run(self):
#     self.result = self.func(self.args0, self.args1, self.args2, self.args3, self.args4, self.args5)

#   def get_result(self):
#     try:
#       return self.result
#     except Exception:
#       return None
  
# # def func1(txt, txt2):
# #   time.sleep(2)
# #   print(str(txt)+str(txt2)+'not return')
# #   return(str(txt)+str(txt2)+'return')


class TSSmtLibParser(SmtLibParser):
    def __init__(self, env=None, interactive=False):
        SmtLibParser.__init__(self, env, interactive)

        del self.commands["define-fun"]
        self.commands["define-fun"] = self._cmd_define_fun

        self.interpreted["next"] = self._operator_adapter(self._next_var)

    def _cmd_define_fun(self, current, tokens):  # the old version without name binding
        """(define-fun <fun_def>)"""
        formal = []
        var = self.parse_atom(tokens, current)
        namedparams = self.parse_named_params(tokens, current)
        rtype = self.parse_type(tokens, current)
        for (x, t) in namedparams:
            v = self._get_var(x, t)
            self.cache.bind(x, v)
            formal.append(v)
        ebody = self.get_expression(tokens)

        self.consume_closing(tokens, current)
        self.cache.define(var, formal, ebody)
        return SmtLibCommand(current, [var, formal, rtype, ebody])

    def _next_var(self, symbol):
        if symbol.is_symbol():
            name = symbol.symbol_name()
            ty = symbol.symbol_type()
            return self.env.formula_manager.Symbol("next_" + name, ty)
        else:
            raise ValueError("'next' operator can be applied only to symbols")

    def get_ts(self, script):
        dff = self.env.formula_manager.TRUE()

        for cmd in self.get_command_generator(script):
            if cmd.name == "define-fun":
                dff = cmd.args[3]
            else:
                # Ignore other commands
                pass

        return dff

    def get_ts_fname(self, script_fname):
        """Given a filename and a Solver, executes the solver on the file."""
        with open(script_fname) as script:
            return self.get_ts(script)


def parse_state(state, v):  # transform to smtlib format and get the expression that sygus template needs
    # 1.parse the expression with X (pysmt.fnode --> smtlib)
    asmpt_and = And(state.asmpt)
    free_var_asmpt = get_free_variables(asmpt_and)
    asmpt_and_smtlib = to_smtlib(asmpt_and)
    # print('asmpt_and',asmpt_and)
    Fun = to_smtlib(v)
    print('Fun to be simplified:', v.serialize())
    free_var = get_free_variables(v)
    type_checker = SimpleTypeChecker()
    Fun_type_init = type_checker.get_type(v)
    if ('BV' in str(Fun_type_init)):
        bv_width = re.findall("\d", str(Fun_type_init))
        Fun_type = '(_ BitVec ' + str(bv_width[0]) + ')'
    else:
        Fun_type = str(Fun_type_init)
    #  (variables in v, variables in asmpt, asmpt, expr to handle, return type)
    return (free_var, free_var_asmpt, asmpt_and_smtlib, Fun, Fun_type)


def run_sygus(free_var, free_var_asmpt, asmpt_and_smtlib, Fun, Fun_type,
              set_of_xvar):  # write sygus script --> run sygus simplify --> return new expression (FunNew) in pysmt format
    # 2.write the sygus script
    with open("sygus_template.sygus", "w") as f:
        line1 = '(set-logic BV)\n\n\n(synth-fun FunNew \n   (\n'
        f.write(line1)
        line2 = '    ({name} (_ BitVec {width}) )\n'

        for var in free_var:
            if var not in set_of_xvar:  # ('X' not in str(var.serialize())):
                var_name = str(var.serialize())
                var_width = str(var.bv_width())

                f.write(line2.format(name=var_name, width=var_width))
        line3 = '   )\n   {fun_type}\n  )\n\n\n\n'
        f.write(line3.format(fun_type=Fun_type))

        line4 = '(declare-var {name} (_ BitVec {width}))\n'
        for var in free_var_asmpt:
            var_name = str(var.serialize())
            var_width = str(var.bv_width())
            f.write(line4.format(name=var_name, width=var_width))

        for var in free_var:
            if var not in free_var_asmpt:
                var_name = str(var.serialize())
                var_width = str(var.bv_width())
                f.write(line4.format(name=var_name, width=var_width))

        line5 = '\n(constraint (=> \n'
        f.write(line5)

        line6 = '    {0} ;\n\n    (=\n'.format(asmpt_and_smtlib)  # assumption_and
        f.write(line6)

        line7 = '        {fun} ;\n        (FunNew '.format(fun=Fun)
        f.write(line7)

        for var in free_var:
            if var not in set_of_xvar:  # ('X' not in str(var.serialize())):
                line8 = '{0} '.format(str(var.serialize()))
                f.write(line8)

        line9 = ') ;\n    )))\n\n\n;\n\n(check-synth)\n'
        f.write(line9)

    # 3.run sygus simplify and transform the FunNew(smtlib) to pysmt.fnode
    # if (os.path.exists("sygus_result_temp.smt2")):
    #     os.remove("sygus_result_temp.smt2")
    run_cmd('cvc5 --lang=sygus2 sygus_template.sygus > sygus_result_temp.smt2', timeout= 1)
    # os.system('cvc5 --lang=sygus2 sygus_template.sygus > sygus_result_temp.smt2')
    linecache.clearcache()  ### remember to clear cache before reuse this linecache!!
    line_11 = linecache.getline("sygus_result_temp.smt2", 2).strip()

    # print(line)
    with open("sygus_result.smt2", "w") as f:
        f.write(line_11)

    smtlib_result = "sygus_result.smt2"

    ts_parser = TSSmtLibParser()
    new_expr = ts_parser.get_ts_fname(smtlib_result)

    return new_expr


def expr_contains_X(expr, set_of_xvar) -> bool:
    vars_in_expr = get_free_variables(expr)
    return any([var in set_of_xvar for var in vars_in_expr])

def child_list_simplify(child_list, state, set_of_xvar):
    child_new_list = []
    for child in child_list:
        if expr_contains_X(child, set_of_xvar):
            #  (variables in v, variables in asmpt, asmpt, expr to handle, return type)
            (free_var, free_var_asmpt, asmpt_and_smtlib, Fun, Fun_type) = parse_state(state, child)
            print('Running sygus simplify!')
            # run_cmd()
            
            new_expr_part = run_sygus(free_var, free_var_asmpt, asmpt_and_smtlib, Fun, Fun_type, set_of_xvar)
            if(str(new_expr_part) == 'True'):
                new_expr_part = structure_simplify(child, state, set_of_xvar)
                # assert False
            elif(str(new_expr_part) == 'False'):
                new_expr_part = structure_simplify(child, state, set_of_xvar)
                print(new_expr_part)
                input()
                # new_expr_part = structure_simplify(child, state, set_of_xvar)
            child = new_expr_part
            print('simplified fun part: ',new_expr_part)
        child_new_list.append(child)
    print(child_new_list)
    return child_new_list

def structure_simplify_new(v, state, set_of_xvar):
    child_list = v.args()
    num_of_args = len(child_list)
    child_new_list = child_list_simplify(child_list, state, set_of_xvar)
    # num of args == 1
    if(num_of_args == 1):
        pass
    elif(num_of_args == 2):
        if(v.is_equals()):
            oper = EqualsOrIff
        elif(v.is_bv_concat()):
            oper = BVConcat
        
        new_expr = oper(child_new_list[0], child_new_list[1])
    elif(num_of_args == 3):
        if(v.is_ite()):
            oper = Ite
        
        new_expr = oper(child_new_list[0], child_new_list[1], child_new_list[2])


def structure_simplify(v, state, set_of_xvar):
    child_list = v.args()
    child_new_list = child_list_simplify(child_list, state, set_of_xvar)
    if ((v.is_ite()) and (len(child_list) == 3)):       
        new_expr = Ite(child_new_list[0], child_new_list[1], child_new_list[2])
    elif((v.is_equals()) and (len(child_list) == 2)):
        new_expr = EqualsOrIff(child_new_list[0], child_new_list[1])
    elif((v.is_bv_concat()) and (len(child_list) == 2)):
        new_expr = BVConcat(child_new_list[0], child_new_list[1])
    elif((v.is_and()) and (len(child_list) == 2)):
        new_expr = And(child_new_list[0], child_new_list[1])
    elif((v.is_or()) and (len(child_list) == 2)):
        new_expr = Or(child_new_list[0], child_new_list[1])
    elif((v.is_bv_not()) and (len(child_list) == 1)):
        new_expr = BVNot(child_new_list[0])
    elif((v.is_bv_comp()) and (len(child_list) == 2)):
        new_expr = BVComp(child_new_list[0], child_new_list[1])
    else:
        print('not ite structure!')
        (free_var, free_var_asmpt, asmpt_and_smtlib, Fun, Fun_type) = parse_state(state, v)
        print('Running sygus simplify!')
        new_expr = run_sygus(free_var, free_var_asmpt, asmpt_and_smtlib, Fun, Fun_type, set_of_xvar)
        if((str(new_expr) == 'True') or (str(new_expr) == 'False')):
            # assert False
            print('new structure?\n',v.serialize())
            print('node type num: ',v.node_type())
            print('node type: ',op_to_str(v.node_type()))
            print('num of args: ',len(v.args()))
            input()
            pass
        print('Fun new:', new_expr.serialize())
        print('sygus simplify finish!')
    
    return new_expr
    
    
def sygus_simplify(state, set_of_xvar):
    for s, v in state.sv.items():
        
        if expr_contains_X(v,
                           set_of_xvar):  # HZ : ('X' in str(v.serialize())) is not safe, what if the Verilog variable name contains X ?
            new_expr = structure_simplify(v, state, set_of_xvar)
            new_sv_dic = {s: new_expr.simplify()}
            state.sv.update(new_sv_dic)
    print('updated state!')

    if (os.path.exists("sygus_template.sygus") and os.path.exists("sygus_result.smt2")):
        os.remove("sygus_template.sygus")
        os.remove("sygus_result.smt2")
        os.remove("sygus_result_temp.smt2")
