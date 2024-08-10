# adapted from : https://github.com/pysmt/pysmt/blob/master/examples/smtlib.py
# NOTE: you need to install pysmt first
#       pip3 install pysmt
#

from io import StringIO
from pysmt.environment import get_env
from pysmt.smtlib.parser import SmtLibParser
from pysmt.smtlib.script import SmtLibCommand
from pysmt.typing import BVType
from pysmt.shortcuts import BVAdd
from pysmt.shortcuts import BVMul
from pysmt.shortcuts import BV

from pysmt.shortcuts import is_sat, substitute
from pysmt.shortcuts import And, Not, Or, Implies, BVOne, BVZero, EqualsOrIff #Implies 就是 imply，EqualsOrIff是equal
from pysmt.shortcuts import Ite
from pysmt.fnode import *
from pysmt.shortcuts import get_model

def tobool(e):
    return EqualsOrIff(e,BVOne(1))
    
def is_valid(e):
    return (not is_sat(Not(e)))

def get_invalid_model(e):
    return (get_model(Not(e)))

def sort_model(m):
    mstr = str(m)
    return ('\n'.join(sorted(mstr.split('\n'))))
    
    
# EXT_SMTLIB="""\

# (init (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvnot tag3) (bvnot tag2)) (ite (= #b0000 stage1) #b1 #b0)) (ite (= #b0000 stage2) #b1 #b0)) tag0) (bvnot tag1)) (bvnot wen_stage1)) (bvnot wen_stage2)) wen_stage3))

# (trans (let (($e1 (bvadd #b0001 (bvmul stage1 #b0010)))) (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvnot (bvand tag2 (bvnot (ite (= stage3 reg_v) #b1 #b0)))) (bvnot (bvand tag2.next (bvnot (ite (= stage3.next reg_v.next) #b1 #b0))))) (ite (= stage3.next (ite (= #b1 rst) w (ite (= #b1 wen_stage2) stage2 stage3))) #b1 #b0)) (ite (= tag3.next (bvand (bvnot rst) tag2)) #b1 #b0)) (ite (= reg_v_comp.next (bvadd (bvmul reg_v #b0010) #b0001)) #b1 #b0)) (ite (= tag2.next (bvand (bvnot rst) tag1)) #b1 #b0)) (ite (= reg_v.next (ite (= #b1 rst) reg_init reg_v)) #b1 #b0)) (ite (= stage1.next (ite (= #b1 rst) #b0000 (ite (= #b1 wen_stage1) $e1 stage3))) #b1 #b0)) (ite (= stage2.next (ite (= #b1 rst) #b0000 $e1)) #b1 #b0)) (ite (= rst tag0.next) #b1 #b0)) (ite (= tag1.next (bvand (bvnot rst) tag0)) #b1 #b0)) (ite (= wen_stage1.next (bvand (bvnot rst) wen_stage3)) #b1 #b0)) (ite (= wen_stage2.next (bvand (bvnot rst) wen_stage1)) #b1 #b0)) (ite (= wen_stage3.next (bvnot (bvand (bvnot rst) (bvnot wen_stage3)))) #b1 #b0)))
# )

# (expr (bvnot (bvand tag3 (bvnot (ite (= stage3 reg_v_comp) #b1 #b0)))))
# (expr (let (($e1 (= stage3 reg_v))) (let (($e2 (bvmul reg_v #b0010))) (let (($e3 (bvadd $e2 #b0001))) (let (($e4 (= $e2 (bvmul stage1 #b0010)))) (let (($e5 (= #b0000 $e2))) (let (($e6 (= reg_v stage2))) (bvand (bvnot (bvand tag3 (bvnot (ite (= stage3 reg_v_comp) #b1 #b0)))) (bvand (bvnot (bvand (ite $e5 #b1 #b0) (bvand (bvnot (ite $e4 #b1 #b0)) (bvand (ite $e1 #b1 #b0) (bvnot wen_stage2))))) (bvand (bvnot (bvand (bvnot (ite (= reg_v $e3) #b1 #b0)) (bvand tag2 (ite $e6 #b1 #b0)))) (bvand (bvnot (bvand (bvnot (ite $e5 #b1 #b0)) (bvand tag2 (ite (= stage2 #b0001) #b1 #b0)))) (bvand (bvnot (bvand tag2 (bvnot (ite (= stage2 $e3) #b1 #b0)))) (bvand (bvnot (bvand (bvnot (ite $e4 #b1 #b0)) (bvand (bvnot wen_stage2) (bvand (ite $e1 #b1 #b0) tag1)))) (bvand (bvnot (bvand tag0 wen_stage2)) (bvand (bvnot (bvand (ite $e6 #b1 #b0) (bvand wen_stage2 (bvnot (ite $e4 #b1 #b0))))) (bvand (bvnot (bvand wen_stage2 (ite (= stage1 #b0010) #b1 #b0))) (bvand (bvnot (ite (= stage2 #b0010) #b1 #b0)) (bvand (bvnot (bvand (ite $e6 #b1 #b0) (bvand (bvnot tag0) (ite $e5 #b1 #b0)))) (bvand (bvnot (bvand tag1 (bvnot wen_stage1))) (bvand wen_stage3 (bvand (bvnot (bvand tag2 (bvnot wen_stage2))) (bvand (bvnot (bvand tag2 (ite (= #b0000 stage2) #b1 #b0))) (bvnot (bvand tag2 (ite (= stage2 $e2) #b1 #b0)))))))))))))))))))))))))


# """

EXT_SMTLIB="""


(init (bvand (bvand (bvand (bvand (bvand wen_stage3 (bvnot tag3)) (bvnot (bvand wen_stage2 (bvnot wen_stage1)))) (bvnot tag2)) tag0) (bvnot tag1)))

(trans (let (($e1 (bvadd #b0001 (bvmul stage1 #b0010)))) (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand (bvand wen_stage3 wen_stage3.next) (bvnot (bvand wen_stage2 (bvnot wen_stage1)))) (bvnot (bvand wen_stage2.next (bvnot wen_stage1.next)))) (bvnot (bvand tag2 (bvnot (ite (= stage3 reg_v) #b1 #b0))))) (bvnot (bvand tag2.next (bvnot (ite (= stage3.next reg_v.next) #b1 #b0))))) (ite (= stage3.next (ite (= #b1 (bvand (bvnot rst) wen_stage2)) stage2 stage3)) #b1 #b0)) (ite (= tag3.next (bvand (bvnot rst) tag2)) #b1 #b0)) (ite (= reg_v_comp.next (bvadd (bvmul reg_v #b0010) #b0001)) #b1 #b0)) (ite (= wen_stage2.next (bvand (bvnot (bvand rst (bvnot wen_stage2))) (bvnot (bvand (bvnot rst) (bvnot wen_stage1))))) #b1 #b0)) (ite (= wen_stage1.next (bvand (bvnot (bvand rst (bvnot wen_stage1))) (bvnot (bvand (bvnot rst) (bvnot wen_stage3))))) #b1 #b0)) (ite (= tag2.next (bvand (bvnot rst) tag1)) #b1 #b0)) (ite (= reg_v.next (ite (= #b1 rst) reg_init reg_v)) #b1 #b0)) (ite (= stage1.next (ite (= #b1 rst) stage1 (ite (= #b1 wen_stage1) $e1 stage3))) #b1 #b0)) (ite (= stage2.next (ite (= #b1 rst) stage2 $e1)) #b1 #b0)) (ite (= rst tag0.next) #b1 #b0)) (ite (= tag1.next (bvand (bvnot rst) tag0)) #b1 #b0))))

(expr (bvnot (bvand tag3 (bvnot (ite (= stage3 reg_v_comp) #b1 #b0))))) 

(expr (let (($e1 (= stage3 reg_v))) (let (($e2 (bvmul reg_v #b0010))) (let (($e3 (bvadd $e2 #b0001))) (let (($e4 (bvmul stage1 #b0010))) (let (($e5 (bvadd #b0001 $e4))) (let (($e6 (= $e2 $e4))) (let (($e7 (= reg_v stage2))) (bvand (bvnot (bvand tag3 (bvnot (ite (= stage3 reg_v_comp) #b1 #b0)))) (bvand (bvnot (bvand (ite $e7 #b1 #b0) (bvand tag2 (bvnot (ite (= reg_v $e3) #b1 #b0))))) (bvand (bvnot (bvand (bvnot (ite $e6 #b1 #b0)) (bvand tag1 (bvand (bvnot wen_stage2) (ite $e1 #b1 #b0))))) (bvand (bvnot (bvand (ite (= stage2 $e5) #b1 #b0) (bvand (ite (= reg_v $e5) #b1 #b0) (bvand (bvnot (ite $e6 #b1 #b0)) (bvand wen_stage2 tag1))))) (bvand (bvnot (bvand (bvnot (ite (= stage2 $e3) #b1 #b0)) (bvand tag2 (bvnot tag1)))) (bvand (bvnot (bvand (ite $e7 #b1 #b0) (bvand (bvnot (ite $e6 #b1 #b0)) (bvand wen_stage2 (bvnot tag0))))) (bvand (bvnot (bvand (bvnot (ite $e6 #b1 #b0)) (bvand (ite $e1 #b1 #b0) (bvand (bvnot wen_stage2) (bvnot tag0))))) (bvand (bvnot (bvand (ite $e7 #b1 #b0) (bvand (bvnot tag0) (ite (= $e2 #b0000) #b1 #b0)))) (bvand (bvnot (bvand tag2 (ite (= stage2 #b0010) #b1 #b0))) (bvand (bvnot (bvand tag2 (ite (= stage2 $e2) #b1 #b0))) (bvand (bvnot (bvand (bvnot wen_stage1) tag1)) (bvnot (bvand (bvnot wen_stage2) tag2)))))))))))))))))))))
"""


class TSSmtLibParser(SmtLibParser):
    def __init__(self, env, interactive=False):
        SmtLibParser.__init__(self, env, interactive)

        # Add new commands
        #
        # The mapping function takes care of consuming the command
        # name from the input stream, e.g., '(init' . Therefore,
        # _cmd_init will receive the rest of the stream, in our
        # example, '(and A B)) ...'
        self.commands["init"] = self._cmd_init
        self.commands["trans"] = self._cmd_trans
        self.commands["expr"] = self._cmd_expr
        
        self.to_next = {}
        self.to_curr = {}
        
        
    def defsv(self,name,width):
        # define a state/input variable 
        # and also its next version
        sv = self.env.formula_manager.Symbol(name,BVType(width))
        svnxt = self.env.formula_manager.Symbol(name+'.next',BVType(width))
        self.cache.bind(name,sv)
        self.cache.bind(name+'.next',svnxt)
        
        self.to_next[sv]=svnxt
        self.to_curr[svnxt] = sv
        return (sv, svnxt)
    
    def _cmd_init(self, current, tokens):
        # This cmd performs the parsing of:
        #   <expr> )
        # and returns a new SmtLibCommand
        expr = self.get_expression(tokens)
        self.consume_closing(tokens, current)
        return SmtLibCommand(name="init", args=(expr,))
        
    def _cmd_trans(self, current, tokens):
        # This performs the same parsing as _cmd_init, but returns a
        # different object. The parser is not restricted to return
        # SmtLibCommand, but using them makes handling them
        # afterwards easier.
        expr = self.get_expression(tokens)
        self.consume_closing(tokens, current)
        return SmtLibCommand(name="trans", args=(expr,))
        
    def _cmd_expr(self, current, tokens):
        # This performs the same parsing as _cmd_init, but returns a
        # different object. The parser is not restricted to return
        # SmtLibCommand, but using them makes handling them
        # afterwards easier.
        expr = self.get_expression(tokens)
        self.consume_closing(tokens, current)
        return SmtLibCommand(name="expr", args=(expr,))


    def get_ts(self, script):
        # New Top-Level command that takes a script stream in input.
        # We return a pair (Init, Trans) that defines the symbolic
        # transition system.
        init = self.env.formula_manager.TRUE()
        trans = self.env.formula_manager.TRUE()
        exprlist = []

        for cmd in self.get_command_generator(script):
            if cmd.name=="init":
                init = cmd.args[0]
            elif cmd.name=="trans":
                trans = cmd.args[0]
            elif cmd.name=='expr':
                exprlist.append(cmd.args[0])
            else:
                # Ignore other commands
                pass
        return (init, trans, exprlist)


# Time to try out the parser !!!


# The new parser can parse our example, and returns the (init, trans) pair
env = get_env()
ts_parser = TSSmtLibParser(env)

tag0,_ = ts_parser.defsv('tag0',1)
tag1,_ = ts_parser.defsv('tag1',1)
tag2,_ = ts_parser.defsv('tag2',1)
tag3,_ = ts_parser.defsv('tag3',1)
tag4,_ = ts_parser.defsv('tag4',1)

stage1_go,_ = ts_parser.defsv('stage1_go',1)


reg_v,_ = ts_parser.defsv('reg_v',4)
reg_v_comp, _ = ts_parser.defsv('reg_v_comp',4)

stage1,_ = ts_parser.defsv('stage1',4)
stage2,_ = ts_parser.defsv('stage2',4)
stage3,_ = ts_parser.defsv('stage3',4)

wen_stage1,_ = ts_parser.defsv('wen_stage1',1)
wen_stage2,_ = ts_parser.defsv('wen_stage2',1)
# wen_stage3,_ = ts_parser.defsv('wen_stage3',1)

ts_parser.defsv('reg_init',4)
ts_parser.defsv('clk',1)
rst,_ = ts_parser.defsv('rst',1)
ts_parser.defsv('stall1in',1)
ts_parser.defsv('stall2in',1)
ts_parser.defsv('stall3in',1)
ts_parser.defsv('w',4)


init, trans, exprlist = ts_parser.get_ts(StringIO(EXT_SMTLIB))
print("INIT: %s" % init.serialize())
print("TRANS: %s" % trans.serialize())

prop = exprlist[0]
inv = exprlist[1]


init, trans, prop, inv = tobool(init), tobool(trans), tobool(prop), tobool(inv)
#print("INIT_tobool: %s" % init.serialize())

v1,v1n = ts_parser.defsv('v1',1)
v2,v2n = ts_parser.defsv('v2',1)

# v3,v3n = ts_parser.defsv('v3',1)

a,an = ts_parser.defsv('a',4) 
b,bn = ts_parser.defsv('b',4)
c,cn = ts_parser.defsv('c',4)
#print("a: %s" % a.serialize())
#print("an: %s" % an.serialize())

# init = And([init, 
#     EqualsOrIff(v1,wen_stage1), EqualsOrIff(v2,wen_stage2), EqualsOrIff(v3,wen_stage3),
#     EqualsOrIff(a,stage1), EqualsOrIff(b,stage2), EqualsOrIff(c,stage3)])

init_new = And([init, 
    EqualsOrIff(v1,wen_stage1), EqualsOrIff(v2,wen_stage2),
    EqualsOrIff(a,stage1), EqualsOrIff(b,stage2), EqualsOrIff(c,stage3),

    EqualsOrIff(rst, BV(0,1))])

# trans = And([trans, 
#     EqualsOrIff(v1n,v1), EqualsOrIff(v2n,v2), EqualsOrIff(v3n,v3),
#     EqualsOrIff(a,an), EqualsOrIff(b,bn), EqualsOrIff(c,cn)])

trans_new = And([trans, 
    EqualsOrIff(v1n,v1), EqualsOrIff(v2n,v2),
    EqualsOrIff(an,a), EqualsOrIff(bn,b), EqualsOrIff(cn,c),

    EqualsOrIff(rst, BV(0,1))])


#inv_new = 
    # tag0 |-> wen_stage1 == v1 /\ ... /\ ...
    # tag1 |-> wen_stage1 == ite(...) /\ ...
    # tag2 |-> ...

#tag0, tag1, tag2, tag3, tag4 = tobool(tag0), tobool(tag1), tobool(tag2), tobool(tag3), tobool(tag4)

# inv_new = And(
#     Or(Not(tag0),And(EqualsOrIff(v1,wen_stage1), EqualsOrIff(v2,wen_stage2), EqualsOrIff(v3,wen_stage3),
#     EqualsOrIff(a,stage1), EqualsOrIff(b,stage2), EqualsOrIff(c,stage3))),

#     Or(Not(tag1),And(EqualsOrIff(v3,wen_stage1), EqualsOrIff(v1,wen_stage2), EqualsOrIff(v3,wen_stage3),
#     EqualsOrIff(Ite(tobool(v1),2*a+1,c),stage1), EqualsOrIff((2*a+1),stage2), EqualsOrIff((Ite(tobool(v2),b,c)),stage3))),

#     Or(Not(tag2),And(EqualsOrIff(v3,wen_stage1), EqualsOrIff(v3,wen_stage2), EqualsOrIff(v3,wen_stage3),
#     EqualsOrIff(2*(Ite(tobool(v1),2*a+1,c))+1,stage1), EqualsOrIff(2*(Ite(tobool(v1),2*a+1,c))+1,stage2), EqualsOrIff((Ite(tobool(v1),2*a+1,c)),stage3))),

#     Or(Not(tag3),And(EqualsOrIff(v3,wen_stage1), EqualsOrIff(v1,wen_stage2), EqualsOrIff(v3,wen_stage3),
#     EqualsOrIff(4*(Ite(tobool(v1),2*a+1,c))+3,stage1), EqualsOrIff(4*(Ite(tobool(v1),2*a+1,c))+3,stage2), EqualsOrIff(2*(Ite(tobool(v1),2*a+1,c))+1,stage3))),
# )

#why implies?
#And(
# (tag0 |-> And(xx,xx,...) , (tag1 |-> And(xx,xx,...) , (tag2 |-> And(xx,xx,...) , (tag3 |-> And(xx,xx,...) ,
#   assume property (~(tag2 ) || (reg_v == stage3));
#   assert property (~(tag3 ) || (reg_v_comp == stage3));
# )

# inv_new = And( 
#     Implies(
#         (tag0),And(EqualsOrIff(v1,wen_stage1), EqualsOrIff(v2,wen_stage2), EqualsOrIff(v3,wen_stage3),
#     EqualsOrIff(a,stage1), EqualsOrIff(b,stage2), EqualsOrIff(c,stage3))
#     ),

#     Implies((tag1),And(EqualsOrIff(v3,wen_stage1), EqualsOrIff(v1,wen_stage2), EqualsOrIff(v3,wen_stage3),
#     EqualsOrIff(Ite(tobool(v1),2*a+1,c),stage1), EqualsOrIff((2*a+1),stage2), EqualsOrIff((Ite(tobool(v2),b,c)),stage3))),

#     Implies((tag2),And(EqualsOrIff(v3,wen_stage1), EqualsOrIff(v3,wen_stage2), EqualsOrIff(v3,wen_stage3),
#     EqualsOrIff(2*(Ite(tobool(v1),2*a+1,c))+1,stage1), EqualsOrIff(2*(Ite(tobool(v1),2*a+1,c))+1,stage2), EqualsOrIff((Ite(tobool(v1),2*a+1,c)),stage3))),

#     Implies((tag3),And(EqualsOrIff(v3,wen_stage1), EqualsOrIff(v3,wen_stage2), EqualsOrIff(v3,wen_stage3),
#     EqualsOrIff(4*(Ite(tobool(v1),2*a+1,c))+3,stage1), EqualsOrIff(4*(Ite(tobool(v1),2*a+1,c))+3,stage2), EqualsOrIff(2*(Ite(tobool(v1),2*a+1,c))+1,stage3))),
    
#     Implies(EqualsOrIff(v2,BV(1,1)), EqualsOrIff(v1,BV(1,1))),
#     Implies(Or(tag2,tag3), EqualsOrIff(reg_v,(Ite(tobool(v1),2*a+1,c)))),
#     Implies(Or(tag1,tag2,tag3), EqualsOrIff(reg_v_comp,reg_v*2+1)),
# )

#check(3 states)
inv_new = And(EqualsOrIff(stage1_go,BV(0,1)),
Or(
    And(EqualsOrIff(v1,wen_stage1),EqualsOrIff(v2,wen_stage2),EqualsOrIff(a,stage1),EqualsOrIff(b,stage2),EqualsOrIff(c,stage3)),
    And(EqualsOrIff(Ite(tobool(v1),BV(0,1),v1),wen_stage1),EqualsOrIff(Ite(tobool(v1),v1,Ite(tobool(v2),BV(0,1),v2)),wen_stage2),EqualsOrIff(a,stage1),EqualsOrIff(Ite(tobool(v1),((a*2)+1),b),stage2),EqualsOrIff(Ite(tobool(v2),Ite(tobool(v2),b,c),c),stage3)),
    And(EqualsOrIff(Ite(tobool(v1),BV(0,1),v1),wen_stage1),EqualsOrIff(v2,wen_stage2),EqualsOrIff(a,stage1),EqualsOrIff(Ite(tobool(v1),((a*2)+1),b),stage2),EqualsOrIff(c,stage3)),
)
)

print("inv_new is: ",inv_new)


inv_prime = substitute(inv_new, ts_parser.to_next)
prop_prime = substitute(prop, ts_parser.to_next)

# forall V, init(V) => inv(V)
print (is_valid(Implies(init_new, inv_new)))

# forall V V', trans(V,V') /\ inv(V) => inv(V')
print (is_valid(Implies(And(trans_new,inv_new), inv_prime)))
print("counter example\n", sort_model(get_invalid_model(Implies(And(trans_new,inv_new), inv_prime))))

# forall V, inv(V) => prop(V)
print (is_valid(Implies(inv_new, prop)))
print("counter example 2\n", sort_model(get_invalid_model(Implies(inv_new, prop))))

# forall V V', trans(V,V') /\ prop(V) =/=> prop(V') 
# namely, `prop` it self is not inductive
# print (is_valid(Implies(And(prop,inv_new), prop_prime )))

'''
counter example 

a := 0_4
a.next := 0_4
b := 13_4
b.next := 13_4
c := 5_4
c.next := 5_4
reg_init := 0_4
reg_v := 13_4
reg_v.next := 13_4
reg_v_comp.next := 11_4
rst := 0_1
stage1 := 5_4
stage1.next := 11_4
stage2 := 1_4
stage2.next := 11_4
stage3 := 13_4
stage3.next := 13_4
tag0 := 0_1
tag0.next := 0_1
tag1 := 1_1
tag1.next := 0_1
tag2 := 0_1
tag2.next := 1_1
tag3 := 0_1
tag3.next := 0_1
v1 := 0_1
v1.next := 0_1
v2 := 1_1
v2.next := 1_1
tag1.next := 0_1
tag0.next := 1_1
stage3 := 8_4
c := 0_4
a := 8_4
v1 := 1_1
stage2 := 0_4
stage1 := 0_4
wen_stage3 := 1_1
v3 := 1_1
v3.next := 1_1
wen_stage1 := 1_1
wen_stage1.next := 1_1
wen_stage2 := 0_1
wen_stage2.next := 1_1
wen_stage3 := 1_1
wen_stage3.next := 1_1



counter example 2

a := 0_4
b := 0_4
c := 0_4
reg_v_comp := 0_4
stage1 := 3_4
stage2 := 3_4
stage3 := 1_4
tag0 := 0_1
tag1 := 0_1
tag2 := 0_1
tag3 := 1_1
v1 := 0_1
v2 := 0_1
v3 := 0_1
wen_stage1 := 0_1
wen_stage2 := 0_1
wen_stage3 := 0_1
'''
