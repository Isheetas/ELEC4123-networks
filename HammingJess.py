import math


def hamming_decode (input, exparity):
    '''
    input: binary string of 1s and 0s
    output: binary string of 1s and 0s - with parity bits removed
    '''

    #input = '011100101110'         #test input

    # caluclate number of parity bits        
    n = len(input)
    if (exparity):
        n = n-1
    numParity = 0
    count = 0
    while 2**numParity < n + numParity + 1:
        numParity = numParity + 1
        
    print ('numParity', numParity)
    #print ('numParity', numParity)
    ##print('parity: ', numParity, n)


    data = input[::-1]          #flip data 
    #data = input
    output = list(data)
    errorDetect = []
    #lookup = []

    for i in range(numParity):
        ##print('i:', i)
        parity = 2 ** i  # 2^0, 2^1, 2^2, ...
        pos = parity - 1
        Sum = 0
        start = pos
        dataBits = []

        while start < len(data):
            cluster = 0
            ##print("start: ", start)

            while (cluster < parity and start + cluster < len(data)):
                Sum = Sum + int(data[start + cluster])
                dataBits.append(start + cluster)
                cluster = cluster + 1

                


            start = start + 2 * parity
            ##print('cluster: ', cluster)

        errorDetect.append(Sum % 2)
        #lookup.append(dataBits)

    p = 0
    oddPar = []
    for x in errorDetect:
        if x == 1:
            oddPar.append(2**p)
            ##print('index: ', 2**p)
        p = p + 1

    index = sum(oddPar)



    if data[index - 1] == '1':
        output[index - 1] = str(0)
    else:
        output[index - 1] = str(1)


    
    # remove parity bits
    r = numParity - 1
    while r >= 0:
        par = 2**r
        output.pop(par-1)
        r = r-1


    output = output[::-1]
    ##print("ouptut before rem: ", "".join(output), len(output))

    if (len(output) > 256):
        rem_bits = len(output) - 256
        ##print('rem_bits: ', rem_bits)
        output = output[rem_bits:]
    

    # convert list output to string
    strOutput = ""
    str_bin = strOutput.join(output)

    return str_bin


def hamming_encode(msg_byte, notskip):
    #HAMMING ENCODER
    #takes in data bits, outputs data bits and parity bits
    #no error detection or correction required
    #even parity

    #input = '11111111'
    if (notskip):
        msg_int = int.from_bytes(msg_byte, byteorder='big')
        msg_bin = bin(msg_int)
        data = msg_bin[2:]

    else:
        data = msg_byte

    data = data[::-1]
    output = list(data)
    #print(int(output[0]))
    ##print(output)

    #calculate how many parity bits are required
    m = len(data)
    r = 0
    count = 0
    while 2**r < m + r + 1:
        r = r + 1
    #insert parity bits in correct positions w value 0
    #print ('numParityencode', r)
    for n in range(0, r):
        output.insert((2**n) - 1, str(0))

    #calculate parity bit values
    for i in range(r):
        ##print('i:', i)
        parity = 2 ** i  # 2^0, 2^1, 2^2, ...
        pos = parity - 1
        sum = 0
        start = pos
        dataBits = []

        while start < len(output):
            cluster = 0

            while (cluster < parity and start + cluster < len(output)):
                ##print(int(output[start + cluster]))
                sum = sum + int(output[start + cluster])
                dataBits.append(start + cluster)
                cluster = cluster + 1

            start = start + 2 * parity

        ##print('sum:', sum)
        #if odd parity
        if sum % 2 == 1:
            output[(2**i) - 1] = str(1)

    ##print(output)

    
    #convert list to string
    if (notskip==0):
        count = output.count('1')
        output.append(str(count%2))
    out = "".join(output)
    #flip back to correct way
    out = out [::-1]
    ##print('after: ', out, len(out))

    return out