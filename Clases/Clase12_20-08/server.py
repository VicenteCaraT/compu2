#!/usr/bin/python3
import socket, os, sys

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
#host = socket.gethostname()
host = ""
#port = int(sys.argv[1])
port = 50001

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

while True:
    serversocket.close()
    # establish a connection
    clientsocket, addr = serversocket.accept()

    print("Conexión desde %s" % str(addr))

    msg = b"Gracias por conectar \r\n"
    clientsocket.send(msg)
    child_pid = os.fork()
    if not child_pid:
        while True:
            msg = clientsocket.recv(1024)
            print(f"Recibido: {msg.decode()} de {addr} desde {os.getpid()}")
            msg = b"Ok \r\n"
            clientsocket.send(msg)
            
        clientsocket.close()
    clientsocket.close()