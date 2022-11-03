import os
from tkinter import *

def ia():
    import datetime
    import speech_recognition as sr
    import sounddevice as sd
    import wavio as wv
    import wikipedia
    import webbrowser
    import random
    from gtts import gTTS
    from playsound import playsound
    import pywhatkit
    import bs4
    import requests
    import joblib

    global none, link

    # Criação de lista de saudação
    lista1 = ['De nada', 'Por nada', 'A seu dispor', 'Até logo']
    lista1 = random.choice(lista1)

    # Criação de lista para acessar sites predefinidos
    meusites = [['gazeta do povo'], ['https://www.gazetadopovo.com.br/'],
                ['youtube'], ['https://www.youtube.com/'],
                ['tudo gostoso'], ['https://www.tudogostoso.com.br/']]

    # Importa arquivos de voz
    filename = 'minhavoz.wav'
    falaia = 'falaia.mp3'

    # Variavel global
    global says

    # Criação da assistente de fala 'Google'
    def fala(text):
        tts = gTTS(text, lang='pt-BR')
        tts.save('falaia.mp3')
        tts.save('falaia.mp3')
        playsound(falaia)
        os.remove(filename)
        os.remove(falaia)

    # Criando Função para gravar o audio
    def grava():
        freq = 48000  
        duration = 5  
        recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
        print('Fale agora!')
        sd.wait()
        wv.write("minhavoz.wav", recording, freq, sampwidth=2)
        print('Ok! Processando')

    # Criando uma função para abir site predefinidos
    def addsite():
        snome = input('Qual o nome do site?')
        slink = input('Qual o link do site?')
        listabase = [snome, slink]
        meusites.append(listabase)

    # Função para pegar as informações os ativos de mercados
    def get_crypto_price(coin):
        url = "https://www.google.com/search?q=" + coin + "hoje"
        HTML = requests.get(url)
        soup = bs4.BeautifulSoup(HTML.text, 'html.parser')
        text = soup.find("div", attrs={'class': 'BNeawe iBp4i AP7Wnd'}).find("div", attrs={
            'class': 'BNeawe iBp4i AP7Wnd'}).text
        fala('O preço de {coin} é de {text}')

    # Criar um lastro de repetição para o código não parar
    while True:
        grava()

        r = sr.Recognizer()
        try:
            with sr.AudioFile(filename) as source:
                audio_data = r.record(source)
                says = r.recognize_google(audio_data, language='pt-BR')
                print('Você disso: ' + says.lower())
                texto = says.lower()

            # Desligar o assistente
            f = open('shutdown.txt', 'r')
            fec = f.read()
            if texto in fec:
                fala('Ok, desligando...')
                janela.destroy()
                break

            # Para dizer o horário
            elif 'horas' in texto or 'hora' in texto:
                hora = datetime.datetime.now().strftime('%H:%M')
                fala('Agora são' + hora)


            # Para realizar uma pesquisa
            elif 'procure por' in texto:
                procurar = texto.replace('procure por', '')
                wikipedia.set_lang('pt')
                resultado = wikipedia.summary(procurar, 2)
                fala(resultado)
                fala.runAndWaint()

            # Para tocar a musica ou video no youtube
            elif 'toque' in texto or 'tocar' in texto:
                tocar = texto.replace('toque', '')
                toque = texto.replace('tocar', '')
                fala('Ok, tocando musica')
                resultado = pywhatkit.playonyt(toque, tocar)
                fala(resultado)
                fala.runAndWaint()

            # Método para abrir site e adicionar sites
            elif 'abrir site' in texto:
                site = texto.replace('abrir site', '')
                mysites = joblib.load('meusites.obj')

                for i in mysites:
                    if i[0] in site:
                        webbrowser.open(i[1])
            elif 'adicionar site' in texto:
                addsite()
                joblib.dump(meusites, 'meusites.obj')

            # Apresentação do assistente virtual
            elif 'apresentar' in texto or 'apresentação' in texto or 'apresente-se' is texto:
                fala('Oi meu nome é Liza, eu sou sua assistente virtual! Você pode me pedir para abrir algum site, ou para tocar alguma música, ou pode perguntar as horas, e mais algumas coisas. Espero que goste!')

            # informações sobre ativos de mercado
            elif 'valor hoje' in texto:
                coin = texto.replace('valor hoje', '')
                get_crypto_price(coin)

            # Criação de algumas respostas simples
            elif 'bom dia' in texto:
                fala('bom dia!')
            elif 'boa tarde' in texto:
                fala('boa tarde!')
            elif 'boa noite' in texto:
                fala('boa noite!')

        # Se causo de algum problema ira exibir um erro
        except:

            print('Ocorreu algum erro, tento novamente')


janela = Tk()
janela.title('Liza - Assistente virtual em Python')

label_l = Label(janela, text='Liza - Assistente virtual em Python', font='Arial 35')
label_l.place(x=200, y=200)

botao_l = Button(janela, height=4, width=67, text='Clique aqui para iniciar!', command=ia, background='grey')
botao_l.place(x=350, y=280)

janela.geometry('1200x500+0+0')

janela.mainloop()