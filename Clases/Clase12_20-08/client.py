import socket

server_host = '127.0.0.1' 
server_port = 50001

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((server_host, server_port))

msg = clientsocket.recv(1024)
print("mensaje del servidor:", msg) 

try:
    while True:
        msg_to_send = input("mensaje a servidor: ")
        
        clientsocket.send(msg_to_send.encode('ascii'))
        
        msg = clientsocket.recv(1024)
        print("respuesta del servidor:", msg)

except KeyboardInterrupt:
    print("\nCerrando conexión...")
    clientsocket.close()
