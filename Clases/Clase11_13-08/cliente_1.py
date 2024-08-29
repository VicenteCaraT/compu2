#!/usr/bin/python3

import socket
import sys

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
#host = socket.gethostname()                           
host = sys.argv[1]

port = int(sys.argv[2])

print("Haciendo el connect")
# connection to hostname on the port.
s.connect((host, port))   
print("Handshake realizado con exito!")

s.send(b'Hola server')
# Receive no more than 1024 bytes
print("Esperando datos desde el server")
msg = s.recv(1024)                                     
#print (msg.decode('ascii'))
print (msg.decode('utf-8'))
s.close()
print("Cerrando conexion")



#python3 cliente_1.py loclahost 7373