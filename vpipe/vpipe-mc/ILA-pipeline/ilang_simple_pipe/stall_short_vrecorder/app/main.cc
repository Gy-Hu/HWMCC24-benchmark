// main.cc
// Synopsis: Entry point for the executable

#include <iostream>

#include <instr_set.h>

using namespace ilang;

int main() {
  
  RtlVerifyConfig cfg;
  cfg.PonoEngine = "ic3ia";
  cfg.PonoOtherOptions = " -k 50 -v 1 ";
  cfg.YosysSmtArrayForRegFile = false;

  std::string rfDir = "../rfmap/";

  IlaVerilogRefinemetChecker(
    SimplePipe::BuildStallModel(),
    {},                            // include
    {"../verilog/simple_pipe_stall_short.v"}, // vlog files
    "pipeline_v",                  // top_module_name
    "../rfmap/vmap-rfmap-pvholder-stall-short.json",         // variable mapping
    "../rfmap/cond-rfmap-pvholder-stall-short.json",         // instruction-mapping
    "../verify",          // verification dir
    ModelCheckerSelection::PONO,
    cfg
  );

  return 0;
}
