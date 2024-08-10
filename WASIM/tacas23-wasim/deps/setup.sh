#!/bin/bash
# TODO:chmod 755 setup.sh

#-------------------------------
# Install all dependent packages
#-------------------------------
echo "Install Dependencies"

DEPSDIR=$(pwd)
#1. install pysmt (pip3)
pip3 install PySMT-0.9.5.tar.gz

#2. install z3 (pip3)
pip3 install z3_solver-4.8.15.0-py2.py3-none-manylinux1_x86_64.whl

#3. install boolector (pip3)
pip3 install PyBoolector-3.2.2.20221010.1-cp310-cp310-manylinux_2_12_x86_64.manylinux2010_x86_64.whl

#4. cvc5-Linux
cp cvc5-Linux ~/
chmod 755 ~/cvc5-Linux


cd ${DEPSDIR}/../
cp -rf wasim ~/
cp -rf abc ~/

#5. abc
unzip -o -d ~/abc/script/ deps/abc.zip
chmod +x ~/abc/script/abc

cd ~/
chmod -R 755 wasim
cd ~/wasim
mkdir output
mkdir log
cd log
mkdir log_demo
mkdir log_simulation
mkdir log_proof

echo
echo "---------------------------"
echo "  Installation Completed.  "
echo "---------------------------"

cd ${DEPSDIR}


