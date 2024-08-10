This framework enables symbolic simulation on Btor2 circuit.

1. design: four kinds of pipelined processors descirbed with Verilog and transfered in Btor2 format by YOSYS

2. log: log of executing the framework and proof construction

3. output: abstract states extracted from the framework

4. proof_construction: use the abstract states to construct inductive invariants to verify the proof

5. symsim_framework: main framework for symbolic simulation

6. user_conctrol: top script to execute the symbolic simulation (choose abstract level, simulation sequence)