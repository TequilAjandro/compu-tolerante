import os
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

class Process:

    def __init__(self, id, init, life):
        self._id = id
        self._init = init
        self._death = life
        self._age = self._init
        self._life = np.arange(init, life)
        self._color = self.random_color()
        print(self._color)

    def run(self):
        if self._death > self._age:
            self._age += 1

    def random_color(self):
        color = np.random.randint(1, 255, size=3)
        color = [hex(x).replace('0x', '') for x in color]
        return '#' + ''.join(color)
         

class Graph:

    def __init__(self):
        pass

def draw_bar(i):
    # ax.clear()
    for p in processes:
        if i >= p._init:
            ax.barh(p._id, p._age, color=p._color, left=p._init)
            p.run()
    plt.box(False)

if __name__ == '__main__':
    long_lived = 0
    processes = list()
    clear = lambda: os.system('cls')

    while True:
        opc = input('1.- Agregar proceso\n2.- Correr procesos\n3.- Salir\n\nElija: ')
        if opc == '1':
            life = int(input())
            death = int(input())
            processes.append(Process(len(processes), life, death))
            
            if death > long_lived:
                long_lived = death

        elif opc == '2':
            # drawed = []
            fig, ax = plt.subplots()
            ax.get_yaxis().set_visible(False)
            plt.xlim(0, long_lived)
            plt.ylabel(ylabel='')
            for i in range(long_lived):
                animator = animation.FuncAnimation(fig, draw_bar)
                # for p in processes:
                #     if i >= p._init:
                #         ax.barh(p._id, p._age, color=p._color)
                #         plt.pause(0.1)
                #         p.run()
                # fig.canvas.draw()
            plt.show()
            processes.clear()
        elif opc == '3':
            break
        else:
            print('Todo meco el vato, pinche baboso')



    # fig, ax = plt.subplots()
    # p = Process(0, 5, 16)
    # p1 = Process(1, 10, 36)
    # print(p._life)
    # # y = np.arange(5, 15)
    # ax.barh(p._id, p._life, color = p._color, left=p._init)
    # ax.barh(p1._id, p1._life, color = p1._color, left=p1._init)
    # plt.xlim(0, 69)
    # plt.show()

# label y: Proceso
# label x: Tiempo - Ciclos - Frecuencia