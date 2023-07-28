import os
from django.http import HttpResponse
from django.template import loader
import requests
from weatherNow.models import Provincia, Municipios

path_root = os.path.dirname(__file__)

def write_log(error):
    """método para escribir los errores

    Args:
        error (_string ): _el error que voy a escribir_

    Returns:
        boolean: True para decir que ha salido todo OK, False para cuando no.
    """
    try:
        file_path = "static/provincias.txt"
        complete_path = os.path.join( path_root, file_path)
        file = open( complete_path, "a")
        file.write(error)
        return True
    except FileExistsError:
        print("No gusta esto...")
        return False


def cargar_provicias():
    respuesta = requests.get('https://www.el-tiempo.net/api/json/v2/provincias',
                             timeout = 5)
    try:
        if respuesta.status_code == 200:
            prov_json = respuesta.json()
            for line in prov_json['provincias']:
                new_provincia = Provincia(
                    prov_code = line['CODPROV'],
                    prov_name = line['NOMBRE_PROVINCIA'],
                    autono_code = line['CODAUTON'],
                    com_auton = line['COMUNIDAD_CIUDAD_AUTONOMA'],
                    capital_city = line['CAPITAL_PROVINCIA'],
                )
                new_provincia.save()
            
            # p = json.loads( respuesta.json(), object_hook = clsProv.Provincia)
            #print( p )
        return True
    except FileNotFoundError:
        write_log("Archivo provincias.json no encontrado.")
        return False


def cargar_municipios():
    respuesta = requests.get('https://www.el-tiempo.net/api/json/v2/municipios',
                            timeout = 5)
    try:
        if respuesta.status_code == 200:
            muni_json = respuesta.json()
            provin_aux = Provincia.objects.get( prov_code = "01")
            for line in muni_json:
                new_municipio = Municipios(
                    muni_code = line['CODIGOINE'][0:5],
                    muni_name = line['NOMBRE'],
                    prov_code = line['CODPROV']
                )
                new_municipio.save()
        return True
    except FileNotFoundError:
        write_log("Archivo provincias.json no encontrado.")
        return False

# Cargamos el index de WeatherNow
def weatherNow( request):
    html_template = loader.get_template('index.html')
    cargar_provicias()
    cargar_municipios()
    return HttpResponse(html_template.render())