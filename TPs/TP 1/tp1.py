import argparse
from PIL import Image, ImageFilter
import multiprocessing

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
    return parts

def apply_filter(image_part, filter_type):
    if filter_type == "blur":
        return image_part.filter(ImageFilter.BLUR)
    elif filter_type == "contour":
        return image_part.filter(ImageFilter.CONTOUR)
    elif filter_type == "edge":
        return image_part.filter(ImageFilter.EDGE_ENHANCE)
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
        print("Received filtered part from pipe")
    
    for process in processes:
        process.join()
        print("Process joined")
    
    for parent_pipe in pipes:
        parent_pipe.close()
        print("Parent pipe closed")
    
    return filtered_parts

def process_image_parts(image_part, filter_type, pipe_conn, lock):
    lock.acquire()
    try:
        print("Starting filter application")
        filtered_part = apply_filter(image_part, filter_type)
        print("Filter applied")
        
        pipe_conn.send(filtered_part)
        print("Filtered part sent")
    finally:
        lock.release()
        print("Lock released")
    
    pipe_conn.close()
    print("Pipe connection closed")

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
    
    image_parts = load_and_split_image(args.image_path, num_splits)
    
    filtered_parts = process_image(image_parts, args.filter)
    
    for idx, part in enumerate(filtered_parts):
        part.show(f"parte_{idx + 1}_filtrada.jpg")