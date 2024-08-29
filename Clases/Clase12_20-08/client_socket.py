import socket
import argparse
import signal
import sys

def signal_handler(sig, frame):
    print('Connection terminated by user.')
    sys.exit(0)

def start_client(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")

        while True:
            try:
                message = input("Enter message: ")
                if message.lower() == 'exit':
                    break
                client_socket.sendall(message.encode())
                response = client_socket.recv(1024)
                print(f"Received: {response.decode()}")
            except KeyboardInterrupt:
                print("Client exiting.")
                break

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description="Socket client")
    parser.add_argument("host", type=str, help="The IP address of the server")
    parser.add_argument("port", type=int, help="The port to connect to")
    args = parser.parse_args()

    start_client(args.host, args.port)
