#client for extension task 1
import socket
from hamming_ext1 import *


def main():
    #send request to task3_server
    HOST = '127.0.0.1'
    PORT = 3000
    #host = 'localhost'

    request = 'request'
    request_bytes = bytes(request, 'utf-8')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
    except socket.error as err:
        print("socket creation failed with error %s" % (err))

    s.connect((HOST, PORT))
    s.send(request_bytes)

    data = s.recv(1024)
    data = bytes_to_bits(data)

    n = 8
    splitresponse = [data[i:i + n] for i in range(0, len(data), n)]

    hammingsplit = []
    resendFlag = 0
    for x in splitresponse:
        binDecoded = hamming_decode(x, 1)
        # print("bin_decodd:", x, binDecoded)

        hammingsplit.append(binDecoded)
        if binDecoded == 'resend':
            #print(x)
            #print("NEED TO RESEND")
            resendFlag = 1

    s.close

    #print(hammingsplit)
    if resendFlag == 1:
        request_again = 'resend'
        request_again_bytes = bytes(request_again, 'utf-8')
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket successfully created")
        except socket.error as err:
            print("socket creation failed with error %s" % (err))

        s.connect((HOST, PORT))
        s.send(request_again_bytes)

        data_again = s.recv(1024)
        s.close()
        #print('Received', repr(data_again)) #same data w new noise
        data_again = bytes_to_bits(data_again)
        splitresponse_again_ = [data_again[i:i + n] for i in range(0, len(data_again), n)]
        hammingsplit_again = []
        #assuming won't need to be resent a third time
        for x in splitresponse_again_:
            binDecoded = hamming_decode(x, 1)
            # print("bin_decodd:", x, binDecoded)

            hammingsplit_again.append(binDecoded)

        # print("hamming_decoded 1:", hammingsplit)

        # print("hamming_decoded 2:", hammingsplit_again)


    #compare both received messages
    final = []
    index = 0
    for i in hammingsplit:
        if i == "resend" and hammingsplit_again[index] != "resend":
            final.append(hammingsplit_again[index])
        else:
            final.append(i)
        index +=1

    # print("final:", final)
    
    if "resend" not in final:
        bin = "".join(final)
        print("msg:", bits_to_bytes(bin))
        print_to_ascii(bits_to_bytes(bin))

    else:
        print("resend in both")
    s.close()



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




if __name__ == '__main__':
    main()