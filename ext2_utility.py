def decrypt_rsa(cipher_bytes, n, d):
    # message to decrypt will always be a multiple of 16
    plaintext_bytes_temp = b''
    plaintext_bytes = b''
    start = 0
    while start < len(cipher_bytes):
        end = start + 16
        cipher_int = int.from_bytes(cipher_bytes[start:end], byteorder='big') # convert cipher to integer form
        plaintext_int = pow(cipher_int, int(d), int(n))
        plaintext_bytes_temp = int_to_bytes(plaintext_int)
        plaintext_bytes = plaintext_bytes + plaintext_bytes_temp
        start = end
    return plaintext_bytes


def encrypt_rsa(msg_bytes, n, e):
    '''
    Encrypt with RSA
    Input plaintext (String e.g 'Hello') - payload to encrypt as a text string, n(String), e(String)
    Output cipher_bytes (String e.g  b'\xa9z\xb7\xf3\')
    '''
    cipher_bytes_temp = b''
    cipher_bytes = b''
    start = 0
    while start < len(msg_bytes):
        end = start + 16
        msg_int = int.from_bytes(msg_bytes[start:end], byteorder='big')
        cipher_int = pow(msg_int, int(e), int(n))
        cipher_bytes_temp = int_to_bytes(cipher_int)
        cipher_bytes = cipher_bytes + cipher_bytes_temp
        start = end
    return cipher_bytes



def int_to_bytes(integer_val):
    '''
    input: int
    output: list of bytes(binary)
    '''
    return integer_val.to_bytes((integer_val.bit_length() + 7) // 8, 'big')


def print_to_ascii(msg_bytes):
    n_entries = msg_bytes[0]
    len_student_bytes = 10 # bytes taken up by each students information
    n = 0
    while n < n_entries:
        start = n*10 + 1
        # print(response[i]) 
        # first byte is number of students
        name = str((msg_bytes[start:(start + 5)]), 'utf-8')
        t1 = msg_bytes[start+5]
        t2 = msg_bytes[start+6]
        t3 = msg_bytes[start+7]
        t4 = msg_bytes[start+8]
        total = msg_bytes[start+9]
        print(name, end = ' ')
        print('t1: ',  t1, end = ' ')
        print('t2: ', t2, end = ' ')
        print('t3: ', t3, end = ' ')
        print('t4: ', t4, end = ' ')
        print('total: ', total)
        # next five bytes form name

        n += 1
