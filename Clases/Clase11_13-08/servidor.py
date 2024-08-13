# Lado del servidor
# ó nc -lt 127.0.0.1 7373

import socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((socket.gethostname(), 7373))
serversocket.listen(5)

(clientsocket, address) = serversocket.accept()
clientsocket.recv(1024)