import argparse
from PIL import Image, ImageFilter
import multiprocessing
import io
import time
import signal

def load_and_split_image(image_path, num_splits, overlap=10):
    """Carga una imágen y la divide en partes iguales según el número de divisiones especificadas por argumento

    Args:
        image_path (str): ruta de la imagen
        num_splits (int): Numero de divisiónes que se aplicarán a la imagen
        overlap (int): Solapamiento entre partes adyacentes (ya que sino se ven las líneas de división en la imágen final). Defaults to 10 pixeles.

    Returns:
        parts (list): Una lista de tuplas que contiene la imágen recortada
        img.size (tuple): Una tupla que contiene el alto y el ancho de la imágen original
    """
    img = Image.open(image_path)
    width, height = img.size
    parts = []
    if width > height:  #dividir verticalmente si la imagen es más ancha
        new_width = width // num_splits
        for i in range(num_splits):
            box = (
                max(i * new_width - overlap, 0),
                0,
                min((i + 1) * new_width + overlap, width),
                height
            )
            parts.append((img.crop(box), box))
    else:  #dividir horizontalmente si la imagen es más alta
        new_height = height // num_splits
        for i in range(num_splits):
            box = (
                0,
                max(i * new_height - overlap, 0),
                width,
                min((i + 1) * new_height + overlap, height)
            )
            parts.append((img.crop(box), box))

    return parts, img.size

def apply_filter(image_part, filter_type):
    """Aplica el filtro especificado por argumento

    Args:
        image_part (Image): Parte de la imágen a la cual se le va a aplicar el filtro
        filter_type (str): Tipo de filtro a aplicar

    Returns:
        image: La parte de la imágen con el filtro aplicado, si no se especifica ninguan filtro se devuelve sin filtro
    """
    if filter_type == "blur":
        return image_part.filter(ImageFilter.BLUR)
    elif filter_type == "contour":
        return image_part.filter(ImageFilter.CONTOUR)
    elif filter_type == "edge":
        return image_part.filter(ImageFilter.EDGE_ENHANCE)
    elif filter_type == "emboss":
        return image_part.filter(ImageFilter.EMBOSS)
    else:
        return image_part

def process_image(image_parts, filter_type):
    """Procesa las partes de una imagen en paralelo
    
    Args:
        image_parts (list/tuple): Lista de tuplas donde cada tuple contiene los datos de una parte de la imagen (bytes)
        filter_type (str): Tipo de filtro a aplicar a cada parte de la imagen

    Returns:
        filtered_parts: Lista de tuplas donde estan contenidas las partes de la imagen ya procesadas
    """
    #se calcula el tamaño total de la memoria compartida en base al tamaño de las imagenes (ancho*alto*canales)
    _, _, part_width, part_height = image_parts[0][1]  #desempaqueta los valores que necesitas
    part_size = part_width * part_height * 3  #3 canales RGB
    shared_array = multiprocessing.Array('c', len(image_parts) * part_size) #creación de la memoria compartida
    processes = [] #lista para almacenar los procesos creados
    pipes = [] #lista para almacenar los pipes de comunicación entre procesos
    lock = multiprocessing.Lock() #lock para la sincronización entre procesos
    
    #se itera por cada parte de la imagen
    for i in range(len(image_parts)):
        parent_pipe, child_pipe = multiprocessing.Pipe() # se crean los pipes de comunicación para cada proceso
        pipes.append(parent_pipe) #se almacenan los pipes creados en una lista
        #se crean los procesos para procesar las partes de la imagen
        process = multiprocessing.Process(
            target=process_image_parts, #función objetivo que realiza cada proceso
            args=(image_parts[i][0], filter_type, child_pipe, lock, shared_array, i, part_size)
        )
        processes.append(process) #se almacena el proceso en la lista
        process.start() #se inician los procesos
        child_pipe.close() #se cierra el extremo del pipe en el proceso hijo
    #espera a que todos los procesos terminen
    for parent_pipe in pipes:
        parent_pipe.recv() #se recibe el mensaje de que la parte fue guardada en la memoria

    for process in processes:
        process.join() #se terminan los procesos

    for parent_pipe in pipes:
        parent_pipe.close() #se cierran todos los pipes del padre
    #reconstruye las partes procesadas a partir del array compartido
    filtered_parts = [
        (Image.open(io.BytesIO(bytes(shared_array[i * part_size: (i + 1) * part_size]))), image_parts[i][1])
        for i in range(len(image_parts))
    ]
    return filtered_parts #devuelve la lista de partes procesadas

def process_image_parts(image_part, filter_type, pipe_conn, lock, shared_array, index, part_size):
    """
    Procesa una parte de la imagen aplicando un filtro y guarda el resultado en memoria compartida.

    Args:
        image_part (bytes): Parte de la imagen en formato de bytes a procesar
        filter_type (str): Tipo de filtro a aplicar a la imagen
        pipe_conn (multiprocessing.PipeConnection): Conexión de pipe para enviar mensajes al proceso principal
        lock (multiprocessing.Lock): Lock para asegurar la sincronización 
        shared_array (multiprocessing.Array): Array compartido en memoria para almacenar las partes procesadas
        index (int): Índice de la parte de la imagen en la lista de partes
        part_size (int): Tamaño en bytes de cada parte de la imagen

    """
    try:
        lock.acquire() #se adquiere el lock
        try:
            filtered_part = apply_filter(image_part, filter_type) #se le aplica el filtro a la parte
            part_bytes = io.BytesIO() #se crea un objeto BytesIO para almacenar la imagen filtrada
            filtered_part.save(part_bytes, format='PNG') #guarda la imagen filtrada en el objeto con formato png
            part_data = part_bytes.getvalue() #se obtienen los datos de la imagen filtrada como bytes
            
            #asegurar que la longitud de part_data sea igual a part_size rellenando con bytes nulos si es necesario
            if len(part_data) < part_size:
                part_data += b'\x00' * (part_size - len(part_data))
        
            #se calcula el índice de inicio y fin para almacenar la parte en el array compartido
            start_idx = index * part_size
            end_idx = start_idx + part_size
            shared_array[start_idx:end_idx] = part_data #se almacena la parte procesada en la memoria compartida

            pipe_conn.send(f"Part {index} saved")
        finally:
            lock.release() #se libera el locka para el siguiente proceso
    except KeyboardInterrupt:
        pass #silencia los logs de error de los procesos hijos
    finally:
        pipe_conn.close() #se cierra la comunicación

def signal_handler(s, f):
    raise KeyboardInterrupt

def combine_image(filtered_parts, image_size, overlap=10):
    """
    Combina partes filtradas de una imagen en una imagen completa, ajustando el solapamiento entre partes.

    Args:
        filtered_parts (list/tuple): Lista de tuplas donde cada tupla contiene una parte filtrada 
        image_size (tuple): Tamaño de la imagen final en píxeles (ancho, alto).
        overlap (int): Cantidad de solapamiento en píxeles entre las partes de la imagen. Default es 10.

    Returns:
        Image: Imagen combinada final
    """
    width, height = image_size #se obtienen las dimemsiones de la imagen final
    new_image = Image.new('RGB', (width, height)) #se crea una nueva imagen con las dimenciones en blanco
    for part, box in filtered_parts:
        #ajustar el tamaño del área de recorte para eliminar el solapamiento
        crop_box = (
            overlap if box[0] > 0 else 0, 
            overlap if box[1] > 0 else 0, 
            part.width - (overlap if box[2] < width else 0),  
            part.height - (overlap if box[3] < height else 0) 
        )
        part = part.crop(crop_box) #se recortar la parte de la imagen según la caja de recorte
        #calcular la posición donde se pegará la parte recortada
        paste_position = (box[0] + crop_box[0], box[1] + crop_box[1])
        new_image.paste(part, paste_position) #se pega la parte en la posicion calculada
    new_image.show() #muestra la imagen
    return new_image #devuelve la imagen combinada

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    parser = argparse.ArgumentParser(description="Procesamiento paralelo de imágenes")
    parser.add_argument("image_path", type=str, help="Ruta de la imagen")
    parser.add_argument("-d", "--division", type=int, help="Número de divisiones para dividir la imagen (activa la división)")
    parser.add_argument("-f", "--filter", type=str, help="Aplica el tipo de filtro ingresado")
    args = parser.parse_args()
    
    if args.division:
        num_splits = args.division
    else:
        num_cores = multiprocessing.cpu_count()
        num_splits = num_cores
    
    try:
        image_parts, image_size = load_and_split_image(args.image_path, num_splits)
        filtered_parts = process_image(image_parts, args.filter)
        combined_image = combine_image(filtered_parts, image_size)
        combined_image.save("imagen_procesada.png")
    except KeyboardInterrupt:
        print("\nProceso interrumpido por el usuario. Terminando procesos...")
        time.sleep(2)
        
        
if __name__ == "__main__":
    main()
