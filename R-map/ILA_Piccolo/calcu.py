#!/usr/bin/python3
# coding=utf-8
import os
import re
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

class preprocessing:
    
    #private
    __files = []
    __reinement = []
    workload_ratio = []
    isa_name = []
    generated_line = []
    generated_reg = []
    refinement_line = -1
    __count_lines_v = -1
    __count_all_lines_v = -1
    __count_reg = -1
    __count_lines_r = 0
    

    def __init__(self,base1,base2):

        self.dir = base1 #verification (wrapper.v)
        self.dir2 = base2 #refinement
        self.__files = self.collect_files_v()
        self.__reinement = self.collect_files_r() #refinement file

        for f in self.__files:
            self.__count_lines_v , self.__count_all_lines_v, self.__count_reg = self.calc_linenum_v(f)
            self.workload_ratio.append((self.__count_lines_v/self.__count_all_lines_v)*100)
            self.generated_line.append(self.__count_lines_v)
            self.generated_reg.append(self.__count_reg)
            self.isa_name.append(os.path.dirname(f).split('/')[-1])
            #print(self.__count_all_lines)
        
        for f in self.__reinement:
            self.__count_lines_r = self.calc_linenum_r(f) + self.__count_lines_r
            #print(self.__count_lines_r)
            self.refinement_line = self.__count_lines_r


    #collect all the *.v file, return in list form
    def collect_files_v(self):
        filelist = []
        for parent,dirnames,filenames in os.walk(self.dir):
            for filename in filenames:
                if filename.endswith('.v') and ((parent.split('/'))[-1]!='invariants'):
                    filelist.append(os.path.join(parent,filename))
        return filelist

    #collect all the *.json file, return in list form
    def collect_files_r(self):
        filelist = []
        for parent,dirnames,filenames in os.walk(self.dir2):
            for filename in filenames:
                if filename.endswith('.json'):
                    filelist.append(os.path.join(parent,filename))      
        #print(filelist)
        return(filelist)

    #Calculate the number of line in individual file
    def calc_linenum_v(self,file):
        with open(file) as fp:
            #f = open('./verification/ADD/wrapper.v','r')
            lines = fp.readlines()
            start = lines.index( '/* GENERATE WRAPPER */\n' )
            end = lines.index( '/* END OF WRAPPER */\n' )
            number_lines_v = end - start - 1
            number_all_lines_v = len(lines)
            number_of_reg = len([reg for reg in lines[start:end] if re.match(r'(.*) reg (.*?).*',reg)!= None])
        return number_lines_v, number_all_lines_v, number_of_reg
    
    #Calculate the number of all lines in refinment file
    def calc_linenum_r(self,file):
        with open(file) as fp:
            lines_r = len(fp.readlines())
        return lines_r


class draw:
    #Define private
    __list1_isa = []
    __list2_lines = []
    __list3_work_ratio = []
    __list4_reg = []

    def __init__(self,list1,list2,list3,list4,refinment_count):
        self.__list1_isa = list1
        self.__list2_lines = list2
        self.__list3_work_ratio = list3
        self.__list4_reg = list4
        self.draw_diagram()
        self.draw_table()
        self.count_r = [refinment_count]

    def draw_diagram(self):
        reduced_workload = self.__list3_work_ratio #get from outside
        ISA = self.__list1_isa
        plt.figure(figsize=(10, 15))
        range_number = len(ISA)
        plt.barh(range(len(ISA)), reduced_workload , height=0.7, color='steelblue', alpha=0.8)
        #plt.barh(range(len(ISA)), reduced_workload , color='steelblue')
        plt.yticks(range(len(ISA)), ISA)
        plt.xlim(10,15)
        plt.xlabel("ratio of workload")
        plt.title("reduced workload by ILAng")
        for x, y in enumerate(reduced_workload):
            plt.text(y + 0.2, x - 0.1, '%s' % y)
        plt.show()

    def draw_table(self):
        data = list(zip(self.__list1_isa,self.__list2_lines,self.__list3_work_ratio,self.__list4_reg))[:]
        df = pd.DataFrame(data,columns=['ISA','Generated Line','Reduced Workload(%)','generated reg'],dtype=float)
        df.to_json("experiment.json")
        #print(df.to_latex(index=False))
        print(df)

    def draw_conclusion_table(self):
        #print([].append(self.count_r))
        data = [['Piccolo','5-stage','RV32I',sum(self.count_r),sum(self.__list4_reg),sum(self.__list4_reg)/len(self.__list4_reg),sum(self.__list2_lines),sum(self.__list2_lines)/len(self.__list2_lines)]]
        #print(data)
        df = pd.DataFrame(data,columns=['Prj','prj_des','ISA_des','Ref','Reg(sum)','Ave_reg','Line(sum)','Ave_line'],dtype=int)
        #df.reset_index(drop=True, inplace=True)
        df.to_json((os.getcwd().split('/'))[-1]+".json")
        print(df)

if __name__ == '__main__':
    #Define the dir of code
    v_base_path = './verification/'
    r_base_path = './refinement'
    pre = preprocessing(v_base_path,r_base_path)
    draw_data = draw(pre.isa_name,pre.generated_line,pre.workload_ratio,pre.generated_reg,pre.refinement_line)
    draw_data.draw_conclusion_table()