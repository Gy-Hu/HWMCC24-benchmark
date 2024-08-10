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
        if type(s)!='str':
            s=str(s)
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

def detectParentheses(l1):
    template = re.compile(r"(.*)=1(.*)")
    matches0 = re.search(template,l1)
    if matches0:
        print('m0_0:',matches0.group(0))
        print('m0_1:',matches0.group(1))
        print('m0_2:',matches0.group(2))

    s = matches0.group(1)
    s2 = str(matches0.group(2))
    # print('s2!!:',s2)
    stack = list(s)
    count1 = 0
    count2 = 0
    i = 1
    ll = len(stack)
    # print('len',ll)
    # print('stack:',stack)

    while (count2 <= count1):
        last = stack.pop()
        i = i + 1
        # print('last',last)
        if(i == ll):
            print('finish!')
            break
        elif(last == ')'):
            count1 = count1 + 1
            # print('count1',count1)
        elif(last == '('):
            count2 = count2 + 1
            # print('count2',count2)
            
        if(count2 == count1):
            pos1 = i

    # print('pos1',pos1)
    pos2 = ll - pos1
    # print('pos2',pos2)

    str1 = s[0:pos2+1]
    str2 = s[pos2+1:ll]
    # print('str1',str1)
    # print('str2',str2)
    s_new = str1 + 'tobool(' + str2 + ')' + s2
    
    return s_new

opPa = Solution()


l1 = '((v1 = 1_1) ? ((a * 2_4) + 1_4) : b)'
# l1 = '((v1 = 1_1) ? 0_1 : v1)'
l1 = '((((v1 = 1_1) ? v1 : ((v2 = 1_1) ? 0_1 : v2)) = 1_1) ? 0_1 : ((v1 = 1_1) ? v1 : ((v2 = 1_1) ? 0_1 : v2)))'
# l1 = '(((tobool(v1)?v1:(tobool(v2)?0:v2))=1)?0:(tobool(v1)?v1:Ite(tobool(v2),BV(0,1),v2)))'
# l1 = '(((tobool(v1)?v1:(tobool(v2)?0:v2))=1)?0:Ite(tobool(v1),v1,Ite(tobool(v2),BV(0,1),v2)))'
# l1 = '(((tobool(v1)?v1:(tobool(v2)?0:Itev2))=1),BV(0,1),Ite(tobool(v1),v1,Ite(tobool(v2),BV(0,1),v2)))'
# l1 = '(((tobool(v1)?v1:Ite(tobool(v2),BV(0,1),Itev2))=1),BV(0,1),Ite(tobool(v1),v1,Ite(tobool(v2),BV(0,1),v2)))'
# l1 = 'Ite(((tobool(v1),v1,Ite(tobool(v2),BV(0,1),Itev2))=1),BV(0,1),Ite(tobool(v1),v1,Ite(tobool(v2),BV(0,1),v2)))'

# l1 = '(((tobool(v1)?v1:(tobool(v2)?0:v2))=1)?0:(tobool(v1)?v1:Ite(tobool(v2),BV(0,1),v2)))'
# l1 = '(((tobool(v1)?v1:(tobool(v2)?0:v2))=1)?0:Ite(tobool(v1),v1,Ite(tobool(v2),BV(0,1),v2)))'
# l1 = '(((tobool(v1)?v1:(tobool(v2)?0:Itev2))=1),BV(0,1),Ite(tobool(v1),v1,Ite(tobool(v2),BV(0,1),v2)))' 
# l1 = '(((tobool(v1)?v1:Ite(tobool(v2),BV(0,1),Itev2))=1),BV(0,1),Ite(tobool(v1),v1,Ite(tobool(v2),BV(0,1),v2)))'
# l1 = 'Ite(((tobool(v1),v1,Ite(tobool(v2),BV(0,1),Itev2))=1),BV(0,1),Ite(tobool(v1),v1,Ite(tobool(v2),BV(0,1),v2)))'
#'Ite(tobool(v1),v1,(Ite(tobool(Ite(tobool(v2),BV(0,1),v2)),BV(0,1),(Ite(tobool(v1),v1,(Ite(tobool(v2),BV(0,1),v2))))))''
# l1 = '((v1 = 1_1) ? ((a * 2_4) + 1_4) : b)'
l1 = '((((v1 = 1_1) ? v1 : ((v2 = 1_1) ? 0_1 : v2)) = 1_1) ? 0_1 : ((v1 = 1_1) ? v1 : ((v2 = 1_1) ? 0_1 : v2)))' 

#EqualsOrIff(Ite(tobool(v1),(2*a+1),b),stage2)
# var1 = "v1"
# pattern1 = '({var} = 1_1)'.format(var=var1)
# repl1 = 'Ite(tobool({var})'.format(var=var1)
# l1_new = re.sub(pattern1,repl1,l1)

#number
pattern1 = '_\d'
repl1 = ''
l1_1 = re.sub(pattern1,repl1,l1)

#tobool
var_list = ["v1","v2","a","b","c"]
# var1 = "v1"
l1_2 = l1_1
for var1 in var_list:
    pattern2 = '\({var} = 1\)'.format(var=var1)
    repl2 = 'tobool({var})'.format(var=var1)
    l1_2 = re.sub(pattern2,repl2,l1_2)

print('l1_final0:',l1_2)
#i==num
# l1_2 = detectParentheses(l1_2)
print('l1_final0:',l1_2)


# print('!!!:',l1_2)

# template = re.compile(r"(.*)=1(.*)")
# matches0 = re.search(template,l1_2)
# if matches0:
#     print(matches0.group(0))
#     print('m0_1:',matches0.group(1))
 



print('l1:',l1)
print('l1_1:',l1_1)
print('l1_2:',l1_2)


l1_2 = re.sub(' ','',l1_2)
#Ite structure
num = l1.count('?')
print('number of ?:',num)
template = re.compile(r"(.*)\?(.*):(.*)")
matches = re.search(template,l1_2)
if matches:
    print(matches.group(0))
    print('m_1:',matches.group(1))
    print(matches.group(2))
    print(matches.group(3))



#BV
bv1='0'or'1'
if(matches.group(2) == bv1):
    pattern3 = '{bv}'.format(bv=bv1)
    repl3 = 'BV({bv},1)'.format(bv=bv1)
    l_group2 = re.sub(pattern3,repl3,matches.group(2))
else:
    l_group2 = matches.group(2)

# print('l_g:',l_group2)

#i<num

template2 = re.compile("(.*):(.*)")
matches2 = re.search(template2,matches.group(1))
if matches2:
    print('m2_0:',matches2.group(0))
    print('m2_1:',matches2.group(1))
    print('m2_2:',matches2.group(2))
## l_m2_goup2 = re.sub('tobool','Ite(tobool',matches2.group(2))
l_m2_group2 = 'Ite' + matches2.group(2)


l1_3 = matches2.group(1) + ':' + l_m2_group2 + ',' + l_group2 +',' + matches.group(3)
print('l1_new:',l1_3)


#i=num
# l1_3 = 'Ite' + matches.group(1) + ',' + l_group2 +',' + matches.group(3)
# print('l1_new:',l1_3)
# #remove invalid parentheses
# l1_4 = opPa.removeInvalidParentheses(l1_3)
# print('l1_final:',l1_4[-1])



l1 = '((((v1 = 1_1) ? v1 : ((v2 = 1_1) ? 0_1 : v2)) = 1_1) ? 0_1 : ((v1 = 1_1) ? v1 : ((v2 = 1_1) ? 0_1 : v2)))'
'(((x ? v1 : (x ? 0_1 : v2)) = 1_1) ? 0_1 : (x ? v1 : (x ? 0_1 : v2)))'