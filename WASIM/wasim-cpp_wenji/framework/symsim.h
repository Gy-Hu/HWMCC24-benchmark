#pragma once
#include <iomanip>
#include <string>
#include <unordered_map>
#include "assert.h"
#include "time.h"

#include "smt-switch/generic_sort.h"
#include "smt-switch/smt.h"

#include "utils/exceptions.h"

#include "term_manip.h"
#include "ts.h"

#include <functional>
#include <iostream>
#include <map>
#include <set>
#include <unordered_map>
#include <utility>
#include <variant>
#include <vector>

namespace wasim {

/// std::string : a symbolic value, int : a concrete value
typedef std::variant<int, std::string> value_type;
/// from string (variable name) to value
typedef std::map<std::string, value_type> assignment_type;

class SymbolicExecutor
{
 private:
  /// a class only used in symbolic executor
  class ChoiceItem
  {
   public:
    ChoiceItem(const smt::TermVec & assumptions,
               const smt::UnorderedTermMap & var_assign)
        : assumptions_(assumptions), var_assign_(var_assign), UsedInSim_(false)
    {
    }

    void setSim()
    {
      assert(!UsedInSim_);
      UsedInSim_ = true;
    }
    void CheckSimed() const { assert(UsedInSim_); }
    void record_prev_assumption_len(unsigned l) { assmpt_len_ = l; }
    unsigned get_prev_assumption_len() const { return assmpt_len_; }

    smt::TermVec assumptions_;
    smt::UnorderedTermMap var_assign_;
    bool UsedInSim_;
    unsigned assmpt_len_;
  };  // end of class ChoiceItem

 public:
  // we will keep a reference to ts
  // and a copy of the pointer to the solver
  SymbolicExecutor(TransitionSystem & ts, const smt::SmtSolver & s)
      : ts_(ts), solver_(s), invar_(ts.inputvars()), svar_(ts.statevars())
  {
  }

 protected:
  TransitionSystem & ts_;
  smt::SmtSolver solver_;  // smt::SmtSolver is a smart pointer
  const smt::UnorderedTermSet & invar_;
  const smt::UnorderedTermSet & svar_;
  std::vector<smt::UnorderedTermMap> trace_;
  std::vector<ChoiceItem> history_choice_;
  std::vector<smt::TermVec> history_assumptions_;
  std::vector<std::vector<std::string>> history_assumptions_interp_;
  std::unordered_map<std::string, int> name_cnt_;
  smt::UnorderedTermSet Xvar_;

  void _check_only_invar(const smt::UnorderedTermMap & vdict) const;
  bool _expr_only_sv(const smt::Term & expr) const;

  /**
   * @brief
   *
   * @param bitwdth
   * @param vname
   * @param x
   * @return smt::Term
   */
  smt::Term new_var(int bitwdth,
                    const std::string & vname = "var",
                    bool x = true);

 public:
  /// get the length of the trace
  unsigned tracelen() const;
  /// collect all assumptions on each frame
  smt::TermVec all_assumptions() const;
  /// collect all interpretations of assumptions on each frame
  std::vector<std::string> all_assumption_interp() const;
  /// get the term for a variable
  smt::Term var(const std::string & n) const;
  /// get the term for name n, then use the current symbolic
  /// variable assignment to substitute all variables in it
  /// if it contains input variable, use the most recent input
  /// variable assignment as well
  smt::Term cur(const std::string & n) const;
  /// print the current state variable assignment
  void print_current_step() const;
  /// get the assumptions (collected from all previous steps)
  void print_current_step_assumptions() const;

  /// a shortcut to create symbolic variables/concrete values in a map
  smt::UnorderedTermMap convert(const assignment_type & vdict) const;

  /// goto the previous simulation step
  void backtrack();
  /// use the given variable assignment to initialize
  void init(const smt::UnorderedTermMap & var_assignment = {});
  /// re-assign the current state
  void set_current_state(const StateAsmpt & s);
  /// set the input variable values before simulating next step
  ///  (and also set some assumptions before the next step)
  void set_input(const smt::UnorderedTermMap & invar_assign,
                 const smt::TermVec & pre_assumptions);
  /// undo the input setting
  /// usage: set_input -> sim_one_step --> (a new state) -> backtrack ->
  /// undo_set_input
  void undo_set_input();

  /// similar to cur(), but will check no reference to the input variables
  smt::Term interpret_state_expr_on_curr_frame(const smt::Term & expr) const;
  /// similar to cur(), but will check no reference to the input variables
  smt::TermVec interpret_state_expr_on_curr_frame(
      const smt::TermVec & expr) const;

  /// do simulation
  void sim_one_step();

  /// get the set of all X variables
  const smt::UnorderedTermSet & get_Xs() const { return Xvar_; }

  /// get (a copy of) the current state
  StateAsmpt get_curr_state(const smt::TermVec & assumptions = {});
  /// a shortcut to create a variable
  smt::Term set_var(int bitwdth, std::string vname = "var");

  /// get solver
  smt::SmtSolver get_solver() const { return solver_; }

};
}  // namespace wasim
