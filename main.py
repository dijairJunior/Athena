# -*- coding: utf-8 -*-

import os
from tkinter import *


def ia():
    # Importando os modulos do chat
    import datetime  # Representar data e hora em vários formatos.
    import speech_recognition as sr  # Para realização de reconhecimento de fala, com suporte para diversos motores e
    # APIs, online e offline.
    import sounddevice as sd  # Ligações com o PyAudio e NumPy
    import wavio as wv  # Ler um arquivo WAV e também gravar um array em NumPy
    import wikipedia  # Modulo de busca de diversos assuntos
    import webbrowser  # Principalmente destinado a evitar erros de importação
    import random
    from gtts import gTTS  # Principal API para reconhecimento de fala e transcrição dos textos reconhecido
    from playsound import playsound  # Para executar um audio gravado
    import pywhatkit  # Realizar automação para WhatsApp e YouTube
    import bs4
    import requests  # Não a nessecidade de adicionar Strings manualmente e fica tudo automaticamente.
    import joblib
    from typing import List, Tuple

    # Criação de lista de saudação
    saudacao = ['De nada', 'Por nada', 'A seu dispor', 'Até logo']
    saudacao_aleatoria = random.choice(saudacao)

    # Criação de lista para acessar sites predefinidos
    meusites: List[Tuple[str, str]] = [
        ('gazeta do povo', 'https://www.gazetadopovo.com.br/'),
        ('youtube', 'https://www.youtube.com/'),
        ('tudo gostoso', 'https://www.tudogostoso.com.br/')
    ]

    # Importa arquivos de voz
    filename = 'minhavoz.wav'
    fala_robo = 'fala_robo.mp3'

    # Variavel global
    global says

    # Criação da assistente de fala 'Google'
    def fala(text):
        tts = gTTS(text, lang='pt-BR')
        tts.save('fala_robo.mp3')
        playsound(fala_robo)
        os.remove(filename)
        os.remove(fala_robo)

    # Criando Função para gravar o audio
    def grava():
        freq = 48000
        duration = 5
        recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
        print('Fale agora!')
        sd.wait()
        wv.write("minhavoz.wav", recording, rate=freq, sampwidth=2)
        print('Ok! Processando')

    # Criando uma função para abir site predefinidos
    def addsite():
        snome = input('Qual o nome do site?')
        slink = input('Qual o link do site?')

        # Verifica se o nome do site já existe na lista
        for endereco in meusites:
            if endereco[0] == snome:
                print('O site já existe na lista!')
                return

        # Se o nome do site não existir na lista, adiciona o novo site
        lista_site = [snome, slink]
        meusites.append(lista_site)

    # Função para pegar as informações os ativos de mercados
    def get_crypto_price(bitcoin):
        url = "https://www.google.com/search?q=" + bitcoin + "hoje&dcr=0"
        html = requests.get(url)
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        text = soup.find("div", attrs={'class': 'BNeawe iBp4i AP7Wnd'}).find("div", attrs={
            'class': 'BNeawe iBp4i AP7Wnd'}).text
        fala(f'O preço de {bitcoin} é de {text}')

    # Criar um lastro de repetição para o código não parar
    while True:
        grava()

        # Função para ouvir e reconhecer a fala
        # Habilita o microfone do usuário
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

            # Para tocar a musica ou video no youtube
            elif 'toque' in texto or 'tocar' in texto:
                tocar = texto.replace('toque', '')
                toque = texto.replace('tocar', '')
                fala('Ok, tocando musica')
                resultado = pywhatkit.playonyt(toque, tocar)
                fala(resultado)

            # Método para abrir site e adicionar sites
            elif 'abrir site' in texto:
                site = texto.replace('abrir site', '')
                meusites = joblib.load('meusites.obj')

                for i in meusites:
                    if i[0] in site:
                        webbrowser.open(i[1])
            elif 'adicionar site' in texto:
                addsite()
                joblib.dump(meusites, 'meusites.obj')

            # Apresentação do assistente virtual
            elif 'apresentar' in texto or 'apresentação' in texto or 'apresente-se' in texto:
                fala(
                    'Oi meu nome é Athena, eu sou sua assistente virtual! Você pode me pedir para abrir algum site, '
                    'ou para tocar alguma música, ou pode perguntar as horas, e mais algumas coisas. Espero que goste!')

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

        # Se nao reconheceu o padrao de fala, exibe a mensagem
        except:
            print('Ocorreu algum erro, tento novamente')


# Criação um painel interativo para execução do Assistente virtual
janela = Tk()
janela.title('ZOYE - Assistente virtual em Python')

label_l = Label(janela, text='ZOYE - Assistente virtual em Python', font='Arial 35')
label_l.place(x=50, y=100)

botao_l = Button(janela, height=4, width=40, text='Clique aqui para iniciar!', font='Arial 15', command=ia,
                 background='#FFFAFA')
botao_l.place(x=220, y=280)

janela.geometry('950x500+0+0')

janela.mainloop()
