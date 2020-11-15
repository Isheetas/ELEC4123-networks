from type_conversions import int_to_bytes, bytes_to_int


def encrypt_rsa(msg_int, n, e):
    '''
    Encrypt with RSA 
    Input plaintext (String e.g 'Hello') - payload to encrypt as a text string, n(String), e(String)
    Output cipher_bytes (String e.g  b'\xa9z\xb7\xf3\')
    '''
    cipher_int = pow(msg_int, int(e), int(n))
    cipher_bytes = int_to_bytes(cipher_int)
    return cipher_bytes

def decrypt_rsa(cipher_int, n, d):
    #cipher_int = int.from_bytes(cipher_bytes, byteorder='big') # convert cipher to integer form
    plaintext_int = pow(cipher_int, int(d), int(n))
    plaintext_bytes = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'big')
    return plaintext_bytes
