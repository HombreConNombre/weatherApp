import os
from django.http import HttpResponse
from django.template import loader
import requests
from weatherNow.models import Provincia, Municipios
from django.core.exceptions import ObjectDoesNotExist

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


def load_provin():
    """Llamamos a AEMET para cargar en la BBDD las provincias.

    Returns:
        Boolean: True = OK, False = #Sad
    """
    try:
        #Comprobamos si existe para que nos salte el error DoesNotExist si no existe.
        Provincia.objects.get( prov_code = '01')
        return True
    except ObjectDoesNotExist:
        respuesta = requests.get('https://www.el-tiempo.net/api/json/v2/provincias',
                             timeout = 5)
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


def load_muni():
    """Llamamos a AEMET para cargar los municipios, los cuales están con un FK con las provincias

    Returns:
        Boolean: True = OK, False = #Sad
    """
    try:
        #Comprobamos si existe para que nos salte el error DoesNotExist si no existe.
        Municipios.objects.get( muni_code = '01001')
        return True
    except ObjectDoesNotExist:
        respuesta = requests.get('https://www.el-tiempo.net/api/json/v2/municipios',
                            timeout = 5)
        if respuesta.status_code == 200:
            muni_json = respuesta.json()
            codigo_inicial = 'x'
            for line in muni_json:
                if codigo_inicial != line['CODPROV']:
                    codigo_inicial = line['CODPROV']
                    provin_aux = Provincia.objects.get( prov_code = codigo_inicial)

                new_municipio = Municipios(
                    muni_code = line['CODIGOINE'][0:5],
                    muni_name = line['NOMBRE'],
                    prov_code = provin_aux
                )
                new_municipio.save()
        return True
    except FileNotFoundError:
        write_log("Archivo provincias.json no encontrado.")
        return False

def IP_location( user_IP):
    response = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=c7a5c06a04ee486f9f2e00ffb7f58808"+
        "& ip_address=", user_IP+
        "& fields=country_code,postal_code"
        )
    if response.status_code == 200:
        IP_json = response.json()
        if IP_json['country_code'] != "ES":
            return False
        municipio = Municipios.objects.get( muni_code = IP_json['postal_code'])
        return municipio
    else:
        write_log("Error al localizar al usuario.")
        return False


def weather_consult( IP):
    municipio = IP_location( IP)
    if municipio == False:
        return False
    prov_code = municipio.prov_code.prov_code
    muni_code = municipio.muni_code
    respuesta = requests.get("https://www.el-tiempo.net/api/json/v2/provincias/",prov_code,"/municipios/",muni_code)
    print(respuesta.json())

# Cargamos el index de WeatherNow
def weatherNow( request):
    html_template = loader.get_template('index.html')
    # Parte que se acabará iendo a una API creada con FastAPI
    load_provin()
    load_muni()
    #Cogemos la IP del usuario
    user_IP = request.META.get('REMOTE_ADDR')
    if user_IP == "127.0.0.1":
        weather_consult( "213.229.164.230")
    else:
        weather_consult( user_IP)

    return HttpResponse(html_template.render())