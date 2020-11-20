import socket
import select
import json
import struct
from type_conversions import *
from rsa import *
from hamming import *

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
        # order in ascending order of totals
        self.sample.sort(key= lambda Student:Student.total, reverse=False)




        # change marks for all students w/ m in name:
        for student in self.sample:
            if "m" in student.get_name(): 
                student.change_marks()
                student.print()
        # stu = self.sample[0]
        # stu.change_marks()
        

    def print(self):
        
        for student in self.sample:
            student.print()

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
            for n in str(stu.name, 'utf-8'):
                msg_byte[i] = n
                i += 1
            msg_byte[i] = stu.t1
            i += 1
            msg_byte[i] = stu.t2
            i += 1
            msg_byte[i] = stu.t3
            i += 1
            msg_byte[i] = stu.t4
            i += 1
            msg_byte[i] = stu.mark_total
            i += 1
            print(msg_byte)

        return msg_byte

class Student:
    def __init__(self, name, t1, t2, t3, t4, mark_total):
        self.name= str(name)
        self.t1 = int(t1)
        self.t2 = int(t2)
        self.t3 = int(t3)
        self.t4 = int(t4)
        self.total = int(mark_total) 
    
    def get_name(self):
        return str(self.name)

    def as_dict(self):
        return {
            "name": self.name,
            "t1": self.t1,
            "t2": self.t2,
            "t3": self.t3,
            "t4": self.t4,
            "mark_total": self.total
        }

    
    def change_marks(self, new_total):
        print("name change:")
        self.total = new_total
        # weighted distribution of new marks between 4 tasks

        # max 25
        self.t1 = self.t1*int(0.25*new_total)
        # max 15
        self.t2 = self.t2*int(0.15*new_total)
        # max 10
        self.t4 = self.t4*int(0.1*new_total)
        # max 50
        self.t3 = new_total = self.t1 - self.t2 - self.t4



    def string(self):
        ret = bytes(self.name) + bytes(self.t1) + bytes(self.t2) \
                + bytes(self.t3) + bytes(self.t4) + bytes(self.t3)
        return ret
    
    def print(self):
        print("name:", str(self.name), end = ' ')
        print("t1:", self.t1, end = ' ')
        print("t2:", self.t2, end = ' ')
        print("t3:", self.t3, end = ' ')
        print("t4:", self.t4, end = ' ')
        print("total:", self.total)
        



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
        # return full message as byte string
        return self.header + self.content

    def set_content(self, content_bytes):
        self.content = content_bytes
        '''
        input: hex_string of content bytes
        '''
        # update content part of message