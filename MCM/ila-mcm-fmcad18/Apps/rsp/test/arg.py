def f0(a, **l):
	print a

def f1(a,b,c):
	print a+b+c


d1 = {'a':1,'b':1,'c':1}

f0(**d1)
f1(**d1)
