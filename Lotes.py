#Del Ángel Mercado Jorge Rafael
#Martínez Ríos Evelyn Yanet

import math
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

n_procesos = 0       #Variables que se utilizan mucho
simbolo_ope=0
contador_procesos=1
procesos = []

def asignar_lotes():    #Función para asignar los procesos a cada lote
    global n_batches, batches
    batches = []
    n_batches = math.ceil(n_procesos / 5)
    for i in range(1, n_batches + 1):
        batch = []
        for j in range((i - 1) * 5 + 1, len(procesos) + 1):
            batch.append(procesos[j - 1])
            if (j % 5 == 0): break
        batches.append(batch)

#Validar números y tambien puse límite de numeros
def validar_entero(P):
    if P.isdigit() or P == "":
        return len(P) <= 5
    else:
        return False

#Es la función que indica que se hace cuando se le pican a las teclas de los operadores
#Actualiza la ventana y tambien actualiza la variable que guarda un numero del 1 al 5 dependiendo la operacion
def on_click(valor):
    global simbolo_ope
    simbolo_ope = valor
    simbolos = ["", "+", "-", "x", "/", "%"]
    signo_label.configure(text=simbolos[valor])

def operacion(num_1, num_2, signo): #Función para determinar la operación a calcular
    signos = ["+", "-", "*", "/", "%"]
    return f"{num_1} {signos[signo - 1]} {num_2}"

#Ventana 1 - Clases
class NumeroProcesos(ctk.CTk):  #Ventana para determinar el número de procesos
    def __init__(self):
        super().__init__()    
        self.resizable(False, False)     #Configuración de la ventana
        self.title("Número de procesos")
        self.geometry("330x210")
        #Etiqueta de número de procesos
        label1 = ctk.CTkLabel(self, text="Número de procesos", padx=10, pady=10, font=("Arial", 16, "bold"))
        label1.pack(pady=10)
        validacion = self.register(validar_entero)
        #Entrada al usuario para el número de procesos
        self.entrada_variable = tk.StringVar()
        entrada = ctk.CTkEntry(self, textvariable=self.entrada_variable, validate="key", validatecommand=(validacion, "%P"), font=("Arial", 16), justify="center")
        entrada.pack(pady=20, padx=20)
        #Botón para aceptar el número ingresado
        aceptar_boton = ctk.CTkButton(self, text="Aceptar", command=self.validar_valor, font=("Arial", 14, "bold"))
        aceptar_boton.pack(pady=10)
    def validar_valor(self): #Validar en n de procesos ingresados
        global n_procesos
        if self.entrada_variable.get() == "" or self.entrada_variable.get() == "0":   #Si no es válido, lanzamos una advertencia al usuario
            messagebox.showwarning("Advertencia", "El número de procesos debe ser mayor a 0") 
        else: #Si es correcto, pasamos a la siguiente ventana
            n_procesos = int(self.entrada_variable.get())
            messagebox.showinfo("¡Felicidades!", "Número de procesos asignado correctamente.")
            self.destroy()

#Ventana 2 - Insertar los procesos
class Operacion(ctk.CTkFrame): 
    def __init__(self, master, validacion, **kwargs):
        super().__init__(master, **kwargs)
        self.validacion_num = validacion
        self.insertar_numeros()
        self.botones_operacion()
    #Insertas los números que quieres usar, ya validados
    def insertar_numeros(self):
        frame = tk.Frame(self.master, bg=self.master["bg"])
        frame.pack(pady=10, padx=10)

        # Número 1
        global num1_var
        num1_var = tk.StringVar()
        num1 = ctk.CTkEntry(frame, textvariable=num1_var, validate="key", validatecommand=(self.validacion_num, "%P"), font=("Arial", 16), justify="center")
        num1.pack(side=tk.LEFT, padx=5)  

        #Signo de operación
        global signo_label
        signo_label = ctk.CTkLabel(frame, text=" ", font=("Arial", 16, "bold"))
        signo_label.pack(side=tk.LEFT, padx=5)

        # Número 2
        global num2_var
        num2_var = tk.StringVar()
        num2 = ctk.CTkEntry(frame, textvariable=num2_var, validate="key", validatecommand=(self.validacion_num, "%P"), font=("Arial", 16), justify="center")
        num2.pack(side=tk.LEFT, padx=5)  

    #Función que llama a on_click cada vez que se presione un botón de símbolo 
    def comando(self, valor):
        return lambda: on_click(valor)

    #Botones de operacion
    def botones_operacion(self):
        global simbolo_ope
        simbolo_ope = 0
        button_frame = ctk.CTkFrame(self.master)
        button_frame.pack(pady=10)
        simbolos = ["+", "-", "x", "/", "%"]
        for i in range(1, 6):
            boton = ctk.CTkButton(button_frame, text=simbolos[i-1], command=self.comando(i), width=40, font=("Arial", 14, "bold"))
            boton.pack(side="left", padx=5)

#Formato de la ventana 2, donde se piden los datos de cada proceso
class IngresarProcesos(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ingresar Procesos")
        self.geometry("400x530")
        self.resizable(False, False)

        frame_rest = ctk.CTkFrame(master=self, width=200, height=200)
        frame_rest.pack(padx=20, pady=25)
        label_rest = ctk.CTkLabel(frame_rest, text="   Procesos Restantes:", padx=0, pady=10, font=("Arial", 12, "bold"))
        label_rest.grid(row=0, column = 0, padx = 5, pady = 0)
        self.num_rest = ctk.CTkLabel(frame_rest, text=f"{n_procesos} ", padx=10, pady=10, font=("Arial", 12, "bold"))
        self.num_rest.grid(row=0, column = 1, padx = 0, pady = 0, sticky="w")
        
        # Insertar nombre
        label_nom = ctk.CTkLabel(self, text="Nombre: ", padx=10, pady=0, font=("Arial", 16, "bold"))
        label_nom.pack(pady=5)
        self.nombre_variable = tk.StringVar()
        validar_caracter = self.register(self.validar_caracteres)
        nombre = ctk.CTkEntry(self, textvariable=self.nombre_variable, validate="key", validatecommand=(validar_caracter, "%P"), font=("Arial", 16), justify="center")
        nombre.pack(pady=0, padx=0)

        #Insertar ID
        label_id = ctk.CTkLabel(self, text="ID: ", padx=10, pady=10, font=("Arial", 16, "bold"))
        label_id.pack(pady=5)
        self.id_variable = tk.StringVar()
        validacion_num = self.register(validar_entero)
        id = ctk.CTkEntry(self, textvariable=self.id_variable, validate="key", validatecommand=(validacion_num, "%P"), font=("Arial", 16), justify="center")
        id.pack(pady=0, padx=0)

        #Insertar Operación 
        label_id = ctk.CTkLabel(self, text="Operación: ", padx=10, pady=10, font=("Arial", 16, "bold"))
        label_id.pack(pady=5)

        self.operacion = Operacion(master=self, validacion=validacion_num)

        #Insertar TME
        label_TME = ctk.CTkLabel(self, text="TME: ", padx=10, pady=0, font=("Arial", 16, "bold"))
        label_TME.pack(pady=5)
        self.TME_variable = tk.StringVar()
        TME = ctk.CTkEntry(self, textvariable=self.TME_variable, validate="key", validatecommand=(validacion_num, "%P"), font=("Arial", 16), justify="center")
        TME.pack(pady=0, padx=0)

        aceptar_boton = ctk.CTkButton(self, text="Aceptar", command=self.mostrar_valor, font=("Arial", 14, "bold"))
        aceptar_boton.pack(pady=25)

    #Verificar que el id no es duplicado
    def id_duplicado(self, id_nuevo):
        for proceso in procesos:
            if proceso["id"] == id_nuevo:
                return True
        return False

    #Verificar que la división no sea entre cero
    def div_cero(self, num2_division):
        if num2_division == 0 and (simbolo_ope == 4 or simbolo_ope == 5):
            return True
        return False

    #Validar que el nombre no sea mayor que 12 caracteres
    def validar_caracteres(self, new_value):
        return len(new_value) <= 12
        
    #Tiempo mayor que 0    
    def validar_tiempo(self, tiempo):
        if tiempo == 0:
            return True
        return False
        
    # Guarda los valores en un diccionario, aparece advertencia si un campo está vacío o si no se cumple con una condición
    def mostrar_valor(self):
        global contador_procesos, procesos

        if not self.nombre_variable.get() or not self.id_variable.get() or not num1_var.get() or not num2_var.get() or not self.TME_variable.get() or simbolo_ope==0 :
            messagebox.showwarning("Advertencia", "Por favor, rellena todos los campos.")
        elif self.id_duplicado(self.id_variable.get()):
            messagebox.showwarning("Advertencia", "El ID ya existe. Por favor, ingresa un ID diferente.")
        elif self.div_cero(int(num2_var.get())):
            messagebox.showwarning("Advertencia", "No se puede dividir entre 0. Por favor, ingresa un número válido")
        elif self.validar_tiempo(int(self.TME_variable.get())):
            messagebox.showwarning("Advertencia", "El tiempo tiene que ser mayor que 0. Por favor, ingresa un número válido")
        else:
            procesos.append( {
            "nombre": self.nombre_variable.get(),
            "id": self.id_variable.get(),
            "num_1": int(num1_var.get()),
            "num_2": int(num2_var.get()),
            "signo": simbolo_ope,
            "tme": int(self.TME_variable.get())
            })
            self.num_rest.configure(text=f"{n_procesos-contador_procesos}")
            #Pone los campos en blanco para hacer otra captura
            self.nombre_variable.set("")
            self.id_variable.set("")
            self.TME_variable.set("")
            num2_var.set("")
            num1_var.set("")
            on_click(0)
            contador_procesos += 1
            if contador_procesos > n_procesos:
                messagebox.showinfo("Registro completo", "¡Los procesos han sido registrados correctamente!")
                self.destroy()

#Ventana 3 - Ejecución de procesos y lotes
class Lotes(ctk.CTkFrame):
    def __init__(self, master, num_lotes_pend, **kwargs):
        super().__init__(master, **kwargs)

        self.num_lotes_pend = num_lotes_pend  #Número de lotes pendientes
        #Etiqueta para los lotes pendientes
        label_1 = ctk.CTkLabel(self, text="No. Lotes Pendientes:  ", padx=5, pady=5, font=("Arial", 16, "bold"))
        label_1.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.num_lotes = ctk.CTkLabel(self, text=str(self.num_lotes_pend), padx=5, pady=5, font=("Arial", 16, "bold"))
        self.num_lotes.grid(row=0, column=1, padx=10, pady=5)

    def lote_completado(self): #Función para alterar el número de lotes pendientes
        self.num_lotes_pend -= 1
        self.num_lotes.configure(text=f"{self.num_lotes_pend}")

class Procesos_Pendientes(ctk.CTkFrame): #Tabla de procesos del lote actual pendientes
    def __init__(self, master, lote_inicial, **kwargs):
        super().__init__(master, **kwargs)
        self.contador = master.contador       #Variables a considerar en la tabla de procesos
        self.lotes_pendientes = master.lote
        self.lote_actual = 1
        self.lote_procesar = lote_inicial
        self.num_pros_pend = len(lote_inicial)
        self.row_count = 2
        self.labels_procesos = []
        #Etiquetas para los procesos pendientes
        label_1 = ctk.CTkLabel(self, text="Procesos Pendientes \n del lote actual: ", padx=5, pady=5, font=("Arial", 14, "bold"))
        label_1.grid(row=0, column=0, padx=10, pady=5)
        self.num_pros = ctk.CTkLabel(self, text=str(self.num_pros_pend), padx=5, pady=5, font=("Arial", 14, "bold"), justify="center")
        self.num_pros.grid(row=0, column=1, padx=10, pady=5)

        label_nom = ctk.CTkLabel(self, text="Nombre:", padx=5, pady=5, font=("Arial", 12, "bold"))
        label_nom.grid(row=1, column=0, padx=10, pady=5)
        label_tme = ctk.CTkLabel(self, text="TME:", padx=5, pady=5, font=("Arial", 12, "bold"))
        label_tme.grid(row=1, column=1, padx=5, pady=5)
        #Ciclo para crear la tabla de procesos pendientes de manera automática
        for proceso in self.lote_procesar:  
            label_nom = ctk.CTkLabel(self, text=f"{proceso['nombre']}", font=("Arial", 14))
            label_nom.grid(row=self.row_count, column = 0, padx = 5, pady = 5)
            label_tme = ctk.CTkLabel(self, text=f"{proceso['tme']}", font=("Arial", 14))
            label_tme.grid(row=self.row_count, column = 1, padx = 5, pady = 5)
            self.labels_procesos.append((label_nom, label_tme))
            self.row_count += 1
    #Función para limpiar la tabla de procesos pendientes
    def limpiar_procesos(self): 
        for label_nom, label_tme in self.labels_procesos:
            label_nom.configure(text="")
            label_tme.configure(text="")
    #Función para recorrer los procesos en la tabla cada que termina un proceso
    def recorrer_procesos(self):
        for i in range (0, self.num_pros_pend):
            self.labels_procesos[i][0].configure(text=f"{self.labels_procesos[i+1][0].cget("text")}")
            self.labels_procesos[i][1].configure(text=f"{self.labels_procesos[i+1][1].cget("text")}")
        self.labels_procesos[self.num_pros_pend][0].configure(text="")
        self.labels_procesos[self.num_pros_pend][1].configure(text="")
    #Función para cambiar la lista de procesos cuando cambia el lote
    def cambiar_procesos(self):
        if(self.num_pros_pend > 0): 
            self.num_pros_pend -= 1
            self.num_pros.configure(text=f"{self.num_pros_pend}")
        if (self.num_pros_pend == 0 and self.lotes_pendientes.num_lotes_pend > 0):
            self.lotes_pendientes.lote_completado()
            self.lote_procesar = batches[self.lote_actual]
            self.cambiar_lote()
            self.lote_actual += 1
        elif (self.num_pros_pend == 0 and self.lotes_pendientes.num_lotes_pend == 0):
            self.limpiar_procesos()
            self.contador.terminar()
    #Función para cambiar el lote
    def cambiar_lote(self):
        self.num_pros_pend = len(self.lote_procesar)
        self.num_pros.configure(text=f"{self.num_pros_pend}")
        num_label = 0
        for proceso in self.lote_procesar:
            self.labels_procesos[num_label][0].configure(text=f"{proceso['nombre']}")
            self.labels_procesos[num_label][1].configure(text=f"{proceso['tme']}")
            num_label += 1
#CLase para la tabla de los procesos en ejecución
class Procesos_Ejecucion(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.procesos_programados = master.proceso_pend
        self.procesos_terminados = master.proceso_term
        self.tiempo_transcurrido = 0
        self.tiempo_restante = 0
        self.num_pros_eje = 0
        self.lote_actual = self.procesos_programados.lote_procesar
        self.proceso_actual = self.lote_actual[0]
        self.ope = ""
        #Etiquetas informativas
        label_1 = ctk.CTkLabel(self, text="Proceso en\nEjecución:", padx=5, pady=5, font=("Arial", 14, "bold"), justify="center")
        label_1.grid(row=0, column=0, padx=10, pady=5)
        self.num_eje = ctk.CTkLabel(self, text=f" {self.num_pros_eje} ", padx=20, pady=5, font=("Arial", 14, "bold"), justify="center")
        self.num_eje.grid(row=0, column=1, padx=10, pady=5)

        #Columna 1
        label_nom = ctk.CTkLabel(self, text="Nombre:", padx=5, pady=5, font=("Arial", 12, "bold"), justify="center")
        label_nom.grid(row=1, column=0, padx=10, pady=5)
        label_id = ctk.CTkLabel(self, text="ID:", padx=5, pady=5, font=("Arial", 12, "bold"), justify="center")
        label_id.grid(row=2, column=0, padx=5, pady=5)
        label_ope = ctk.CTkLabel(self, text="Operación:", padx=5, pady=5, font=("Arial", 12, "bold"), justify="center")
        label_ope.grid(row=3, column=0, padx=5, pady=5)
        label_ope = ctk.CTkLabel(self, text="Tiempo Max\nEstimado:", padx=5, pady=5, font=("Arial", 12, "bold"), justify="center")
        label_ope.grid(row=4, column=0, padx=5, pady=5)
        label_tt = ctk.CTkLabel(self, text="Tiempo  \nTranscurrido:", padx=5, pady=5, font=("Arial", 12, "bold"), justify="center")
        label_tt.grid(row=5, column=0, padx=5, pady=5)
        label_tr = ctk.CTkLabel(self, text="Tiempo\n  Restante:", padx=5, pady=5, font=("Arial", 12, "bold"), justify="center")
        label_tr.grid(row=6, column=0, padx=5, pady=5)

        #Columna 2
        self.texto_nom = ctk.CTkLabel(self, text="", padx=5, pady=5, font=("Arial", 13))
        self.texto_nom.grid(row=1, column=1, padx=10, pady=5)
        self.texto_id = ctk.CTkLabel(self, text="", padx=5, pady=5, font=("Arial", 13))
        self.texto_id.grid(row=2, column=1, padx=5, pady=5)
        self.texto_ope = ctk.CTkLabel(self, text="", padx=5, pady=5, font=("Arial", 13))
        self.texto_ope.grid(row=3, column=1, padx=5, pady=5)
        self.texto_tme = ctk.CTkLabel(self, text="", padx=5, pady=5, font=("Arial", 13))
        self.texto_tme.grid(row=4, column=1, padx=5, pady=5)
        self.texto_tt = ctk.CTkLabel(self, text="", padx=5, pady=5, font=("Arial", 13))
        self.texto_tt.grid(row=5, column=1, padx=5, pady=5)
        self.texto_tr = ctk.CTkLabel(self, text="", padx=5, pady=5, font=("Arial", 13))
        self.texto_tr.grid(row=6, column=1, padx=5, pady=5)

        self.avanzar_tiempo()
    #Función para el cambio de proceso en la tabla
    def proceso_en_ejecucion(self, proceso):
        self.tiempo_transcurrido = 0
        self.texto_nom.configure(text=f"{proceso['nombre']}")
        self.texto_id.configure(text=f"{proceso['id']}")
        self.ope = operacion(proceso['num_1'], proceso['num_2'], proceso['signo']) 
        self.texto_ope.configure(text=self.ope)
        self.texto_tme.configure(text=f"{proceso['tme']}")
        self.texto_tt.configure(text=f"{self.tiempo_transcurrido}")
        self.tiempo_restante = proceso['tme']
        self.texto_tr.configure(text=f"{self.tiempo_restante}")
        self.num_pros_eje += 1
        self.num_eje.configure(text=f"{self.num_pros_eje}")
    #Función para limpiar los campos de la tabla de procesos
    def limpiar_datos(self):
        self.texto_nom.configure(text="")
        self.texto_id.configure(text="")
        self.texto_ope.configure(text="")
        self.texto_tme.configure(text="")
        self.texto_tt.configure(text="")
        self.texto_tr.configure(text="")
    #Función para el avance del tiempo en la ejecución del proceso
    def avanzar_tiempo(self):
        self.tiempo_transcurrido += 1
        self.tiempo_restante -= 1
        self.texto_tt.configure(text=f"{self.tiempo_transcurrido}")
        self.texto_tr.configure(text=f"{self.tiempo_restante}")    
        if (self.tiempo_restante == 0): #Si el tiempo restante es 0, se hace lo siguiente:
            self.procesos_terminados.agregar_proceso(self.proceso_actual, self.procesos_programados.lote_actual, self.ope)  
            self.procesos_programados.cambiar_procesos()
            if (self.procesos_programados.num_pros_pend > 0 and self.procesos_programados.num_pros_pend != len(self.procesos_programados.lote_procesar)):  #Si existen más procesos en el lote, se cambia de proceso
                self.procesos_programados.recorrer_procesos()  
                self.lote_actual.pop(0)
                self.proceso_actual = self.lote_actual[0]
                self.proceso_en_ejecucion(self.proceso_actual)
            else: #De lo contrario, se cambia el lote
                self.lote_actual = self.procesos_programados.lote_procesar
                self.proceso_actual = self.lote_actual[0]
                self.proceso_en_ejecucion(self.proceso_actual)
        #Si ya no existe ningún proceso ni lote, se termina el conteo
        if (self.procesos_programados.lotes_pendientes.num_lotes_pend == 0 and self.procesos_programados.num_pros_pend == 0): 
            self.limpiar_datos()
            self.num_eje.configure(text="N/A")
            return
        self.after(1000, self.avanzar_tiempo) #Esto se ejecuta cada segundo
#Clase para la tabla de procesos terminados
class Procesos_Terminados(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.num_pros_term = 0 
        self.row_count = 2 #Esto nos sirve para ubicarnos en la tabla correctamente
        #Etiquetas informativas
        label_1 = ctk.CTkLabel(self, text="Procesos \nTerminados: ", padx=5, pady=5, font=("Arial", 14, "bold"))
        label_1.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.num_term = ctk.CTkLabel(self, text=str(self.num_pros_term), padx=5, pady=5, font=("Arial", 14, "bold"))
        self.num_term.grid(row=0, column=1, padx=10, pady=5)
        #Etiquetas de encabezado de los procesos finalizados
        label_lote = ctk.CTkLabel(self, text="No. Lote:", padx=5, pady=5, font=("Arial", 12, "bold"), justify="center")
        label_lote.grid(row=1, column=0, padx=10, pady=5)
        label_id = ctk.CTkLabel(self, text="ID:", padx=5, pady=5, font=("Arial", 12, "bold"), justify="center")
        label_id.grid(row=1, column=1, padx=10, pady=5)
        label_ope = ctk.CTkLabel(self, text="Operación: ", padx=5, pady=5, font=("Arial", 12, "bold"), justify="center")
        label_ope.grid(row=1, column=2, padx=5, pady=5)
        label_res = ctk.CTkLabel(self, text="Resultado: ", padx=5, pady=5, font=("Arial", 12, "bold"), justify="center")
        label_res.grid(row=1, column=3, padx=5, pady=5)
    #Función para agregar un proceso finalizado a la tabla de procesos finalizados
    def agregar_proceso(self, proceso, lote, ope):
        ctk.CTkLabel(self, text=f"{lote}", font=("Arial", 13)).grid(row=self.row_count, column = 0, pady = 5)
        ctk.CTkLabel(self, text=f"{proceso['id']}", font=("Arial", 13)).grid(row=self.row_count, column = 1, pady = 5)
        ctk.CTkLabel(self, text=f"{ope}", font=("Arial", 13)).grid(row=self.row_count, column = 2, pady = 5)
        ctk.CTkLabel(self, text=f"{int(eval(ope)) if eval(ope).is_integer() else f'{eval(ope):.2f}'}", font=("Arial", 13)).grid(row=self.row_count, column=3, pady=5)
        self.row_count += 1
        self.num_pros_term += 1
        self.num_term.configure(text=f"{self.num_pros_term}")

#Clase del contador que muestra el tiempo transcurrido
class Contador(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.tiempo_total = 0
        self.contar = True  #Esto nos sirve para saber cuándo finalizar el conteo
        #Etiquetas informativas
        label_1 = ctk.CTkLabel(self, text="Contador:", padx=5, pady=5, font=("Arial", 16, "bold"))
        label_1.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.label_tiempo = ctk.CTkLabel(self, text="0", padx=5, pady=5, font=("Arial", 16, "bold"))
        self.label_tiempo.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.actualizar_tiempo()
    #Función para contar
    def actualizar_tiempo(self):
        if self.contar == True:  #Siempre que contar sea True, cuenta
            self.label_tiempo.configure(text=f"{self.tiempo_total}")
            self.tiempo_total += 1
            self.after(1000, self.actualizar_tiempo)
    #Función para terminar el conteo
    def terminar(self):
        self.contar = False #Aquí determinamos que ya no queremos contar
        messagebox.showinfo("Finalizar", "¡Todos los procesos han sido ejecutados correctamente!")
#Clase para la ventana 3 de ejecución de procesos
class Aplicacion(ctk.CTk):
    def __init__(self):
        super().__init__()
        proceso_ejecucion = batches[0][0]   #Proceso inicial
        self.num_pros_pend=len(batches[0])  #Determinar cuántos procesos tiene el lote
        self.num_lotes_pend=len(batches) - 1    #Determinar cuántos lotes quedan pendientes
        #Configuración de la ventana
        self.title("Ventana de Procesos")
        self.grid_rowconfigure(0, weight=0)  
        self.grid_columnconfigure(0, weight=0)
        self.resizable(False, False)
        #Creación del contador global
        self.contador = Contador(master=self)
        self.contador.grid(row=2, column=2, padx=20, pady=10, sticky="nsew")
        #Creación del cuadro de lotes pendientes
        self.lote = Lotes(master=self, num_lotes_pend=self.num_lotes_pend)
        self.lote.grid(row=0, column=0, padx=30, pady=20, sticky="nw")
        #Creación de la tabla de procesos pendientes
        self.proceso_pend = Procesos_Pendientes(master=self, lote_inicial=batches[0])
        self.proceso_pend.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        #Creación de la tabla de procesos terminados
        self.proceso_term = Procesos_Terminados(master=self, width = 340)
        self.proceso_term.grid(row=1, column=2, padx=20, pady=10, sticky="nsew")
        #Creación de la tabla de procesos en ejecución
        self.proceso_eje = Procesos_Ejecucion(master=self)
        self.proceso_eje.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        #Ejecutar el primer proceso
        self.proceso_eje.proceso_en_ejecucion(proceso_ejecucion)
#Creación y ejecución de la ventana inicial para el ingreso del número de procesos
inicial = NumeroProcesos()
inicial.mainloop()
#Si el número de procesos asignados es 0, se termina todo
if (n_procesos == 0): exit()
#Creación y ejecución de la ventana de captura de procesos
captura = IngresarProcesos()
captura.mainloop()
#Si no se registraron todos los procesos, nos vamos todos
if (contador_procesos <= n_procesos): exit()
#Asignamos los procesos a cada lote
asignar_lotes()
#Creación y ejecución de la ventana de ejecución de procesos
lotes = Aplicacion()
lotes.mainloop()