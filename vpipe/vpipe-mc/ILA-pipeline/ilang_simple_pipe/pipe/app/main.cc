// main.cc
// Synopsis: Entry point for the executable

#include <iostream>

#include <instr_set.h>

using namespace ilang;

int main() {

  std::string rfDir = "../rfmap/";

  IlaVerilogRefinemetChecker(
    SimplePipe::BuildModel(),
    {},                            // include
    {"../verilog/simple_pipe.v"}, // vlog files
    "pipeline_v",                  // top_module_name
    "../rfmap/vmap.json",         // variable mapping
    "../rfmap/cond.json",         // instruction-mapping
    "../verify",          // verification dir
    ModelCheckerSelection::PONO
  );

  return 0;
}
