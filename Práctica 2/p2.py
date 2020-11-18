import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

class Process:

    def __init__(self, id, init, life):
        self._id = id
        self._init = init
        self._death = life+1
        self._age = self._init
        self._color = self.random_color()

    def run(self):
        if self._death > self._age:
            self._age += 1

    def random_color(self):
        color = [random.randint(1, 255) for i in range(3) ]
        color = [hex(x) for x in color]
        color = [x.replace('0x', '') if len(x) == 4 else x.replace('x', '') for x in color ]
        return '#' + ''.join(color)
         

class Graph:

    def __init__(self):
        pass

def draw_bar(i):
    for p in processes:
        if i >= p._init:
            ax.barh(p._id, p._age, color=p._color, capstyle='round', left=p._init)
            p.run()
    plt.pause(0.2)
    plt.box(False)

if __name__ == '__main__':
    long_lived = 0
    processes = list()

    while True:
        opc = input('1.- Agregar proceso\n2.- Correr procesos\n3.- Salir\n\nElija: ')
        if opc == '1':
            life = int(input())
            death = int(input())
            processes.append(Process(len(processes), life, death))
            
            if death > long_lived:
                long_lived = death

        elif opc == '2':
            fig, ax = plt.subplots()
            ax.get_yaxis().set_visible(False)
            plt.xlim(0, long_lived, 1)
            plt.ylabel(ylabel='')
            for i in range(long_lived):
                animator = animation.FuncAnimation(fig, draw_bar)
            plt.show()
            processes.clear()
        elif opc == '3':
            break
        else:
            print('Todo meco el vato, pinche baboso')