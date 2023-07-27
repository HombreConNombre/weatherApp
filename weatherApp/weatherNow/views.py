import os
import json
from django.http import HttpResponse
from django.template import loader
import requests

path_root = os.path.dirname(__file__)

def write_log(error):
    try:
        file_path = "static/provincias.txt"
        complete_path = os.path.join( path_root, file_path)
        file = open( complete_path, "a")
        file.write(error)
        return None
    except FileExistsError:
        print("No gusta esto...")
        return None
#Hacemos llamadas a la API de AEMET para cargar un JSON con todos los códigos de las provincias.
def cargar_provicias():
    respuesta = requests.get('https://www.el-tiempo.net/api/json/v2/provincias')
    try:
        if respuesta.status_code == 200:
            file_path = "static/municipios.json"
            complete_path = os.path.join( path_root, file_path)
            file = open( complete_path, "w")
            #file.write(str(respuesta.content))
            print( respuesta.json())
        return None
    except FileNotFoundError:
        write_log("Archivo provincias.json no encontrado.")
        return None

#Hacemos llamadas a la API de AEMET para cargar un JSON con todos los códigos de los municipios.
def cargar_municipios():
    respuesta = requests.get('https://www.el-tiempo.net/api/json/v2/municipios')
    try:
        if respuesta.status_code == 200:
            file_path = "static/municipios.json"
            complete_path = os.path.join( path_root, file_path)
            file = open( complete_path, "w")
            file.write(str(respuesta.content))
        
        return None
    except FileNotFoundError:
        write_log("Archivo municipios.json no encontrado.")
        return None


# Cargamos el index de WeatherNow
def weatherNow(request):
    html_template = loader.get_template('index.html')
    cargar_provicias()
    cargar_municipios()
    return HttpResponse(html_template.render())