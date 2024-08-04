# Practical Assignment No. 1: Parallel Image Processing

## How the Application Works
- The application enables the parallel processing of images by applying various filters. To function correctly, all parameters must be passed as arguments in the command line.

## Usage of the Application
```bash
python3 tp1.py <image_path> -d <number_of_divisions (optional)> -f <filter_type>
```

## Arguments
- `<image_path>`: The path to the image that you want to process.
- `-d <number_of_divisions>`: (Optional) Specifies how many parts the image will be divided into for parallel processing. If not specified, the image will be divided based on the number of cores available on your processor.
- `-f <filter_type>`: Specifies the type of filter to be applied to the image. Available filters:
    - `blur`
    - `contour`
    - `edge`
    - `emboss`

## Example of Usage
```bash
python3 tp1.py test_img2.jpg -d 10 -f emboss
```

## Required Libraries
- Pillow
```bash
pip3 install pillow
```
## Author: Vicente Cara Tapia
