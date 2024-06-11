import argparse
from PIL import Image, ImageFilter
import multiprocessing
import os, sys, signal

def load_and_split_image(image_path, num_splits):
    image = Image.open(image_path)
    width, height = image.size
    
    image_parts = []

    if width >= height:
        split_width = width // num_splits
        for i in range(num_splits):
            left = i * split_width
            right = (i + 1) * split_width if (i + 1) * split_width <= width else width
            part = image.crop((left, 0, right, height))
            image_parts.append(part)
    else:
        split_height = height // num_splits
        for i in range(num_splits):
            upper = i * split_height
            lower = (i + 1) * split_height if (i + 1) * split_height <= height else height
            part = image.crop((0, upper, width, lower))
            image_parts.append(part)
    
    return image_parts

def apply_filter(image_part, filter_type):
    if filter_type == "blur":
        return image_part.filter(ImageFilter.BLUR)
    elif filter_type == "contour":
        return image_part.filter(ImageFilter.CONTOUR)
    elif filter_type == "edge":
        return image_part.filter(ImageFilter.EDGE_ENHANCE)
    else:
        return image_part

#crear función que cree los procesos y le aplique filtro a cada imagen

#crear función que maneje la señal de interrupción


    
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
    
    for idx, part in enumerate(image_parts):
        filtered_part = apply_filter(part, args.filter)
        filtered_part.show(f"parte_{idx + 1}_filtrada.jpg")