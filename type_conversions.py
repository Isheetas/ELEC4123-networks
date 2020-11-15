from bitstring import BitArray



'''
FUNCTIONS TO CONVERT BETWEEN PYTHON TYPES
'''

def bytes_to_int(byte):
    return int.from_bytes(byte, byteorder='big') # convert cipher to integer form

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