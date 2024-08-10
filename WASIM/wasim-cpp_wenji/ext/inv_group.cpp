#include "inv_group.h"
using namespace std;

namespace wasim {

smt::Term tobool(smt::Term expr, smt::SmtSolver & solver)
{
  return solver->make_term(smt::Equal, expr, solver->make_term(1));
}

void InvGroup::branch2state()
{
  // 1. get state group
  for (const auto & state_list : branch_list_) {
    smt::Term state_expr_single = {};
    smt::TermVec state_expr_vec = {};
    for (const auto & sv : state_list.at(layer_).sv_) {
      auto var = sv.first;
      auto value = sv.second;
      state_expr_single = solver_->make_term(smt::Equal, var, value);
      state_expr_vec.push_back(state_expr_single);
    }
    smt::Term state_expr;
    if (state_expr_vec.size() > 1) {
      state_expr = solver_->make_term(smt::And, state_expr_vec);
    } else {
      state_expr = state_expr_vec.at(0);
    }
    state_group_.push_back(state_expr);

    auto asmpt = state_list.at(layer_).asmpt_;
    auto asmpt_and = solver_->make_term(smt::And, asmpt);
    asmpt_group_.push_back(asmpt_and);
  }
  // get state group end

  // 2. get inv group
  for (const auto & state_expr : state_group_) {
    auto inv_expr = solver_->make_term(smt::Implies, tag_, state_expr);
    inv_group_.push_back(inv_expr);
  }

  // 3. get state dedup
  for (const auto & state_expr : state_group_) {
    if (std::find(state_dedup_.begin(), state_dedup_.end(), state_expr)
        != state_dedup_.end()) {
      // found state_expr in state_dedup
      continue;
    } else {
      state_dedup_.push_back(state_expr);
    }
  }

  for (const auto & asmpt_expr : asmpt_group_) {
    if (std::find(asmpt_dedup_.begin(), asmpt_dedup_.end(), asmpt_expr)
        != asmpt_dedup_.end()) {
      // found state_expr in state_dedup
      continue;
    } else {
      asmpt_dedup_.push_back(asmpt_expr);
    }
  }

  // 4. get inv dedup
  for (auto inv_expr : inv_group_) {
    if (std::find(inv_dedup_.begin(), inv_dedup_.end(), inv_expr)
        != inv_dedup_.end()) {
      // found state_expr in state_dedup
      continue;
    }
    inv_dedup_.push_back(inv_expr);
  }
}

smt::TermVec InvGroup::state_group() { return state_group_; }

smt::TermVec InvGroup::asmpt_group() { return asmpt_group_; }

smt::TermVec InvGroup::inv_group() { return inv_group_; }

smt::TermVec InvGroup::state_dedup() { return state_dedup_; }

smt::TermVec InvGroup::inv_dedup() { return inv_dedup_; }

smt::TermVec InvGroup::extract_prop(std::string var_name)
{
  smt::TermVec extract_vec = {};
  for (const auto & state_list : branch_list_) {
    for (const auto & sv : state_list.at(layer_).sv_) {
      auto var = sv.first;
      auto value = sv.second;
      if (var->to_string() == var_name) {
        extract_vec.push_back(value);
      }
    }
  }
  return extract_vec;
}

std::vector<int> InvGroup::check_unsat_expr(std::vector<int> truelist_num,
                                            smt::Term cex_expr)
{
  /// IMPORTANT: modify the assumptions with cex_expr simultaneously
  smt::TermVec asmpt_group_temp = {};
  for (int i = 0; i < asmpt_group_.size(); i++) {  // may be slow
    smt::Term asmpt = {};
    for (const auto & num : truelist_num) {
      if (i == num) {
        asmpt = solver_->make_term(smt::And,
                                   solver_->make_term(smt::Not, cex_expr),
                                   asmpt_group_.at(i));
      } else {
        asmpt = asmpt_group_.at(i);
      }
    }
    asmpt_group_temp.push_back(asmpt);
  }
  assert(asmpt_group_temp.size() == asmpt_group_.size());
  asmpt_group_.clear();
  asmpt_group_.insert(
      asmpt_group_.end(), asmpt_group_temp.begin(), asmpt_group_temp.end());

  /// check truelist
  std::vector<int> truelist_num_ret = {};
  for (const auto & num : truelist_num) {
    auto asmpt_sat_check =
        solver_->make_term(smt::And, asmpt_group_.at(num), cex_expr);
    auto unsat_check_res = is_sat_res(smt::TermVec{ asmpt_sat_check }, solver_);
    if (unsat_check_res.is_unsat() == false) {
      cout << "UNSAT check false!!\n\n" << endl;
      cout << num << endl;
      // assert(false);
    } else {
      truelist_num_ret.push_back(num);
    }
  }
  cout << "num: " << truelist_num_ret.size() << endl;
  assert(truelist_num_ret.size() != 0);
  // assert(truelist_num.size() == truelist_num_ret.size());
  return truelist_num_ret;
}

void InvGroup::add_unsat_asmpt(smt::Term unsat_expr, int idx)
{
  smt::TermVec state_group_temp = {};
  smt::TermVec inv_group_temp = {};
  /// update state group
  for (int i = 0; i < state_group_.size(); i++) {
    auto state_expr = state_group_.at(i);
    smt::Term state_expr_new = {};
    if (i == idx) {
      state_expr_new = solver_->make_term(smt::And, state_expr, unsat_expr);
    } else {
      state_expr_new = state_expr;
    }
    state_group_temp.push_back(state_expr_new);
  }
  state_group_.clear();
  state_group_.insert(
      state_group_.end(), state_group_temp.begin(), state_group_temp.end());

  /// update inv group
  inv_group_.clear();
  for (const auto & state_expr : state_group_) {
    auto inv_expr = solver_->make_term(smt::Implies, tag_, state_expr);
    inv_group_.push_back(inv_expr);
  }
}

check_res init_check(smt::Term init,
                     smt::Term inv,
                     smt::Term asmpt /*={}*/,
                     smt::SmtSolver & solver)
{
  auto LHS = solver->make_term(smt::And, init, asmpt);
  auto RHS = inv;
  auto sat_check_expr = solver->make_term(smt::Implies, LHS, RHS);
  auto check_result = is_valid_bool(sat_check_expr, solver);
  cout << "\nInit check: " << check_result << endl;
  check_res res = {};
  if (check_result == false) {
    cout << "Counter Example:" << endl;
    #error HERE is a problem. is_sat_res already pop. Model might be unavailable/unreliable
    auto cex = get_invalid_model(sat_check_expr, solver);
    auto cex_str = sort_model(cex);
    res = make_pair(check_result, cex);
  } else {
    cout << "No Counter Example!" << endl;
    smt::UnorderedTermMap cex_none = {};
    res = make_pair(check_result, cex_none);
  }

  return res;
}

check_res inv_check(smt::Term inv,
                    smt::Term trans_update,
                    smt::Term asmpt /*={}*/,
                    TransitionSystem sts,
                    smt::SmtSolver & solver)
{
  auto LHS =
      solver->make_term(smt::And, smt::TermVec{ inv, asmpt, trans_update });
  auto RHS = solver->substitute(inv, sts.state_updates());
  auto sat_check_expr = solver->make_term(smt::Implies, LHS, RHS);
  auto check_result = is_valid_bool(sat_check_expr, solver);

  cout << "\nInv check: " << check_result << endl;
  check_res res = {};
  if (check_result == false) {
    cout << "Counter Example:" << endl;
    #error HERE is a problem. is_sat_res already pop. Model might be unavailable/unreliable
    auto cex = get_invalid_model(sat_check_expr, solver);
    auto cex_str = sort_model(cex);
    res = make_pair(check_result, cex);
  } else {
    cout << "No Counter Example!" << endl;
    smt::UnorderedTermMap cex_none = {};
    res = make_pair(check_result, cex_none);
  }

  return res;
}

check_res prop_check(smt::Term prop,
                     smt::Term inv,
                     smt::Term asmpt,
                     smt::SmtSolver & solver)
{
  auto LHS = solver->make_term(smt::And, inv, asmpt);
  auto RHS = prop;
  auto sat_check_expr = solver->make_term(smt::Implies, LHS, RHS);
  auto check_result = is_valid_bool(sat_check_expr, solver);
  cout << "\nProp check: " << check_result << endl;
  check_res res = {};
  if (check_result == false) {
    cout << "Counter Example:" << endl;
    #error HERE is a problem. is_sat_res already pop. Model might be unavailable/unreliable
    auto cex = get_invalid_model(sat_check_expr, solver);
    auto cex_str = sort_model(cex);
    res = make_pair(check_result, cex);
  } else {
    cout << "No Counter Example!" << endl;
    smt::UnorderedTermMap cex_none = {};
    res = make_pair(check_result, cex_none);
  }

  return res;
}

smt::TermVec deduplicate(smt::TermVec vec)
{
  smt::TermVec dedup_vec = {};
  for (const auto & expr : vec) {
    if (std::find(dedup_vec.begin(), dedup_vec.end(), expr)
        != dedup_vec.end()) {
      // found state_expr in state_dedup
      continue;
    } else {
      dedup_vec.push_back(expr);
    }
  }
  return dedup_vec;
}

cex_res cex_parser(smt::UnorderedTermMap cex,
                   std::unordered_set<std::string> tag_set,
                   std::unordered_set<std::string> ctrl_set,
                   smt::SmtSolver & solver)
{
  // 1. get current tag
  smt::Term tag_ret = {};
  smt::UnorderedTermMap ctrl_map = {};
  smt::TermVec ctrl_ret = {};
  for (const auto & cex_expr : cex) {
    auto var = cex_expr.first;
    auto value = cex_expr.second;
    if (tag_set.find(var->to_string()) != tag_set.end()) {
      if (value->to_int() == 1) {
        tag_ret = var;
      }
    }

    if (ctrl_set.find(var->to_string()) != ctrl_set.end()) {
      auto expr = solver->make_term(smt::Equal, var, value);
      ctrl_ret.push_back(expr);
    }
  }

  cex_res ret = make_pair(tag_ret, ctrl_ret);
  return ret;
}

std::vector<int> test_cex(smt::TermVec formula_vec,
                          smt::UnorderedTermMap cex,
                          smt::SmtSolver & solver)
{
  std::vector<int> true_vec_num = {};
  for (int i = 0; i < formula_vec.size(); i++) {
    auto inv_formula = formula_vec.at(i);
    cout << i << endl;
    cout << inv_formula->to_string() << endl;
    auto cex_eva = solver->substitute(inv_formula, cex);
    cout << "---------> " << cex_eva->to_string() << endl;
    if (cex_eva->to_string() == "#b1") {  // TODO: maybe not safe
      true_vec_num.push_back(i);
    }
  }
  return true_vec_num;
}

std::vector<int> comb_unq(std::vector<int> vec1, std::vector<int> vec2)
{
  std::vector<int> vec3 = {};
  vec3.insert(vec3.end(), vec1.begin(), vec1.end());
  vec3.insert(vec3.end(), vec2.begin(), vec2.end());
  std::set<int> vecset(vec3.begin(), vec3.end());
  std::vector<int> vec_ret(vecset.begin(), vecset.end());
  std::sort(vec_ret.begin(), vec_ret.end());

  return vec_ret;
}

}  // namespace wasim
