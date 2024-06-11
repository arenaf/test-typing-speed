import tkinter
from wonderwords import RandomWord
import random

# -------- Colores --------
BACKGROUND = "#393E46"
FOREGROUND = "#F6F1E9"
SUCCESS = "#A1DD70"
ERROR = "#FF004D"
# -------- Fuente --------
FONT = "courier"
# -------- Palabras del texto --------
MIN_WORDS = 30
MAX_WORDS = 35


class TypingSpeed:
    def __init__(self):
        self.fill_color = FOREGROUND
        self.fill_color_error = FOREGROUND
        self.stop = True # Stop del tiempo

    def new_text(self):
        """
        Genera palabras aleatorias
        :return: retorna todas la palabras en la variable text
        """
        num_words = random.randint(MIN_WORDS, MAX_WORDS)
        num_sentences = num_words // 5
        text = ""
        r = RandomWord()
        for i in range(num_sentences):
            words = r.random_words(num_sentences)
            sentences = " ".join(words).capitalize() + ". "
            text += sentences
        return text.strip()

    def start_typing(self, *event):
        """
        Inicia las variables, activa los widget text de "input_text" (donde escribe el usuario) y "text_to_write"
        texto que se debe teclear.
        Introduce el texto aleatorio en el widget text "text_to_write".
        Llama a la función que actualiza el tiempo.
        :param event: evento teclado, recoge qué letras se están tecleando y llama a la función "key_pressed".
        """
        start_button.place_forget()
        self.text = self.new_text()
        self.stop = False
        self.pos = 0
        self.sec = 0
        self.min = 0
        self.typing_time = 0.0
        self.cont_error = 0
        input_text.config(state="normal")
        input_text.bind("<Key>", self.key_pressed)
        input_text.place(x=70, y=370)
        text_to_write.config(state="normal")
        text_to_write.insert("0.0", self.text)
        self.timer_update()

    def key_pressed(self, event):
        """
        Comprueba que los caracteres introducidos por teclado sean iguales a los del texto aleatorio.
        Pinta la letra de verde en caso de acierto y de rojo en caso de fallo.
        Compara si se llegó al final del texto, en caso afirmativo, llama a la función "end_sentence"
        :param event: caracter que se acaba de pulsar.
        """
        self.total_chars = int(len(self.text))
        try:
            if event.char == self.text[self.pos]:
                text_to_write.tag_add("good", f"1.{self.pos}", f"1.{self.pos + 1}")
                text_to_write.tag_config("good", foreground=SUCCESS)
                self.pos += 1
            elif event.keycode == 16:
                if self.text[self.pos].isupper():
                    pass
            else:
                text_to_write.tag_add("error", f"1.{self.pos}", f"1.{self.pos + 1}")
                text_to_write.tag_config("error", foreground=ERROR)
                self.cont_error += 1
                self.pos += 1
        except IndexError:
                pass
        if self.total_chars == self.pos:
            self.end_sentence()

    def timer_update(self):
        """
        Actualiza el tiempo y lo muestra por pantalla en "timer_label".
        """
        if self.stop == False:
            self.sec += 1
            if self.sec == 60:
                self.sec = 0
                self.min += 1

            self.total_time = f"{self.min:02}:{self.sec:02}"
            timer_label.config(text=self.total_time)
            window.after(1000, self.timer_update)

    def end_sentence(self):
        """
        Se ejecuta cuando se llega al final del texto.
        Cuenta: cuántos errores se cometió, el porcentaje de acierto, los caracteres por minuto y las palabras por
        minuto.
        Llama a la función que mostrará estos datos por pantalla
        """
        print(timer_label["text"])
        self.stop = True # Detiene el tiempo
        print("Contador errores: ", self.cont_error)
        if self.cont_error == 0: # Contador de errores
            self.fill_color_error = SUCCESS
        else:
            self.fill_color_error = ERROR
        self.accuracy = (self.total_chars - self.cont_error) * 100 / self.total_chars # Porcentaje de acierto
        print(f"Porcentaje de acierto: {self.accuracy:.0f} %")
        if self.accuracy >= 80:
            self.fill_color = SUCCESS
        else:
            self.fill_color = ERROR

        self.typing_time = float(f"{self.min}.{self.sec}") # Tiempo en float para calcular cpm
        self.cpm = self.total_chars / self.typing_time  # Caracteres por minuto
        print(f"CPM: {self.cpm:.0f}")
        self.wpm = self.total_chars / 5  # Palabras por minuto
        print(f"WPM: {self.wpm}")

        self.canvas_screen()

    def canvas_screen(self):
        """
        Muestra la pantalla final con los resultados obtenidos: caracteres por minuto, palabras por minuto, tiempo,
        errores y porcentaje de acierto.
        Botón con la posibilidad de reiniciar.
        """
        canvas.create_image(415, 260, image=card_img)
        wpm_canvas = canvas.create_text(200, 170, text=f"WPM:\n {self.wpm:.0f}", fill=FOREGROUND,
                                        font=(FONT, 30, "bold"))
        wpm_description = canvas.create_text(200, 230, text="Words Per Minute", fill=FOREGROUND,
                                             font=(FONT, 10, "normal"))
        cpm_canvas = canvas.create_text(400, 170, text=f"CPM:\n {self.cpm:.0f}", fill=FOREGROUND,
                                        font=(FONT, 30, "bold"))
        cpm_description = canvas.create_text(400, 230, text="Characters Per Minute", fill=FOREGROUND,
                                             font=(FONT, 10, "normal"))
        time_canvas = canvas.create_text(600, 170, text=f"Time:\n{timer_label['text']}", fill=FOREGROUND,
                                         font=(FONT, 30, "bold"))
        time_description = canvas.create_text(600, 230, text="Total Time", fill=FOREGROUND, font=(FONT, 10, "normal"))
        error_canvas = canvas.create_text(280, 340, text=f"{self.cont_error}", fill=self.fill_color_error,
                                          font=(FONT, 30, "bold"))
        error_description = canvas.create_text(280, 380, text="Total Errors", fill=FOREGROUND,
                                               font=(FONT, 20, "bold"))
        accuracy_canvas = canvas.create_text(510, 340, text=f"{self.accuracy:.0f}%", fill=self.fill_color,
                                             font=(FONT, 30, "bold"))
        accuracy_description = canvas.create_text(510, 380, text="Accuracy", fill=FOREGROUND, font=(FONT, 20, "bold"))
        canvas.grid(row=0, column=0)
        restart_button.place(x=590, y=470)

    def restart(self):
        """
        Se ejecuta si se pulsa "Restart" para reiniciar todos los valores.
        """
        canvas.grid_forget()
        restart_button.place_forget()
        timer_label.config(text="00:00")
        input_text.delete("0.0", tkinter.END)
        input_text.config(state="disabled")
        input_text.place_forget()
        text_to_write.delete("0.0", tkinter.END)
        text_to_write.config(state="disabled")
        canvas.delete("all")
        start_button.place(x=350, y=220)


# -------- UI --------
window = tkinter.Tk()
window.resizable(0, 0)
window.geometry("900x600")
window.title("Test Your Typing Speed")
window.config(padx=30, pady=30, background=BACKGROUND)

typing_speed = TypingSpeed()

# -------- Título --------
title = tkinter.Label(text="Test Your Typing Speed", font=(FONT, 15, "bold"), background=BACKGROUND,
                      foreground="#7F8487")
title.place(x=70, y=5)
label = tkinter.Label(text="arena", font=(FONT, 7, "normal"), background=BACKGROUND, foreground=FOREGROUND)
label.place(x=70, y=530)

# -------- Cajas de texto --------
text_to_write = tkinter.Text(width=55, height=10, font=(FONT, 15, "bold"), background=BACKGROUND,
                             foreground="#dee2e6", relief="flat", state="disabled", wrap="word")
text_to_write.place(x=70, y=160)
input_text = tkinter.Text(width=65, height=5, font=(FONT, 12, "normal"), background="#686D76", state="disabled",
                          relief="flat", wrap="word")
input_text.focus()
input_text.place_forget()

# -------- Etiqueta tiempo --------
timer_label = tkinter.Label(text="00:00", font=(FONT, 15, "bold"), background=BACKGROUND,
                            foreground=FOREGROUND)
timer_label.place(x=670, y=40)

# -------- Botón inicio ---------
start_button = tkinter.Button(width=8, height=2, text="Start", font=(FONT, 20, "bold"), command=typing_speed.start_typing)
start_button.place(x=350, y=220)

# --------- Canvas --------
canvas = tkinter.Canvas(width=800, height=526, highlightthickness=False, background=BACKGROUND)
card_img = tkinter.PhotoImage(file="card.png")

# --------- Botón reinicio --------
restart_button = tkinter.Button(text="Restart", font=(FONT, 10, "bold"), command=typing_speed.restart)

# --------- Mantiene la ventana abierta --------
window.mainloop()
