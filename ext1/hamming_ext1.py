import math
from type_conversions import *


def hamming_decode(input, extraparity):
    '''
    input: binary string of 1s and 0s
    output: binary string of 1s and 0s - with parity bits removed
    '''

    # input = '011100101110'         #test input

    # caluclate number of parity bits
    if extraparity:
        #input = bytes_to_bits(input)
        extrabit = int(input[0])
        input = input[1:]
    '''
    else:
        input = bytes_to_bits(input)
        input = input[2:]
    '''
    n = len(input)
    numParity = 0
    while 2 ** numParity < n + 1:
        numParity = numParity + 1
    data = input[::-1]  # flip data
    output = list(data)
    errorDetect = []

    for i in range(numParity):
        parity = 2 ** i  # 2^0, 2^1, 2^2, ...
        pos = parity - 1
        Sum = 0
        start = pos
        dataBits = []

        while start < len(data):
            cluster = 0

            while (cluster < parity and start + cluster < len(data)):
                valueparity = int(data[start + cluster])
                Sum = Sum + valueparity
                if extraparity:
                    if extrabit == 0 & valueparity != 0:
                        return 'resend'
                dataBits.append(start + cluster)
                cluster = cluster + 1

            start = start + 2 * parity

        errorDetect.append(Sum % 2)

    p = 0
    oddPar = []
    for x in errorDetect:
        if x == 1:
            oddPar.append(2 ** p)
        p = p + 1

    index = sum(oddPar)

    print("index:", index)
    print(len(data))
    if index > 0 and data[index - 1] == '1':
        output[index - 1] = str(0)
    elif index > 0:

        output[index - 1] = str(1)

    # remove parity bits
    r = numParity - 1
    while r >= 0:
        par = 2 ** r
        output.pop(par - 1)
        r = r - 1

    output = output[::-1]
    output = [str(x) for x in output]
    # convert list output to string
    strOutput = ""
    str_bin = strOutput.join(output)

    return str_bin


def hamming_encode(msg_byte, extraparity):
    # HAMMING ENCODER
    # takes in data bits, outputs data bits and parity bits
    # no error detection or correction required
    # even parity
    if extraparity:
        data = msg_byte

    else:
        msg_int = int.from_bytes(msg_byte, byteorder='big')
        msg_bin = bin(msg_int)

        data = msg_bin[2:]

    # print("before encoding:", int(data,2), len(data))
    # print("before:", int(data,2))

    data = data[::-1]
    output = list(data)
    #print(output)

    # calculate how many parity bits are required
    m = len(data)
    r = 0
    while 2 ** r < m + r + 1:
        r = r + 1

    # print ("r", r)
    # insert parity bits in correct positions w value 0

    for n in range(0, r):
        output.insert((2 ** n) - 1, str(0))

    # calculate parity bit values
    for i in range(r):
        parity = 2 ** i  # 2^0, 2^1, 2^2, ...
        pos = parity - 1
        sum = 0
        start = pos
        dataBits = []

        while start < len(output):
            cluster = 0

            while (cluster < parity and start + cluster < len(output)):
                sum = sum + int(output[start + cluster])
                dataBits.append(start + cluster)
                cluster = cluster + 1

            start = start + 2 * parity

        # if odd parity
        if sum % 2 == 1:
            output[(2 ** i) - 1] = str(1)

    # convert list to string
    #print(output)
    # strOutput = ""
    # out = strOutput.join(output)

    #out = [str(x) for x in output]
    out = output
    #print(out)

    if extraparity:
        i = 0
        countones = 0
        while (i < len(out)):
            if out[i] == '1':
                countones = countones + 1
            i = i + 1

        if (countones % 2):
            out.append('1')
        else:
            out.append('0')
    #convert list of strings to string
    strOutput = ""
    out = strOutput.join(out)
    # flip back to correct way
    out = out[::-1]
    encoded_bytes = bits_to_bytes(out)

    #encoded_bytes = encoded_bytes[::-1]
    return encoded_bytes