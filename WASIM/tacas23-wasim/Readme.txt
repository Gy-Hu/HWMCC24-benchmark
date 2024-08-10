############# ARTIFACT LINK #############
Please download the zip archive through the Zenodo link: https://doi.org/10.5281/zenodo.7247147

############# ADDITIONAL REQUIREMENTS #############
All the software dependencies are open-source and already downloaded in tacas23-wasim.zip, which could be installed automatically by the script tacas23-wasim/deps/setup.sh. 
The recommended minimum hardware requirements to run the artifact are listed as follows:
• CPU: Intel (64-bit x86 ISA, frequncy >= 2.40GHz) 
• Operating System: Ubuntu
• RAM: 16GB
• Storage: 128GB
Note: it seems that the AEC Virtual Machine may require allocating at least two CPU cores and 128MB video memory on certain host to startup successfully.

############# EXPERIMENT RUNTIME #############
There are five sub-experiments in total, as stated in the abstract of the artifact submission. The total runtime for these experiments is around 25 minutes, which is estimated on a server running Ubuntu 20.04 with a 2.9 GHz Intel Xeon(R) Platinum 8375C CPU and 128G RAM.
Runtime for each sub-experiments:
• Demo: several seconds
• Case study1: several seconds
• Case study2: 15 minutes
• Case study3: 10 minutes
• Berkeley-abc experiments: please terminate the process manually in a few minutes.


############# REPRODUCIBILITY INSTRUCTIONS #############
========= Installation =========
1. Please first download the zip archive from the link we provided.
2. Unzip the archive. Open a terminal and change directory into the folder which contains the zip archive. You can do this by first using the file explorer to navigate into the folder and right clicking in the blank space of the file explorer and select "Open in Terminal". In the terminal, run
    $ unzip -o -d tacas23-wasim tacas23-wasim.zip
3. Install dependencies for WASIM: in the same terminal just opened in the previous step, run
    $ cd tacas23-wasim/deps
    $ chmod 755 setup.sh
    $ ./setup.sh

========= Reproduce Results of Case Studies =========
A unified script named run_script.py is used in all experiments. The usage of run_script could be inquired by the command: `python3 run_script.py -h`

1. Demo
    Directly run the following commands, and the results could be seen in the terminal.
    These will reproduce all the screenshots in Appendix. 
    $ cd ~/wasim/demo
    $ python3 run_script.py -s api.py -l ../log/log_demo/ -i 'none'
    $ python3 run_script.py -s abs.py -l ../log/log_demo/ -i 'none'
    $ python3 run_script.py -s fpv.py -l ../log/log_demo/ -i 'none'
    $ python3 run_script.py -s inv.py -l ../log/log_demo/ -i 'none'
2. Case Studies
    The execution processes are similar for the following three case studies, including 
        • simulation in user_interface/ to obtain the traces of abstract states stored in output/ with pickle format
        • formal property check in proof_construction/
        • invariant check  in proof_construction/

    As the symbolic simulation in 2.2 and 2.3 below may take a while (> 10mins) in the virtual machine, please be patient.
    
    2.1 Case study1: simple_pipe_no_stall
            $ cd ~/wasim/user_interface
            $ python3 run_script.py -s simulation_simple_MAC_no_stall.py -l ../log/log_simulation/ -i 'none'
            $ cd ~/wasim/proof_construction
            $ python3 run_script.py -s prop_check_simple_MAC_no_stall.py -l ../log/log_proof/ -i 'none' -v fpv
            $ python3 run_script.py -s inv_check_simple_MAC_no_stall.py -l ../log/log_proof/ -i 'none' -v inv
    
    2.2 Case study2: simple_pipe_stall
            $ cd ~/wasim/user_interface
            $ python3 run_script.py -s simulation_simple_MAC_stall.py -l ../log/log_simulation/ -i 'none'
            $ cd ~/wasim/proof_construction
            $ python3 run_script.py -s prop_check_simple_MAC_stall.py -l ../log/log_proof/ -i 'none' -v fpv
            $ python3 run_script.py -s inv_check_simple_MAC_stall.py -l ../log/log_proof/ -i 'none' -v inv
    
    2.3 Case study3:3_stage_pipe (with four instructions)
            $ cd ~/wasim/user_interface
            $ python3 run_script.py -s simulation_3_stage_pipe.py -l ../log/log_simulation/ -i 'all'
            $ cd ~/wasim/proof_construction
            $ python3 run_script.py -s prop_check_3_stage_pipe.py -l ../log/log_proof/ -i 'all' -v fpv
            $ python3 run_script.py -s inv_check_3_stage_pipe.py -l ../log/log_proof/ -i 'all' -v inv

    2.4 Collecting experimental results 
            $ cd ~/wasim
            $ python3 statistic.py
        After this step, all the experimental results will be written into `~/wasim/statistics.log`, corresponding to Table 1 in the paper.
        You can view the statistics by the command:
            $ cat ~/wasim/statistics.log

        After running all commands listed above, you will be able to  reproduce all results in Table 1 (except for the "IC3/PDR" column, which is in Step 5). The reported running time might be slightly different due to the differences in the machine configurations.
            
3. Output files and log files.
    • All of the output traces of states will be stored in `~/wasim/output` in pickle format.
    • All running logs will be stored in `~/wasim/log`, including `log_demo`, `log_simulation`, and `log_proof` for demo, simulation and verification, respectively. Each log file is named by the concatenation of the execution script and the instruction type.

4. Help information for the APIs of WASIM are also available in the artifact. You can check the manual through `help(object)` in Python.
    Here is an example:
    $ cd ~/wasim/symsim_framework
    $ python3 
    $ import symsim
    $ help(symsim)
    Then the usage of the symbolic simulator will be displayed, including classes with attributes and functions with arguments. After viewing the help information, you can press the 'q' key on your keyboard, and then type `quit()` to exit Python.

5. Reproduce the comparison with Berkeley-abc
    Please note here, Berkeley-abc is not our tool. We include experiments using Berkeley-abc in this artifact just as a comparison to our tool. This is to show our tool is advantageous on certain problems that are typically hard for a hardware model checker.  The experiments are invoked by a single script 'abc-script.ys'. 

    $ cd ~/abc/script
    $ ./abc -F abc-script.ys

    In the experiments, Berkeley-abc will not terminate for at least 72 hours, so please terminate the process by Ctrl+C manually after you see the output of the terminal gets stuck for a long time without any progress.

    These experiments correpond to the "IC3/PDR" column in Table 1 of the paper.

    This is the end of the demo. To conclude, after running all above commands, you have reproduced the results reported in Table 1, as well as the screenshots in the Appendix.

