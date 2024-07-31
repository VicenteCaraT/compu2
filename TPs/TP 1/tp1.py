import argparse
from PIL import Image, ImageFilter
import multiprocessing
import io

def load_and_split_image(image_path, num_splits, overlap=10):
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
                box = (
                    max(j * new_width - overlap, 0),
                    max(i * new_height - overlap, 0),
                    min((j + 1) * new_width + overlap, width),
                    min((i + 1) * new_height + overlap, height)
                )
                parts.append((img.crop(box), box))
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
    part_size = 1024 * 1024 
    shared_array = multiprocessing.Array('c', num_parts * part_size)

    processes = []
    pipes = []
    lock = multiprocessing.Lock()

    for i in range(num_parts):
        parent_pipe, child_pipe = multiprocessing.Pipe()
        pipes.append(parent_pipe)

        process = multiprocessing.Process(
            target=process_image_parts,
            args=(image_parts[i][0], filter_type, child_pipe, lock, shared_array, i, part_size)
        )
        processes.append(process)
        process.start()
        child_pipe.close()

    for parent_pipe in pipes:
        parent_pipe.recv()

    for process in processes:
        process.join()

    for parent_pipe in pipes:
        parent_pipe.close()

    filtered_parts = [
        (Image.open(io.BytesIO(bytes(shared_array[i * part_size: (i + 1) * part_size]))), image_parts[i][1])
        for i in range(num_parts)
    ]

    return filtered_parts

def process_image_parts(image_part, filter_type, pipe_conn, lock, shared_array, index, part_size):
    lock.acquire()
    try:
        filtered_part = apply_filter(image_part, filter_type)
        part_bytes = io.BytesIO()
        filtered_part.save(part_bytes, format='PNG')
        part_data = part_bytes.getvalue()
        
        if len(part_data) < part_size:
            part_data += b'\x00' * (part_size - len(part_data))

        start_idx = index * part_size
        end_idx = start_idx + part_size
        shared_array[start_idx:end_idx] = part_data

        pipe_conn.send(f"Part {index} saved to shared memory")
    finally:
        lock.release()
    pipe_conn.close()

def signal_handler():
    pass

def combine_image(filtered_parts, image_size, grid_size, overlap=10):
    width, height = image_size
    rows, cols = grid_size
    new_image = Image.new('RGB', (width, height))

    for idx, (part, box) in enumerate(filtered_parts):
        row = idx // cols
        col = idx % cols
        crop_box = (
            overlap if col > 0 else 0,
            overlap if row > 0 else 0,
            part.width - (overlap if col < cols - 1 else 0),
            part.height - (overlap if row < rows - 1 else 0)
        )
        part = part.crop(crop_box)
        new_image.paste(part, (box[0] + crop_box[0], box[1] + crop_box[1]))

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