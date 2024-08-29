import socket
import multiprocessing
import signal
import sys
#cerrar socket activo en el padre y cerrar los socket pasivo en el hijo

def handle_client(client_socket):
    with client_socket:
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received from client: {data.decode()}")
                
                # Enviar una respuesta automática
                response = f"Server received: {data.decode()}"
                client_socket.sendall(response.encode())
                
            except Exception as e:
                print(f"Error: {e}")
                break
        print("Connection closed")
    sys.exit(0)

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr}")
        process = multiprocessing.Process(target=handle_client, args=(client_socket,))
        process.start()

def signal_handler(sig, frame):
    print('Server shutting down.')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    start_server("0.0.0.0", 9999)
