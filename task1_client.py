import socket
import select
import math

 
def main():
 
    # 1. Send well-formed HTTP requests
    HOST = '149.171.36.192'
    PORT = 12274
    content = '252837207378338387332619197259204540353,65537'
 
    # HTTP request headers
    request = 'GET / HTTP/1.1\r\nHost: ' + HOST + '\r\nContent-Length: ' + str(len(content)) + '\r\n\r\n' + content
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
    databits = convert_payload_binary(payload)       #
    print('binary payload: ')
    print(databits)

    corrected_databits = hamming(databits)
    print('corrected: ')
    print(corrected_databits, ' ', len(corrected_databits))


    d=48393883292703003300067554859838128129
    N=252837207378338387332619197259204540353


    #convert the int to bytes, and concatenate each bytes  


    int_cipher = int(corrected_databits, 2)     #convert the bytes into an int, assumed big endian
    print('int_cipher: ', int_cipher)

    decoded = pow(int_cipher, d, N)                     #decrypt the cipher(type is int, return an int)
    print('decoded: ', decoded)


    
    decoded_bytes = int_to_Bytes(decoded)               #converts int and returns a list of 8bits binary in string format
    
    
    out = []
    for i in decoded_bytes:
        out.append(int(i, base=2))                      #converts string of 8bit (1s 0s) into ints of range(0-255)
        print('int char: ', int(i, base=2))
    print(decoded_bytes)

    print('Ascii: ')
    for i in out:
        
        print(i, chr(i), end = ' ')                         #convert int to ascii
       
 
    s.close()
 
def convert_payload_binary(data):
    print('data')
    print(data)

    con = ''
    databits = []
    for i in data:
        integer = int(i)
        binary = bin(integer)
        binary = binary[2:]
        if len(binary) < 8:
            pad = 8 - len(binary)
            zeros = ''
            for i in range(pad):
                zeros = zeros+'0'
            binary = zeros+binary
        databits.append(binary) 
        con = con + binary
   

    # convert bitstring stored i list into byte string
    #decrypt rsa https://www.kite.com/python/answers/how-to-encrypt-and-decrypt-a-message-with-rsa-in-python
    return con
 
############HAMMING#############

#DYNAMIC HAMMING DECODER
def hamming (input):
#    input = '01110101'

    # caluclate number of parity bits
    n = len(input)
    numParity = math.log(n, 2) + 1
    numParity = math.floor(numParity)
    # print(numParity)


    data = input[::-1]
    output = list(data)
    # print(data)
    errorDetect = []
    lookup = []

    for i in range(numParity):
        # print('i:', i)
        parity = 2 ** i  # 2^0, 2^1, 2^2, ...
        pos = parity - 1
        sum = 0
        start = pos
        dataBits = []

        while start < len(data):
            cluster = 0

            while (cluster < parity and start + cluster < len(data)):
                sum = sum + int(data[start + cluster])
                dataBits.append(start + cluster)
                # print(data[start+cluster])

                cluster = cluster + 1

            start = start + 2 * parity

        # print('sum:', sum)
        errorDetect.append(sum % 2)
        lookup.append(dataBits)
    # print(errorDetect)

    p = 0
    oddPar = []
    for x in errorDetect:
        if x == 1:
            oddPar.append(p)
        p = p + 1

    # print(oddPar)
    # print(lookup)

    erroneousSets = []
    for x in oddPar:
        erroneousSets.append(set(lookup[x]))

    if len(oddPar) > 1:
        u = set.intersection(*erroneousSets)
        # print(input)
        output[min(u)] = str(int(not data[min(u)]))

    else:
        output[oddPar[0]] = str(int(not data[oddPar[0]]))

    # remove parity bits
    '''
    c = 0
    for r in range(numParity-1, 0):
        par = (2 ** r)
        print(output)
        output.remove(output[par-1])
        c = c + 1
        '''
    r = numParity - 1
    while r >= 0:
        par = 2**r
        output.pop(par-1)
        r = r-1

    output = output[::-1]
    # print(output)
    # print(type(output[0]))

    # convert list output to string
    strOutput = ""
    out = strOutput.join(output)

    return out
    
def int_to_Bytes(integer):
    
    #print('int to sting of 0s and 1s')
    #print(bin(integer))
    binary = bin(integer)       #return binary of integers in string format 
    binary = binary[2:]         #chop off the first two element (0b)
    print('binary: ', binary, len(binary))



    list_of_bytes = []          #will contain whole binary into list of 8bits (string)
    n = 8
    l = [binary[i:i+8] for i in range(0, len(binary), n)]
    print(l)
        
    #print(len(binary))
    #print(list_of_bytes)


    return l



 
if __name__ == '__main__':
    main()
 
 