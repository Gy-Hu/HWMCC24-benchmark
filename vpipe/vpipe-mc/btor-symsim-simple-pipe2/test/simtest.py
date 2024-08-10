# Check if a expression is independent of a var
# (namely, if var can be reduced in expression)

from z3 import *

def reduce_model(f, m, varset):
  #model = [(v,m[v]) for v in varset]
  remaining = set()
  for v in varset:
    testm = [(vrest,m[vrest]) for vrest in varset if vrest is not v]
    assert(len(testm) == len(varset)-1)
    s = Solver()
    for vrest,val in testm:
      s.add(vrest == val)
    s.add(v == Not(m[v]))
    assert(s.check() == sat)
    if str( s.model().eval(f) ) == 'True':
      f = And(substitute(f, [(v, Not(m[v]))]),substitute(f, [(v, m[v])]))
      print (f)
    else:
      remaining.add(v)
  return remaining
  

# ----------------------------------------------------------

def test_btor_parsing():
  varA = Bool("A")
  varB = Bool("B")
  varC = Bool("C")
  f = Or(varA, varB, varC)
  s = Solver()
  s.add(f)
  s.add(varA)
  s.add(Not(varB))
  s.add(varC)
  res = s.check()
  assert (res == sat)
  model = s.model()
  print (model)
  d = reduce_model(f, model, {varA, varB, varC})
  print (d)  


if __name__ == '__main__':
    test_btor_parsing()
