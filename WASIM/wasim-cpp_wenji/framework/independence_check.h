#pragma once

#include <string>
// #include <iomanip>
// #include <unordered_map>

#include "assert.h"
#include "smt-switch/exceptions.h"
#include "smt-switch/smt.h"
#include "term_manip.h"

// #include "ts.h"

// #include <iostream>
// #include <unordered_map>
// #include <utility>
// #include <functional>
// #include <vector>
// #include <set>
// #include <any>
// #include <variant>

using namespace std;

namespace wasim {
// bool is_bv_constant(smt::Term e);

// NOTE: all these functions require that there are no other contraints in
// SmtSolvers

// returns ( ! SAT(e == 0) ) given assumptions
bool e_is_always_valid(const smt::Term & e,
                       smt::TermVec assumptions /*={}*/,
                       const smt::SmtSolver & s);  // no test

// returns ( ! SAT(e == 1) ) given assumptions
bool e_is_always_invalid(const smt::Term & e,
                         smt::TermVec assumptions /*={}*/,
                         const smt::SmtSolver & s);  // no test

// make two copies of v : v1, v2.  Check if  UNSAT( e[v/v1] != e[v/v2] ) , given
// the assumptions
bool e_is_independent_of_v(const smt::Term & e,
                           const smt::Term & v,
                           const smt::TermVec & assumptions); 

  // HZ: the reason for making a new solver is because I want to make the
  // context of the original solver clear from the new variables we created
  // locally in this function I was hoping push/pop can be used to create
  // temporary SMT variables however, it is not the case.

// bool is_valid(smt::Term e, smt::SmtSolver& s); // no test

}  // namespace wasim
