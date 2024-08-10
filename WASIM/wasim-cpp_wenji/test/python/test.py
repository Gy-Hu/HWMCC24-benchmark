import os
import sys

script_path = os.path.realpath(__file__)
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
build_dir = os.path.join(parent_dir, 'build')
sys.path.append(build_dir)

import pywasim
ts = pywasim.TransSys('pipe.btor2')
updates = ts.state_updates()
for s,e in updates.items():
  print(s,e.to_string())
  print (e.get_op())
  

prop = ts.prop()[0]
prop_prev = prop.substitute(updates)
print (prop)
print (prop_prev)

init_constant = ts.init_constants()
print (init_constant)

