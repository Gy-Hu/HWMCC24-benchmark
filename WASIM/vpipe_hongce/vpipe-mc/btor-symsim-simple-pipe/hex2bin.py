import sys

if __name__ == '__main__':
    hex_num = sys.argv[1]
    print('HEX:',hex_num)
    int_num = int(hex_num, 16)
    bin_num = bin(int_num)
    bin_num = '{:08b}'.format(int_num)
    print('DEC:',int_num)
    print('BIN:',bin_num)



