from asyncore import write
from re import S
from pysmt.shortcuts import substitute, get_free_variables, serialize, Ite, BV
from pysmt.smtlib.printers import to_smtlib
from pysmt.smtlib.parser import SmtLibParser
from symsim import And
import os, linecache
from six import StringIO
from pysmt.smtlib.script import SmtLibCommand
from pysmt.type_checker import SimpleTypeChecker
import re, copy


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
    if (os.path.exists("sygus_result_temp.smt2")):
        os.remove("sygus_result_temp.smt2")
    os.system('cvc5 --lang=sygus2 sygus_template.sygus > sygus_result_temp.smt2')
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
    
def sygus_simplify(state, set_of_xvar):
    for s, v in state.sv.items():
        if expr_contains_X(v,
                           set_of_xvar):  # HZ : ('X' in str(v.serialize())) is not safe, what if the Verilog variable name contains X ?
            arg = v.args()
            # HZ: TODO: in the future, we need to make this part more generic!
            if ((v.is_ite) and (len(arg) == 3)):  # for Ite structure
                # input()

                v_arg_list = []
                for v_arg in arg:
                    if expr_contains_X(v_arg, set_of_xvar):
                        #  (variables in v, variables in asmpt, asmpt, expr to handle, return type)
                        (free_var, free_var_asmpt, asmpt_and_smtlib, Fun, Fun_type) = parse_state(state, v_arg)
                        print('Running sygus simplify!')
                        new_expr_part = run_sygus(free_var, free_var_asmpt, asmpt_and_smtlib, Fun, Fun_type,
                                                  set_of_xvar)
                        v_arg = new_expr_part
                        print('sygus simplify finish!')
                        # print('simplified fun part: ',new_expr_part)
                    v_arg_list.append(v_arg)
                new_expr = Ite(v_arg_list[0], v_arg_list[1], v_arg_list[2])
                print('new_expr', new_expr.simplify())

            # elif(): #for other structures, future work
            #   pass

            else:
                print(v)
                print('not ite structure!')
                (free_var, free_var_asmpt, asmpt_and_smtlib, Fun, Fun_type) = parse_state(state, v)
                print('Running sygus simplify!')
                new_expr = run_sygus(free_var, free_var_asmpt, asmpt_and_smtlib, Fun, Fun_type, set_of_xvar)
                print('Fun new:', new_expr.serialize())
                print('sygus simplify finish!')

            new_sv_dic = {s: new_expr.simplify()}
            state.sv.update(new_sv_dic)
    print('updated state!')

    if (os.path.exists("sygus_template.sygus") and os.path.exists("sygus_result.smt2")):
        os.remove("sygus_template.sygus")
        os.remove("sygus_result.smt2")
        os.remove("sygus_result_temp.smt2")
