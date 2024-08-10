
from pysmt.shortcuts import Symbol, Not, And, Or, Implies, Ite, BVAdd, BV, EqualsOrIff, BVNot, BVSub, TRUE
from pysmt.typing import BOOL, BVType
from sts import TransitionSystem


class BaseAddrCnt(TransitionSystem):
    def __init__(self, nbits):
        self.nbits = nbits # save the number of bits
        self.mask = 2**(nbits)-1

        base = Symbol('base', BVType(nbits))
        addr = Symbol('addr', BVType(nbits))
        cnt  = Symbol('cnt',  BVType(nbits))
        inp  = Symbol('inp',  BVType(nbits))
        lden = Symbol('lden',  BVType(1))

        self.base = base 
        self.addr = addr 
        self.cnt  = cnt  
        self.inp  = inp  
        self.lden = lden 


        variables = [base, addr, cnt, inp, lden]
        prime_variables = [TransitionSystem.get_prime(v) for v in variables]
        init = base.Equals(0) & addr.Equals(0) & cnt.Equals(0)
        trans= TransitionSystem.get_prime(base).Equals( \
            Ite(lden.Equals(1), inp, base  )) & \
            TransitionSystem.get_prime(addr).Equals( \
            Ite(lden.Equals(1), inp, BVAdd(addr, BV(1, nbits) ) )) & \
            TransitionSystem.get_prime(cnt).Equals( \
            Ite(lden.Equals(1), BV(0, nbits), BVAdd(cnt, BV(1, nbits) ) ))
            
        TransitionSystem.__init__(self, \
          variables = variables, \
          prime_variables = prime_variables, \
          init = init, trans = trans )

    def neq_property(self, base, addr, cnt):
        addr = addr & self.mask
        base = base & self.mask
        cnt  = cnt  & self.mask

        assert ( addr !=  ((base+cnt) & self.mask) )

        return Not( self.addr.Equals(addr) & self.base.Equals(base) & self.cnt.Equals(cnt) )


class TwoCnt(TransitionSystem):
    def __init__(self, nbits, zero_init = False):
        self.nbits = nbits # save the number of bits
        self.mask = 2**(nbits)-1

        self.c1   = Symbol('c1', BVType(nbits))
        self.c2   = Symbol('c2', BVType(nbits))
        self.inp  = Symbol('inp',  BVType(nbits))
        self.lden = Symbol('lden',  BVType(1))

        variables = [self.c1, self.c2, self.inp, self.lden]
        prime_variables = [TransitionSystem.get_prime(v) for v in variables]
        if zero_init:
            init = self.c1.Equals(0) & self.c2.Equals(self.mask)
        else:
            init = self.c1.Equals(self.inp) & self.c2.Equals(BVNot(self.inp))
        trans= TransitionSystem.get_prime(self.c1).Equals( \
            Ite(self.lden.Equals(1), self.inp, BVAdd(self.c1, BV(1, nbits)  ))) & \
            TransitionSystem.get_prime(self.c2).Equals( \
            Ite(self.lden.Equals(1), BVNot(self.inp), BVSub(self.c2, BV(1, nbits)  )))
            
        TransitionSystem.__init__(self, \
          variables = variables, \
          prime_variables = prime_variables, \
          init = init, trans = trans )

    def neq_property(self, c1, c2):
        c1 = c1 & self.mask
        c2 = c2 & self.mask

        assert ( c1 + c2 != self.mask)

        return Not( self.c1.Equals(c1) & self.c2.Equals(c2) )

    def false_property(self, c1, c2):
        c1 = c1 & self.mask
        c2 = c2 & self.mask

        assert ( c1 + c2 == self.mask)

        return Not( self.c1.Equals(c1) & self.c2.Equals(c2) )


class TwoCntNoload(TransitionSystem):
    def __init__(self, nbits, zero_init = False):
        self.nbits = nbits # save the number of bits
        self.mask = 2**(nbits)-1

        self.c1   = Symbol('c1', BVType(nbits))
        self.c2   = Symbol('c2', BVType(nbits))
        self.inp  = Symbol('inp',  BVType(nbits))

        variables = [self.c1, self.c2, self.inp]
        prime_variables = [TransitionSystem.get_prime(v) for v in variables]
        if zero_init:
            init = self.c1.Equals(0) & self.c2.Equals(self.mask)
        else:
            init = self.c1.Equals(self.inp) & self.c2.Equals(BVNot(self.inp))
        trans= TransitionSystem.get_prime(self.c1).Equals( \
            BVAdd(self.c1, BV(1, nbits)  )) & \
            TransitionSystem.get_prime(self.c2).Equals( \
            BVSub(self.c2, BV(1, nbits)  ))
            
        TransitionSystem.__init__(self, \
          variables = variables, \
          prime_variables = prime_variables, \
          init = init, trans = trans )

    def neq_property(self, c1, c2):
        c1 = c1 & self.mask
        c2 = c2 & self.mask

        assert ( c1 + c2 != self.mask)

        return Not( self.c1.Equals(c1) & self.c2.Equals(c2) )

    def false_property(self, c1, c2):
        c1 = c1 & self.mask
        c2 = c2 & self.mask

        assert ( c1 + c2 == self.mask)

        return Not( self.c1.Equals(c1) & self.c2.Equals(c2) )
