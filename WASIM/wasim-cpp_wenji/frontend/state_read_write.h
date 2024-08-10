#pragma once
#include <framework/ts.h>
#include <framework/symsim.h>
#include <frontend/smt_in.h>

namespace wasim {

class StateRW
{
 public:
  StateRW(const smt::SmtSolver & s) : solver_(s) { }

  // return true if succeed
  bool StateWrite(const wasim::StateAsmpt & state,
                  const std::string & outfile_sv);
  // Read/Write a single state
  StateAsmpt StateRead(const std::string & infile_sv);

  // Read/Write a tree of states
  void StateWriteTree(const std::vector<std::vector<StateAsmpt>> & branch_list,
                      const std::string & out_dir);
  std::vector<std::vector<StateAsmpt>> StateReadTree(const std::string & in_dir,
                                                     int i,
                                                     int j);
 protected:
  void write_sv_val_pair(std::ofstream & fout, const smt::Term & sv, const smt::Term & val);
  void write_expr(std::ofstream & fout, const smt::Term & sv, const smt::Sort & svtype);
  smt::Term read_expr(std::ifstream & fin);


 private:
  smt::SmtSolver solver_;
  // smt::SmtSolver solver_asmpt_;
};

} // end of namespace wasim
