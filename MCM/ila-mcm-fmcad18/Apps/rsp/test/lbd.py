
class lpToC:
	def __init__(self, l):
		self.l = l
	def __call__(self,n):
		return self.l[n]

def f(y):
	l1 = lambda x: x(1) + y
	return l1

f2 = f(2)
l = range(5)
C = lpToC(l)

y = 5
print f2( C )
