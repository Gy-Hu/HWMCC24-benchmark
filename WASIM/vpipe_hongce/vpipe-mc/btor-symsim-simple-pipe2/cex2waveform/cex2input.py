inputline = []
with open("cex.txt",'r') as f:
    for cexline in f.readlines():
        if(('__ILA_I_inst' in cexline) or ('inst_valid' in cexline) or ('stallex' in cexline) or ('stallwb' in cexline)):
            inputline.append(cexline)
        elif('RTL_registers' in cexline):
            inputline.append(cexline)

with open("input.txt",'w') as f:
    for line in inputline:
        f.write(line)

        # elif('inst_valid' in cexline):
        #     print(cexline)
        # elif('stallex' in cexline):
        #     print(cexline)
        # elif('stallwb' in cexline):
        #     print(cexline)
        # elif('dummy_read_rf' in cexline):
        #     print(cexline)