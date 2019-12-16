import os
import json
import time
import PySimpleGUI as sg
from pydub import AudioSegment
import speech_recognition as sr


def speech_to_text():
    """
        Este es el módulo que anda bien
    """
    audios=['audio1.wav','audio2.wav','audio3.wav']
    r=sr.Recognizer() #Declaro el objeto reconocedor120
    r.energy_threshold = 4000
    for i in audios:
        duration_value=180 #Duration es cuánto grabar del audio
        offset_value=0 #Offset es desde dónde arrancar el audio
        demo=sr.AudioFile(i) #Le paso el audio
        for i in range(2):
            with demo as source:
                r.adjust_for_ambient_noise(source) #Le ajusto el sonido ambiente

                print('Valor offset ',offset_value)
                print('Valor duracion',duration_value)
                audio=r.record(source,offset=offset_value,duration=duration_value) #Lo paso a la variable audio 
                    
                output=r.recognize_google(audio,show_all=True, language="es-ES") 
                print(output)
                guardar_salida((output['alternative'][0]['transcript']))
                    
                duration_value=120
                offset_value=179


def speech_to_text3():
    "Convert only one audio"
    salida=''
    r=sr.Recognizer() #Declaro el objeto reconocedor120
    r.energy_threshold = 4000
    duration_value=180 #Duration es cuánto grabar del audio
    offset_value=0 #Offset es desde dónde arrancar el audio
    demo=sr.AudioFile('audio4.wav') #Le paso el audio
    with demo as source:
        r.adjust_for_ambient_noise(source) #Le ajusto el sonido ambiente

        print('Valor offset ',offset_value)
        print('Valor duracion',duration_value)
        audio=r.record(source,offset=179,duration=166) #Lo paso a la variable audio 
                    
        output=r.recognize_google(audio,show_all=True, language="es-ES") 
        salida=salida+' '+(output['alternative'][0]['transcript'])
        print(salida)
        print(salida)



def get_extension(string):
    fileToConvert= (string.split('/'))
    fileToConvert=fileToConvert[len(fileToConvert)-1]
    return ((os.path.splitext(fileToConvert)[1])[1:])

def convert_audio_to_mp3(audio,location):
    extension=get_extension(audio)
    audio = AudioSegment.from_file(audio,format=extension)
    location=location+'/'+'archivoNuevo.mp3'
    audio.export(location,format='mp3')
    audio.export('audioWav.wav',format='wav')


#print(os.getcwd())
layout = [
            [sg.Text('Elija el archivo a convertir')],
            [sg.Input(), sg.FileBrowse()],
            [sg.Text('Elija donde guardar')],
            [sg.Input(),sg.FolderBrowse()],
            [sg.Submit('Confirmar'),sg.Cancel('Cancelar')]

        ]
window = sg.Window('Ventana',size=(500,500)).layout(layout)

while True:
    event,values = window.Read()
    print('Evento {}'.format(event))
    print('Valores {}'.format(values))
    if(event == 'Confirmar' and values['Browse'] != '' and values['Browse0'] != ''):
        print('Entre ',values['Browse'])
        location = values['Browse0']
        convert_audio_to_mp3(values['Browse'],location)
        window.Close()
        break
    elif(event == None):
        break
