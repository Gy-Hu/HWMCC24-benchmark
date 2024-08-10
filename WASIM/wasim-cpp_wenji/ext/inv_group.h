#include "symtraverse.h"
using namespace std;

namespace wasim {
typedef std::pair<bool, smt::UnorderedTermMap> check_res;
typedef std::pair<smt::Term, smt::TermVec> cex_res;
smt::Term tobool(smt::Term expr, smt::SmtSolver & solver);

class InvGroup
{
 public:
  InvGroup(int layer,
           smt::Term tag,
           std::vector<std::vector<StateAsmpt>> branch_list,
           smt::SmtSolver & s)
      : layer_(layer), tag_(tag), branch_list_(branch_list), solver_(s)
  {
  }

  void branch2state();
  smt::TermVec state_group();
  smt::TermVec asmpt_group();
  smt::TermVec inv_group();
  smt::TermVec state_dedup();
  smt::TermVec inv_dedup();
  smt::TermVec extract_prop(std::string var_name);
  std::vector<int> check_unsat_expr(std::vector<int> truelist_num,
                                    smt::Term cex_expr);
  void add_unsat_asmpt(smt::Term unsat_expr, int idx);

 private:
  int layer_;
  smt::Term tag_;
  std::vector<std::vector<StateAsmpt>> branch_list_;
  smt::SmtSolver solver_;
  smt::TermVec state_group_;
  smt::TermVec asmpt_group_;
  smt::TermVec inv_group_;
  smt::TermVec state_dedup_;
  smt::TermVec asmpt_dedup_;
  smt::TermVec inv_dedup_;
};  // end of class ChoiceItem

check_res init_check(smt::Term init,
                     smt::Term inv,
                     smt::Term asmpt,
                     smt::SmtSolver & solver);
check_res inv_check(smt::Term inv,
                    smt::Term trans_update,
                    smt::Term asmpt,
                    TransitionSystem sts,
                    smt::SmtSolver & solver);
check_res prop_check(smt::Term prop,
                     smt::Term inv,
                     smt::Term asmpt,
                     smt::SmtSolver & solver);

smt::TermVec deduplicate(smt::TermVec vec);
cex_res cex_parser(smt::UnorderedTermMap cex,
                   std::unordered_set<std::string> tag_set,
                   std::unordered_set<std::string> ctrl_set,
                   smt::SmtSolver & solver);

std::vector<int> test_cex(smt::TermVec formula_vec,
                          smt::UnorderedTermMap cex,
                          smt::SmtSolver & solver);

std::vector<int> comb_unq(std::vector<int> vec1, std::vector<int> vec2);
}  // namespace wasim
