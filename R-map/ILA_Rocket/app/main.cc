#include "riscvIla.hpp"

using namespace ilang;

int main() {

  riscvILA_user riscvILA(0);
  riscvILA.addInstructions(); // 37 base integer instructions

  std::vector<std::string> design_files = {
    "BreakpointUnit.v",
    "CSRFile.v",
    "IBuf.v",
    "ALU.v",
    "MulDiv.v",
    "Rocket.v",
    "RVCExpander.v"
  };

  // Generate verification target
  RtlVerifyConfig cfg;
  cfg.ForceInstCheckReset = true; //
  cfg.PonoGenJgScript = true;

  std::string RootPath = "..";
  std::string VerilogPath = RootPath + "/verilog/";

  std::string RefrelPath = RootPath + "/refinement/";
  std::string OutputPath = RootPath + "/verification/";

  std::vector<std::string> path_to_design_files; // update path
  for(auto && f : design_files)
    path_to_design_files.push_back( VerilogPath + f );

  IlaVerilogRefinemetChecker(
    riscvILA.model,
    {},                             // no include
    path_to_design_files,           // rtl design
    "Rocket",                       // top_module_name
    RefrelPath + "varmap.json",     // variable mapping
    RefrelPath + "instcond.json",   // conditions of start/ready
    OutputPath,                     // output path
    ModelCheckerSelection::PONO,    // backend selector
    cfg
  );


  return 0;
} // end of main

