#pragma once

#include "tracemgr.h"
#include "ts.h"


using namespace std;

namespace wasim {

// will attempt to simplify (remove the set of xvar)
// it is better if you can first use independence check to find a set of
// xvar that can be simplified
//   namely: state_simplify.h / get_xvar_independent
smt::Term sygus_simplify_expr(
    const smt::Term & expr, 
    const smt::UnorderedTermSet & set_of_xvar_btor,
    smt::SmtSolver & solver);

// attempt to simplify the variable assigments in state_btor
// assuming all expressions in state_btor are in solver btor
// will create a CVC solver inside and do the translation
void sygus_simplify(StateAsmpt & state_btor,
                    const smt::UnorderedTermSet & set_of_xvar_btor,
                    smt::SmtSolver & solver);

}  // namespace wasim