# Trabajo Práctico Nº 1: Procesamiento de Imágenes en Paralelo

## ¿Cómo Funciona la aplicación?
- La aplicación permite el proceso paralelo de imagenes aplicando distintos filtros. Para que la aplicación funciones correctamente, es necesario pasar todos los parámetros medinte argumentos en la línea de comandos. 

## Uso de la Aplicación
```bash
python3 tp1.py <ruta_de_la_imagen> -d <número_de_divisiones (opcional)> -f <tipo_de_filtro>
```

## Argumentos
- `<ruta_de_la_imagen>`: Es la ruta donde se encuentra la imagen a procesar.
- `-d <número_de_divisiones>`: (Opcional) Indica en cuántas partes se dividirá la imagen para su procesamiento en paralelo. Es un argumento opcional, por lo que si no se especifica una división, la imagen se dividirá en función del número de núcleos con los que cuente tu procesador.
- `-f <tipo_de_filtro>`: Se tiene que especificar el tipo de filtro que se aplicará a la imagen. Filtros disponibles:
    - `blur`
    - `contour`
    - `edge`
    - `emboss`

## Ejemplo de uso
```bash
python3 tp1.py test_img2.jpg -d 10 -f emboss
```

## Librerías Necesarias
- Pillow <pip3 install pillow> 