import tkinter as tk
from tkinter import messagebox
import random
import time

class NumberInputDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Adivinar número")
        self.geometry("200x120")
        self.resizable(False, False)

        self.label = tk.Label(self, text="Ingresa un número (1-100):")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self, width=10)
        self.entry.pack()

        self.button = tk.Button(self, text="Adivinar", command=self.submit)
        self.button.pack(pady=10)

        self.result = None

    def submit(self):
        input_text = self.entry.get()
        try:
            number = int(input_text)
            if 1 <= number <= 100:
                self.result = number
                self.destroy()
            else:
                messagebox.showwarning("Número inválido", "El número debe estar entre 1 y 100.")
        except ValueError:
            messagebox.showwarning("Número inválido", "Ingresa un número válido.")

def update_timer(label, start_time):
    elapsed_time = time.time() - start_time
    label.config(text="Tiempo: {:.0f}".format(elapsed_time))
    if elapsed_time < 60:
        label.after(1000, lambda: update_timer(label, start_time))

def start_game():
    # Generar un número aleatorio entre 1 y 100
    num = random.randint(1, 100)

    # Mostrar las instrucciones del juego
    output_text.insert(tk.END, "Bienvenido al juego de adivinanza de números.\n")
    output_text.insert(tk.END, "Tienes 60 segundos y/o 20 intentos para adivinar el número correcto.\n")
    output_text.insert(tk.END, "El número está entre 1 y 100.\n\n")

    # Iniciar el temporizador
    start_time = time.time()
    timer_label.config(text="Tiempo: 0")
    update_timer(timer_label, start_time)

    # Inicializar el contador de intentos
    num_intentos = 0

    def end_game():
        # Detener el temporizador
        timer_label.after_cancel(update_timer)
        
        # Preguntar al usuario si desea reiniciar el juego
        reintentar = messagebox.askyesno("Reiniciar juego", "¿Quieres jugar de nuevo?")
        if reintentar:
            output_text.insert(tk.END, "\n-------------------\n")
            start_game()
        else:
            output_text.insert(tk.END, "\n-------------------\n")
            output_text.insert(tk.END, "Gracias por jugar\n")

    # Iniciar el ciclo del juego
    while True:
        # Calcular el tiempo restante y verificar si se agotó el tiempo
        tiempo_restante = round(60 - (time.time() - start_time))
        if tiempo_restante <= 0:
            # Si se agotó el tiempo, mostrar el número correcto y el número de intentos
            tiempo_total = round(time.time() - start_time)
            output_text.insert(tk.END, "Se agotó el tiempo. El número correcto era {} y realizaste {} intentos en {} segundos, tienes 0 puntos.\n".format(num, num_intentos, tiempo_total))
            end_game()
            break
        elif num_intentos >= 20:
            # Si se agotaron los intentos, mostrar el número correcto y el número de intentos
            tiempo_total = round(time.time() - start_time)
            output_text.insert(tk.END, "Se acabaron los intentos. El número correcto era {} y realizaste {} intentos en {} segundos, tienes 0 puntos.\n".format(num, num_intentos, tiempo_total))
            end_game()
            break

        # Pedir al usuario que ingrese un número
        dialog = NumberInputDialog(window)
        window.wait_window(dialog)
        intento = dialog.result

        if intento is not None:
            # Incrementar el contador de intentos
            num_intentos += 1

            # Verificar si el número es demasiado alto o demasiado bajo
            if intento < num:
                output_text.insert(tk.END, "El número es demasiado bajo.\n")
            elif intento > num:
                output_text.insert(tk.END, "El número es demasiado alto.\n")
            else:
                # Si el usuario adivina el número, detener el temporizador y mostrar el tiempo y el número de intentos
                final = time.time()
                tiempo_total = final - start_time
                puntaje = round(10000 + (((tiempo_total-1) * (-250/3)) + ((num_intentos-1) * (-250))))
                output_text.insert(tk.END, "¡Felicitaciones! Adivinaste el número en {} intentos y {} segundos, te quedaron {} segundos y tu puntaje es de: {}.\n".format(num_intentos, round(tiempo_total), round(60 - (time.time() - start_time)), round(puntaje)))
                end_game()
                break

# Crear la ventana principal
window = tk.Tk()
window.title("Juego de Adivinanza de Números")
window.geometry("800x600")

# Crear la etiqueta del temporizador
timer_label = tk.Label(window, text="Tiempo: 0", anchor=tk.NE)
timer_label.pack()

# Crear el botón de inicio del juego
start_button = tk.Button(window, text="Iniciar Juego", command=start_game)
start_button.pack()

# Crear el área de texto para mostrar los mensajes de salida
output_text = tk.Text(window, width=40, height=10)
output_text.pack()

window.mainloop()