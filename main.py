import threading
import activeMQ

sklearn_nome='sklearn'

class Program(threading.Thread):

    def __init__(self,fila):
        threading.Thread.__init__(self)
        self.fila = fila

    def run(self):
        activeMQ.ActiveMQ(self.fila).listener()

sklearn = Program(sklearn_nome)
sklearn.start()
sklearn.join()