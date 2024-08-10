from ast import Eq
from ctypes.wintypes import PLARGE_INTEGER
from operator import ge, le
from time import pthread_getcpuclockid
from unittest import result
from inv_group_new import *
from cex_parser import cex_parser
from pysmt.rewritings import conjunctive_partition
from parse_asmpt import *
from pysmt.shortcuts import Int, Symbol, GE, Plus, And, EqualsOrIff, GT, StrToInt
from pysmt.typing import INT

def add(a, b):
  result = 0
  while(b != 0):
    result = a ^ b
    b = (a & b) << 1
    a = result
  return result

def multiply(n1, n2):
    result = 0
    sign = 0
    if n1 == 0 or n2 == 0:
        return 0
    if n1 < 0 and n2 < 0:
        n1 = -n1; n2 = -n2
    if n1 > 0 and n2 < 0:
        n2 = -n2; sign = 1
    while n2 != 0:
        if n2&1 != 0: result += n1
        n1 <<= 1; n2 >>= 1
    return result if not sign else -result


print(multiply(12,2), 12*2)
print(multiply(23,100), 23*100)
print(multiply(123,456), 123*456)
print(multiply(-10,789), -10*789)
print(multiply(10,-56789), 10*-56789)
print(multiply(-12345,-98765), -12345*-98765)
print(multiply(0, 7788), 0*7788)

def main():
  re = add(100, 112)
  print(re)
    
   

if __name__ == '__main__':
  main()


