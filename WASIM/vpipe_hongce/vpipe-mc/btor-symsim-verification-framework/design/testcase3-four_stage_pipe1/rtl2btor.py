import sys, getopt, re, os

def main(argv):
   ifile = ''
   ofile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:t:o:",["ifile=","top=","ofile="])
   except getopt.GetoptError:
      print('test.py -i <inputfile> -t <topname> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('rtl2btor.py -i <inputfile> -t <topname> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         ifile = arg
      elif opt in ("-t", "--top"):
         top = arg
      elif opt in ("-o", "--ofile"):
         ofile = arg
   print('input file: ', ifile)
   print('top name:   ', top)
   print('output file:', ofile)

   ## regular expression to replace the gen_btor_template.ys
   f_t = open('gen_btor_template.ys', 'r')
   f = open('gen_btor.ys', 'w')
   lines = f_t.readlines()
   for line in lines:
        if('input_file_000' in str(line)):
            line_new = re.sub(r'input_file_000', str(ifile), line)
        elif('top_name_000' in str(line)):
            line_new = re.sub(r'top_name_000', str(top), line)
        elif('output_file_000' in str(line)):
            line_new = re.sub(r'output_file_000', str(ofile), line)
        else:
            line_new = line
        f.writelines(line_new)
   f_t.close()
   f.close()
   
   ## run yosys to generate btor file from verilog
   os.system('yosys gen_btor.ys')

   ## check btor format
   f_b = open(str(ofile), 'r')
   f_b_new = open('{}.new'.format(ofile), 'w')
   lines = f_b.readlines()
   for line in lines:
        if('RTL.' in str(line)):
            line_new = re.sub(r'RTL.', 'RTL_', line)
        elif('ILA.' in str(line)):
            line_new = re.sub(r'ILA.', 'ILA_', line)
        else:
            line_new = line
        f_b_new.writelines(line_new)
   f_b.close()
   f_b_new.close()

   os.remove('{}'.format(ofile))
   os.system('mv {new_file} {old_file}'.format(new_file = '{}.new'.format(ofile), old_file = str(ofile)))

   ## print some information
   btor_path = os.path.abspath(str(ofile))
   print('\n\n')
   print('-'*10, 'Script Information', '-'*10)
   print('input file: ', ifile)
   print('top name:   ', top)
   print('output file:', ofile)
   print('output btor file path:', btor_path)


if __name__ == "__main__":
   main(sys.argv[1:])