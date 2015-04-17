import os, socket, sys, time

HOST = '192.168.1.122'
PORT = 8888
COLLECTION_TIME = 180
SAMPLES = 1000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

output = open("radar_log.txt", "w")

def client_name(conn, addr):
    name = addr[0][10:13]
    print addr
    if name == '133':
        print 'Connected with Spark1.'
        radar = 1
        if not client_name.r1set:
            client_name.r1set = True
            client_name.count += 1
    elif name == '124':
        print 'Connected with Spark2.'
        radar = 2
        if not client_name.r2set:
            client_name.r2set = True
            client_name.count += 1
    elif name == '107':
        print 'Connected with Spark3.'
        radar = 3
        if not client_name.r3set:
            client_name.r3set = True
            client_name.count += 1
    elif name == '118':
        print 'Connected with Spark4.'
        radar = 4
        if not client_name.r4set:
            client_name.r4set = True
            client_name.count += 1
    return radar, client_name.count

def main():
    clear = lambda: os.system('cls')
    clear()
    
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        print 'Socket bind completed.'
    except socket.error as msg:
        print 'Bind failed: Error Code : ' + str(msg[0]) + ' Message: ' + msg[1]
        sys.exit()
    
    s.listen(10)
    print 'Socket now listening...'
    
    client_name.count = 0
    client_name.r1set = client_name.r2set = client_name.r3set = client_name.r4set = False
    while True:
        conn, addr = s.accept()
        radar, value = client_name(conn, addr)
        if radar == 1:
            conn1 = conn
        elif radar == 2:
            conn2 = conn
        elif radar == 3:
            conn3 = conn
        elif radar == 4:
            conn4 = conn
        if value == 4:
            break
    
    print 'All nodes connected.'
    
    raw_input("Press enter to start:")
    
    print 'Collecting data...'
    
    count = 0
    
    while count < (COLLECTION_TIME * 2 / 5):
        
        conn1.send('A');
        conn2.send('A');
        conn3.send('A');
        conn4.send('A');
        
        count += 1
    
    count = 0
    
    starttime = time.time()
    
    while count < (COLLECTION_TIME * 2 / 5):
        
        # collects data from radar 1
        buff1_1 = bytearray(SAMPLES)
        view1_1 = memoryview(buff1_1)
        conn1.recv_into(view1_1, SAMPLES)
        
        buff1_2 = bytearray(SAMPLES)
        view1_2 = memoryview(buff1_2)
        conn1.recv_into(view1_2, SAMPLES)
        
        # collects data from radar 2
        buff2_1 = bytearray(SAMPLES)
        view2_1 = memoryview(buff2_1)
        conn2.recv_into(view2_1, SAMPLES)
        
        buff2_2 = bytearray(SAMPLES)
        view2_2 = memoryview(buff2_2)
        conn2.recv_into(view2_2, SAMPLES)
        
        # collects data from radar 3
        buff3_1 = bytearray(SAMPLES)
        view3_1 = memoryview(buff3_1)
        conn3.recv_into(view3_1, SAMPLES)
        
        buff3_2 = bytearray(SAMPLES)
        view3_2 = memoryview(buff3_2)
        conn3.recv_into(view3_2, SAMPLES)
        
        # collects data from radar 4
        buff4_1 = bytearray(SAMPLES)
        view4_1 = memoryview(buff4_1)
        conn4.recv_into(view4_1, SAMPLES)
        
        buff4_2 = bytearray(SAMPLES)
        view4_2 = memoryview(buff4_2)
        conn4.recv_into(view4_2, SAMPLES)
        
        stamp = str(int(time.time() * 1000))
        for i in xrange(0, 998, 2):
            print >> output , '%s,"%s,%s,%s,%s,%s,%s,%s,%s"' % (stamp, ((buff1_1[i + 1] << 8) | buff1_1[i]) , ((buff1_2[i + 1] << 8) | buff1_2[i]) , \
                                                                  ((buff2_1[i + 1] << 8) | buff2_1[i]) , ((buff2_2[i + 1] << 8) | buff2_2[i]) , \
                                                                  ((buff3_1[i + 1] << 8) | buff3_1[i]) , ((buff3_2[i + 1] << 8) | buff3_2[i]) , \
                                                                  ((buff4_1[i + 1] << 8) | buff4_1[i]) , ((buff4_2[i + 1] << 8) | buff4_2[i]))
            stamp = int(stamp) + 5
        print >> output

        
        count += 1
        
    print time.time() - starttime
    
    print 'Done.'
    output.close()
    conn1.close()
    conn2.close()
    conn3.close()
    conn4.close()
    s.close()

main()
