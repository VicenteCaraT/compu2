# Practical Assignment No. 2: Image Processing with AsyncServer (HTTP) and SocketServer + Multiprocessing

## Requirements
`Pillow`

`aiohttp`

Make sure to install requirements.txt:
```bash
pip3 install -r requirements.txt
```

## Overview

This application demonstrates an image processing system using an asynchronous HTTP server (Server A) and a Socket server (Server B) with multiprocessing capabilities. It allows users to upload images for processing, applying a specified scale factor, and then retrieve the results using unique task identifiers.

## How the Application Works

1. **Server A** (AsyncServer) receives image processing requests via HTTP and scale factor.
2. Each image is sent to **Server B** using a socket connection.
3. **Server B** processes the image using multiprocessing.
4. The processed image is returned to Server A
5. Users can check the status of their image processing task using the unique task ID provided upon upload.

## Usage Instructions

### Display Help

To view available options and usage instructions, run:

```bash
python3 main.py -h
```

### Configuring Server A (IP Address and Port)

You can change the IP address and port for Server A using the following flags:

- `-i` to specify the IP address (IPv4/IPv6)
- `-p` to specify the port

#### Examples

**Using IPv4**:

```bash
python3 main.py -i 127.0.0.1 -p 5454
```

**Using IPv6**:

```bash
python3 main.py -i ::1 -p 5454
```

### Image Processing Request

To process an image, use a `POST` request to upload the image along with the desired scale factor:

```bash
curl -X POST http://[::1]:5454/upload -F "image=@<image_path>" -F "scale_factor=<scale_factor=(e.g., 0.1 or 0.5)>"
```

- Replace `<image_path>` with the path to the image you want to process.
- Replace `<scale_factor>` with the desired scale factor (e.g., `0.1` for 10% of the original size).

### Checking Task Status

After submitting an image for processing, you will receive a unique `task_id`. To check the status of your image processing task, use the following `GET` request:

```bash
curl -X GET http://[::1]:5454/status/<task_id>
```

- Replace `<task_id>` with the ID provided when the image was submitted.
