import math
import socket
import select
import json
import struct
from type_conversions import *


def get_data_from_db(host, port, N, e, d):
    

    content = str(N) + "," + str(e)
    print('content: ', content)
    # HTTP request headers
    request = 'GET / HTTP/1.1\r\nHost: ' + host + '\r\nContent-Length: ' + str(len(content)) + '\r\n\r\n' + content
    request_bytes =  bytes(request, 'utf-8') 
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print ("Socket successfully created")
    except socket.error as err: 
        print ("socket creation failed with error %s" %(err))
    
    
    s.connect((host, port))
    s.send (request_bytes)
    
    ready = select.select([s], [], [], 10)
    if ready[0]:
        recieved = s.recv(64000)
    #print(bytearray(data)) 

    s.close

    return HTTP_message(recieved)
    

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


    data = input[::-1]          #flip data 
    #data = input
    output = list(data)
    errorDetect = []
    #lookup = []

    for i in range(numParity):
        #print('i:', i)
        parity = 2 ** i  # 2^0, 2^1, 2^2, ...
        pos = parity - 1
        Sum = 0
        start = pos
        dataBits = []

        while start < len(data):
            cluster = 0
            #print("start: ", start)

            while (cluster < parity and start + cluster < len(data)):
                Sum = Sum + int(data[start + cluster])
                dataBits.append(start + cluster)
                cluster = cluster + 1

                


            start = start + 2 * parity
            #print('cluster: ', cluster)

        errorDetect.append(Sum % 2)
        #lookup.append(dataBits)

    p = 0
    oddPar = []
    for x in errorDetect:
        if x == 1:
            oddPar.append(2**p)
            #print('index: ', 2**p)
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
    #print("ouptut before rem: ", "".join(output), len(output))

    if (len(output) > 256):
        rem_bits = len(output) - 256
        #print('rem_bits: ', rem_bits)
        output = output[rem_bits:]
    

    # convert list output to string
    strOutput = ""
    str_bin = strOutput.join(output)

    return str_bin

def decrypt_rsa(cipher_bytes, n, d):
    '''
    Decrypt with RSA
    Input cipher (Byte String e.g. b'\xa9z\xb7\xf3\') - payload to decrypt as a text string, n(String), d(String)
    Output plaintext (String e.g 'Hello')
    '''
    cipher_int = int.from_bytes(cipher_bytes, byteorder='big') # convert cipher to integer form
    #print('dec_cipher_int: ', cipher_int)
    #print('dec_cipher_byt: ', cipher_bytes)
    plaintext_int = pow(cipher_int, int(d), int(n))
    plaintext_bytes = int_to_bytes(plaintext_int)
    return plaintext_bytes

def create_db(msg_bytes):
    db = Database()
    n_entries = msg_bytes[0]
    len_student_bytes = 10 # bytes taken up by each students information
    n = 0
    while n < n_entries:
        start = n*10 + 1
        # print(response[i]) 
        # first byte is number of students
        name = (msg_bytes[start:(start + 5)])
        t1 = msg_bytes[start+5]
        t2 = msg_bytes[start+6]
        t3 = msg_bytes[start+7]
        t4 = msg_bytes[start+8]
        total = msg_bytes[start+9]
        db.add_student(Student(name, t1, t2, t3, t4, total))
        print('name:', name, end = ' ')
        print('t1: ',  t1, end = ' ')
        print('t2: ', t2, end = ' ')
        print('t3: ', t3, end = ' ')
        print('t4: ', t4, end = ' ')
        print('total: ', total)
        # next five bytes form name

        n += 1

        
    return db


def hamming_encode(msg_byte):
    #HAMMING ENCODER
    #takes in data bits, outputs data bits and parity bits
    #no error detection or correction required
    #even parity

    #input = '11111111'

    msg_int = int.from_bytes(msg_byte, byteorder='big')
    msg_bin = bin(msg_int)

    data = msg_bin[2:]

    data = data[::-1]
    output = list(data)
    print(int(output[0]))
    #print(output)

    #calculate how many parity bits are required
    m = len(msg_bin)
    r = 0
    while 2**r < m + r + 1:
        r = r + 1

    #insert parity bits in correct positions w value 0

    for n in range(0, r):
        output.insert((2**n) - 1, str(0))

    #calculate parity bit values
    for i in range(r):
        #print('i:', i)
        parity = 2 ** i  # 2^0, 2^1, 2^2, ...
        pos = parity - 1
        sum = 0
        start = pos
        dataBits = []

        while start < len(output):
            cluster = 0

            while (cluster < parity and start + cluster < len(output)):
                #print(int(output[start + cluster]))
                sum = sum + int(output[start + cluster])
                dataBits.append(start + cluster)
                cluster = cluster + 1

            start = start + 2 * parity

        #print('sum:', sum)
        #if odd parity
        if sum % 2 == 1:
            output[(2**i) - 1] = str(1)

    #print(output)

    #convert list to string
    strOutput = ""
    out = strOutput.join(output)

    #flip back to correct way
    out = out [::-1]
    #print('after: ', out, len(out))

    return out

def encrypt_rsa(msg_int, n, e):
    '''
    Encrypt with RSA 
    Input plaintext (String e.g 'Hello') - payload to encrypt as a text string, n(String), e(String)
    Output cipher_bytes (String e.g  b'\xa9z\xb7\xf3\')
    '''
    cipher_int = pow(msg_int, int(e), int(n))
    cipher_bytes = int_to_bytes(cipher_int)
    return cipher_bytes

'''
CLASS DEFINITIONS
'''
class Database:
    def __init__(self):
        self.n_entries = 0
        self.sample = list()

    def add_student(self, student):
        self.sample.append(student)
        self.n_entries += 1

    def as_dict(self):
        student_dict = list()
        for student in self.sample:
            student_dict.append(student.as_dict())

        return {
            "n_entries": self.n_entries,
            "sample": student_dict,
        }

    def change_marks(self):
        stu = self.sample[0]
        stu.change_marks()

    def json(self):
        return json.dumps(self.as_dict())

    def get_bytes(self):
        size = 10*self.n_entries + 1
        msg_byte = bytearray(size)
        i = 0
        msg_byte[i] =  self.n_entries
        i += 1
        #msg_str = msg
        print(msg_byte)

        for stu in self.sample:
            for n in stu.student_name:
                msg_byte[i] = n
                i += 1
            msg_byte[i] = stu.mark_task1
            i += 1
            msg_byte[i] = stu.mark_task2
            i += 1
            msg_byte[i] = stu.mark_task3
            i += 1
            msg_byte[i] = stu.mark_task4
            i += 1
            msg_byte[i] = stu.mark_total
            i += 1
            print(msg_byte)

        return msg_byte

class Student:
    def __init__(self, name, mark_task1, mark_task2, mark_task3, mark_task4, mark_total):
        self.student_name= name
        self.mark_task1 = mark_task1
        self.mark_task2 = mark_task2
        self.mark_task3 = mark_task3
        self.mark_task4 = mark_task4
        self.mark_total = mark_total 

    def as_dict(self):
        return {
            "student_name": self.student_name,
            "mark_task1": self.mark_task1,
            "mark_task2": self.mark_task2,
            "mark_task3": self.mark_task3,
            "mark_task4": self.mark_task4,
            "mark_total": self.mark_total
        }
    def change_marks(self):
        self.mark_total = 90

    def string(self):
        ret = bytes(self.student_name) + bytes(self.mark_task1) + bytes(self.mark_task2) \
                + bytes(self.mark_task3) + bytes(self.mark_task4) + bytes(self.mark_total)
        return ret



''' 
http message class
construct and extract parts of http message
'''
class HTTP_message:
    def __init__(self, message_string):
        response_tokens = message_string.split(b'\r\n\r\n')
        self.header = response_tokens[0] + b'\r\n\r\n'
        #print(b'response header:' + response_header)
        self.content = response_tokens[1]
    
    def get_header(self):
        return self.header
    
    def get_content(self):
        return self.content
    
    def as_string(self):
        # return full message as string
        return self.header + self.content

    def set_content(self, content_bytes):
        self.content = content_bytes
        '''
        input: hex_string of content bytes
        '''
        # update content part of message










