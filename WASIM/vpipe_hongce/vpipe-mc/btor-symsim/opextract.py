# this is to walk the ITP and get the useful constants, bvoperators
import pysmt.operators as op
from pysmt.walkers.dag import DagWalker

# future work : deal with memories


op_str_map = dict([
    (op.EQUALS,'='),
    (op.BV_COMP,'='),
    (op.IFF,'='),

    (op.AND,'and'),
    (op.OR,'or'),
    (op.IMPLIES,'=>'),

    (op.NOT,'not'),
    (op.BV_NOT,'bvnot'),
    (op.BV_NEG,'bvneg'),

    (op.BV_AND,'bvand'),
    (op.BV_OR,'bvor'),
    (op.BV_XOR,'bvxor'),

    (op.BV_ADD,'bvadd'),
    (op.BV_SUB,'bvsub'),
    (op.BV_MUL,'bvmul'),
    (op.BV_UDIV,'bvudiv'),
    (op.BV_UREM,'bvurem'),
    (op.BV_SDIV,'bvsdiv'),
    (op.BV_SREM,'bvsrem'),
    (op.BV_ASHR,'bvashr'),
    (op.BV_LSHL,'bvshl'),
    (op.BV_LSHR,'bvlshr'),

    # no concat, no extract
    (op.BV_ULT,'bvult'),
    (op.BV_ULE,'bvule'),
    (op.BV_SLT,'bvslt'),
    (op.BV_SLE,'bvsle'),

    (op.BV_ROL,'rotate_left'), 
    (op.BV_ROR,'rotate_right'),

    (op.BV_ZEXT,'zero_extend'),
    (op.BV_SEXT,'sign_extend')
    ])

unary_op = set([op.NOT, op.BV_NOT, op.BV_NEG])
arithm_op = set([op.BV_AND, op.BV_OR, op.BV_XOR, op.BV_ADD, op.BV_SUB, op.BV_MUL, \
    op.BV_UDIV, op.BV_UREM, op.BV_SDIV, op.BV_SREM, op.BV_ASHR, op.BV_LSHL, op.BV_LSHR, \
    op.AND, op.OR, op.IMPLIES])
comp_op = set([op.BV_ULT,op.BV_ULE,op.BV_SLT,op.BV_SLE, op.BV_COMP,op.EQUALS,op.IFF])
rotate_op = set([op.BV_ROL,op.BV_ROR])
extend_op = set([op.BV_ZEXT,op.BV_SEXT])


def _const_to_str(fn):
  if fn.is_bv_constant():
    return '#b' + fn.bv_str()
  elif fn.is_bool_constant():
    return 'true' if fn.is_true() else 'false'
  assert (False) # unknown type


class VarExtractor(DagWalker):
    def __init__(self, env=None, invalidate_memoization=None):

        # 0 for bool
        self.Symbols = set([])
        # comp/eq --> '='

        # no need to worry about variables
        VarExtractor.set_handler(OpExtractor.walk_nop, *op.ALL_TYPES)
        VarExtractor.set_handler(OpExtractor.walk_symbol_rec, op.SYMBOL)

        # the above must be done first

        DagWalker.__init__(self,
                           env=env,
                           invalidate_memoization=invalidate_memoization)

    def walk_symbol_rec(self, formula, args, **kwargs):
        self.Symbols.add( formula )
                               
    def walk_nop(self, formula, args, **kwargs):
        pass # do nothing



class OpExtractor(DagWalker):
    def __init__(self, env=None, invalidate_memoization=None):

        # 0 for bool
        self.BvUnary = {}    # width -> set[ops] (op convert to strings)
        self.BvOps = {}      # you need to know the width also : width -> set[ops] (same width)
        self.BvComps = {}    # you need to know the width also : width -> set[ops] (same width)
        self.BvConsts = {}   # width -> set[consts (should be string already)] # const eq?
        self.BvConcats = {}  # result width -> set[(width1, width2)]
        self.BvExtracts = {} # result width -> set[(input width, h, l)]
        self.BvRotates = {}   # result width -> set[(op, param)]
        self.BvExts = {}     # result width -> set[(op, param， input width )] op 
        self.Symbols = set([])
        # comp/eq --> '='

        # no need to worry about variables
        OpExtractor.set_handler(OpExtractor.walk_nop, *op.ALL_TYPES)
        OpExtractor.set_handler(OpExtractor.walk_combine_bv, *op.BV_OPERATORS)
        OpExtractor.set_handler(OpExtractor.walk_constant_bv, op.BV_CONSTANT)
        OpExtractor.set_handler(OpExtractor.walk_combine_bool, *op.BOOL_CONNECTIVES)
        OpExtractor.set_handler(OpExtractor.walk_constant_bool, op.BOOL_CONSTANT)
        OpExtractor.set_handler(OpExtractor.walk_symbol_rec, op.SYMBOL)

        # the above must be done first

        DagWalker.__init__(self,
                           env=env,
                           invalidate_memoization=invalidate_memoization)

    def walk_symbol_rec(self, formula, args, **kwargs):
        self.Symbols.add( formula )
                               
    def walk_nop(self, formula, args, **kwargs):
        pass # do nothing

    def walk_combine_bool(self, formula, args, **kwargs):
        w = 0
        if formula.node_type() in unary_op:
            assert (formula.node_type() in op_str_map)
            op = op_str_map[formula.node_type()]
            if w not in self.BvUnary:
                self.BvUnary[w] = set([])
            self.BvUnary[w].add(op)

        elif formula.node_type() in arithm_op:
            assert (formula.node_type() in op_str_map)
            op = op_str_map[formula.node_type()]
            if w not in self.BvOps:
                self.BvOps[w] = set([])
            self.BvOps[w].add(op)
        
        elif formula.node_type() in comp_op:
            assert (formula.node_type() in op_str_map)
            op = op_str_map[formula.node_type()]
            if w not in self.BvComps:
                self.BvComps[w] = set([])
            self.BvComps[w].add(op)
        else:
            print ('bool op: ' + str(formula.node_type()) + ' is ignored.' )


    def walk_combine_bv(self, formula, args, **kwargs):

        if formula.node_type() in unary_op:
            w = formula.bv_width()
            assert (w > 0)
            assert (formula.node_type() in op_str_map)
            op = op_str_map[formula.node_type()]
            if w not in self.BvUnary:
                self.BvUnary[w] = set([])
            self.BvUnary[w].add(op)

        elif formula.node_type() in arithm_op:
            w = formula.bv_width()
            assert (w > 0)
            assert (formula.node_type() in op_str_map)
            op = op_str_map[formula.node_type()]
            if w not in self.BvOps:
                self.BvOps[w] = set([])
            self.BvOps[w].add(op)
        
        elif formula.node_type() in comp_op:
            w = formula.bv_width()
            assert (w > 0)
            assert (formula.node_type() in op_str_map)
            op = op_str_map[formula.node_type()]
            if w not in self.BvComps:
                self.BvComps[w] = set([])
            self.BvComps[w].add(op)

        elif formula.node_type() in rotate_op:
            w = formula.bv_width()
            p = formula.bv_rotation_step()
            assert (w > 0)
            assert (p > 0)
            assert (formula.node_type() in op_str_map)
            op = op_str_map[formula.node_type()]
            if w not in self.BvRotates:
                self.BvRotates[w] = set([])
            self.BvRotates[w].add((op, p))

        elif formula.node_type() in extend_op:
            w = formula.bv_width()
            p = formula.bv_extend_step()
            assert (w > 0)
            assert (p > 0)
            assert (formula.node_type() in op_str_map)
            op = op_str_map[formula.node_type()]
            inw = formula.arg(0).bv_width()
            if w not in self.BvExts:
                self.BvExts[w] = set([])
            self.BvExts[w].add((op, p, inw))

        elif formula.is_bv_concat():
            w = formula.bv_width()
            inw = [a.bv_width() for a in formula.args()]
            assert (len(inw) == 2)
            assert (w > 0)
            for iw in inw: assert (iw > 0)
            if w not in self.BvConcats:
                self.BvConcats[w] = set([])
            self.BvConcats[w].add((inw[0],inw[1]))

        elif formula.is_bv_extract():
            w = formula.bv_width()
            h = formula.bv_extract_start()
            l = formula.bv_extract_end()
            assert (h >= l and l >=0)
            assert (w > 0)
            
            inw = [a.bv_width() for a in formula.args()]
            assert (len(inw) == 1)
            for iw in inw: assert (iw > 0 and iw > h)

            if w not in self.BvExtracts:
                self.BvExtracts[w] = set([])
            self.BvExtracts[w].add((inw[0], h, l))
        else:
            print ('bvop: ' + str(formula.node_type()) + ' is ignored.' )


    def walk_constant_bv(self, formula, args, **kwargs):
        w = formula.bv_width()
        if w not in self.BvConsts:
            self.BvConsts[w] = set([])
        self.BvConsts[w].add(_const_to_str(formula))


    def walk_constant_bool(self, formula, args, **kwargs):
        w = 0
        if w not in self.BvConsts:
            self.BvConsts[w] = set([])
        self.BvConsts[w].add(_const_to_str(formula))


def get_all_var_of_e(e):
  var_ext = VarExtractor()
  var_ext.walk(e)
  return var_ext.Symbols
  
if __name__ == '__main__':
    # test
    from pysmt.shortcuts import Symbol, Not, And, Or, Implies, Ite, BVAdd, BVSub, BV
    from pysmt.shortcuts import is_sat, is_unsat, Solver, TRUE
    from pysmt.typing import BOOL, BVType

    nbits = 4

    base = Symbol('base', BVType(nbits))
    addr = Symbol('addr', BVType(nbits))
    cnt  = Symbol('cnt',  BVType(nbits-1))
    e1  = Symbol('e1',  BOOL)

    a = Ite( And(e1, base.Equals(0)) , BVAdd(addr, base), BVAdd( base, BV(1,nbits)) )
    ext = OpExtractor()
    ext.walk(a)
    print ('-'*10)
    print (ext.BvUnary)# = 
    print (ext.BvOps)# = {}
    print (ext.BvComps)# = 
    print (ext.BvConsts)# =
    print (ext.BvConcats)# 
    print (ext.BvExtracts)#
    print (ext.BvRotates)# 
    print (ext.BvExts)# = {
    print (ext.Symbols)
    print ('-'*10)
    ext.walk(Ite( Or(Not(e1), cnt.Equals(3)) , BVSub(cnt, BV(5,3)),  BVAdd(cnt, BV(4,3))))
    print (ext.BvUnary)# = 
    print (ext.BvOps)# = {}
    print (ext.BvComps)# = 
    print (ext.BvConsts)# =
    print (ext.BvConcats)# 
    print (ext.BvExtracts)#
    print (ext.BvRotates)# 
    print (ext.BvExts)# = {
    print (ext.Symbols)
    print ('-'*10)
