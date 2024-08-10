#include "traverse_manip.h"

namespace wasim {

void extend_branch_init(std::vector<std::vector<StateAsmpt>> & branch_list,
                        SymbolicExecutor & executor,
                        TransitionSystem & sts,
                        std::unordered_set<std::string> base_sv,
                        std::string flag,
                        smt::TermVec flag_asmpt,
                        std::vector<TraverseBranchingNode> order,
                        smt::SmtSolver & solver)
{
  auto branch_list_old(branch_list);
  branch_list.clear();
  auto executor_temp(executor);
  smt::UnorderedTermSet base_variable;
  for (const auto n : base_sv) {
    base_variable.insert(executor_temp.var(n));
  }
  SymbolicTraverse traverse_temp(sts, executor_temp, solver, base_variable);
  auto assumptions = flag_asmpt;
  traverse_temp.traverse(assumptions, order, {});
  cout << "number of state " << flag << ": 1-> "
       << traverse_temp.tracemgr_.get_abs_state().size() << endl;

  for (const auto & nextstate : traverse_temp.tracemgr_.get_abs_state()) {
    std::vector<StateAsmpt> state_vec_extend;
    state_vec_extend.push_back(nextstate);
    branch_list.push_back(state_vec_extend);
    nextstate.print();
    if (nextstate.syntactically_contains_x(executor.get_Xs())) {
      assert(false);
    }
    // nextstate.print_assumptions();
  }
  cout << "number of state " << flag << " in total: " << branch_list_old.size()
       << " --> " << branch_list.size() << endl;
}

void extend_branch_next_phase(
    std::vector<std::vector<StateAsmpt>> & branch_list,
    SymbolicExecutor & executor,
    TransitionSystem & sts,
    std::unordered_set<std::string> base_sv,
    std::string flag,
    smt::TermVec flag_asmpt,
    assignment_type phase_marker,
    std::vector<TraverseBranchingNode> order,
    smt::SmtSolver & solver)
{
  auto branch_list_old(branch_list);
  branch_list.clear();
  for (auto state_list_old : branch_list_old) {
    auto state_list(state_list_old);
    auto s = state_list.back();
    auto executor_temp(executor);
    auto d = executor_temp.convert(phase_marker);
    std::swap(s.sv_, d);
    s.sv_.insert(d.begin(),
                 d.end());  // for the same variable, d will overwrite s
    // s.print();
    // s.print_assumptions();
    executor_temp.set_current_state(s);
    smt::UnorderedTermSet base_variable;
    for (const auto n : base_sv) {
      base_variable.insert(executor_temp.var(n));
    }
    SymbolicTraverse traverse_temp(sts, executor_temp, solver, base_variable);
    auto assumptions = flag_asmpt;
    // TODO: you should first set the state to s before this (due to API change of traverse_one_step
    traverse_temp.traverse_one_step(assumptions, order, { s });
    cout << "number of state " << flag << ": 1-> "
         << traverse_temp.tracemgr_.abs_state_one_step_.size() << endl;

    for (auto & nextstate : traverse_temp.tracemgr_.abs_state_one_step_) {
      auto state_vec_extend(state_list);
      state_vec_extend.push_back(nextstate);
      branch_list.push_back(state_vec_extend);
      nextstate.print();
      // nextstate.print_assumptions();
    }
  }
  int start_num = branch_list_old.size();
  int end_num = branch_list.size();
  cout << "number of state " << flag << " in total: " << branch_list_old.size()
       << " --> " << branch_list.size() << endl;
}

void extend_branch_same_phase(
    std::vector<std::vector<StateAsmpt>> & branch_list,
    SymbolicExecutor & executor,
    TransitionSystem & sts,
    std::unordered_set<std::string> base_sv,
    std::string flag,
    smt::TermVec flag_asmpt,
    assignment_type phase_marker,
    std::vector<TraverseBranchingNode> order,
    smt::SmtSolver & solver)
{
  auto branch_list_old(branch_list);
  branch_list.clear();
  for (auto state_list_old : branch_list_old) {
    auto state_list(state_list_old);
    auto s = state_list.back();
    auto s_init(s);
    auto executor_temp(executor);
    auto d = executor_temp.convert(phase_marker);
    std::swap(s.sv_, d);  // swap will only exchange the pointers
    s.sv_.insert(d.begin(),
                 d.end());  // for the same variable, d will overwrite s
    executor_temp.set_current_state(s);
    smt::UnorderedTermSet base_variable;
    for (const auto n : base_sv) {
      base_variable.insert(executor_temp.var(n));
    }
    SymbolicTraverse traverse_temp(sts, executor_temp, solver, base_variable);
    auto assumptions = flag_asmpt;
    traverse_temp.traverse(assumptions, order, { s_init });
    cout << "number of state " << flag << ": 1-> "
         << traverse_temp.get_abs_state().size() << endl;

    for (const auto & nextstate : traverse_temp.get_abs_state()) {
      auto state_vec_extend(state_list);
      state_vec_extend.push_back(nextstate);
      branch_list.push_back(state_vec_extend);
      nextstate.print();
      // nextstate.print_assumptions();
    }
  }
  int start_num = branch_list_old.size();
  int end_num = branch_list.size();
  cout << "number of state " << flag << " in total: " << branch_list_old.size()
       << " --> " << branch_list.size() << endl;
}

}  // namespace wasim
