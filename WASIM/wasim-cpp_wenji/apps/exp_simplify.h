#pragma once 

#include "term_manip.h"

namespace wasim {
    // check if contains some + - concat bvlshr bvshl and bitwidth etc
    // bool is_expr_likely_datapath(const smt::Term & t);

    smt::Term simplify_ite_subcase(const smt::Term & t);
    // smt::
}
