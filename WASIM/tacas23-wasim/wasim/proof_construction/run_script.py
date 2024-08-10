import sys, getopt, re, os, time

def main(argv):
   script = ''
   logdir = ''
   try:
      opts, args = getopt.getopt(argv,"hs:l:i:v:",["script=","logdir=","inst=","verify="])
   except getopt.GetoptError:
      ('run_script.py  -s <script> -l <logpath> -i <inst_type> -v <verify>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('run_script.py -s <script> -l <logdir> -i <inst_type> -v <verify>')
         sys.exit()
    #   elif opt in ("-i", "--inst"):
    #      inst = arg
      elif opt in ("-s", "--script"):
         script = arg
      elif opt in ("-l", "--logdir"):
         logdir = arg
      elif opt in ("-i", "--inst"):
         inst_type = arg
      elif opt in ("-v", "--verify"):
         ver_type = arg
   print('Script name:   ', script)
   print('Log path:', logdir)
   print('Instruction type:', inst_type)
   print('\n')
   print('Script name:   ', script)
   print('Instruction type:', inst_type)
   print('\n')
   assert str(ver_type) in ['fpv', 'inv']
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
             if('inv' in script):
                   design_name = script[10:-3]
             else:
                   design_name = script[11:-3]
        else:
             if('inv' in script):
                   design_name = script[10:-3]+'_'+inst
             else:
                   design_name = script[11:-3]+'_'+inst
        ex_res = "../experimental_results_{}.log".format(design_name)
        with open(ex_res, "a") as f:
            runtime = end_time-start_time
            if(str(ver_type) == 'fpv'):
               line4 = "   FPV time: {:.3f}(s)\n".format(runtime)
            elif(str(ver_type) == 'inv'):
               line4 = "   Inv time: {:.3f}(s)\n".format(runtime)
            else:
                   print('ERROR: wrong -v parameter!')
                   assert(False)
            f.write(line4)
            f.close()
        
        
        
if __name__ == "__main__":
   main(sys.argv[1:])
