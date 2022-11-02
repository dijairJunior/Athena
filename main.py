# Our main file.

# Importando as bibliotecas para os demais comandos
import speech_recognition as sr
import pyttsx3

#Trainamento do bot para o reconhecimento de falar e exibindo na tela
rec = sr.Recognizer()
# print(sr.Microphone().list_microphone_names())
with sr.Microphone(3) as mic:
    rec.adjust_for_ambient_noise(mic)
    print("Pode falar que eu vou gravar")
    audio = rec.listen(mic)
    texto = rec.recognize_google(audio, language="pt-BR")
    print(texto)