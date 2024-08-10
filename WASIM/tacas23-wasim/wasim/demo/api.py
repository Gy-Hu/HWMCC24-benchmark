import sys
sys.path.append('/home/tacas23/wasim')
sys.path.append('/home/tacas23/wasim/symsim_framework')

from pathlib import Path
from symsim_framework.symtraverse import *

btor_parser = BTOR2Parser()
sts, _ = btor_parser.parse_file(Path("/home/tacas23/wasim/design/simple_MAC_no_stall.btor2"))
executor = SymbolicExecutor(sts)

executor.init(
  executor.convert({
    'wen_stage1':'v1',
    'wen_stage2':'v2',
    'wen_stage3':'v3',
    'stage1':'a',
    'stage2':'b',
    'stage3':'c'
  }))

executor.print_current_step() 
executor.print_current_step_assumptions()

executor.set_input(
    executor.convert({'rst':0}), [])
executor.sim_one_step()

state = executor.get_curr_state()
state.print()
state = executor.get_curr_state()

