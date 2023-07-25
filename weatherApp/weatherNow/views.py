import os
from django.http import HttpResponse
from django.template import loader
import requests

#Hacemos llamadas a la API de AEMET
def cargar_provicias():
    response = requests.get('https://www.el-tiempo.net/api/json/v2/provincias')

    if response.status_code == 200:
       path = os.path.join(os.path.dirname(__file__), 'dictionary.txt')
       file = open( path, "w")
       file.write(response.json)
    
    return None

# Cargamos el index de WeatherNow
def weatherNow(request):
    html_template = loader.get_template('index.html')
    cargar_provicias()
    return HttpResponse(html_template.render())