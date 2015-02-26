import math, serial, socket, time

HOST = "localhost"
PORT = 8124
radar_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
radar_serv.connect((HOST, PORT))

arduino = serial.Serial('/dev/cu.usbmodem1411', 115200) # instantiates serial communication

while True:
    while (arduino.inWaiting() == 0): # waits for data
        pass
    
    serialString = arduino.readline() # reads line from serial
    data = serialString.split(',')
    if len(data) != 4:
        pass
    else:
        #print data
        i1 = int(data[0].rstrip()) # casts first element to integer and saves temp value
        q1 = int(data[1].rstrip()) # casts second element to integer and saves temp value
        i2 = int(data[2].rstrip()) # casts first element to integer and saves temp value
        q2 = int(data[3].rstrip()) # casts second element to integer and saves temp value
        
        output = str(i1) + ',' + str(q1) + ',' + str(math.atan2(q1, i1))        
        
        radar_serv.sendto(output, (HOST,PORT)) # writes raw value
        print output        
        time.sleep(0.00001)
    
arduino.close()
radar_serv.close()
