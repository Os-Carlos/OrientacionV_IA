import threading
import tkinter as tk

import cv2
import numpy as np
import speech_recognition as sr
from PIL import Image, ImageTk
from keras.models import load_model

# Definir las etiquetas de las expresiones
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']


class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Cargar el modelo de expresiones
        self.model = load_model('entrenamiento/expresiones.h5')

        self.video_source = 1  # Esto representa tu cámara, podría ser otro valor dependiendo de tu configuración
        self.vid = cv2.VideoCapture(self.video_source)

        self.emotions_detected = []
        self.last_recognition = ""

        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH),
                                height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_listen = tk.Button(window, text="Habla", command=self.start_listening_thread)
        self.btn_listen.pack()

        self.lbl_status = tk.Label(window, text="Presiona 'Habla' para iniciar el reconocimiento de voz")
        self.lbl_status.pack()

        self.delay = 10
        self.update()

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            # Convertir el cuadro de video a escala de grises
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Cargar el clasificador haarcascade para la detección de caras
            faces = cv2.CascadeClassifier('entrenamiento/haarcascade_frontalface_default.xml').detectMultiScale(gray)

            for (x, y, w, h) in faces:
                # Recortar la región de interés (ROI) del cuadro de video
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                # Normalizar la ROI y convertirla a un arreglo 4D
                roi = np.expand_dims(np.expand_dims(roi_gray, -1), 0) / 255.0

                # Realizar la predicción utilizando el modelo
                preds = self.model.predict(roi)[0]
                label = EMOTIONS[np.argmax(preds)]

                # Almacenar la emoción detectada
                self.emotions_detected.append(label)

            # Convertir la imagen de OpenCV a formato compatible con Tkinter
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def start_listening_thread(self):
        # Ejecutar la función de reconocimiento de voz en un hilo separado
        threading.Thread(target=self.start_listening).start()

    def start_listening(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.lbl_status.config(text="Escuchando...")
            try:
                audio = self.recognizer.listen(source, timeout=5)
                recognized_text = self.recognizer.recognize_google(audio, language="es-ES")
                self.last_recognition = recognized_text
                if recognized_text.lower() == "adiós":
                    self.lbl_status.config(text=self.last_recognition)
                    self.show_emotions()
                else:
                    self.lbl_status.config(text=self.last_recognition)
            except sr.WaitTimeoutError:
                self.lbl_status.config(text="Presiona 'Habla' para iniciar el reconocimiento de voz")

    def show_emotions(self):
        if self.emotions_detected:
            emotion_count = {emotion: self.emotions_detected.count(emotion) for emotion in set(self.emotions_detected)}
            emotions_text = "\n".join([f"{emotion}: {count} veces" for emotion, count in emotion_count.items()])
            self.lbl_status.config(text=emotions_text)
        else:
            self.lbl_status.config(text="No se detectaron emociones.")


App(tk.Tk(), "Orientador Vocacional Inteligente")
