import sys
import socket
import random
import time

HOST = "localhost"
PORT = 8124
radar_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
radar_serv.connect((HOST, PORT))


x = 0
for x in range(0,100000):
    i=str(random.randint(1,100))
    radar_serv.sendto(i, (HOST,PORT))
    print i
    time.sleep(0.1)
radar_serv.close()
