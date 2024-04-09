import os

# comunicacion bidireccional entre el padre y el hijo
pipe_r_padre, pipe_w_hijo = os.pipe()  # comunicacion del padre al hijo (padre escribe en pipe_w_hijo, hijo lee desde pipe_r_padre)
pipe_r_hijo, pipe_w_padre = os.pipe()  # comunicacion del hijo al padre (hijo escribe en pipe_w_padre, padre lee desde pipe_r_hijo)

pid = os.fork()

if pid > 0:
    os.close(pipe_r_padre)  # cierra lectura del padre
    os.close(pipe_w_padre)  # cierra escritura del padre

    pipe_w_hijo = os.fdopen(pipe_w_hijo, 'w')
    pipe_r_hijo = os.fdopen(pipe_r_hijo)

    msj_del_hijo = pipe_r_hijo.readline().rstrip()
    print('Padre recibe:', msj_del_hijo)

    respuesta_padre = "Hola Hijo"
    print('Padre responde:', respuesta_padre)
    pipe_w_hijo.write(respuesta_padre)
    pipe_w_hijo.close()
    pipe_r_hijo.close()

else:
    os.close(pipe_w_hijo)
    os.close(pipe_r_hijo)

    pipe_w_padre = os.fdopen(pipe_w_padre, 'w')
    pipe_r_padre = os.fdopen(pipe_r_padre)

    msj_al_padre = "Hola Padre"
    pipe_w_padre.write(msj_al_padre)
    pipe_w_padre.close()

    respuesta_del_padre = pipe_r_padre.readline().rstrip()
    print('Hijo recibe respuesta del padre:', respuesta_del_padre)

    pipe_r_padre.close()