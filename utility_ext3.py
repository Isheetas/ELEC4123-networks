import socket
import select
import json
import struct
from type_conversions import *

import statistics

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
        db.add_name(name)
        db.add_task1(t1)
        db.add_task2(t2)
        db.add_task3(t3)
        db.add_task4(t4)
        db.add_total(total)

        print('name:', name, end = ' ')
        print('t1:',  t1, end = ' ')
        print('t2:', t2, end = ' ')
        print('t3:', t3, end = ' ')
        print('t4:', t4, end = ' ')
        print('total:', total)
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
        self.name = list()
        self.task1 = list()
        self.task2 = list()
        self.task3 = list()
        self.task4 = list()
        self.total = list()

    def add_name(self, name):
        self.name.append(str(name))
        self.n_entries += 1
    def add_task1(self, t1):
        self.task1.append(t1)
    def add_task2(self, t2):
        self.task2.append(t2)
    def add_task3(self, t3):
        self.task3.append(t3)
    def add_task4(self, t4):
        self.task4.append(t4)
    def add_total(self, total):
        self.total.append(total)

    def get_stu(self, i):
        ret = list()
        ret.append(self.name[i])
        ret.append(self.task1[i])
        ret.append(self.task2[i])
        ret.append(self.task3[i])
        ret.append(self.task4[i])
        ret.append(self.total[i])
        return ret


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
        

    def get_marks_to_change(self):
        i = 0

        for stu_name in self.name:
            if "m" in stu_name or "M" in stu_name:
                return i
            i += 1
        return 0


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
        #print(msg_byte)

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
            #print(msg_byte)

        return msg_byte

    def get_stdev(self):
        return statistics.stdev(self.total)
    
    def get_mean(self):
        return statistics.mean(self.total)

    def get_name(self):
        return self.name
    def get_total_marks(self):
        return self.total
    
    def set_total_marks(self, total):
        self.total = total
    
    def get_task1(self):
        return self.task1

    def get_task2(self):
        return self.task2

    def get_task3(self):
        return self.task3
        
    def get_task4(self):
        return self.task4

    def get_closest(self):

        #if the person with m is closest to 90 - than dont swap

        diff = [abs(x-90) for x in self.total]
        index = diff.index(min(diff))
        return index
        



        



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