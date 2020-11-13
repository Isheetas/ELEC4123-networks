import socket
import select
import math


def main():
    # 1. Send well-formed HTTP requests
    HOST = '149.171.36.192'
    PORT = 12274
    host = '149.171.36.192'

    # N = 63148583107154283585608284940392418734726981382069355868003882013090711003369
    # e = 65537
    # d = 51783437651169347215431900289402465246791119526563008636281618633074802696377
    N = 252837207378338387332619197259204540353
    e = 65537
    d = 48393883292703003300067554859838128129

    content = str(N) + "," + str(e)
    #print('content: ', content)
    # HTTP request headers
    request = 'GET / HTTP/1.1\r\nHost: ' + host + '\r\nContent-Length: ' + str(len(content)) + '\r\n\r\n' + content
    request_bytes = bytes(request, 'utf-8')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
    except socket.error as err:
        print("socket creation failed with error %s" % (err))

    s.connect((HOST, PORT))
    s.send(request_bytes)

    ready = select.select([s], [], [], 10)
    if ready[0]:
        response = s.recv(64000)
    # print(bytearray(data))

    # print(b'received msg: ' + response)
    response_tokens = response.split(b'\r\n\r\n')
    response_header = response_tokens[0] + b'\r\n\r\n'
    # print(b'response header:' + response_header)
    payload = response_tokens[1]
    print('received payload bytes: ', len(payload))

    # extract output content - comes after \r\n\r\n

    # 2. Resolve hamming code on payload
    databits = convert_payload_binary(payload)  # makes payload into binary
    print('binary payload: ', databits, len(databits))
    # print(databits)

    corrected_databits = hamming(databits)
    # print('corrected: ')
    print('corrected: ', corrected_databits, ' ', len(corrected_databits))

    int_cipher = int(corrected_databits, 2)  # convert the bytes into an int, assumed big endian
    # print('int_cipher: ', int_cipher)

    decrypted_payload = decrypt_rsa(int_cipher, N, d)
    print('dec: ', decrypted_payload)
    print('size: ', len(decrypted_payload))

    extract_marks(decrypted_payload)


    decoded = pow(int_cipher, d, N)                     #decrypt the cipher(type is int, return an int)
    print('decoded: ', decoded)
    #convert int into ascii -> to get the message
    decoded_bytes = int_to_Bytes(decoded)               #converts int and returns a list of 8bits binary in string format


    out = []
    for i in decoded_bytes:
        out.append(int(i, base=2))                      #converts string of 8bit (1s 0s) into ints of range(0-255)
    #convert ints into char
    for i in out:
        print(i, chr(i), end = ' ')                     #convert int to ascii


    s.close()


def extract_marks(data):
    n_entries = data[0]
    print("n_entires: ", n_entries)
    len_student_bytes = 10  # bytes taken up by each students information
    n = 0

    while n < n_entries:
        start = n * 10 + 1
        # print(response[i])
        # first byte is number of students
        name = str(data[start:(start + 4)])
        t1 = data[start + 5]
        t2 = data[start + 6]
        t3 = data[start + 7]
        t4 = data[start + 8]
        total = data[start + 9]
        print('name: ' + name)
        print('t1:', t1)
        print('t2:', t2)
        print('t3:', t3)
        print('t4:', t4)
        print('total:', total)
        n = n + 1


def convert_payload_binary(data):
    '''
    Input: array of hex (bytearray)
    Output: string of binary (1s and 0s)
    '''
    # print('data')
    # print(data)

    con = ''
    databits = []
    for i in data:
        integer = int(i)
        binary = bin(integer)
        binary = binary[2:]
        if len(binary) < 8:  # pad with zero if bits are less than zero -> ?? need to do that or no
            pad = 8 - len(binary)
            zeros = ''
            for i in range(pad):
                zeros = zeros + '0'
            binary = zeros + binary
        databits.append(binary)
        con = con + binary
    return con


# DYNAMIC HAMMING DECODER
def hamming(input):
    '''
    input: binary string of 1s and 0s
    output: binary string of 1s and 0s - with parity bits removed
    '''

    # input = '011100101110'         #test input

    # caluclate number of parity bits
    n = len(input)
    numParity = math.log(n, 2) + 1
    numParity = math.floor(numParity)
    print('parity: ', numParity, n)

    data = input[::-1]  # flip data
    # data = input
    output = list(data)
    errorDetect = []
    # lookup = []

    for i in range(numParity):
        print('i:', i)
        parity = 2 ** i  # 2^0, 2^1, 2^2, ...
        pos = parity - 1
        Sum = 0
        start = pos
        dataBits = []

        while start < len(data):
            cluster = 0

            while (cluster < parity and start + cluster < len(data)):
                Sum = Sum + int(data[start + cluster])
                dataBits.append(start + cluster)
                cluster = cluster + 1

            start = start + 2 * parity
        print(Sum % 2)
        errorDetect.append(Sum % 2)
        # lookup.append(dataBits)

    p = 0
    oddPar = []
    for x in errorDetect:
        if x == 1:
            oddPar.append(2 ** p)
            print('index: ', 2**p)
        p = p + 1

    index = sum(oddPar)
    # print('incorred index: ', index)
    #print(output[index-1])

    #output[index - 1] = str(int(not data[index - 1]))
    print(data[index - 1])
    if data[index - 1] == '1':
        output[index - 1] = str(0)
    else:
        output[index - 1] = str(1)
    print(output[index - 1])
    # print('in_data: ')
    # print(data)
    # print("".join(output))

    # remove parity bits
    r = numParity - 1
    while r >= 0:
        par = 2 ** r
        output.pop(par - 1)
        r = r - 1

    output = output[::-1]
    print("ouptut before rem: ", "".join(output), len(output))

    if (len(output) > 256):
        rem_bits = len(output) - 256
        #print('rem_bits: ', rem_bits)
        output = output[rem_bits:]

    # convert list output to string
    strOutput = ""
    str_bin = strOutput.join(output)

    return str_bin


def int_to_Bytes(integer):
    '''
    input: int
    output: list of bytes(binary) - WHAT IF NOT DIVISIBLE BY 8????
    '''

    binary = bin(integer)  # return binary of integers in string format
    binary = binary[2:]  # chop off the first two element (0b)

    list_of_bytes = []  # will contain whole binary into list of 8bits (string)
    n = 8
    list_of_bytes = [binary[i:i + 8] for i in range(0, len(binary), n)]
    print(list_of_bytes)

    return list_of_bytes


def decrypt_rsa(cipher_int, n, d):
    # cipher_int = int.from_bytes(cipher_bytes, byteorder='big') # convert cipher to integer form
    plaintext_int = pow(cipher_int, int(d), int(n))
    plaintext_bytes = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'big')
    return plaintext_bytes


if __name__ == '__main__':
    main()