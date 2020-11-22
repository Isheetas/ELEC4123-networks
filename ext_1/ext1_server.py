# create server and client
import socket
import select
from hamming_ext1 import *
from bitstring import BitArray
from type_conversions import *

def main():
    #CREATE SERVER
    HOST = '127.0.0.1'
    PORT = 3000
    HOST_server = '149.171.36.192'
    PORT_d = 12000
    PORT_n = 12002

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((HOST, PORT))
    s.listen(5)
    
    while True:
        conn, addr = s.accept()
        print(f"Connection from {addr} has been established.")

        clientmsg = str(conn.recv(1024))
        clientmsg = clientmsg[2:len(clientmsg)-1]

        print("cli msg:", clientmsg)

        if (clientmsg == "request"):
            #CONNECT TO DATA SERVER
            content = '4,3'
            request_bytes =  bytes(content, 'utf-8')

            try:
                s_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print ("Socket successfully created to data server")
            except socket.error as err:
                print ("socket creation failed with error %s to data server" %(err))

            s_data.connect((HOST_server, PORT_d))
            s_data.send (request_bytes)

            s_data.send (request_bytes)
            ready = select.select([s_data], [], [], 10)
            if ready[0]:
                response = s_data.recv(64000)

            s_data.close()

            #convert data into bits
            #response = b'\x01Kevin\x0c\t\x14\x05.'
            data = bytes_to_bits(response)
            print("response from data server: ", response)


            # split data bits into blocks of 4 so it can be encoded
            n = 4
            splitresponse = [data[i:i + n] for i in range(0, len(data), n)]
            print("splitresponse:", splitresponse)

            hammingsplit = []
            for x in splitresponse:
                hammingsplit.append(hamming_encode(x, 1))

            #print(type(hammingsplit[0]))
            #print("hamming_split:", hammingsplit)

            hamming_bin = "".join(hammingsplit)
            #print("hamming_bin:", hamming_bin)

            encoded = bits_to_bytes(hamming_bin)  # b'': separator


            #CONNECT TO NOISE SERVER
            try:
                s_noise = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print ("Socket successfully created to noise server")
            except socket.error as err:
                print ("socket creation failed with error %s to noise server" %(err))

            s_noise.connect((HOST_server, PORT_n))
            s_noise.send (encoded)

            ready_noise = select.select([s_noise], [], [], 10)
            if ready_noise[0]:
                noiseResponse = s_noise.recv(64000)

            s_noise.close()

            print("noiseResponse:", bytes_to_bits(noiseResponse))

            #send noisy payload to client
            conn.sendall(noiseResponse)
        elif clientmsg == "resend":
            print("IN RESEND")
            #send encoded through noise server
            print("response:", response)
            try:
                s_noise = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("Socket successfully created to noise server")
            except socket.error as err:
                print("socket creation failed with error %s to noise server" % (err))

            s_noise.connect((HOST_server, PORT_n))
            s_noise.send(encoded)

            ready_noise = select.select([s_noise], [], [], 10)
            if ready_noise[0]:
                noiseResponse = s_noise.recv(64000)

            #send noisy signal to client
            conn.sendall(noiseResponse)
            s_noise.close()


        



        

        # RESEND CODE: LISTEN FOR "resend" CLIENT MESSAGE RERUN encoded THROUGH NOISE SERVER
        #print("")
        #s.listen(1)
        #conn, addr = s.accept()
        #print(f"Connection from {addr} has been established.")
        #clientmsg = conn.recv(1024)
        #print(clientmsg)
        #if clientmsg == b'resend':
            

if __name__ == '__main__':
    main()

