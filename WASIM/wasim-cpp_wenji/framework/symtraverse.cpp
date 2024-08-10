#include "symtraverse.h"
#include "utils/logger.h"

namespace wasim {


std::string PerStateStack::repr() const
{
  std::string stack_str;
  for (auto && node : stack_) {
    stack_str += node.repr();
  }
  std::string suffix;
  if (no_next_choice_) {
    suffix = " (END)";
  } else {
    suffix = "";
  }

  auto ret_str = "[" + stack_str + "]" + " ptr: " + to_string(ptr_) + suffix;
  return ret_str;
}


  // convert the choices so far into input assignments or assumptions
  // along witht the (optional) additional assumptions
std::pair<smt::UnorderedTermMap, smt::TermVec> PerStateStack::get_iv_asmpt(
    const smt::TermVec & assumptions) const
{
  smt::UnorderedTermMap iv;
  smt::TermVec asmpt;
  for (auto && branch_node : stack_) {
    auto d =
        simulator_.convert({ { branch_node.var_name(), branch_node.var_value() } });

    if (branch_node.branch_on_inputvar()) {
      iv.insert(d.begin(), d.end());
    } else {
      assert(d.size() == 1);
      auto asmpt_term =
          solver_->make_term(smt::Equal, d.begin()->first, d.begin()->second);
      asmpt.push_back(asmpt_term);
    }
  }
  asmpt.insert(asmpt.end(), assumptions.begin(), assumptions.end());

  auto ret = make_pair(iv, asmpt);
  return ret;
}

// try next choice allowed, return true if possible
bool PerStateStack::next_choice()
{
  bool succ = false;
  while (! succ) {
    if (stack_.size() == 0) {
      no_next_choice_ = true;
      return false;
    }
    succ = stack_.back().next();
    if (! succ) {
      ptr_--;
      stack_.pop_back();
    }
  }
  return true;
}

bool PerStateStack::deeper_choice()
{
  if (ptr_ == branching_point_.size()) {
    return false;
  }
  const auto & branch_node = branching_point_.at(ptr_);
  stack_.push_back(branch_node.copy_node_without_value());
  ptr_++;
  return true;
}

unsigned SymbolicTraverse::traverse_one_step(
    const smt::TermVec & assumptions,
    const std::vector<TraverseBranchingNode> & branching_point)
{
  auto state = executor_.get_curr_state(assumptions);
  bool reachable = tracemgr_.check_reachable(state);
  
  WASIM_WARN_IF(! reachable) << "[DEBUG warning] not reachable! skip!";
  if (! reachable)
    return 0;

  bool concrete_enough =
      tracemgr_.check_concrete_enough(state, executor_.get_Xs());
  assert(concrete_enough);
  auto is_new_state = tracemgr_.record_state(state, executor_.get_Xs());
  assert(is_new_state);

  PerStateStack init_choice(branching_point, executor_);

  while (init_choice.has_valid_choice()) {
    WASIM_DLOG("traverse_one_step") << ">> [" << init_choice.repr() << "]  ";
    auto iv_asmpt_pair = init_choice.get_iv_asmpt(assumptions);
    auto iv = iv_asmpt_pair.first;
    auto asmpt = iv_asmpt_pair.second;
    executor_.set_input(iv, asmpt);
    executor_.sim_one_step();
    auto state = executor_.get_curr_state();
    bool reachable = tracemgr_.check_reachable(state);

    if (! reachable) {
      WASIM_DLOG("traverse_one_step") << "not reachable.";
      init_choice.next_choice();
      executor_.backtrack();
      executor_.undo_set_input();
      continue;
    }

    bool concrete_enough =
        tracemgr_.check_concrete_enough(state, executor_.get_Xs());
    if (! concrete_enough) {
      WASIM_DLOG("traverse_one_step")  << "not concrete. Retry with deeper choice.";
      auto succ = init_choice.deeper_choice();
      if (succ) {
        executor_.backtrack();
        executor_.undo_set_input();
        continue;
      }
      WASIM_ERROR
           << "cannot reach a concrete state even if all choices are "
              "made. Future work.";

      auto state = executor_.get_curr_state();
      // state.print();
      WASIM_CHECK(false);
    }

    bool is_new_state =
        tracemgr_.record_state(state, executor_.get_Xs());

    init_choice.next_choice();
    executor_.backtrack();
    executor_.undo_set_input();
  }

  WASIM_DLOG("traverse_one_step") << "=============================" ;
  WASIM_DLOG("traverse_one_step") << "Finish!" ;
  WASIM_DLOG("traverse_one_step") << "Get #state: " << tracemgr_.get_abs_state().size();

  // TODO : simplification procedure
  for (auto & abs_state_one_step : tracemgr_.update_abs_state()) {
    bool reachable_before_simplification =
        tracemgr_.check_reachable(abs_state_one_step);
    state_simplify_xvar(abs_state_one_step, executor_.get_Xs(), solver_);
    sygus_simplify(abs_state_one_step, executor_.get_Xs(), solver_);
    assert(! abs_state_one_step.syntactically_contains_x(executor_.get_Xs()));
    bool reachable_after_simplification =
        tracemgr_.check_reachable(abs_state_one_step);
    assert(reachable_before_simplification);
    assert(reachable_after_simplification);
  }
  return tracemgr_.get_abs_state().size();
}

unsigned SymbolicTraverse::traverse(
    const smt::TermVec & assumptions,
    const std::vector<TraverseBranchingNode> & branching_point)
{
  auto state = executor_.get_curr_state(assumptions);
  auto reachable = tracemgr_.check_reachable(state);
  if (! reachable) {
    WASIM_WARN << "[traverse] state is not reachable! skip!";
    return 0;
  }

  bool concrete_enough =
      tracemgr_.check_concrete_enough(state, executor_.get_Xs());
  assert(concrete_enough);

  bool is_new_state = tracemgr_.record_state(state, executor_.get_Xs());
  assert(is_new_state);

  PerStateStack init_stack(branching_point, executor_);
  std::vector<PerStateStack> stack_per_state;
  stack_per_state.push_back(init_stack);
  WASIM_DLOG("traverse") << "init stack per state: " << init_stack.repr() ;
  WASIM_DLOG("traverse") << "init tracelen: " << executor_.tracelen() ;
  unsigned init_tracelen = executor_.tracelen() - 1;
  vector<StateAsmpt> curr_branch;
  curr_branch.push_back(state);

  bool branch_end_flag = false;
  while (stack_per_state.size() != 0) {
    state = executor_.get_curr_state();

    WASIM_DLOG("traverse")
         << "Trace: " << executor_.tracelen() - init_tracelen
         << " Stack: " << stack_per_state.size();
    WASIM_DLOG("traverse") << ">> [";
    for (const auto & perstack : stack_per_state)
      WASIM_DLOG("traverse") << perstack.repr() << " ";
    WASIM_DLOG("traverse") << " ] : ";

    if (! stack_per_state.back().has_valid_choice()) {
      WASIM_DLOG("traverse") << " no new choices, back to prev state";
      stack_per_state.pop_back();
      if (stack_per_state.size() != 0) {
        executor_.backtrack();
        executor_.undo_set_input();

        // store current branch (we have finished on this branch)
        all_branches_.push_back(curr_branch);
        curr_branch.pop_back(); // we are going to backtrack
        branch_end_flag = true;
      }
      continue;
    }
    auto iv_asmpt = stack_per_state.back().get_iv_asmpt(assumptions);
    auto iv = iv_asmpt.first;
    auto asmpt = iv_asmpt.second;
    executor_.set_input(iv, asmpt);
    executor_.sim_one_step();
    state = executor_.get_curr_state();
    auto & curr_state = state;

    auto reachable = tracemgr_.check_reachable(state);
    if (! reachable) {
      WASIM_DLOG("traverse") << " not reachable." ;
      stack_per_state.back().next_choice();
      executor_.backtrack();
      executor_.undo_set_input();
      continue;
    }

    auto concrete_enough =
        tracemgr_.check_concrete_enough(state, executor_.get_Xs());
    if (! concrete_enough) {
      WASIM_DLOG("traverse") << "not concrete. Retry with deeper choice.";
      auto succ = stack_per_state.back().deeper_choice();
      if (succ) {
        executor_.backtrack();
        executor_.undo_set_input();
        continue;
      } // else : run out of choices

      auto state = executor_.get_curr_state();
      // state.print();
      for (const auto & sv : state.get_sv()) {
        auto s = sv.first;
        auto v = sv.second;
        if (expr_contains_X(v, executor_.get_Xs())) {
          WASIM_DLOG("traverse") << v;
        }
      }
      WASIM_ERROR
           << "cannot reach a concrete state even if all choices are "
              "made.";
      throw SimulatorException("cannot reach a concrete state even if all choices are made");
    } // end of not concrete enough

    const std::vector<wasim::StateAsmpt> & state_vec = 
      branch_end_flag ? all_branches_.back() : curr_branch;

    if (branch_end_flag)
      branch_end_flag = false;

    auto is_new_state =
        tracemgr_.record_state_nonexisted_in_vec(state_vec, state, executor_.get_Xs());

    if (is_new_state) {
      WASIM_DLOG("traverse") << "A new state!" ;
      curr_branch.push_back(curr_state);
      stack_per_state.push_back(PerStateStack(branching_point, executor_)); // new stack
    } else {
      WASIM_DLOG("traverse") << " not new state. Go back. Try next." ;
      auto test = stack_per_state.back().next_choice();
      executor_.backtrack();
      executor_.undo_set_input();
    }
  }

  WASIM_DLOG("traverse") << "=============================" ;
  WASIM_DLOG("traverse") << "Finish!" ;
  WASIM_DLOG("traverse") << "Get #state: " << tracemgr_.get_abs_state().size() ;

  // TODO : simplification procedure
  for (auto & abs_state : tracemgr_.update_abs_state()) {
    bool reachable_before_simplification = tracemgr_.check_reachable(abs_state);
    state_simplify_xvar(abs_state, executor_.get_Xs(), solver_);
    sygus_simplify(abs_state, executor_.get_Xs(), solver_);
    assert(! abs_state.syntactically_contains_x(executor_.get_Xs()));
    bool reachable_after_simplification = tracemgr_.check_reachable(abs_state);
    assert(reachable_before_simplification);
    assert(reachable_after_simplification);
  }
  return tracemgr_.get_abs_state().size();
} // end of traverse

}  // namespace wasim
