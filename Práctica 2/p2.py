import os
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Process:

    def __init__(self, id, init, life):
        self._id = id
        self._init = init
        self._death = life
        self._age = self._init
        self._life = np.arange(init, life)
        self._color = np.random.randint(0, 255, size=3)
        # self._color = [hex(x) for x in self._color]
        # print(self._color)

    def run(self):
        if self._death > self._age:
            self._age += 1

class Graph:

    def __init__(self):
        pass

if __name__ == '__main__':
    long_lived = 0
    processes = list()
    clear = lambda: os.system('cls')

    while True:
        opc = input('1.- Agregar proceso\n2.- Correr procesos\n3.-Salir\n\nElija: ')
        if opc == '1':
            life = int(input())
            death = int(input())
            processes.append(Process(len(processes), life, death))
            
            if death > long_lived:
                long_lived = death

        elif opc == '2':
            fig, ax = plt.subplots()
            ax.get_yaxis().set_visible(False)
            for i in range(long_lived):
                plt.cla()
                for p in processes:
                    if i >= p._init:
                        ax.barh(p._id, p._age, color='#4300e7')
                        p.run()
                        plt.ylabel(ylabel='')
                        plt.xlim(0, long_lived)
                        plt.pause(0.1)
                fig.canvas.draw()
            plt.show()
            processes.clear()
        elif opc == '3':
            break
        else:
            print('Todo meco el vato, pinche baboso')

# label y: Proceso
# label x: Tiempo - Ciclos - Frecuencia