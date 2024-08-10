#include "symsim.h"

#include "smt-switch/utils.h"

using namespace std;

namespace wasim {

unsigned SymbolicExecutor::tracelen() const { return trace_.size(); }

smt::TermVec SymbolicExecutor::all_assumptions() const
{
  smt::TermVec ret_vec;
  for (const auto & l : history_assumptions_) {
    for (const auto & c : l) {
      ret_vec.push_back(c);
    }
  }
  return ret_vec;
}

std::vector<std::string> SymbolicExecutor::all_assumption_interp() const
{
  std::vector<std::string> ret_vec;
  for (const auto & l : history_assumptions_interp_) {
    for (const auto & c : l) {
      ret_vec.push_back(c);
    }
  }
  return ret_vec;
}

smt::Term SymbolicExecutor::var(const std::string & n) const
{
  return ts_.named_terms().at(n);
}

smt::Term SymbolicExecutor::cur(const std::string & n) const
{
  const auto & sv_mapping = trace_.back();
  smt::Term expr = var(n);
  if (!_expr_only_sv(expr)) {
    assert(history_choice_.size() != 0);
    assert(!history_choice_.back().UsedInSim_);
    smt::UnorderedTermMap iv_mapping = history_choice_.back().var_assign_;
    auto subs_mapping = sv_mapping;  // make a copy
    subs_mapping.insert(iv_mapping.begin(), iv_mapping.end());
    smt::Term expr = solver_->substitute(expr, subs_mapping);
  } else {
    smt::Term expr = solver_->substitute(expr, sv_mapping);
  }
  return expr;
}

void SymbolicExecutor::_check_only_invar(
    const smt::UnorderedTermMap & vdict) const
{
  for (const auto & v : vdict) {
    if (invar_.find(v.first) == invar_.end())
      throw SimulatorException("Expecting " + v.first->to_string()
                          + " to be input var");
  }
}

bool SymbolicExecutor::_expr_only_sv(const smt::Term & expr) const
{
  smt::UnorderedTermSet var_set;
  smt::get_free_symbols(expr, var_set);

  for (const auto & v : var_set) {
    if (svar_.find(v) != svar_.end())
      return true;
    else
      return false;
  }
  // if there is no variable, then it is also only sv
  return true;
}

smt::UnorderedTermMap SymbolicExecutor::convert(
    const assignment_type & vdict) const
{
  smt::UnorderedTermMap retdict;
  for (const auto & v : vdict) {  // check key only
    const auto & key = v.first;
    const auto & value = v.second;

    smt::Term key_new = var(key);
    // if(svar_.find(key_new) == svar_.end() && invar_.find(key_new) ==
    // invar_.end())
    //    throw SimulatorException("var name " + key + " is not a state/input
    //    variable");

    if (std::holds_alternative<std::string>(value)) {
      auto value_str = std::get<std::string>(value);
      auto key_sort = key_new->get_sort();
      auto value_new = solver_->make_symbol(value_str, key_sort);
      retdict.emplace(key_new, value_new);
    } else if (std::holds_alternative<int>(value)) {
      auto value_int = std::get<int>(value);
      auto key_sort = key_new->get_sort();

      auto value_new = solver_->make_term(value_int, key_sort);
      retdict.emplace(key_new, value_new);
    } else
      throw SimulatorException("Unhandled case in assignment_type");
  }
  return retdict;
}

void SymbolicExecutor::backtrack()
{
  assert(history_choice_.size() != 0);
  trace_.pop_back();
  history_assumptions_.pop_back();
  history_assumptions_interp_.pop_back();
  history_choice_.back().UsedInSim_ = false;
}

void SymbolicExecutor::init(
    const smt::UnorderedTermMap & var_assignment /*={}*/)
{
  trace_.push_back(var_assignment);

  auto & var_assignment_ref = trace_.back();
  for (const auto & v : svar_) {
    if (var_assignment_ref.find(v) == var_assignment_ref.end()) {
      var_assignment_ref[v] =
          new_var(v->get_sort()->get_width(), v->to_string(), false);
    }
  }

  // make sure the init constraint only contains state variables
  // you cannot constrain input variables in the initial state
  // btorparser will help convert the TS to avoid this
  _expr_only_sv(ts_.init());

  auto init_constr = solver_->substitute(ts_.init(), var_assignment_ref);
  history_assumptions_.push_back({ init_constr });
  history_assumptions_interp_.push_back({ "init" });
}

void SymbolicExecutor::set_current_state(const StateAsmpt & s)
{
  trace_.clear();
  trace_.push_back(s.get_sv());

  // smt::TermVec asmpt_copy(s.asmpt_.begin(), s.asmpt_.end());
  // std::vector<std::string> asmpt_interp_copy(s.assumption_interp_.begin(),
  // s.assumption_interp_.end());

  history_assumptions_.clear();
  history_assumptions_.push_back(s.get_assumptions());
  history_assumptions_interp_.clear();
  history_assumptions_interp_.push_back(s.get_assumption_interpretations());
  history_choice_.clear();
}

void SymbolicExecutor::print_current_step() const
{
  const auto & prev_sv = trace_.back();
  // cout << "sv  rhs" << endl;
  cout << "--------------------------------" << endl;
  cout << "| " << setiosflags(ios::left) << setw(20) << "sv"
       << "| " << setw(20) << "value" << endl;
  cout << "--------------------------------" << endl;
  for (const auto & sv : prev_sv) {
    cout << "| " << setiosflags(ios::left) << setw(20) << sv.first->to_string()
         << "| " << setw(20) << sv.second->to_string() << endl;
  }
}

void SymbolicExecutor::print_current_step_assumptions() const
{
  int i = 0;
  for (const auto & l : history_assumptions_) {
    int j = 0;
    for (const auto & a : l) {
      const auto & interp = history_assumptions_interp_.at(i).at(j);
      cout << "A" << i << ", " << j << " " << interp << endl;
      cout << "A" << i << ", " << j << " " << a << endl;
      j++;
    }
    i++;
  }
}

void SymbolicExecutor::set_input(const smt::UnorderedTermMap & invar_assign,
                                 const smt::TermVec & pre_assumptions)
{
  if (history_choice_.size() != 0) {
    history_choice_.back().CheckSimed();
  }
  _check_only_invar(invar_assign);
  const auto & prev_sv(trace_.back());

  history_choice_.push_back(ChoiceItem(
      pre_assumptions, invar_assign));  // construct by r-value reference
  auto & c = history_choice_.back();

  for (const auto & v : invar_) {
    if (prev_sv.find(v) != prev_sv.end()) {
      cout << "WARNING: shadowing input assignment as assigned by prev-state "
           << v->to_string() << endl;
    }
    if (c.var_assign_.find(v) == c.var_assign_.end()) {
      c.var_assign_[v] =
          new_var(v->get_sort()->get_width(), v->to_string(), true);
    }
  }
  const auto & invar_assign_all = c.var_assign_;

  unsigned len = history_assumptions_.back().size();
  c.record_prev_assumption_len(len);

  assert(history_assumptions_.size() == history_assumptions_interp_.size());
  assert(history_assumptions_.back().size()
         == history_assumptions_interp_.back().size());

  auto submap(prev_sv);  // copy here is needed anyway
  submap.insert(invar_assign_all.begin(), invar_assign_all.end());

  // TODO: constraints here are different from those in COSA btor parser!
  // the second Boolean has no use in our case
  smt::TermVec assmpt_vec;
  for (const auto & vect : ts_.constraints()) {
    auto assumption = solver_->substitute(vect.first, submap);
    assmpt_vec.push_back(assumption);
  }

  smt::Term assmpt;
  if (assmpt_vec.size() == 1) {
    assmpt = assmpt_vec.back();
  } else {
    assmpt = solver_->make_term(smt::And, assmpt_vec);
  }

  history_assumptions_.back().push_back(assmpt);
  history_assumptions_interp_.back().push_back(
      "ts.asmpt @" + (std::to_string(trace_.size() - 1)));

  for (const auto & vect : pre_assumptions) {
    auto assmpt_temp = solver_->substitute(vect, submap);
    history_assumptions_.back().push_back(assmpt_temp);
    history_assumptions_interp_.back().push_back(
        vect->to_string() + "@" + std::to_string(trace_.size() - 1));
  }
}  // end of set_input

void SymbolicExecutor::undo_set_input()
{
  assert(history_choice_.size() != 0);
  const auto & c = history_choice_.back();  // avoid copy
  assert(!c.UsedInSim_);
  auto l = c.get_prev_assumption_len();
  history_assumptions_.back().resize(l);
  history_assumptions_interp_.back().resize(l);
  history_choice_
      .pop_back();  // you can only pop in the end, o.w. reference will fail
}

/// similar to cur(), but will check no reference to the input variables
smt::Term SymbolicExecutor::interpret_state_expr_on_curr_frame(
    const smt::Term & expr) const
{
  if (!_expr_only_sv(expr))
    throw SimulatorException("expr should only contain only state variables");
  const auto & prev_sv = trace_.back();
  return solver_->substitute(expr, prev_sv);
}

/// similar to cur(), but will check no reference to the input variables
smt::TermVec SymbolicExecutor::interpret_state_expr_on_curr_frame(
    const smt::TermVec & expr_list) const
{
  smt::TermVec ret;
  for (const auto & e : expr_list) {
    smt::Term e_term = interpret_state_expr_on_curr_frame(e);
    ret.push_back(std::move(e_term));
  }
  return ret;
}

void SymbolicExecutor::sim_one_step()
{
  assert(history_choice_.size() != 0);

  auto & c = history_choice_.back();
  c.setSim();

  const auto & invar_assign = c.var_assign_;
  const auto & prev_sv = trace_.back();
  smt::UnorderedTermMap svmap;
  auto submap = prev_sv;
  submap.insert(invar_assign.begin(), invar_assign.end());
  for (const auto & sv : ts_.state_updates()) {
    svmap[sv.first] = solver_->substitute(sv.second, submap);
  }
  trace_.push_back(
      std::move(svmap));  // svmap will not be used afterwards, avoid copy
  history_assumptions_.push_back({});
  history_assumptions_interp_.push_back({});
}

// void SymbolicExecutor::sim_one_step_direct()
// {
//   const auto & prev_sv = trace_.back();
//   smt::UnorderedTermMap svmap;
//   for (const auto & sv : ts_.state_updates()) {
//     svmap[sv.first] = solver_->substitute(sv.second, prev_sv);
//   }
//   trace_.push_back(std::move(svmap));
//   history_assumptions_.push_back({});
//   history_assumptions_interp_.push_back({});
// }

smt::Term SymbolicExecutor::new_var(int bitwdth,
                                    const std::string & vname /*"=var"*/,
                                    bool x /*=true*/)
{
  std::string n = x ? vname + "X" : vname;
  auto symb_sort = solver_->make_sort(smt::BV, bitwdth);
  smt::Term symb = free_make_symbol(n, symb_sort, name_cnt_, solver_);

  if (x) Xvar_.insert(symb);
  return symb;
}

StateAsmpt SymbolicExecutor::get_curr_state(const smt::TermVec & assumptions)
{
  auto need_to_push_input = false;
  if ((history_choice_.size() == 0) || (history_choice_.back().UsedInSim_))
    need_to_push_input = true;

  if (need_to_push_input)
    set_input({}, assumptions);
  else if (assumptions.size() != 0)
    cout << "WARNING: assumptions are not used in get_curr_state" << endl;

  StateAsmpt ret(trace_.back(), all_assumptions(), all_assumption_interp());
  if (need_to_push_input) {
    undo_set_input();
  }
  return ret;
}

smt::Term SymbolicExecutor::set_var(int bitwdth, std::string vname /*= "var"*/)
{
  auto symb_sort = solver_->make_sort(smt::BV, bitwdth);
  auto symb = solver_->make_symbol(vname, symb_sort);
  return symb;
}

}  // namespace wasim