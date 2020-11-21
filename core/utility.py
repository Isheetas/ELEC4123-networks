
import socket
import select
import json
import struct
from type_conversions import *
from rsa import *
from hamming import *

def get_data_from_db(host, port, N, e, d):
    

    content = str(N) + "," + str(e)
    #print('content: ', content)
    # HTTP request headers
    request = 'GET / HTTP/1.1\r\nHost: ' + host + '\r\nContent-Length: ' + str(len(content)) + '\r\n\r\n' + content
    request_bytes =  bytes(request, 'utf-8') 
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print ("Socket successfully created to demo db")
    except socket.error as err: 
        print ("socket creation failed with error %s" %(err))
    
    
    s.connect((host, port))
    s.send (request_bytes)
    
    ready = select.select([s], [], [], 10)
    if ready[0]:
        recieved = s.recv(64000)
    #print(bytearray(data)) 

    s.close


    return split_http_message(recieved)


def split_http_message(message_bytes):
    '''
    split header & content bytes
    return as dict w/ 'header': header bytestring 'content': content bytestring
    '''
    msg_tokens = message_bytes.split(b'\r\n\r\n')
    header = msg_tokens[0] + b'\r\n\r\n'
        #print(b'response header:' + response_header)
    content = msg_tokens[1]
    return {'header': header, 'content': content}


def set_key(size):

    tup_128 = (252837207378338387332619197259204540353,65537,48393883292703003300067554859838128129)
    tup_256 = (63148583107154283585608284940392418734726981382069355868003882013090711003369,65537,51783437651169347215431900289402465246791119526563008636281618633074802696377)
    tup_512 = (8970390971863115293607640428673687999254972927235154691542229862779928818191497867276608223970519838284414340107378134391857351696176024011425314547707437,65537,2691514229682718145986246568952490971777008218886309746471251476596495417130742890415399202072710693207354976533556735077478241083226230682882713819251905)
    tup_1024 = (119484048255701441436361811740544499805482989972762171328000832460793482937842746490520045389267019914879180293493128527411951756175646012207372245640392613181330180655929701724130504407998065166504932760922418859359543355490102783596328490356612554010085829097705629454807851698735754870179265036374094717849,65537,98169554028663195074268552344192732906999665503049451108954221656222986744450928903192736378388878867457838199542716308146908681554447642908863140933908360961506320097008245680412967700092994045241465985522036307059609765358467340869704010033821712100383554558800942218221868532481354259885666372749501435361)
    tup_2048 = (22946363129994826577290485132048269530367907435865564505398980418770939980335605558922215490228827703369553743626870315255204846515969276672521953249260400066138871749246384596075747255554938943120569769420923823686164862968767839306248417957032703462245871947555296177875829693435733439160109407765234856561636468093388251400122393226115460553654948341945632248422505234342191276574649191089998930866384791495629609740703256945567786500796606036156932805990473521378549032729928164863421133267054266084277047689600401729486564350762792635097639715603761556993068515886895509613259566547005980540352656342746261262537,65537,252792684740776428411488628795014275919337613389305851242779862708891445531567011208047966552408770646090266611205889308547200805415716583877212112943314598589381042814835736734465866892147426902864814891159299337800189680080723560417952572821118023402681226576360282594966950557099036316459261436754634731889905201747103851611449210570319678170771358908293749523108746287938161045351335725021400509975663317393973710483203568059596657971449782305265385988995877764594815999847585302822520276427822531443733852892804878775517133081958601862663391675487488874170650718742484619889643980014838982209372664534895730689)

    if size == 128:
        N = tup_128[0]
        e = tup_128[1]
        d = tup_128[2]
    elif size == 256:
        N = tup_256[0]
        e = tup_256[1]
        d = tup_256[2]
    elif size == 512:
        N = tup_512[0]
        e = tup_512[1]
        d = tup_512[2]
    elif size == 1024:
        N = tup_1024[0]
        e = tup_1024[1]
        d = tup_1024[2]
    else:
        N = tup_2048[0]
        e = tup_2048[1]
        d = tup_2048[2]
    
    return N, e, d

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
        # change marks for all students w/ m in name:
        for student in self.sample:
            if "m" in student.get_name(): student.change_marks(90)
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
        #print(msg_byte)

        for stu in self.sample:
            #print(bytes(stu.name, 'utf-8'))
            for n in bytes(stu.name, 'utf-8'):        
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
            msg_byte[i] = stu.total
            
            i += 1
            #print(msg_byte)


        return msg_byte

class Student:
    def __init__(self, name, t1, t2, t3, t4, mark_total):
        self.name= str(name, 'utf-8')
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
        self.total = new_total
        # weighted distribution of new marks between 4 tasks

        # max 25
        self.t1 = int(0.25*new_total)
        # max 15
        self.t2 = int(0.15*new_total)
        # max 10
        self.t4 = int(0.1*new_total)
        # max 50
        self.t3 = int(new_total - self.t1 - self.t2 - self.t4)



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
        










