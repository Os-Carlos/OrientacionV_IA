import os
import sys

import cv2
import numpy as np
from keras.models import load_model

# Guardar las referencias originales de sys.stdout y sys.stderr
original_stdout = sys.stdout
original_stderr = sys.stderr

# Redirigir la salida estándar y la salida de error a devnull
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

# Cargar el modelo de expresiones
model = load_model('entrenamiento/expresiones.h5')

# Definir las etiquetas de las expresiones
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Inicializar la cámara
cap = cv2.VideoCapture(1)

emotions_detected = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

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
        preds = model.predict(roi)[0]
        label = EMOTIONS[np.argmax(preds)]

        # Almacenar la emoción detectada
        emotions_detected.append(label)

        # Dibujar el cuadro de la cara y mostrar la expresión reconocida
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

    # Mostrar el cuadro de video con las predicciones
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Restaurar la salida estándar y la salida de error a su estado original
sys.stdout = original_stdout
sys.stderr = original_stderr

# Liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()

if emotions_detected:
    print("Emociones detectadas:")
    for emotion in set(emotions_detected):
        print(f"{emotion}: {emotions_detected.count(emotion)} veces")
else:
    print("No se detectaron emociones.")
