from pydub import AudioSegment
import speech_recognition as sr
import json
import os
import time
lista=list()
def guardar_salida(salida):
    if os.stat('archivo.json').st_size == 0:
         with open('archivo.json','w',encoding='utf-8') as file:
            lista.append(salida)
            json.dump(lista,file)
    else:
        with open('archivo.json','r',encoding='utf-8') as file:
            contenido=json.load(file)
            contenido[0]=contenido[0]+' '+salida
        with open('archivo.json','w',encoding='utf-8') as file:
            json.dump(contenido,file)

def leer_lo_guardado():
    with open('archivo.json','r',encoding='utf-8') as file:
        print(json.load(file))

def speech_to_text():
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

def get_iterations(segundos):
    i=1
    while segundos > 0:
        segundosPrueba-=180
        i+=1
    return i

def speech_to_textV2(audio,duration):
    """
        This function returns a string of the audio converted into string.
    """
    seconds = (duration * 60)
    iterations=get_iterations(second)
    string=''
    r = sr.Recognizer()
    r.energy_threshold=4000
    offset_value=0
    duration_value=180
    r.adjust_for_ambient_noise(source)        
    for i in iterations:
        with audio as source:
            r.record(source,offset=offset_value,duration=duration_value) #Grabo el archivo wav
            output=r.recognize_google(audio,show_all=True,language='es-ES') #Lo paso por el recognizer de google
            string=string+' '+output #Concateno la salida con lo que ya tenía en el string
            offset_value+=180 #Me muevo 180 segundos más del audio, para arrancar de donde quedé 
    return string

    
leer_lo_guardado()