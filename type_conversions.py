from bitstring import BitArray



'''
FUNCTIONS TO CONVERT BETWEEN PYTHON TYPES
'''

def bytes_to_int(byte):
    print('in bytes->int')
    fin = ""
    print(len(byte))
    for i in byte:
        binary = bin(i)
        binary = binary[2:]
        fin = fin + binary.zfill(8) 
    print(fin, len(fin))

    integer = int(fin, 2)
    print('integer: ', integer)


    return integer

def int_to_bytes(integer_val):
    '''
    input: int
    output: list of bytes(binary) 
    '''
    return integer_val.to_bytes((integer_val.bit_length() + 7) // 8, 'big')



def bytes_to_bits(byte_array):
    '''
    Input: array of hex (bytearray)
    Output: string of binary (1s and 0s) nb return bitclass if necessary: get rid of .bin
    '''
    res = BitArray(byte_array) #type - bitclass - use .bin method to see bits
    return res.bin