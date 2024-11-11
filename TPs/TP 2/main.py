import argparse
import asyncio
import multiprocessing
import signal
import sys
from aiohttp import web
from serverA import create_app
from serverB import run_image_scaling_server

async def start_server_a(ip, port):
    """
    Inicia el servidor A utilizando aiohttp de forma asincrónica.
    """
    app = create_app()
    print(f"Servidor HTTP(asincrono) Funcionando y Escuchando en {ip}:{port}")
    await web._run_app(app, host=ip, port=port)

def start_server_b():
    """
    Inicia el servidor B utilizando socketserver con una IP y puerto fijos.
    """
    b_ip_address = "127.0.0.1" 
    b_port = 12345 
    run_image_scaling_server(b_ip_address, b_port)

async def main():
    parser = argparse.ArgumentParser(
        description="Tp2 - procesa imágenes",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-i", "--ip", default="127.0.0.1", help="Dirección de escucha para el Servidor A. Acepta (IPv4/IPv6) (por defecto: 127.0.0.1)")
    parser.add_argument("-p", "--port", type=int, default=8888, help="Puerto de escucha para el Servidor A (por defecto: 8888)")
        
    args = parser.parse_args()

    ip_address = args.ip
    port = args.port

    # Iniciar el servidor A de manera asincrónica
    server_a_task = asyncio.create_task(start_server_a(ip_address, port))

    # Iniciar el servidor B en un proceso separado
    server_b_process = multiprocessing.Process(target=start_server_b)
    server_b_process.start()

    try:
        await server_a_task
    except asyncio.CancelledError:
        print("Servidor A cancelado")

    server_b_process.terminate()
    server_b_process.join()

def handle_signal(sig, frame):
    print("\nInterrupción detectada. Cerrando servidores...")
    loop = asyncio.get_running_loop()
    loop.stop() 

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Proceso terminado por el usuario.")
        sys.exit(0)