import socket
import select
 
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
    decoded_payload = hamming_decode(payload)       #


    print('decoded_payload playload')
    print(decoded_payload)

    d=48393883292703003300067554859838128129
    N=252837207378338387332619197259204540353


    #convert the int to bytes, and concatenate each bytes       
    b = b""                         
    for x in decoded_payload:
        b = b"".join([b, bytes([x])])
        print(b)
        #b is bytes in the formal b'\xc2x\xcb\xa3'
    
    int_cipher = int.from_bytes(b, byteorder='big')     #convert the bytes into an int, assumed big endian
    print(int_cipher)

    decoded = pow(int_cipher, d, N)                     #decrypt the cipher(type is int, return an int)
    print(decoded)


    decoded_bytes = int_to_Bytes(decoded)               #converts int and returns a list of 8bits binary in string format
    out = []
    for i in decoded_bytes:
        out.append(int(i, base=2))                      #converts string of 8bit (1s 0s) into ints of range(0-255)
        print(int(i, base=2))
    print(decoded_bytes)

    for i in out:
        print(chr(i), end = '')                         #convert int to ascii
 
    s.close()
 
def hamming_decode(data):
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
    print ('databits')
    print (databits)
    print('con')
    print (con)
        #print(integ)
        #print(binar)


    

    
    i=0
    alldata = []
    while i<(len(databits)/8)-8:
        databin = databits [i*8:(i*8+8)]
        databin = databin[0:7]
        out = hamming(databin)
        alldata.append(out)
        i=i+1
    # print(alldata)
    databyte = []
    i=0

    #print(databyte)
 
    while (i<len(alldata)-1):
        if (i%2==0):
            buff = alldata[i]+alldata[i+1]
            databyte.append(buff)
        i=i+1
    #print('databyte')
    #print ((databyte))
    
    i=0
    listToStr = []
    while (i<len(databyte)):
        buff1 = ''.join([str(elem) for elem in databyte[i]])
        buff1 = int(buff1,2)
        listToStr.append(buff1)
        i=i+1
    #print (listToStr)
    #print(len(listToStr))
 
    # convert bitstring stored i list into byte string
    #decrypt rsa https://www.kite.com/python/answers/how-to-encrypt-and-decrypt-a-message-with-rsa-in-python
    return listToStr
 
############HAMMING#############
def hamming (binInput):
    #binInput = [1,0,1,1,0,1,0]
    output = binInput
   
    p1 = [int(binInput[4]), int(binInput[2]), int(binInput[0]), int(binInput[6])]
    p2 = [int(binInput[4]), int(binInput[1]), int(binInput[0]), int(binInput[5])]
    p4 = [int(binInput[2]), int(binInput[1]), int(binInput[0]), int(binInput[3])]
    parity = [sum(p1) % 2, sum(p2) % 2, sum(p4) % 2]
    #print(parity)
    # if even parity, flip errored bit
    if parity[0] and parity[1] and parity[2]:
        output[0] = int(not (binInput[0]))
    elif parity[0] and parity[1]:
        output[4] = int(not(binInput[4]))
    elif parity[0] and parity[2]:
        output[2] = int(not (binInput[2]))
    elif parity[1] and parity[2]:
        output[1] = int(not (binInput[1]))
    elif parity[0]:
        output[6] = int(not (binInput[6]))
    elif parity[1]:
        output[5] = int(not(binInput[5]))
    elif parity[2]:
        output[3] = int(not(binInput[3]))
 
    #print(output)
 
    #Remove parity bits to leave data bits only
    output = [output[0],output[1],output[2],output[4]]
#print(output)
    return output
 
def access_bit(data, num):                  #bytes into binary (string)
    base = int(num // 8)
    shift = int(num % 8)
 
    return (data[base] & (1<<shift)) >> shift

def int_to_Bytes(integer):
    
    #print('int to sting of 0s and 1s')
    #print(bin(integer))
    binary = bin(integer)       #return binary of integers in string format 
    binary = binary[2:]         #chop off the first two element (0b)
    #print(binary)

    list_of_bytes = []          #will contain whole binary into list of 8bits (string)
    i = 0
    while i<(len(binary)/8)-8:              #size of list of bytes less than what it should be - need to fix
        databin = binary [i*8:(i*8+8)]
        list_of_bytes.append(databin)
        i=i+1
    
    #print(len(binary))
    #print(len(list_of_bytes))



    return list_of_bytes


 
if __name__ == '__main__':
    main()
 
 