#include "riscvIla.hpp"

using namespace ilang;

int main() {

  riscvILA_user riscvILA(0);
  riscvILA.addInstructions(); // 37 base integer instructions

  std::vector<std::string> design_files = {
    "alloc_issue_ino.v",
    "alu.v",
    "arf.v",
    "brimm_gen.v",
    "btb.v",
    "decoder.v",
    "dmem.v",
    "exunit_alu.v",
    "exunit_branch.v",
    "exunit_ldst.v",
    "exunit_mul.v",
    "gshare.v",
    "imem_outa.v",
    "imem.v",
    "imm_gen.v",
    "mpft.v",
    "multiplier.v",
    "oldest_finder.v",
    "pipeline_if.v",
    "pipeline.v",
    "prioenc.v",
    "ram_sync_nolatch.v",
    "reorderbuf.v",
    "rrf_freelistmanager.v",
    "rrf.v",
    "rs_alu.v",
    "rs_branch.v",
    "rs_ldst.v",
    "rs_mul.v",
    "rs_reqgen.v",
    "search_be.v",
    "src_manager.v",
    "srcopr_manager.v",
    "srcsel.v",
    "storebuf.v",
    "tag_generator.v"
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

  IlaVerilogRefinementChecker (
      riscvILA.model,                 // model
      {VerilogPath+"include/"},       // 1 include
      path_to_design_files,           // designs
      "pipeline",                     // top_module_name
      RefrelPath + "vmap.json",            // variable mapping
      RefrelPath + "cond.json",          // conditions of start/ready
      OutputPath,                     // output path
      ModelCheckerSelection::PONO,    // backend: PONO
      cfg); // verilog generator configuration


  return 0;
} // end of main

