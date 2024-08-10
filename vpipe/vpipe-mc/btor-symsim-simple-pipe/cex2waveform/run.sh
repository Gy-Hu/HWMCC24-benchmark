#!/bin/bash
echo "===== compile ======"
iverilog -o wave -y ./pipeline.v pipeline_tb.v -g2005-sv
echo "===== waveform ====="
vvp -n wave -lxt2
gtkwave wave.vcd


