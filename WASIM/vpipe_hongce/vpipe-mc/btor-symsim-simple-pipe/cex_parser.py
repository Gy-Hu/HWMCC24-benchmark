import os

def sort_model(m):
    mstr = str(m)
    return ('\n'.join(sorted(mstr.split('\n'))))

def cex_parser(cex):
    # create cex.txt
    cex_file = '/home/fwj/vpipe-mc/btor-symsim-simple-pipe/cex.txt'
    with open (cex_file, 'w') as f:
        f.write(sort_model(cex))
    
    #extract information from txt by regular expression
    for line in open (cex_file, 'r'):
        if(line == '__START__ := 0_1\n'):
            n_tag0 = 0
        elif(line == '__START__ := 1_1\n'):
            n_tag0 = 1
        elif(line == 'ppl_stage_ex := 0_1\n'):
            n_tag1 = 0
        elif(line == 'ppl_stage_ex := 1_1\n'):
            n_tag1 = 1
        elif(line == 'ppl_stage_wb := 0_1\n'):
            n_tag2 = 0
        elif(line == 'ppl_stage_wb := 1_1\n'):
            n_tag2 = 1
        elif(line == 'ppl_stage_finish := 0_1\n'):
            n_tag3 = 0
        elif(line == 'ppl_stage_finish := 1_1\n'):
            n_tag3 = 1
        elif(line == 'v1 := 0_1\n'):
            v1 = 0
        elif(line == 'v1 := 1_1\n'):
            v1 = 1
        elif(line == 'v2 := 0_1\n'):
            v2 = 0
        elif(line == 'v2 := 1_1\n'):
            v2 = 1
        elif(line == 'w1 := 0_1\n'):
            w1 = 0
        elif(line == 'w1 := 1_1\n'):
            w1 = 1
        elif(line == 'w2 := 0_1\n'):
            w2 = 0
        elif(line == 'w2 := 1_1\n'):
            w2 = 1
        
    
    if((v1==0 and v2==0)):
        v_cons = 0
    elif((v1==0 and v2==1)):
        v_cons = 1
    elif((v1==1 and v2==0)):
        v_cons = 2
    elif((v1==1 and v2==1)):
        v_cons = 3
    
    if((w1==0 and w2==0)):
        w_cons = 0
    elif((w1==0 and w2==1)):
        w_cons = 1
    elif((w1==1 and w2==0)):
        w_cons = 2
    elif((w1==1 and w2==1)):
        w_cons = 3
    
    os.remove(cex_file)
    return (v_cons,n_tag0,n_tag1,n_tag2,n_tag3)
