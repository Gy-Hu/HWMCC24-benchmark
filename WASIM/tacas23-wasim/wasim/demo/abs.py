import sys
sys.path.append('/home/tacas23/wasim')
sys.path.append('/home/tacas23/wasim/symsim_framework')
from pathlib import Path
import copy
from symsim_framework.symtraverse import *
from abstraction_interface import *
from pysmt.shortcuts import FALSE, TRUE, BVULT, BV, Symbol
from pysmt.typing import BOOL, BVType
from utils import e_is_valid, e_is_invalid

class PredicateAbstraction(Abstraction):
    def __init__(self, cnt):
        self.cnt = cnt
        self.pred = Symbol('pred', BOOL)

    def __call__(self, state : StateAsmpt) -> StateAsmpt:
        predicate =  BVULT(self.cnt, BV(11,4))
        abs_state = \
          StateAsmpt({self.cnt:self.cnt, self.pred:predicate}, [], [])
        
        p_valid = e_is_valid(state.eval(predicate), state.asmpt)
        if p_valid:
            abs_state.add_assumption(EqualsOrIff(predicate, TRUE()), 'pred')
            
        p_invalid = e_is_invalid(state.eval(predicate), state.asmpt)
        if p_invalid:
            abs_state.add_assumption(EqualsOrIff(predicate, FALSE()), 'pred')
       
        print ('---------before abstraction---------')
        state.print()
        state.print_assumptions()
        print ('---------after abstraction---------')
        abs_state.print()
        abs_state.print_assumptions()
        
        
        return abs_state     
        
    def abs_eq(self, s1: StateAsmpt, s2: StateAsmpt) -> bool:
        expr = EqualsOrIff( s1.sv[self.pred], s2.sv[self.pred] )
        assumptions = s1.asmpt + s2.asmpt
        return e_is_valid(expr, assumptions)

def main():
    btor_parser = BTOR2Parser()
    sts, _ = btor_parser.parse_file(Path("/home/tacas23/wasim/design/counter.btor2"))
    executor = SymbolicExecutor(sts)

    executor.init({})

    traverser = SymbolicTraverse(sts, executor, [])
    all_states = \
    traverser.traverse_all_states([], no_branching(), 
        PredicateAbstraction(executor.sv("cnt")) , no_refinement())
        
    print('Explored #. of states:',len(all_states))
if __name__ == '__main__':
    main()





