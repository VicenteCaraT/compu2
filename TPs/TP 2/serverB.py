import socketserver
import struct
from PIL import Image
import io
import socket

class ForkingTCPRequestHandler(socketserver.BaseRequestHandler):
    """Clase para manejar las solicitudes recibidas en el servidor B mediante Forks.
    Esta clase maneja las conexiones TCP entrantes, recibe imágenes desde el cliente,
    las escala y devuelve la imagen procesada.

    Args:
        socketserver (Base): Clase base para manejo de solicitudes
    """
    def handle(self):
        try:
            # Recibir el tamaño de la imagen
            data = self.request.recv(8)
            if not data:
                print("No se recibió el tamaño de la imagen.")
                return
            image_length = struct.unpack('!Q', data)[0]
            image_data = b""

            # Recibir la imagen en fragmentos hasta completarla
            while len(image_data) < image_length:
                packet = self.request.recv(min(4096, image_length - len(image_data)))
                if not packet:
                    break
                image_data += packet

            # Verificar que la imagen tenga datos
            if len(image_data) == 0:
                print("La imagen no se recibió correctamente.")
                return
            print("Imagen recibida correctamente.")

            # Procesar la imagen
            print("Procesando la imagen...")
            try:
                image = Image.open(io.BytesIO(image_data)).convert("L")  # Convertir a escala de grises
            except Exception as e:
                print(f"Error al procesar la imagen: {e}")
                return

            # Recibir el factor de escala
            try:
                scale_factor = self.request.recv(32).decode().strip()
                scale_factor = float(scale_factor)  # Convertir a flotante
            except Exception as e:
                print(f"Error al recibir el factor de escala: {e}")
                return

            # Aplicar el escalado
            print("Aplicando el escalado...")
            new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
            scaled_image = image.resize(new_size)

            # Enviar la imagen procesada en fragmentos
            print("Enviando la imagen procesada de vuelta...")
            output = io.BytesIO()
            scaled_image.save(output, format="JPEG")
            processed_image_data = output.getvalue()

            self.request.sendall(processed_image_data)
            print("Imagen procesada enviada correctamente.")

            self.request.shutdown(socket.SHUT_WR)  # Indicar que ya no se enviarán más datos.
            self.request.close()
        except Exception as e:
            print(f"Error en el procesamiento: {e}")

class ForkingTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    """
    Servidor TCP que crea un nuevo proceso para manejar cada conexión entrante.
    """
    pass

def run_image_scaling_server(ip, port):
    """
    Inicia el servidor B de procesamiento en función de la dirección IP y el puerto.
    """
    with ForkingTCPServer((ip, port), ForkingTCPRequestHandler) as server:
        print(f"Servidor de Procesamiento Funcionando y Escuchando en {ip}:{port}")
        server.serve_forever()
