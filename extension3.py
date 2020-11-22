'''
Dummy file to get samples 
'''
from utility_ext3 import *
import socket
import select
import math

'''
scores = rand ([1,10]);
mina = 0;
maxa = 100;
scores = round(mina+(maxa-mina).*scores);
scores
meanorig = mean (scores);
stdorig = std (scores);

%change 1st score to 90
differ = abs(90-scores);
[M,I] = min(differ);
buff = scores(1);
scores(1) = scores (I);
scores(I) = buff;

diff = 90-scores(1);
scores(1) = 90;
distance = scores(1)-diff-meanorig;
obtainmark = round(meanorig-distance);
difff = abs(scores-obtainmark);
[M,index] = min(difff);
scores(index) = scores(index)+diff;
scores
stdorig-std(scores)
'''

def closest(lst, k):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))] 

def main():
 
    # 1. Send well-formed HTTP requests
    HOST = '149.171.36.192'
    PORT = 12000
    content = '4,10'
 
    # HTTP request headers
    #request = 'GET / HTTP/1.1\r\nHost: ' + HOST + '\r\nContent-Length: ' + str(len(content)) + '\r\n\r\n' + content
    request_bytes =  bytes(content, 'utf-8') 
    print(content)

    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print ("Socket successfully created")
    except socket.error as err: 
        print ("socket creation failed with error %s" %(err))

    s.connect((HOST, PORT))
    s.send (request_bytes)
    
    ready = select.select([s], [], [], 10)
    if ready[0]:
        response = s.recv(64000)

    print(response)



    db = create_db(response)

    marks = db.get_total_marks()
    print("before marks:", marks)


    std_orig = db.get_stdev()
    print("bef std:", std_orig)
    mean_orig = db.get_mean()
    print("bef mean:", mean_orig)

    print("name:", db.get_name())

    to_change = db.get_marks_to_change()            #index of marks that need to be changed
    print("to_change:", to_change)

    swap_i = db.get_closest()
    print("swap_i:", swap_i)
    
    buff = marks[to_change]
    if swap_i is not to_change:
        print("swap and to change not same")
        marks[to_change] = marks[swap_i]
        
        marks[swap_i] = buff
        diff = 90-marks[to_change]
        
        marks[to_change] = 90
    else:
        marks[to_change] = 90


    #ADJUST TASK MARKS
    diff_after_change = marks[to_change] - buff
    single = round(diff_after_change//4)
    rem = diff_after_change - 4*single
    print("round,rem", round,rem)
    tup = [db.task1[to_change], db.task2[to_change], db.task3[to_change], db.task4[to_change]]
    max_i = tup.index(max(tup))
    min_i = tup.index(min(tup))
    if tup[max_i] + single < 100:
        db.task1[to_change] += single
        db.task2[to_change] += single
        db.task3[to_change] += single
        db.task4[to_change] += single + rem
    
    print("changed:", db.get_stu(to_change))
    



    



    distance = marks[to_change] - diff - mean_orig
    obtainmark = round(mean_orig - distance)
    diff2 = [abs(x - obtainmark) for x in marks]

    i = diff2.index(min(diff2))
    marks[i] = marks[i] + diff


    print("after marks:", marks)
    db.set_total_marks(marks)

    std_orig = db.get_stdev()
    print("after std:", std_orig)
    mean_orig = db.get_mean()
    print("after mean:", mean_orig)






    #print('after: ', db.json())

    db.print()

    '''
    modify code
    '''

    '''
    send it back
    '''

if __name__ == '__main__':
    main()