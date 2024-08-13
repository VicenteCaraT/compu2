# Lado del cliente
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 7373))
#s.send(b'Hola desde cliente')
#s.recv(20)#cantidad de bytes