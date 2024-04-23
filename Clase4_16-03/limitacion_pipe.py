import os

pid = os.fork()

if pid > 0:
    print("padre:", os.getpid())
    input()
    os.wait()

else:
    print("hijo:", os.getpid())
    input()


#la limitacion es que la comunicacion se da entre archivos relacionados(padre-hijo)
#ya que el fork() comparten los file descriptor(fd)
#si se quiere comunicar con otro proceso, con diferentes fd, no se podra comunicar