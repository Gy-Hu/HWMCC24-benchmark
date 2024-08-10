# Copyright 2018 Cristian Mattarei
#
# Licensed under the modified BSD (3-clause BSD) License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from pathlib import Path
from typing import List, NamedTuple, Tuple

from pysmt.fnode import FNode
from pysmt.shortcuts import Not, TRUE, And, BVNot, BVNeg, BVAnd, BVOr, BVAdd, Or, Symbol, BV, EqualsOrIff, \
    Implies, BVMul, BVExtract, BVUGT, BVUGE, BVULT, BVULE, BVSGT, BVSGE, BVSLT, BVSLE, \
    Ite, BVZExt, BVSExt, BVXor, BVConcat, get_type, BVSub, Xor, Select, Store, BVComp, simplify, \
    BVLShl, BVAShr, BVLShr, Array, BVSRem, BVURem, BVSDiv, BVUDiv
from pysmt.typing import BOOL, BVType, ArrayType

from sts import TransitionSystem as TS
# compared to keep a map, we'd rather just do a walk
from opextract import get_all_var_of_e


Config_Warning = True
Config_NODOLLAR_NAME = True


#from cosa.utils.formula_mngm import quote_names, B2BV, BV2B
def B2BV(f): #B?BV
    if get_type(f).is_bv_type():
        return f
    return Ite(f, BV(1,1), BV(0,1))


def BV2B(f):
    if get_type(f).is_bool_type():
        return f
    return EqualsOrIff(f, BV(1,1))

#from cosa.utils.generic import bin_to_dec
def bin_to_dec(val):
    return int(val, 2)

NL = "\n"
COLON_REP = "_c_"

SN="N%s"

COM=";"
SORT="sort"
BITVEC="bitvec"
ARRAY="array"
WRITE="write"
READ="read"
ZERO="zero"
ONE="one"
ONES="ones"
STATE="state"
INPUT="input"
OUTPUT="output"
ADD="add"
EQ="eq"
NEQ="neq"
MUL="mul"
SLICE="slice"
CONST="const"
CONSTD="constd"
UGT="ugt"
UGTE="ugte"
ULT="ult"
ULTE="ulte"
SGT="sgt"
SGTE="sgte"
SLT="slt"
SLTE="slte"
AND="and"
XOR="xor"
XNOR = "xnor"
NAND="nand"
IMPLIES="implies"
OR="or"
ITE="ite"
NOT="not"
NEG="neg"
REDOR="redor"
REDAND="redand"
UEXT="uext"
SEXT="sext"
CONCAT="concat"
SUB="sub"
SLL="sll"
SRA="sra"
SRL="srl"
SREM="srem"
UREM="urem"
SDIV="sdiv"
UDIV="udiv"

INIT="init"
NEXT="next"
CONSTRAINT="constraint"
BAD="bad"
ASSERTINFO="btor-assert"

special_char_replacements = {"$": "", "\\": ".", ":": COLON_REP}

class BTOR2Parser:
    parser = None
    extensions = ["btor2","btor"]
    name = "BTOR2"
    config = None


    def __init__(self):
        pass

    def get_model_info(self):
        return None

    def parse_file(self,
                   filepath:Path,
                   flags:str=None)->Tuple[TS, List[FNode]]:
        self.symbolic_init = False
        with filepath.open("r", errors='surrogateescape') as f:
            text = f.read()
            self.preprocess(text)
            return self.parse_string(text)

    def is_available(self):
        return True

    def get_extensions(self):
        return self.extensions

    @staticmethod
    def get_extensions():
        return BTOR2Parser.extensions

    def remap_an2or(self, name):
        return name

    def remap_or2an(self, name):
        return name

    def preprocess(self, strinput):
        self.nid_state_name = {}
        self.output_stateid_set = set()
        self.skipped_name_nid = set()

        for line in strinput.split(NL):
            linetok = line.split()
            if len(linetok) == 0:
                continue
            if linetok[0] == COM:
                continue

            (nid, ntype, *nids) = linetok
            
            if Config_NODOLLAR_NAME:
                idx = len(nids)-1
                while idx > -1:
                  if str(nids[idx]).isdigit():
                    break
                  idx -= 1
                idx += 1
                if 0 <= idx and idx < len(nids):
                    wirename = str(' '.join(nids[idx:]))
                    if wirename[0] == '$':
                      self.skipped_name_nid.add(nid)
            
            
            if ntype == STATE:
                if  len(nids) > 1:
                    self.nid_state_name[nid] = nids[1]
                else:
                    self.nid_state_name[nid] = ''
            elif ntype == OUTPUT:

                sid = nids[0]
                sname = nids[1]
                if sid in self.nid_state_name:
                    if self.nid_state_name[sid] != '' and self.nid_state_name[sid] != sname:
                        print ('Warning: will not rename state:', self.nid_state_name[sid] , ' to output name: ', sname)
                    elif self.nid_state_name[sid] == '':
                        self.nid_state_name[sid] = sname
                        self.output_stateid_set.add(nid)



    def parse_string(self, strinput):

        ts = TS(variables = None, prime_variables = None, init = None, trans = None)

        nodemap = {}
        node_covered = set([])

        # list of tuples of var and cond_assign_list
        # cond_assign_list is tuples of (condition, value)
        # where everything is a pysmt FNode
        # for btor, the condition is always True
        ftrans = []
        nxt_node_set = set() # set of int, to rule out them in the check
        output_node_set = set()
        initlist = []
        invarlist = []

        invar_props = []

        prop_count = 0

        # clean string input, remove special characters from names
        for sc, rep in special_char_replacements.items():
            strinput = strinput.replace(sc, rep)

        def getnode(nid):
            assert(nid not in  output_node_set)
            node_covered.add(nid)
            if int(nid) < 0:
                return Ite(BV2B(nodemap[str(-int(nid))]), BV(0,1), BV(1,1))
            return nodemap[nid]

        def binary_op(bvop, bop, left, right):
            if (get_type(left) == BOOL) and (get_type(right) == BOOL):
                return bop(left, right)
            return bvop(B2BV(left), B2BV(right))

        def unary_op(bvop, bop, left):
            if (get_type(left) == BOOL):
                return bop(left)
            return bvop(left)

        for line in strinput.split(NL):
            linetok = line.split()
            if len(linetok) == 0:
                continue
            if linetok[0] == COM:
                continue

            (nid, ntype, *nids) = linetok

            if ntype == SORT:
                (stype, *attr) = nids
                if stype == BITVEC:
                    nodemap[nid] = BVType(int(attr[0]))
                    node_covered.add(nid)
                if stype == ARRAY:
                    nodemap[nid] = ArrayType(getnode(attr[0]), getnode(attr[1]))
                    node_covered.add(nid)

            if ntype == WRITE:
                nodemap[nid] = Store(*[getnode(n) for n in nids[1:4]])

            if ntype == READ:
                nodemap[nid] = Select(getnode(nids[1]), getnode(nids[2]))

            if ntype == ZERO:
                nodemap[nid] = BV(0, getnode(nids[0]).width)

            if ntype == ONE:
                nodemap[nid] = BV(1, getnode(nids[0]).width)

            if ntype == ONES:
                width = getnode(nids[0]).width
                nodemap[nid] = BV((2**width)-1, width)

            if ntype == REDOR:
                width = get_type(getnode(nids[1])).width
                zeros = BV(0, width)
                nodemap[nid] = BVNot(BVComp(getnode(nids[1]), zeros))

            if ntype == REDAND:
                width = get_type(getnode(nids[1])).width
                ones = BV((2**width)-1, width)
                nodemap[nid] = BVComp(getnode(nids[1]), ones)

            if ntype == CONSTD:
                width = getnode(nids[0]).width
                nodemap[nid] = BV(int(nids[1]), width)

            if ntype == CONST:
                width = getnode(nids[0]).width
                try:
                    nodemap[nid] = BV(bin_to_dec(nids[1]), width)
                except ValueError:
                    if not all([i == 'x' or i == 'z' for i in nids[1]]):
                        raise RuntimeError("If not a valid number, only support "
                                           "all don't cares or high-impedance but got {}".format(nids[1]))
                    # create a fresh variable for this non-deterministic constant
                    nodemap[nid] = Symbol('const_'+nids[1], BVType(width))
                    ts.add_state_var(nodemap[nid])
                    print("Creating a fresh symbol for unsupported X/Z constant %s"%nids[1])

            if ntype == STATE:
                if len(nids) > 1:
                    nodemap[nid] = Symbol(nids[1], getnode(nids[0]))
                else:
                    sname = self.nid_state_name.get(nid,'')
                    if sname != '':
                        nodemap[nid] = Symbol(sname, getnode(nids[0]))
                    else:
                        nodemap[nid] = Symbol((SN%nid), getnode(nids[0]))
                        print ('Warning: has unnamed state!')
                ts.add_state_var(nodemap[nid])

            if ntype == INPUT:
                if len(nids) > 1:
                    nodemap[nid] = Symbol(nids[1], getnode(nids[0]))
                else:
                    nodemap[nid] = Symbol((SN%nid), getnode(nids[0]))
                    print ('Warning: has unnamed input!')
                ts.add_input_var(nodemap[nid])

            if ntype == OUTPUT:
                if nid not in self.output_stateid_set:
                    # unfortunately we need to create an extra symbol just to have the output name
                    # we could be smarter about this, but then this parser can't be greedy
                    # hz note: here I fix it
                    print ('Warning: ignore output: ', nids[1])
                    output_node_set.add(nid)
                    ts.register_wire_name(nids[1], getnode(nids[0]))
                    # print (nids)
                    # original_symbol = B2BV(getnode(nids[0]))
                    # output_symbol = Symbol(nids[1], original_symbol.get_type())
                    # nodemap[nid] = EqualsOrIff(output_symbol, original_symbol)
                    # invarlist.append(nodemap[nid])
                    # node_covered.add(nid)
                    # ts.add_output_var(output_symbol)

            if ntype == AND:
                nodemap[nid] = binary_op(BVAnd, And, getnode(nids[1]), getnode(nids[2]))

            if ntype == CONCAT:
                nodemap[nid] = BVConcat(B2BV(getnode(nids[1])), B2BV(getnode(nids[2])))

            if ntype == XOR:
                nodemap[nid] = binary_op(BVXor, Xor, getnode(nids[1]), getnode(nids[2]))

            if ntype == XNOR:
                nodemap[nid] = BVNot(binary_op(BVXor, Xor, getnode(nids[1]), getnode(nids[2])))

            if ntype == NAND:
                bvop = lambda x,y: BVNot(BVAnd(x, y))
                bop = lambda x,y: Not(And(x, y))
                nodemap[nid] = binary_op(bvop, bop, getnode(nids[1]), getnode(nids[2]))

            if ntype == IMPLIES:
                nodemap[nid] = BVOr(BVNot(getnode(nids[1])), getnode(nids[2]))

            if ntype == NOT:
                nodemap[nid] = unary_op(BVNot, Not, getnode(nids[1]))

            if ntype == NEG:
                nodemap[nid] = unary_op(BVNeg, Not, getnode(nids[1]))

            if ntype == UEXT:
                nodemap[nid] = BVZExt(B2BV(getnode(nids[1])), int(nids[2]))

            if ntype == SEXT:
                nodemap[nid] = BVSExt(B2BV(getnode(nids[1])), int(nids[2]))

            if ntype == OR:
                nodemap[nid] = binary_op(BVOr, Or, getnode(nids[1]), getnode(nids[2]))

            if ntype == ADD:
                nodemap[nid] = BVAdd(B2BV(getnode(nids[1])), B2BV(getnode(nids[2])))

            if ntype == SUB:
                nodemap[nid] = BVSub(B2BV(getnode(nids[1])), B2BV(getnode(nids[2])))
            
            # mod/div
            if ntype == SREM:
                nodemap[nid] = BVSRem(B2BV(getnode(nids[1])), B2BV(getnode(nids[2])))
            if ntype == UREM:
                nodemap[nid] = BVURem(B2BV(getnode(nids[1])), B2BV(getnode(nids[2])))
            if ntype == SDIV:
                nodemap[nid] = BVSDiv(B2BV(getnode(nids[1])), B2BV(getnode(nids[2])))
            if ntype == UDIV:
                nodemap[nid] = BVUDiv(B2BV(getnode(nids[1])), B2BV(getnode(nids[2])))

            if ntype == UGT:
                nodemap[nid] = BVUGT(B2BV(getnode(nids[1])), B2BV(getnode(nids[2])))

            if ntype == UGTE:
                nodemap[nid] = BVUGE(B2BV(getnode(nids[1])), B2BV(getnode(nids[2])))

            if ntype == ULT:
                nodemap[nid] = BVULT(B2BV(getnode(nids[1])), B2BV(getnode(nids[2])))

            if ntype == ULTE:
                nodemap[nid] = BVULE(B2BV(getnode(nids[1])), B2BV(getnode(nids[2])))

            if ntype == SGT:
                nodemap[nid] = BVSGT(B2BV(getnode(nids[1])), B2BV(getnode(nids[2])))

            if ntype == SGTE:
                nodemap[nid] = BVSGE(B2BV(getnode(nids[1])), B2BV(getnode(nids[2])))

            if ntype == SLT:
                nodemap[nid] = BVSLT(B2BV(getnode(nids[1])), B2BV(getnode(nids[2])))

            if ntype == SLTE:
                nodemap[nid] = BVSLE(B2BV(getnode(nids[1])), B2BV(getnode(nids[2])))

            if ntype == EQ:
                nodemap[nid] = BVComp(B2BV(getnode(nids[1])), B2BV(getnode(nids[2])))

            if ntype == NEQ:
                nodemap[nid] = BVNot(BVComp(getnode(nids[1]), getnode(nids[2])))

            if ntype == MUL:
                nodemap[nid] = BVMul(B2BV(getnode(nids[1])), B2BV(getnode(nids[2])))

            if ntype == SLICE:
                nodemap[nid] = BVExtract(B2BV(getnode(nids[1])), int(nids[3]), int(nids[2]))

            if ntype == SLL:
                nodemap[nid] = BVLShl(getnode(nids[1]), getnode(nids[2]))

            if ntype == SRA:
                nodemap[nid] = BVAShr(getnode(nids[1]), getnode(nids[2]))

            if ntype == SRL:
                nodemap[nid] = BVLShr(getnode(nids[1]), getnode(nids[2]))

            if ntype == ITE:
                if (get_type(getnode(nids[2])) == BOOL) or (get_type(getnode(nids[3])) == BOOL):
                    nodemap[nid] = Ite(BV2B(getnode(nids[1])), B2BV(getnode(nids[2])), B2BV(getnode(nids[3])))
                else:
                    nodemap[nid] = Ite(BV2B(getnode(nids[1])), getnode(nids[2]), getnode(nids[3]))

            if ntype == NEXT:
                if (get_type(getnode(nids[1])) == BOOL) or (get_type(getnode(nids[2])) == BOOL):
                    lval = TS.get_prime(getnode(nids[1]))
                    rval = B2BV(getnode(nids[2]))
                else:
                    lval = TS.get_prime(getnode(nids[1]))
                    rval = getnode(nids[2])

                nxt_node_set.add(nid)
                nodemap[nid] = EqualsOrIff(lval, rval)

                ftrans.append(
                     (lval,
                     rval)
                )

            if ntype == INIT:
                if (get_type(getnode(nids[1])) == BOOL) or (get_type(getnode(nids[2])) == BOOL):
                    nodemap[nid] = EqualsOrIff(BV2B(getnode(nids[1])), BV2B(getnode(nids[2])))
                elif get_type(getnode(nids[1])).is_array_type():
                    _type = get_type(getnode(nids[1]))
                    nodemap[nid] = EqualsOrIff(getnode(nids[1]), Array(_type.index_type, default=getnode(nids[2])))
                else:
                    nodemap[nid] = EqualsOrIff(getnode(nids[1]), getnode(nids[2]))
                initlist.append(getnode(nid))

            if ntype == CONSTRAINT:
                nodemap[nid] = BV2B(getnode(nids[0]))
                invarlist.append(getnode(nid))

            if ntype == BAD:
                nodemap[nid] = getnode(nids[0])

                if ASSERTINFO in line:
                    filename_lineno = os.path.basename(nids[3])
                    assert_name = 'embedded_assertion_%s'%filename_lineno
                    description = "Embedded assertion at line {1} in {0}".format(*filename_lineno.split(COLON_REP))
                else:
                    assert_name = 'embedded_assertion_%i'%prop_count
                    description = 'Embedded assertion number %i'%prop_count
                    prop_count += 1

                # Following problem format (name, description, strformula)
                invar_props.append((assert_name, description, simplify(Not(BV2B(getnode(nid))))))

            if nid not in nodemap and ntype != OUTPUT:
                print("Unknown node type \"%s\""%ntype)
                exit(1)

            # get wirename if it exists
            if ntype not in {STATE, INPUT, BAD, OUTPUT}:
                # skipp those with '$' in the head
                if nid not in self.skipped_name_nid:
                    # check for wirename, if it's an integer, then it's a node ref
                    idx = len(nids)-1
                    while idx > -1:
                      if str(nids[idx]).isdigit():
                        break
                      idx -= 1
                    idx += 1
                    if 0 <= idx and idx < len(nids):
                        wirename = str(' '.join(nids[idx:]))
                        wirename = wirename.split(' ; ')[0]
                        expr = nodemap[str(nid)]
                        ts.register_wire_name(wirename, expr)
                    

        if Config_Warning: #TODO: fix the warning!
            name = lambda x: str(nodemap[x]) if nodemap[x].is_symbol() else x
            uncovered = [name(x) for x in nodemap if\
                x not in node_covered and \
                x not in nxt_node_set and \
                x not in output_node_set]
            uncovered.sort()
            if len(uncovered) > 0:
                print("Unlinked nodes \"%s\""%",".join(uncovered))
            nxt_node_used = node_covered.intersection(nxt_node_set)
            if len(nxt_node_used) > 0:
                print('Next node used : ', nxt_node_used)

        init = simplify(And(initlist))

        invar = simplify(And(invarlist))

        # instead of trans, we're using the ftrans format -- see below
        ts.set_init(init)
        # add dependent relations
        for prime_var, rhs in ftrans:
            ts.record_dependent_sv(TS.get_primal(prime_var), get_all_var_of_e(rhs))
            ts.set_per_sv_update(TS.get_primal(prime_var), rhs)
            
            
        ts.finish_record_dependent_sv()
        
        # add ftrans
        ts.add_func_trans( And([EqualsOrIff(prime_var,rhs) for prime_var, rhs in ftrans]) )
        ts.set_assertion(simplify(And([p[2] for p in invar_props])))
        ts.set_assumption(invar)
        
            
        ts.finish_adding()

        return (ts, invar_props)


def test_btor_parsing():
    btor_parser = BTOR2Parser()
    sts, propList = btor_parser.parse_file(Path("example/pipe-with-stall.btor2"))
    # print(propList)
    print (sts.variables) #{clk, reg_init, rst, stall1in, stall2in, stall3in, w, stage3, tag3, reg_v_comp, tag2, reg_v, stage1, wen_stage2, wen_stage1, stage2, tag0, tag1}
    print (sts.init) #tag
    print (sts.trans.serialize()) #
    print (propList[0][2].serialize()) #(! ((! ((! tag3) | (reg_v_comp bvcomp stage3))) = 1_1))
    for pv, prevs in sts.sv_dependent_map.items():
        print (str(pv), '<---', prevs)
    for v, nxtvs in sts.sv_influence_map.items():
        print (str(v), '--->', nxtvs)
    for n,expr in sts.named_var.items():
        print (str(n), '--e-->', expr.serialize())


if __name__ == '__main__':
    test_btor_parsing()

#input: btor2
#output: prevs ---> pv
#        v ---> nxtvs
#        n --e--> expr