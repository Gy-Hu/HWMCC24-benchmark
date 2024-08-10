import os
def main():
    g = os.walk(r"./")
    # for path, dir_list, file_list in g:
    #         for file_name in file_list:
    #                 if('exp' in file_name):
    #                     design_dir = os.path.join(path, file_name)
    #                     print(design_dir)
    serch_list = ['experimental_results_simple_MAC_no_stall.log', 'experimental_results_simple_MAC_stall.log',\
                  'experimental_results_3_stage_pipe_add.log', 'experimental_results_3_stage_pipe_nand.log', \
                  'experimental_results_3_stage_pipe_set.log', 'experimental_results_3_stage_pipe_nop.log']
    exper_file = "statistics.log"
    for design in serch_list:
        with open(exper_file, "a") as f:
            f.write('-----------------------------------\n')
            f.write(open(design, 'r').read())
            f.write('-----------------------------------\n\n')
        os.remove(design)





if __name__ == '__main__':
  main()