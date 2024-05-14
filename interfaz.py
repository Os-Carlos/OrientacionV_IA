import tkinter as tk

from PIL import Image, ImageTk


class InterfazVocacional(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agente de Orientación Vocacional")
        self.geometry("800x600")
        self.configure(bg="lightblue")

        self.label_titulo = tk.Label(self, text="Resultados de Agente Vocacional", font=("Arial", 18), bg="lightblue")
        self.label_titulo.pack(pady=10)

        self.frame_resultados = tk.Frame(self, bg="lightblue")
        self.frame_resultados.pack(pady=20)

        self.label_carrera = tk.Label(self.frame_resultados, text="Carrera recomendada:", font=("Arial", 14),
                                      bg="lightblue")
        self.label_carrera.pack(side=tk.LEFT)

        self.entry_carrera = tk.Entry(self.frame_resultados, font=("Arial", 14))
        self.entry_carrera.pack(side=tk.LEFT)

        # Imagen
        imagen = Image.open("entrenamiento/images.png")
        imagen = imagen.resize((400, 300), Image.LANCZOS)
        imagen = ImageTk.PhotoImage(imagen)

        # Mostrar imagen
        self.label_imagen = tk.Label(self, image=imagen, bg="lightblue")
        self.label_imagen.image = imagen
        self.label_imagen.pack()

        # Textos
        self.label_proyecto = tk.Label(self, text="Proyecto Inteligencia Artificial", font=("Arial", 16),
                                       bg="lightblue")
        self.label_proyecto.pack(pady=5)

        self.label_autores = tk.Label(self, text="Carlos Osorio\nJader Chocón\nJosé Argueta", font=("Arial", 14),
                                      bg="lightblue")
        self.label_autores.pack(pady=5)

        self.button_ver_mas = tk.Button(self, text="Ver más detalles", command=self.ver_mas_detalles,
                                        font=("Arial", 14, "bold"), pady=15)
        self.button_ver_mas.pack(pady=10)

    def ver_mas_detalles(self):
        pass


if __name__ == "__main__":
    app = InterfazVocacional()
    app.mainloop()
