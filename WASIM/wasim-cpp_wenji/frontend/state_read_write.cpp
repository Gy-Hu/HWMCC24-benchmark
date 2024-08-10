#include <frontend/state_read_write.h>
#include <utils/exceptions.h>

#include "smt-switch/utils.h"

using namespace std;

namespace wasim {

void StateRW::write_sv_val_pair(std::ofstream & fout, const smt::Term & sv, const smt::Term & val) {  
  write_expr(fout, sv, sv->get_sort());
  write_expr(fout, val, sv->get_sort());
}

// this will dump a return at the end of line
void StateRW::write_expr(std::ofstream & fout, const smt::Term & expr, const smt::Sort & svtype) {
  smt::UnorderedTermSet free_value_var;
  smt::get_free_symbols(expr, free_value_var);

  fout << "(define-fun FunNew (";

  bool first = true;
  for (const auto & arg : free_value_var) {
    if (!first)
      fout << " ";
    fout << "(" << arg->to_string() << " " << arg->get_sort()->to_string() << ")";
    first = false;
  }
  fout << ") " << svtype->to_string() << " ";
  // make sure to convert type
  auto expr_sort = expr->get_sort();
  if (svtype == expr_sort)
    fout << expr->to_string();
  else {
    if (svtype->get_sort_kind() == smt::SortKind::BOOL && 
        expr_sort->get_sort_kind() == smt::SortKind::BV && expr_sort->get_width() == 1) {
      fout << "(= #b1 ";
      fout << expr->to_string();
      fout << ")";
    } else if (expr_sort->get_sort_kind() == smt::SortKind::BOOL && 
        svtype->get_sort_kind() == smt::SortKind::BV && svtype->get_width() == 1) {
      fout << "(ite " << expr->to_string() << " #b1 #b0)";
    } else
      throw SimulatorException("unmatched sort: " + svtype->to_string() + " and " + expr_sort->to_string());
  }
  fout << ")\n";
}

smt::Term StateRW::read_expr(std::ifstream & fin) {
  std::string temp_file = "temp_sv.log";

  std::string linedata;
  getline(fin, linedata);
  std::ofstream temp(temp_file);
  if (!temp.is_open())
    throw SimulatorException("unable to open file for write " + temp_file); 
  temp << linedata << endl;

  WasimSmtLib2Parser pi(temp_file, solver_);
  return pi.return_defs();
}


bool StateRW::StateWrite(const wasim::StateAsmpt & state,
                         const std::string & outfile_sv)
{
  // 1. write the number of state variables and the number of assumptions
  ofstream fout(outfile_sv);
  if (!fout.is_open())
    return false;
  fout << state.get_sv().size()
       << " " << state.get_assumptions().size() << std::endl;
  for (const auto & sv_val_pair : state.get_sv())
    write_sv_val_pair(fout, sv_val_pair.first, sv_val_pair.second);
  
  const auto bool_sort = solver_->make_sort(smt::BOOL);
  for (size_t idx = 0; idx < state.get_assumptions().size(); ++ idx) {
    write_expr(fout, state.get_assumptions().at(idx), bool_sort);
    fout << state.get_assumption_interpretations().at(idx) << std::endl;
  }
  return true;
}

StateAsmpt StateRW::StateRead(const std::string & infile_sv)
{
  // 1. read sv
  smt::UnorderedTermMap state_sv;

  std::ifstream fin(infile_sv);
  size_t num_sv, num_assumpt;
  fin >> num_sv >> num_assumpt;
  
  for (size_t idx = 0; idx < num_sv; ++ idx ) {
    auto sv = read_expr(fin);
    auto expr = read_expr(fin);
    state_sv.emplace(sv, expr);
  }
  
  smt::TermVec state_asmpt_vec;
  std::vector<std::string> state_asmpt_interp_vec;
  for (size_t idx = 0; idx < num_assumpt; ++ idx ) {
    auto asmpt = read_expr(fin);
    state_asmpt_vec.push_back(asmpt);

    std::string assumpt_interp;
    getline(fin, assumpt_interp);
    state_asmpt_interp_vec.push_back(assumpt_interp);
  }

  StateAsmpt state_ret(state_sv, state_asmpt_vec, state_asmpt_interp_vec);
  return state_ret;
}

#if 0
void StateRW::StateWriteTree(const std::vector<std::vector<StateAsmpt>> & branch_list,
                             const std::string & out_dir)
{
  for (int i = 0; i < branch_list.size(); i++) {
    auto state_list = branch_list.at(i);
    for (int j = 0; j < state_list.size(); j++) {
      auto state = state_list.at(j);
      std::string outfile_sv =
          out_dir + "state_sv_" + to_string(i) + "_" + to_string(j);
      std::string outfile_asmpt =
          out_dir + "state_asmpt_" + to_string(i) + "_" + to_string(j);
      StateWrite(state, outfile_sv, outfile_asmpt);
      // cout << "i = " << to_string(i) << ", j = " << to_string(j) << endl;
      // cout << outfile_sv << endl;
    }
  }
}

std::vector<std::vector<StateAsmpt>> StateRW::StateReadTree(const std::string & in_dir,
                                                            int num_i,
                                                            int num_j)
{
  cout << "Reading files. Please wait for seconds." << endl;
  std::vector<std::vector<StateAsmpt>> branch_list = {};
  for (int i = 0; i < num_i; i++) {
    std::vector<StateAsmpt> state_list = {};
    for (int j = 0; j < num_j; j++) {
      std::string infile_sv =
          in_dir + "state_sv_" + to_string(i) + "_" + to_string(j);
      std::string infile_asmpt =
          in_dir + "state_asmpt_" + to_string(i) + "_" + to_string(j);
      // std::string infile_asmpt = "";
      auto state = StateRead(infile_sv, infile_asmpt);
      state_list.push_back(state);

      // cout << "i = " << i << ", j = " << j << endl;
      // cout << infile_sv << endl;
    }
    branch_list.push_back(state_list);
  }
  cout << "Reading complete!" << endl;

  return branch_list;
}
#endif

} // end of namespace wasim
