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


    
    def _cmd_define_fun(self, current, tokens):  #the old version without name binding
        """(define-fun <fun_def>)"""
        formal = []
        var = self.parse_atom(tokens, current)
        namedparams = self.parse_named_params(tokens, current)
        rtype = self.parse_type(tokens, current)
        for (x,t) in namedparams:
            v = self._get_var(x,t)
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
            if cmd.name=="define-fun":
                dff = cmd.args[3]
            else:
                # Ignore other commands
                pass

        return dff
    
    def get_ts_fname(self, script_fname):
        """Given a filename and a Solver, executes the solver on the file."""
        with open (script_fname) as script:
            return self.get_ts(script)


    

smtlib_result = "sygus_result.smt2"
result = "(define-fun FunNew ((v2 (_ BitVec 1)) (w2 (_ BitVec 1))) Bool (bvult #b0 w2))"

ts_parser = TSSmtLibParser()
new_expr = ts_parser.get_ts_fname(smtlib_result)
# new_expr = ts_parser.get_ts(result)
print(new_expr)
print(type(new_expr))
arg = new_expr.args()
print(arg)
print(new_expr.is_bv_ult())     
