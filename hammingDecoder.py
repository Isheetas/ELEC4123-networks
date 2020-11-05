#DYNAMIC HAMMING DECODER
import math
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

    print(out)
    return out