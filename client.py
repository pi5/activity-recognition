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
    #radar_serv.send(str(random.randint(1,1000)) + "\n")
    #radar_serv.sendall(str(x) + "\n")
    radar_serv.sendto(str(random.randint(1,100)), (HOST,PORT))
    time.sleep(0.01)
radar_serv.close()
