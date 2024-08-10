import sys

if __name__ == '__main__':
    int_num = int(sys.argv[1])
    bin_num = '{:08b}'.format(int_num)
   # bin_num = bin(int_num)
    print('DEC:',int_num)
    print('BIN:',bin_num)


