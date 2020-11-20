import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class Process:

    def __init__(self, id, init, life):
        self._id = id
        self._init = init
        self._death = life
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
    
    def list(self):
        return [self._id, self._init, self._death]

class Graph:

    def __init__(self, frame, long_lived, processes):
        self._fig, self._ax = plt.subplots()
        self._canvas = FigureCanvasTkAgg(self._fig, master=frame)
        self._long_lived = long_lived
        self._processes = processes

        self.setup_graph()

    def setup_graph(self):
        plt.box(False)
        self._ax.get_yaxis().set_visible(False)
        plt.ylabel(ylabel='')
        self._canvas.draw()
        self._canvas.get_tk_widget().pack(fill='both', expand=1)
        self._fig.patch.set_facecolor('#F0F0F0')
        self._ax.patch.set_facecolor('#F0F0F0')

    def draw_bar(self, i):
        for p in self._processes:
            if i >= p._init:
                self._ax.barh(p._id, p._age, color=p._color, capstyle='round', left=p._init)
                p.run()
        plt.pause(0.01)

    def animate(self):
        plt.xlim(0, self._long_lived, 1)
        for i in range(self._long_lived):
            animator = animation.FuncAnimation(self._fig, self.draw_bar)
        plt.close(self._fig)
        self._canvas.draw()
        # plt.show()

class ProcessWindow:

    def __init__(self, processes, count_row):
        self._root = tk.Tk()
        self._processes = processes
        self._count_row = count_row
        self._long_lived = 0
        self._y = 0
        self._ordered = None
         
        self._title_frame = None
        self._graph_frame = None
        self._table_frame = None
        self._button_frame = None

        self._title_label = None
        self._back_button = None   

        self.setup_window()
        self.setup_title()
        self.setup_button()

        self.animate()
        self.create_processes_table()
        self.create_ordered_processes_table()
        self.time_label()
        self._root.mainloop()

    def setup_window(self):
        # Se definen aspectos de la ventana
        self._root.geometry(('1420x700'))
        self._root.resizable(width=False, height=False)
        self._root.title('Administrador de procesos')
        # Creación de frames
        self._title_frame = tk.Frame(self._root, background="#F0F0F0", relief="flat")
        self._graph_frame = tk.Frame(self._root, background="#F0F0F0", relief="sunken")
        self._table_frame = tk.Frame(self._root, background="#eeeeee", relief="sunken")
        self._button_frame = tk.Frame(self._table_frame, background="#F0F0F0", relief="flat")
        # Se define la posición de los frames
        self._title_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=0)
        self._graph_frame.grid(row=1, column=1, sticky="nsew", padx=2, pady=0)
        self._table_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=0)
        self._button_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=0)
        # Definimos la estructura de la ventana principal: Filas y columna
        self._root.grid_rowconfigure(0, weight=2)
        self._root.grid_rowconfigure(1, weight=18)
        self._root.grid_columnconfigure(0, weight=6)
        self._root.grid_columnconfigure(1, weight=10)
        self._table_frame.grid_rowconfigure(0, weight=18)
        self._table_frame.grid_rowconfigure(1, weight=1)
        self._table_frame.grid_columnconfigure(0, weight=50)

    def setup_title(self):
        self._title_label = tk.Label(self._title_frame, text='Ejecución de procesos', font='Helvetica 32 bold', 
                pady=10).pack(side='top')

    def setup_button(self):
        self._back_button = tk.Button(self._button_frame, font='Helvetica 32', text='Regresar', command=self.quit)
        self._back_button.pack(fill='both', expand=2)
        
    def quit(self):
        self._root.destroy()

    def create_processes_table(self):
        p_table = None
        header = ['ID', 'Inicio', 'Duración']
        x = 0
        y = 28
        tk.Label(self._table_frame, text='Tabla de procesos', font=('Arial', 15, 'bold')).place(x=x, y=0)
        for j in range(3):
            p_table = tk.Entry(self._table_frame, width=12, fg='black', font=('Arial', 15, 'bold'))
            p_table.grid(row=0, column=j)
            x += 52
            p_table.place(x=x, y=28)
            p_table.insert(tk.END, header[j])
        x=0
        for i in range(1, self._count_row+1):
            y += 28
            for j in range(3):
                p_table = tk.Entry(self._table_frame, width=12, fg='black', font=('Arial', 15))
                p_table.grid(row=i, column=j)
                x += 52
                p_table.place(x=x, y=y)
                p_table.insert(tk.END, self._processes[i-1].list()[j])
            x = 0
        self._y = y

    def create_ordered_processes_table(self):
        self._ordered = self._processes
        self._ordered.sort(key=lambda x: x._init)

        p_table = None
        header = ['ID', 'Inicio', 'Duración']
        x = 0
        y = self._y + 72
        tk.Label(self._table_frame, text='Tabla de procesos en orden de ejecución', font=('Arial', 15, 'bold')).place(x=x, y=y)
        y += 28
        for j in range(3):
            p_table = tk.Entry(self._table_frame, width=12, fg='black', font=('Arial', 15, 'bold'))
            p_table.grid(row=0, column=j)
            x += 52
            p_table.place(x=x, y=y)
            p_table.insert(tk.END, header[j])
        x=0
        for i in range(1, self._count_row+1):
            y += 28
            for j in range(3):
                p_table = tk.Entry(self._table_frame, width=12, fg='black', font=('Arial', 15))
                p_table.grid(row=i, column=j)
                x += 52
                p_table.place(x=x, y=y)
                p_table.insert(tk.END, self._ordered[i-1].list()[j])
            x = 0

        self._y = y

    def time_label(self):
        time_label = None
        longest = self._ordered
        longest.sort(key=lambda x: x._death)
        time_label = tk.Label(self._table_frame, text=str(longest[-1]._death), font=('Arial', 35, 'bold'))
        time_label.place(x=100, y=self._y+80)

    def animate(self):
        for x in self._processes:
            if x[1] > self._long_lived:
                self._long_lived = x[1]
        self._processes = [Process(i, elem[0], elem[1]) for i, elem in enumerate(self._processes) ]
        graph = Graph(self._graph_frame, self._long_lived, self._processes)
        graph.animate()
        self._long_lived = 0

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
                # ordenarlos
                # mandarlos junto con la cantidad de filas usadas
                self.clear()
                p = ProcessWindow(processes, self._count_row)
                del(p)
        self._root.destroy()

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
        for init, duration in zip(self._init_text_inputs, self._duration_text_inputs):
            init.delete(0, 'end')
            duration.delete(0, 'end')


if __name__ == '__main__':
    processes = list()
    window = SetupWindow()