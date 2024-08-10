#include <chrono>
#include "assert.h"
#include "config/testpath.h"
#include "frontend/btor2_encoder.h"
#include "framework/symsim.h"
#include "framework/ts.h"
#include "smt-switch/boolector_factory.h"

using namespace wasim;
using namespace smt;

int main() {


  SmtSolver solver = BoolectorSolverFactory::create(false);

  solver->set_logic("QF_UFBV");
  solver->set_opt("incremental", "true");
  solver->set_opt("produce-models", "true");
  solver->set_opt("produce-unsat-assumptions", "true");


  TransitionSystem sts(solver);
  BTOR2Encoder btor_parser("design/test/pipe-no-stall.btor2", sts);

  std::cout << sts.trans()->to_string() << std::endl;

  return 0;
}


