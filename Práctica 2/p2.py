import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import tkinter as tk

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
        self._fig, self._ax = plt.subplots()
        plt.box(False)
        self._ax.get_yaxis().set_visible(False)
        plt.ylabel(ylabel='')

    def draw_bar(self, i):
        for p in processes:
            if i >= p._init:
                self._ax.barh(p._id, p._age, color=p._color, capstyle='round', left=p._init)
                p.run()
        plt.pause(0.05)

    def animate(self, long_lived, processes):
        plt.xlim(0, long_lived, 1)
        for i in range(long_lived):
            animator = animation.FuncAnimation(self._fig, self.draw_bar)
        plt.show()

class ProcessWindow:

    def __init__(self, processes):
        self._root = tk.Tk()
        self._root.geometry(('850x850'))
        self._processes = processes
        print(self._processes)
        self._root.mainloop()


class SetupWindow:

    def __init__(self):
        self._root = tk.Tk()

        self._input_frame = None
        self._confirmation_frame = None

        self._init_labels = []
        self._init_text_inputs = []
        self._duration_labels = []
        self._duration_text_inputs = []
        self._add_buttons = []

        self._count_row = 1

        self._run_button = None

        self.setup_window()
        self._root.mainloop()

    def setup_window(self):
        # Se definen aspectos de la ventana
        self._root.geometry(('380x400'))
        self._root.resizable(width=False, height=False)
        self._root.title('Administrador de procesos')
        # Creación de frames
        self._input_frame = tk.Frame(self._root, background="#F0F0F0", relief="flat")
        self._confirmation_frame = tk.Frame(self._root, background="#F0F0F0", relief="flat")
        # Se define la posición de los frames
        self._input_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=0)
        self._confirmation_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=0)
        # Definimos la estructura de la ventana principal: Filas y columna
        self._root.grid_rowconfigure(0, weight=12)
        self._root.grid_rowconfigure(1, weight=1)
        self._root.grid_columnconfigure(0, weight=4)
        # 
        self.setup_process_row()


    def setup_process_row(self):
        tk.Label(self._input_frame, text='Añadir procesos', font='Helvetica 14 bold', 
                pady=10).pack(side='top')
        self.define_process_widget()
        self.define_process_pos(x_pos=20, y_pos=50, x_button=330, y_button=45)
        self._run_button = tk.Button(self._confirmation_frame, text='Comenzar', width=200,
                                    height=3, font='20',command=self.run_processes)
        self._run_button.pack(side='bottom')


    def define_process_widget(self):
        # 
        self._init_labels.append(tk.Label(self._input_frame, text='Inicio', font='15'))
        self._init_text_inputs.append(tk.Entry(self._input_frame, width=9))
        self._duration_labels.append(tk.Label(self._input_frame, text='Duración', font='15'))
        self._duration_text_inputs.append(tk.Entry(self._input_frame, width=9))
        # 
        self._add_buttons.append(tk.Button(self._input_frame, text='+', command=self.add_process_row))

    def define_process_pos(self, x_pos, y_pos, x_button, y_button):
        self._init_labels[-1].place(x=x_pos, y=y_pos)
        self._init_text_inputs[-1].place(x=x_pos+50, y=y_pos)
        self._duration_labels[-1].place(x=x_pos+140, y=y_pos)
        self._duration_text_inputs[-1].place(x=x_pos+220, y=y_pos)
        self._add_buttons[-1].place(x=x_button, y=y_button)

    # 
    def add_process_row(self):
        if self._count_row < 8:
            x, y = self.get_row_position()
            self.define_process_widget()
            self.define_process_pos(x_pos=x, y_pos=y+33, x_button=330, y_button=y+30)
            self._count_row += 1
        else:
            tk.messagebox.showerror(title='Error', message='Limite de procesos alcanzado')

    # 
    def get_row_position(self):
        return self._init_labels[-1].winfo_x(), self._init_labels[-1].winfo_y()

    # 
    def run_processes(self):
        while True:
            if self.verify_all_field():
                processes = zip(self._init_text_inputs, self._duration_text_inputs)
                processes = [(int(init.get()), int(duration.get())) for init, duration in processes ]
                # print(items)
                # ordenarlos
                # mandarlos junto con la cantidad de filas usadas
                # crear nueva ventana
                p = ProcessWindow(processes)



    def is_valid(self):
        state = True
        for i, init in enumerate(self._init_text_inputs):
            try:
                state, error, field, no = self.verify_field(init, 'Inicio', i+1)
                return state, error, field, no
            except:
                state = self.verify_field(init, 'Inicio', i+1)
            
        for i, duration in enumerate(self._duration_text_inputs):
            try:
                state, error, field, no = self.verify_field(duration, 'Duración', i+1)
                return state, error, field, no
            except:
                state = self.verify_field(duration, 'Duración', i+1)
        return state
    
    # 
    def has_nulls(self, field):
        return len(field.get()) == 0

    def is_string(self, field):
        try:
            int(field.get())
            return False
        except: 
            return True

    def is_valid_number(self, init, duration, i):
        if int(init.get()) <= 0 or int(duration.get()) <= 1:
            return False, 'El inicio o la duración tienen que ser mayores a su valor actual', i
        if int(init.get()) >= int(duration.get()):
            return False, 'El inicio no puede ser mayor o igual a la duración', i
        return True

    def verify_field(self, field, name, i):
        if self.has_nulls(field):
            return False, 'está vacio', name, i
        if self.is_string(field):
            return False, 'tiene strings', name, i
        return True
    
    def verify_all_field(self):
        state = True
        try:
            state, error, field, no = self.is_valid()
            tk.messagebox.showerror(title='Error', message='Campo de '+ 
                                    field + ' número ' + str(no) + ' ' + error)
            return False
        except:
            state = self.is_valid()
            return True

        if state:
            for i, (init, duration) in enumerate(zip(self._init_text_inputs, self._duration_text_inputs)):
                try:
                    state, error, no = self.is_valid_number(init, duration, i+1)
                    tk.messagebox.showerror(title='Error', message='Linea '+ ' número ' 
                                            + str(no) + ': ' + error)
                    return False
                except:
                    state = self.is_valid_number(init, duration, i+1)
                    return True

        def clear(self):
            pass

if __name__ == '__main__':
    # long_lived = 0
    processes = list()

    # while True:
    #     opc = input('1.- Agregar proceso\n2.- Correr procesos\n3.- Salir\n\nElija: ')
    #     if opc == '1':
    #         life = int(input())
    #         death = int(input())
    #         processes.append(Process(len(processes), life, death))
            
    #         if death > long_lived:
    #             long_lived = death

    #     elif opc == '2':
    #         graph = Graph()
    #         graph.animate(long_lived, processes)
    #         processes.clear()
    #     elif opc == '3':
    #         break
    #     else:
    #         print('Todo meco el vato, pinche baboso')

    alchl = SetupWindow()