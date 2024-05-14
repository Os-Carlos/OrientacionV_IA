import json
from collections import defaultdict

import pyttsx3
import speech_recognition as sr

# Inicializa el motor TTS (Text-to-Speech)
engine = pyttsx3.init()

recognizer = sr.Recognizer()
mic = sr.Microphone()


def reconocer_carrera(texto, json_carreras):
    # Cargar el JSON de carreras
    with open(json_carreras) as f:
        data = json.load(f)

    # Crear un diccionario para contar los términos reconocidos por carrera
    conteo_carreras = defaultdict(int)

    # Dividir el texto en palabras
    palabras = texto.split()

    # Iterar sobre cada carrera y sus términos
    for categoria in data["categorias"]:
        for carrera in categoria["carreras"]:
            for termino in carrera["terminos"]:
                if termino in palabras:
                    # Incrementar el contador para esta carrera
                    conteo_carreras[carrera["nombre"]] += 1

    # Encontrar la carrera con el conteo más alto
    carrera_mas_reconocida = max(conteo_carreras, key=conteo_carreras.get)

    # Encontrar la categoría de la carrera más reconocida
    categoria_carrera_mas_reconocida = next(
        (categoria["nombre"] for categoria in data["categorias"] for carrera in categoria["carreras"] if
         carrera["nombre"] == carrera_mas_reconocida), None)

    return carrera_mas_reconocida, categoria_carrera_mas_reconocida


evaluation_active = False
text = ""
carrera = ""
json_carreras = "entrenamiento/carreras.json"


# Función para que el programa hable
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Saludo inicial
speak("Para comenzar la evaluación, por favor di 'hola'.")

while True:
    with mic as source:
        print("Escuchando...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language='es-ES')
        print(f'Usuario: {text}')

        # Comienza la evaluación si el usuario dice "hola" y la evaluación no está activa
        if "hola" in text.lower() and not evaluation_active:
            speak("La evaluación ha comenzado. Por favor, comparte tus habilidades e intereses.")
            evaluation_active = True
            continue  # Salta a la siguiente iteración del bucle

        if evaluation_active and text.lower() != "hola" and text.lower() != "adiós":
            carrera, categoria = reconocer_carrera(text.lower(), json_carreras)

        # Termina la evaluación si el usuario dice "adios" y la evaluación está activa
        if "adiós" in text.lower() and evaluation_active:
            evaluation_active = False
            speak("La evaluación ha finalizado. Calculando la carrera recomendada...")
            print(f"Basado en la información que has brindado, puedo recomendarte la carrera de '{carrera}'.")
            speak(f"Basado en la información que has brindado, puedo recomendarte la carrera de '{carrera}'.")
            break

    except sr.UnknownValueError:
        print("Lo siento, no pude entender lo que dijiste.")
    except sr.RequestError:
        print("Lo siento, hubo un error en la solicitud. Intenta de nuevo.")

# Ejemplo de uso
