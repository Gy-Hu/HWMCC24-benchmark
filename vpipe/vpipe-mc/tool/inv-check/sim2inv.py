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
    stack = list(s)
    count1 = 0
    count2 = 0
    i = 1
    ll = len(stack)

    while (count2 <= count1):
        last = stack.pop()
        i = i + 1
        if(i == ll):
            print('finish!')
            break
        elif(last == ')'):
            count1 = count1 + 1
        elif(last == '('):
            count2 = count2 + 1
        if(count2 == count1):
            pos1 = i
    pos2 = ll - pos1
    str1 = s[0:pos2+1]
    str2 = s[pos2+1:ll]
    s_new = str1 + 'tobool(' + str2 + ')' + s2
    return s_new

opPa = Solution()



def sim2inv(l1):
    num = l1.count('?')
    print('number of \'?\':',num)
    i = 0
    if(num==0):
        l1_final = l1

    while (num!=0)and(i <= num):
        i = i + 1
        print('i:',i)
        #number operation: _number --> number
        pattern1 = '_\d'
        repl1 = ''
        l1_1 = re.sub(pattern1,repl1,l1)

        #tobool
        var_list = ["v1","v2","a","b","c"]
        l1_2 = l1_1
        for var1 in var_list:
            pattern2 = '\({var} = 1\)'.format(var=var1)
            repl2 = 'tobool({var})'.format(var=var1)
            l1_2 = re.sub(pattern2,repl2,l1_2)

        # l1_2 = re.sub(' ','',l1_2)



        l1_2 = re.sub(' ','',l1_2)
        #Ite structure
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
        

        #i<num
        if(i < num):
            # num_equal = l1.count('=1')
            # print('number of \'?\':',num)
            # if(num_equal==0):
            template2 = re.compile("(.*):(.*)")
            matches2 = re.search(template2,matches.group(1))
            if matches2:
                print('m2_0:',matches2.group(0))
                print('m2_1:',matches2.group(1))
                print('m2_2:',matches2.group(2))
            l_m2_group2 = 'Ite' + matches2.group(2)
            # else:
            #     print('future work')


            l1_3 = matches2.group(1) + ':' + l_m2_group2 + ',' + l_group2 +',' + matches.group(3)
            print('l1_new1:',l1_3)
            l1 = l1_3
        #i=num
        elif(i == num):
            l1_3 = 'Ite' + matches.group(1) + ',' + l_group2 +',' + matches.group(3)
            l1_final = l1_3
            print('l1_new2:',l1_3)
            i = i+1
            break

    if((i == num+1)and(i!=2)):
        print('i:',i)
        num2 = l1_3.count('=1')
        print('number of \'=1\':',num2)
        while num2>0:
            print('num2:',num2)
            num2=num2-1
            l1_3 = detectParentheses(l1_3)
        l1_4 = opPa.removeInvalidParentheses(l1_3)
        l1_final = l1_4[-1]
        #remove invalid parentheses
    
    return l1_final

def sim2inv_one_step(l1):
    #number operation: _number --> number
    pattern1 = '_\d'
    repl1 = ''
    l1_1 = re.sub(pattern1,repl1,l1)

    #tobool
    var_list = ["v1","v2","a","b","c"]
    l1_2 = l1_1
    for var1 in var_list:
        pattern2 = '\({var} = 1\)'.format(var=var1)
        repl2 = 'tobool({var})'.format(var=var1)
        l1_2 = re.sub(pattern2,repl2,l1_2)

    l1_2 = re.sub(' ','',l1_2)
    #Ite structure
    template = re.compile(r"(.*)\?(.*):(.*)")
    matches = re.search(template,l1_2)
    # if matches:
    #     print(matches.group(0))
    #     print('m_1:',matches.group(1))
    #     print(matches.group(2))
    #     print(matches.group(3))



    #BV
    bv1='0'or'1'
    if(matches.group(2) == bv1):
        pattern3 = '{bv}'.format(bv=bv1)
        repl3 = 'BV({bv},1)'.format(bv=bv1)
        l_group2 = re.sub(pattern3,repl3,matches.group(2))
    else:
        l_group2 = matches.group(2)

    #i=num
    l1_3 = 'Ite' + matches.group(1) + ',' + l_group2 +',' + matches.group(3)
    l1_final = l1_3
    print('l1_new2:',l1_3)

    return l1_3
        

def struc_fix(l1):
    i = 1
    while i<=2:
        i = i + 1
        #structure recognition
        template1 = re.compile(r"(.*)\?([^\:\?]*)\?([^\:\?]*):([^\:\?]*):(.*)")
        matches1 = re.search(template1,l1)
        template2 = re.compile(r"(.*):([^\:\?]*)\?([^\:\?]*):([^\:\?]*):(.*)")
        matches2 = re.search(template2,l1)
        if matches1:
            print('Structure1 !!')
            print(matches1.group(0))
            print(matches1.group(1))
            print(matches1.group(2))
            print(matches1.group(3))
            print(matches1.group(4))
            print(matches1.group(5))
            l2 = matches1.group(2) + '?' + matches1.group(3) + ':' + matches1.group(4)
            print('l2:',l2)

            l2_1 = sim2inv_one_step(l2)
            l2_new = matches1.group(1)+ '?' + l2_1 + ':' + matches1.group(5)
            print('l2_new:',l2_new)
            l1 = l2_new
        if matches2:
            print('Structure2 !!')
            print('m2_0',matches2.group(0))
            print(matches2.group(1))
            print(matches2.group(2))
            print(matches2.group(3))
            print(matches2.group(4))
            print(matches2.group(5))
            l2 = matches2.group(2) + '?' + matches2.group(3) + ':' + matches2.group(4)
            print('l2:',l2)

            l2_1 = sim2inv_one_step(l2)
            l2_new = matches2.group(1)+ ':' + l2_1 + ':' + matches2.group(5)
            print('l2_new:',l2_new)
            l1 = l2_new
    return l1



# error example
# l1 = '((v2 = 1_1) ? ((v2 = 1_1) ? b : c) : c)' ###1.no ok
# l1 = '((((v1 = 1_1) ? 0_1 : 1_1) = 1_1) ? ((v1 = 1_1) ? ((a * 2_4) + 1_4) : ((v2 = 1_1) ? b : c)) : a)'###2.error ok
# l1 = '(((((((v1 = 1_1) ? 0_1 : 1_1) = 1_1) ? 1_1 : v1) & ((((v2 = 1_1) ? 0_1 : v2) = 1_1) ? 0_1 : 1_1)) = 1_1) ? ((((v1 = 1_1) ? 0_1 : 1_1) = 1_1) ? 1_1 : v1) : ((v2 = 1_1) ? 0_1 : v2))'###3.error:and
l1 = '((v1 = 1_1) ? 0_1 : v1)'
l1 = '((v1 = 1_1) ? v1 : ((v2 = 1_1) ? 0_1 : v2))'
l1 = '((v1 = 1_1) ? ((a * 2_4) + 1_4) : b)'
l1 = '((v2 = 1_1) ? ((v2 = 1_1) ? b : c) : c)'
l1 = '((((v1 = 1_1) ? v1 : ((v2 = 1_1) ? 0_1 : v2)) = 1_1) ? 0_1 : ((v1 = 1_1) ? v1 : ((v2 = 1_1) ? 0_1 : v2)))' ###error


##detect '&'
template_and = re.compile(r"(.*)\&(,*)")
matches_and = re.search(template_and,l1)
if matches_and:
    print(matches_and.group(0))
    print(matches_and.group(1))
    print(matches_and.group(2))
    l0_1 = matches_and.group(1)
    print('l0_1',l0_1)
    l0_2 = matches_and.group(2)
    l1_1 = struc_fix(l0_1)
    print('l1_1',l1_1)
    l2_1 = sim2inv(l1_1)
else:
    l1 = struc_fix(l1)
    l1_final = sim2inv(l1)
    print('l1_final:',l1_final)


# l1_final = sim2inv(l0_1)

# print('l1_final:',l1_final)
'(((tobool(v1)?v1:(tobool(v2)?0:v2))=1)?0:(tobool(v1)?v1:Ite(tobool(v2),BV(0,1),v2)))'