# How to install ILAng

## Prerequisites

1. `git clone https://github.com/zhanghongce/ILA-Tools.git` - get the ILAng
2. `cd ILA-Tools && git checkout refinement-upgrade && git checkout d7e0df6b3a4ccf86883d3b6d6afab5cb5236c302` - checkout the version used in the paper
3. `mkdir -p build && cd build` - create a build directory
4. `cmake .. && make -j$(nproc)` - build the ILAng
5. `make run_test` - make sure pass the run test
6. `make install DESTDIR=xxx/HWMCC24-benchmark/tmp/ILA-install` - install the ILAng

note: 
* Here should add `export LD_LIBRARY_PATH=/xx/tmp/ILA-install/usr/local/lib:$LD_LIBRARY_PATH` to the `~/.bashrc` or `~/.zshrc` file
* For `Piccolo`, use `c88eb9c9548223e3c89f809a06e7ecd8d9e32ffe` in refinement-upgrade branch
* For `Ridecore`, use `76a99fa4300a2338feb208fa124443bef94eda87` (latest commit) in refinement-upgrade branch

## Try starter

7. `cd xxx/ILA-Tools/test/starter` - go to the starter test
8. `mkdir build && cd build` - create a build directory
9. `cmake -DCMAKE_PREFIX_PATH=/xxx/tmp/ILA-install/usr/local ..` - set the ILAng path
10. `make -j$(nproc)` - build the starter test
11. `./starter` - run the starter test

## Try ILA_AES (Tabby Yosys required)

12. `cd xxx/ILA_AES` - go to the ILA_AES test
13. `mkdir verification` - create a verification directory
14. `mkdir build && cd build` - create a build directory
15. `cmake -DCMAKE_PREFIX_PATH=/xxx/tmp/ILA-install/usr/local ..` - set the ILAng path
16. `make -j$(nproc)` - build the ILA_AES test
17. `./AESExe Solver=btor` - run the ILA_AES
18. go to `verification` directory and use `yosys gen_btor.ys` to generate the BTOR file (use tabby yosys). It generates `problem.btor2` file.

## Model checking

19. `pono -e ic3bits problem.btor2` - run the model checking (use pono)
