#include "riscvIla.hpp"
using namespace ilang;

void verify(
  Ila& model,
  const std::vector<std::string> & design_files,
  const std::string & varmap,
  const std::string & instcont
  ) {
  RtlVerifyConfig cfg;
  cfg.PonoAddKeep = false;
  cfg.ForceInstCheckReset = true;

  cfg.WrapperPreheader = "`define BSV_NO_INITIAL_BLOCKS 1";


  std::string RootPath = "..";
  std::string VerilogPath = RootPath + "/verilog/";
  //std::string IncludePath = VerilogPath + "include/";
  std::string RefrelPath = RootPath + "/refinement/";
  std::string OutputPath = RootPath + "/verification/";

  std::vector<std::string> path_to_design_files; // update path
  for(auto && f : design_files)
    path_to_design_files.push_back( VerilogPath + f );

  IlaVerilogRefinemetChecker (
      model,                          // model
      {},                             // no include
      path_to_design_files,           // designs
      "mkCPU",                        // top_module_name
      RefrelPath + varmap,            // variable mapping
      RefrelPath + instcont,          // conditions of start/ready
      OutputPath,                     // output path
      ModelCheckerSelection::PONO,    // backend: PONO
      cfg); // verilog generator configuration

}



int main(int argc, char **argv) {
  // TODO

  std::vector<std::string> design_files = {
    "BRAM2.v",
    "FIFO20.v",
    "FIFO2.v",
    "mkBranch_Predictor.v",
    "mkCPU.v",
    "mkCSR_MIE.v",
    "mkCSR_MIP.v",
    "mkCSR_RegFile.v",
    "mkGPR_RegFile.v",
    "mkMMU_Cache.v",
    "mkNear_Mem.v",
    "mkSoC_Map.v",
    "RegFile.v"
  };

  // build the model
  riscvILA_user piccolo;
  piccolo.addInstructions(); // 37 base integer instructions

  verify(piccolo.model, design_files, "varmap.json", "instcond.json");

  // riscvILA_user riscvILA(0);
  return 0;
}
