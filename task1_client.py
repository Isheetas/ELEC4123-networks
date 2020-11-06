import socket
import select
import math

 
def main():
 
    # 1. Send well-formed HTTP requests
    HOST = '149.171.36.192'
    PORT = 12274
    content = '252837207378338387332619197259204540353,65537'
    host = '149.171.36.192' 
    # HTTP request headers
    request = 'GET / HTTP/1.1\r\nHost: ' + host + '\r\nContent-Length: ' + str(len(content)) + '\r\n\r\n' + content
    request_bytes =  bytes(request, 'utf-8') 
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print ("Socket successfully created")
    except socket.error as err: 
        print ("socket creation failed with error %s" %(err))
    
    
    s.connect((HOST, PORT))
    s.send (request_bytes)
    
    ready = select.select([s], [], [], 10)
    if ready[0]:
        response = s.recv(64000)
    #print(bytearray(data)) 
    
    print(b'received msg: ' + response)
    response_tokens = response.split(b'\r\n\r\n')
    response_header = response_tokens[0] + b'\r\n\r\n'
    print(b'response header:' + response_header)
    payload = response_tokens[1]
    print(payload)
 
    # extract output content - comes after \r\n\r\n
 
    # 2. Resolve hamming code on payload
    databits = convert_payload_binary(payload)       #makes payload into binary
    print('binary payload: ')
    print(databits)

    corrected_databits = hamming(databits)
    print('corrected: ')
    print(corrected_databits, ' ', len(corrected_databits))


    #3. RSA decryption
    d=48393883292703003300067554859838128129
    N=252837207378338387332619197259204540353


    int_cipher = int(corrected_databits, 2)     #convert the bytes into an int, assumed big endian
    print('int_cipher: ', int_cipher)

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
 
def convert_payload_binary(data):
    '''
    Input: array of hex (bytearray)
    Output: string of binary (1s and 0s)
    '''
    #print('data')
    #print(data)

    con = ''
    databits = []
    for i in data:
        integer = int(i)
        binary = bin(integer)
        binary = binary[2:]
        if len(binary) < 8:             #pad with zero if bits are less than zero -> ?? need to do that or no
            pad = 8 - len(binary)
            zeros = ''
            for i in range(pad):
                zeros = zeros+'0'
            binary = zeros+binary
        databits.append(binary) 
        con = con + binary
    return con
 

#DYNAMIC HAMMING DECODER
def hamming (input):
    '''
    input: binary string of 1s and 0s
    output: binary string of 1s and 0s - with parity bits removed
    '''

    #input = '011100101110'         #test input

    # caluclate number of parity bits
    n = len(input)
    numParity = math.log(n, 2) + 1
    numParity = math.floor(numParity)
    #print('parity: ', numParity, n)


    data = input[::-1]
    #data = input
    output = list(data)
    print(data)
    errorDetect = []
    lookup = []

    for i in range(numParity):
        #print('i:', i)
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

        errorDetect.append(Sum % 2)
        lookup.append(dataBits)

    p = 0
    oddPar = []
    for x in errorDetect:
        if x == 1:
            oddPar.append(2**p)
            print('index: ', 2**p)
        p = p + 1

    index = sum(oddPar)
    output[index-1] = str(int(not data[index-1]))

    # remove parity bits
    c = 0   #needed to update the index - as the index changes after each parity bit is removed                  
    for r in range(0, numParity):
        par = (2 ** r) - 1 - c
        output.pop(par)
        c = c + 1

    
    # convert list output to string
    strOutput = ""
    str_bin = strOutput.join(output)

    return str_bin
    
def int_to_Bytes(integer):
    '''
    input: int
    output: list of bytes(binary) - WHAT IF NOT DIVISIBLE BY 8????
    '''

    binary = bin(integer)       #return binary of integers in string format 
    binary = binary[2:]         #chop off the first two element (0b)

    list_of_bytes = []          #will contain whole binary into list of 8bits (string)
    n = 8
    list_of_bytes = [binary[i:i+8] for i in range(0, len(binary), n)]
    print(list_of_bytes)
        
    return list_of_bytes



 
if __name__ == '__main__':
    main()
 
 