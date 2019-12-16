import os
import json
import time
import mutagen #Manage audio metadata
import PySimpleGUI as sg
from pydub import AudioSegment #Manage an audio as an AudioObject 
import speech_recognition as sr #Recognize audio and convert it to text



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



def get_extension(string):
    """
        Return the extension of a file
    """
    fileToConvert= (string.split('/'))
    fileToConvert=fileToConvert[len(fileToConvert)-1]
    return ((os.path.splitext(fileToConvert)[1])[1:])

def convert_audio_to_mp3(audio,location):
    """
        Convert the selected audio into mp3 and wav
    """
    extension=get_extension(audio)
    audio = AudioSegment.from_file(audio,format=extension) #Get an audio object
    location=location+'/'+'archivoNuevo.mp3'
    audio.export(location,format='mp3') #Export the audio to mp3
    audio.export('audioWav.wav',format='wav') #Export the audio to wav

    #export function export('location to save the file', format = 'file format')


def get_audio_duration(audio):
    """
        Return audio duration
    """
    file = ((mutagen.File(audio)).info.pprint()).split(' ') #Print metada of a file as a list
    return (file[len(file)-2])

def main():
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
            audio = values['Browse']
            location = values['Browse0']
            convert_audio_to_mp3(audio,location)
            window.Close()
            break
        elif(event == None):
            break


main()

