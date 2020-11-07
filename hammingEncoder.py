#HAMMING ENCODER
#takes in data bits, outputs data bits and parity bits
#no error detection or correction required
#even parity

input = '11111111'

data = input[::-1]
output = list(data)
#print(output)

#calculate how many parity bits are required
m = len(data)
r = 0
while 2**r < m + r + 1:
    r = r + 1

#insert parity bits in correct positions w value 0
for n in range(0, r):
    output.insert((2**n) - 1, str(0))
print(output)

#calculate parity bit values
for i in range(r):
    print('i:', i)
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
            #print(output[start+cluster])
            print(start+cluster)

            cluster = cluster + 1

        start = start + 2 * parity

    print('sum:', sum)
    #if odd parity
    if sum % 2 == 1:
        output[(2**i) - 1] = str(1)

#print(output)

#convert list to string
strOutput = ""
out = strOutput.join(output)

#flip back to correct way
out = out [::-1]
print(out)