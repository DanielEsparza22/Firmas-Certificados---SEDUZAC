from django.db import connection, connections
import requests
import json
from datetime import datetime
from .models import FolioSequencePE

def api_firma(rfc, documento, sistema, cadena):
    url = "http://api-firma.k8.seduzac.gob.mx/sello-json"

    payload = json.dumps({
    "rfc": rfc, #"SAFC7105149R3",
    "documento": documento, #"certificado",
    "sistema": sistema, #"certificacion",
    "cadena": cadena #"||1.0|3|SAFC710514MDFLLR06|Secretaria de Educación|SECRETARÍA DE EDUCACIÓN DEL ESTADO DE ZACATECAS|Secretaría de Educación del Estado de Zacatecas|32EBH0010L|000|32|FOCA070804MZSLSRA1|AURORA MARGARITA|FLORES|CASTRELLON|4|C|2024-05-07T12:00:00||"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)

    return response.text

def fecha_a_texto(fecha_str):
    meses = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio',
        7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
    }
    numeros = {
        0: 'cero', 1: 'uno', 2: 'dos', 3: 'tres', 4: 'cuatro', 5: 'cinco', 6: 'seis',
        7: 'siete', 8: 'ocho', 9: 'nueve', 10: 'diez', 11: 'once', 12: 'doce',
        13: 'trece', 14: 'catorce', 15: 'quince', 16: 'dieciseis', 17: 'diecisiete',
        18: 'dieciocho', 19: 'diecinueve', 20: 'veinte', 21: 'veintiuno', 22: 'veintidós',
        23: 'veintitres', 24: 'veinticuatro', 25: 'veinticinco', 26: 'veintiseis',
        27: 'veintisiete', 28: 'veintiocho', 29: 'veintinueve', 30: 'treinta', 31: 'treinta y uno'
    }
    anios = {
        2024: 'dos mil veinticuatro',
        2025: 'dos mil veinticinco'
    }

    fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")

    dia = fecha.day
    mes = fecha.month
    anio = fecha.year

    dia_texto = numeros[dia]
    mes_texto = meses[mes]
    anio_texto = anios.get(anio, str(anio))

    resultado = f"{dia_texto} días del mes de {mes_texto} del año {anio_texto}"
    return resultado

def reiniciar_secuencia_folio():
    with connection.cursor() as cursor:
        FolioSequencePE.objects.all().delete()

        cursor.execute("ALTER TABLE BachilleratoDistanciaApp_foliosequencebd AUTO_INCREMENT = 1;")