import os
import json
import time
import mutagen #Manage audio metadata
import PySimpleGUI as sg
from pydub import AudioSegment #Manage an audio as an AudioObject 
import speech_recognition as sr #Recognize audio and convert it to text



def speech_to_text(iterations):
    "Convert only one audio"
    index=1
    salida=''
    r = sr.Recognizer() #Declaro el objeto reconocedor120
    r.energy_threshold = 4000
    duration_value=180 #Duration es cuánto grabar del audio
    offset_value=0 #Offset es desde dónde arrancar el audio
    demo=sr.AudioFile('audioWav.wav') #Le paso el audio
    while index <= iterations:
        with demo as source:
            r.adjust_for_ambient_noise(source) #Le ajusto el sonido ambiente
            audio=r.record(source,offset=offset_value,duration=180) #Lo paso a la variable audio 
            output=r.recognize_google(audio,show_all=True, language="es-ES") 
            print('Salida {}'.format(output))
            if (output != []): #Si pudo hacer la conversión
                index+=1
                salida=salida+' '+(output['alternative'][0]['transcript'])
                offset_value+=179
                print('Cambia')
            else:
                print('Hubo error, probamos de vuelta')
    return salida

    
def get_extension(string):
    """
        Return the extension of a file
    """
    fileToConvert= (string.split('/'))
    fileToConvert=fileToConvert[len(fileToConvert)-1]
    return ((os.path.splitext(fileToConvert)[1])[1:])

def convert_audio_to_mp3(audio,location,audio_name):
    """
        Convert the selected audio into mp3 and wav
    """
    extension=get_extension(audio)
    audio = AudioSegment.from_file(audio,format=extension) #Get an audio object
    location=location+'/'+audio_name+'.mp3'
    audio.export(location,format='mp3') #Export the audio to mp3
    audio.export('audioWav.wav',format='wav') #Export the audio to wav
    return location
    #export function export('location to save the file', format = 'file format')


def get_audio_duration(audio):
    """
        Return audio duration
    """
    file = ((mutagen.File(audio)).info.pprint()).split(' ') #Print metada of a file as a list
    return (file[len(file)-2])

def select_audio():
    """
        Show a layout to select audio and location to save it
    """
    layout = [
                [sg.Text('Elija el archivo a convertir')],
                [sg.Image(filename='imagenAudio.png'),sg.Input(), sg.FileBrowse('Archivo')],
                [sg.Text('Elija donde guardar')],
                [sg.Image(filename='imagenCarpeta(1).png'),sg.Input(),sg.FolderBrowse('Carpeta')],
                [sg.Submit('Confirmar'),sg.Cancel('Cancelar')]

            ]

    window = sg.Window('Ventana',size=(470,200)).layout(layout)

    while True:
        event,values = window.Read()
        if(event == 'Confirmar' and values['Archivo'] != '' and values['Carpeta'] != ''):
            audio = values['Archivo']
            location = values['Carpeta']
            window.Close()
            return (audio,location)
        elif(event == None):
            window.Close()
            os._exit(0)

def select_name_audio():
    """
        Show a layout to put the name of the new audio
    """
    layout = [
                [sg.Text('Ingrese el nombre del nuevo audio .mp3'),sg.Input(size=(15,20))],
                [sg.Submit('Enviar')]            
             ]
    window = sg.Window('Ventana',layout)
    while True:
        event,values = window.Read()
        print('Evento ',event)
        print('Valores ',values)
        if values[0] != '':
            window.Close()
            return values[0]
        if event == None:
            window.Close()
            os._exit(0)

def main():
    audio,location = select_audio()
    audio_name= select_name_audio()
    location = convert_audio_to_mp3(audio,location,audio_name) 
    audio_duration = get_audio_duration(location) #This audio_duration is in seconds
    iterations = (float(audio_duration) // 180) + 1 
    salida = speech_to_text(int(iterations))
    print(salida)   

main()
