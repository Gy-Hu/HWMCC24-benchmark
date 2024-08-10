
# interface for overloading
from sre_parse import State
from sts import StateAsmpt

class BranchingSelector:
    def __init__(self):
        pass
    
    def set_way_point(self, search_tree, queue, curr_node):
        pass

    def has_valid_choice(self) -> bool:
        pass

    def get_inputvar_asmpt(self, assumptions):
        pass

class no_branching(BranchingSelector):
    def __init__(self):
        pass

    def set_way_point(self, search_tree, queue, curr_node):
        self.has_choice = True
    
    def has_valid_choice(self):
        if self.has_choice:
            self.has_choice = False
            return True
        return False

    def get_inputvar_asmpt(self, assumptions):
        return {}, assumptions
        

class Abstraction:
    def __init__(self):
        pass

    def __call__(self, state : StateAsmpt) -> StateAsmpt:
        pass

    def abs_eq(self, s1: StateAsmpt, s2: StateAsmpt) -> bool:
        pass


class Refinement:
    def __init__(self):
        pass

    def __call__(self, parent_state: StateAsmpt, current_state: StateAsmpt, inputvars, assumptions) -> StateAsmpt:
        pass

    def needs_refinement(state : StateAsmpt) -> bool:
        pass



class no_refinement(Refinement):
    def __init__(self):
        pass

    def __call__(self, parent_state: StateAsmpt, current_state: StateAsmpt, inputvars, assumptions) -> StateAsmpt:
        return current_state

    def needs_refinement(state : StateAsmpt) -> bool:
        return False
