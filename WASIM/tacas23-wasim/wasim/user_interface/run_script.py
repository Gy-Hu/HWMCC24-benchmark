import sys, getopt, re, os, time

def main(argv):
   
   script = ''
   logdir = ''
   try:
      opts, args = getopt.getopt(argv,"hs:l:i:",["script=","logdir=","inst="])
   except getopt.GetoptError:
      ('run_script.py  -s <script> -l <logpath> -i <inst_type>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('run_script.py -s <script> -l <logdir> -i <inst_type>')
         sys.exit()
    #   elif opt in ("-i", "--inst"):
    #      inst = arg
      elif opt in ("-s", "--script"):
         script = arg
      elif opt in ("-l", "--logdir"):
         logdir = arg
      elif opt in ("-i", "--inst"):
         inst_type = arg
   print('Script name:   ', script)
   print('Log path:', logdir)
   print('Instruction type:', inst_type)
   print('\n')
   print('Script name:   ', script)
   print('Instruction type:', inst_type)
   print('\n')
   assert inst_type in ['all', 'add', 'nand', 'nop', 'set', 'none']
   if inst_type == 'all':
      inst_list = ['add', 'nand', 'set', 'nop']
   else:
      inst_list = [str(inst_type)]

   temp_script = 'temp_'+str(script)
   for inst in inst_list:
        ## regular expression to replace the script
        f_t = open(str(script), 'r')
        f = open(str(temp_script), 'w')
        lines = f_t.readlines()
        for line in lines:
                if('_inst.' in str(line)):
                    line_new = re.sub(r'_inst.', '_'+str(inst)+'.', line)
                else:
                    line_new = line
                f.writelines(line_new)
        f_t.close()
        f.close()
        print('Running script:', script)
        if(len(inst_list) > 1):
           print('Current instruction:', inst)
        start_time = time.perf_counter()
        os.system('python3 {s} | tee {l}{s_n}_{i}.log'.format(s=temp_script, l=logdir, s_n=script[:-3], i=inst))
        end_time = time.perf_counter()
        os.remove(temp_script)
        print('Finish!\n\n')

        ## write statistcs 
        #1. wite name:
        if(inst_type == 'none'):
             design_name = script[11:-3]
        else:
             design_name = script[11:-3]+'_'+inst
        ex_res = "../experimental_results_{}.log".format(design_name)
        with open(ex_res, "a") as f:
            #1.1 design name
            line1 = "Design: {0}\n".format(design_name)
            f.write(line1)
            #1.2 design statistics
            g = os.walk(r"../../abc/design")
            for path, dir_list, file_list in g:
                   for file_name in file_list:
                         if(design_name in file_name):
                           design_dir = os.path.join(path, file_name)
            design_txt = design_dir[:-4]+'.txt'
            os.system("cp {0} {1}".format(design_dir, design_txt))
            with open(design_txt, "r", encoding='latin1') as d:
               d_lines = d.readlines()
               aig_str = d_lines[0]
               d.close()
            os.remove(design_txt)
            statis = re.search(r'aig (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)', aig_str)
            state_bit = statis.group(3)
            logic_gate = statis.group(5)
            
            line2 = "   #. state bit: {}\n".format(state_bit)
            f.write(line2)
            line3 = "   #. logic gate: {}\n".format(logic_gate)
            f.write(line3)
            runtime = end_time-start_time
            line4 = "   Simulation time: {:.3f}(s)\n".format(runtime)
            f.write(line4)
            f.close()
            

            

        
        
        
if __name__ == "__main__":
   main(sys.argv[1:])
