import argparse
from PIL import Image, ImageFilter
import multiprocessing
import io

def load_and_split_image(image_path, num_splits):
    img = Image.open(image_path)
    width, height = img.size
    parts = []
    if num_splits > 1:
        rows = int(num_splits ** 0.5)
        cols = num_splits // rows
        new_width = width // cols
        new_height = height // rows
        for i in range(rows):
            for j in range(cols):
                box = (j * new_width, i * new_height, (j + 1) * new_width, (i + 1) * new_height)
                parts.append(img.crop(box))
    return parts, img.size, (rows, cols)

def apply_filter(image_part, filter_type):
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
    num_parts = len(image_parts)
    processes = []
    pipes = []
    lock = multiprocessing.Lock()
    
    for i in range(num_parts):
        parent_pipe, child_pipe = multiprocessing.Pipe()
        pipes.append(parent_pipe)
        
        process = multiprocessing.Process(
            target=process_image_parts,
            args=(image_parts[i], filter_type, child_pipe, lock)
        )
        processes.append(process)
        process.start()
        child_pipe.close()
        
    filtered_parts = []
    for parent_pipe in pipes:
        filtered_part = parent_pipe.recv()
        filtered_parts.append(filtered_part)
    
    for process in processes:
        process.join()
    
    for parent_pipe in pipes:
        parent_pipe.close()
    return filtered_parts

def process_image_parts(image_part, filter_type, pipe_conn, lock):
    lock.acquire()
    try:
        filtered_part = apply_filter(image_part, filter_type)      
        pipe_conn.send(filtered_part)
    finally:
        lock.release()
    pipe_conn.close()
    
def signal_handler():
    pass


def combine_image(filtered_parts, image_size, grid_size):
    width, height = image_size
    rows, cols = grid_size
    num_parts = len(filtered_parts)

    #estimar el tamaño máximo de los datos de la imagen serializada
    max_part_size = 0
    part_bytes_list = []

    for part in filtered_parts:
        part_bytes = io.BytesIO()
        part.save(part_bytes, format='PNG')
        part_data = part_bytes.getvalue()
        part_bytes_list.append(part_data)
        if len(part_data) > max_part_size:
            max_part_size = len(part_data)

    #crear el array compartido con el tamaño máximo estimado
    shared_array = multiprocessing.Array('c', num_parts * max_part_size)

    #serializar las partes de la imagen y guardarlas en la memoria compartida
    for idx, part_data in enumerate(part_bytes_list):
        if len(part_data) < max_part_size:
            part_data += b'\x00' * (max_part_size - len(part_data))
        shared_array[idx * max_part_size:(idx + 1) * max_part_size] = part_data
        print(f"Part {idx} saved to shared memory")

    #deserializar las partes de la imagen desde la memoria compartida
    parts = []
    for i in range(num_parts):
        part_data = bytes(shared_array[i * max_part_size:(i + 1) * max_part_size])
        part_img = Image.open(io.BytesIO(part_data))
        parts.append(part_img)

    #combinar las partes en una imagen completa
    new_image = Image.new('RGB', (width, height))
    part_width = width // cols
    part_height = height // rows

    for idx, part in enumerate(parts):
        row = idx // cols
        col = idx % cols
        new_image.paste(part, (col * part_width, row * part_height))

    new_image.show()
    return new_image


if __name__ == "__main__":
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
    
    image_parts, image_size, grid_size = load_and_split_image(args.image_path, num_splits)
    
    filtered_parts = process_image(image_parts, args.filter)
    
    combined_image = combine_image(filtered_parts, image_size, grid_size)