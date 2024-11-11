import asyncio
from aiohttp import web
import socket
import uuid
import datetime
import struct

# Diccionario para almacenar las tareas en curso
tasks = {}

async def handle_client(request):
    """
    Maneja la conexión HTTP del cliente: recibe una imagen y un factor de escala,
    y envía estos datos al servidor B para su procesamiento.

    Argumentos:
    - request: Objeto de solicitud HTTP recibido, que contiene los datos de la imagen y el factor de escala.
    
    Retorna:
    - Respuesta HTTP con el ID de la tarea o un error si faltan los datos requeridos.
    """
    try:
        data = await request.post()
        image_file = data.get('image')
        scale_factor = data.get('scale_factor')

        if not image_file or not scale_factor:
            return web.Response(text="Error: Se requiere una imagen y un factor de escala", status=400)

        # Leer la imagen recibida
        image_data = image_file.file.read()
        scale_factor = float(scale_factor)

        # Generar un ID único para la tarea
        task_id = str(uuid.uuid4())

        # Almacenar la tarea como pendiente
        tasks[task_id] = {"status": "pending", "result": None}

        # Procesar la imagen de forma asincrónica
        asyncio.create_task(process_img(task_id, image_data, scale_factor))

        # Devolver el ID de la tarea
        return web.json_response({"task_id": task_id})

    except Exception as e:
        print(f"Error al manejar la solicitud: {str(e)}")
        return web.Response(text=f"Error al manejar la solicitud: {str(e)}", status=500)

import asyncio
import struct
import datetime

async def process_img(task_id, image_data, scale_factor):
    """
    Procesa la imagen conectándose al servidor B para su procesamiento utilizando asyncio streams.

    Argumentos:
    - task_id: ID único de la tarea que se está procesando.
    - image_data: Datos de la imagen que se van a procesar.
    - scale_factor: Factor de escala para ajustar el tamaño de la imagen.

    Actualiza el estado de la tarea en el diccionario `tasks` y guarda la imagen procesada si tiene éxito.
    """
    try:
        # Dirección del servidor B
        server_b_host = "127.0.0.1"
        server_b_port = 12345

        # Conectarse al servidor B utilizando asyncio streams
        reader, writer = await asyncio.open_connection(server_b_host, server_b_port)

        # Enviar el tamaño de la imagen como un entero de 8 bytes
        image_length = len(image_data)
        writer.write(struct.pack('!Q', image_length))
        await writer.drain()

        # Enviar la imagen
        writer.write(image_data)
        await writer.drain()

        # Enviar el factor de escala como texto
        writer.write(str(scale_factor).encode('utf-8'))
        await writer.drain()

        # Recibir la imagen procesada
        processed_image_data = b""
        while True:
            data = await reader.read(4096)
            if not data:
                break
            processed_image_data += data

        # Guardar la imagen procesada
        if processed_image_data:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_image_path = f"imagen_procesada_{timestamp}.jpg"
            with open(output_image_path, "wb") as out_file:
                out_file.write(processed_image_data)

            # Actualizar el estado de la tarea
            tasks[task_id]["status"] = "completed"
            tasks[task_id]["result"] = output_image_path
        else:
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["result"] = "Error al recibir la imagen procesada"

        # Cerrar el escritor
        writer.close()
        await writer.wait_closed()

    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["result"] = f"Error al conectar con el servidor B: {str(e)}"

async def get_task_status(request):
    """
    Devuelve el estado de una tarea.

    Argumentos:
    - request: Objeto de solicitud HTTP que contiene el ID de la tarea.

    Retorna:
    - Respuesta HTTP con el estado de la tarea o un error si la tarea no existe.
    """
    task_id = request.match_info.get('task_id')

    if task_id not in tasks:
        return web.Response(text="Error: No se encontró la tarea", status=404)

    task = tasks[task_id]
    return web.json_response(task)

def create_app():
    """
    Crea y configura la aplicación web usando aiohttp.

    Retorna:
    - La instancia de la aplicación aiohttp configurada.
    """
    app = web.Application()
    app.router.add_post('/upload', handle_client)
    app.router.add_get('/status/{task_id}', get_task_status)
    return app

# if __name__ == '__main__':
#     app = create_app()
#     web.run_app(app, host='0.0.0.0', port=8080)