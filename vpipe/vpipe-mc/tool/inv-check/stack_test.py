# adapted from : https://github.com/pysmt/pysmt/blob/master/examples/smtlib.py
# NOTE: you need to install pysmt first
#       pip3 install pysmt
#

from io import StringIO
from typing import Pattern
from pysmt.environment import get_env
from pysmt.smtlib.parser import SmtLibParser
from pysmt.smtlib.script import SmtLibCommand
from pysmt.typing import BVType
from pysmt.shortcuts import BVAdd
from pysmt.shortcuts import BVMul
from pysmt.shortcuts import BV

from pysmt.shortcuts import is_sat, substitute
from pysmt.shortcuts import And, Not, Or, Implies, BVOne, BVZero, EqualsOrIff #Implies 就是 imply，EqualsOrIff是equal
from pysmt.shortcuts import Ite
from pysmt.fnode import *
from pysmt.shortcuts import get_model

import re

#removeInvalidParentheses
class Solution:
    def removeInvalidParentheses(self, s):
        self.res = []
        self.DFS(s, ')', 0, 0)
        return self.res
    
    def DFS(self, s, c, last_i, last_j):
        count = 0
        for i in range(last_i, len(s)):
            if s[i] == '(' or s[i] == ')':
                if s[i] == c: count += 1
                else: count -= 1
            if count <= 0: continue
            for j in range(last_j, i+1):
                if s[j] == c and (j == last_j or s[j] != s[j-1]):
                    self.DFS(s[:j] + s[j+1:], c, i, j)
            return #break out of DFS function directly
        s = list(s)[::-1]
        s = ''.join(s)
        if c == ')': self.DFS(s, '(', 0, 0)
        else: self.res.append(s)

removePa = Solution()


l1 = '((v1 = 1_1) ? ((a * 2_4) + 1_4) : b)'
# l1 = '((v1 = 1_1) ? 0_1 : v1)'
l1 = '((((v1 = 1_1) ? v1 : ((v2 = 1_1) ? 0_1 : v2)) = 1_1) ? 0_1 : ((v1 = 1_1) ? v1 : ((v2 = 1_1) ? 0_1 : v2)))'
l1 = '(((tobool(v1)?v1:(tobool(v2)?0:v2))=1)?0:(tobool(v1)?v1:Ite(tobool(v2),BV(0,1),v2)))'
l1 = '(((tobool(v1)?v1:(tobool(v2)?0:v2))=1)?0:Ite(tobool(v1),v1,Ite(tobool(v2),BV(0,1),v2)))'
l1 = '(((tobool(v1)?v1:(tobool(v2)?0:Itev2))=1),BV(0,1),Ite(tobool(v1),v1,Ite(tobool(v2),BV(0,1),v2)))' 
l1 = '(((tobool(v1)?v1:Ite(tobool(v2),BV(0,1),Itev2))=1),BV(0,1),Ite(tobool(v1),v1,Ite(tobool(v2),BV(0,1),v2)))'
# l1 = 'Ite(((tobool(v1),v1,Ite(tobool(v2),BV(0,1),Itev2))=1),BV(0,1),Ite(tobool(v1),v1,Ite(tobool(v2),BV(0,1),v2)))'
#'Ite(tobool(v1),v1,(Ite(tobool(Ite(tobool(v2),BV(0,1),v2)),BV(0,1),(Ite(tobool(v1),v1,(Ite(tobool(v2),BV(0,1),v2))))))''
l1 = '((((v1 = 1_1) ? v1 : ((v2 = 1_1) ? 0_1 : v2)) = 1_1) ? 0_1 : ((v1 = 1_1) ? v1 : ((v2 = 1_1) ? 0_1 : v2)))'


l1_2 = l1
template = re.compile(r"(.*)=1(.*)")
matches0 = re.search(template,l1_2)
if matches0:
    print('m0_0:',matches0.group(0))
    print('m0_1:',matches0.group(1))
    print('m0_2:',matches0.group(2))

s = matches0.group(1)
s2 = str(matches0.group(2))
print('s2!!:',s2)
stack = list(s)
count1 = 0
count2 = 0
i = 1
len = len(stack)
print('len',len)
print('stack:',stack)

while (count2 <= count1):
    last = stack.pop()
    i = i + 1
    # print('last',last)
    if(i == len):
        print('finish!')
        break
    elif(last == ')'):
        count1 = count1 + 1
        print('count1',count1)
    elif(last == '('):
        count2 = count2 + 1
        print('count2',count2)
        # pos = i
    if(count2 == count1):
        pos1 = i

print('pos1',pos1)
pos2 = len - pos1
print('pos2',pos2)

str1 = s[0:pos2+1]
str2 = s[pos2+1:len]
print('str1',str1)
print('str2',str2)
s_new = str1 + 'Ite(tobool(' + str2 + ')' + s2
print('s_new',s_new)

'Ite((tobool((tobool(v1),v1,Ite(tobool(v2),BV(0,1),Itev2)))),BV(0,1),Ite(tobool(v1),v1,Ite(tobool(v2),BV(0,1),v2)))'