
class t(object):
	def __init__(self,x):
		self.x = x

t1 = t(1)
t2 = t(2)

d1 = {}
d1[t1] = 1
d1[t2] = 2

print d1[t1]
print d1[t2]
