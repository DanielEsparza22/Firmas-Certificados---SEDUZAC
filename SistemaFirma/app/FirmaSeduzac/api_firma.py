import requests
import json

url = "http://api-firma.k8.seduzac.gob.mx/sello-json"

payload = json.dumps({
"rfc": "SAFC7105149R3",
"documento": "certificado",
"sistema": "certificacion",
"cadena": "||1.0|3|SAFC710514MDFLLR06|Secretaria de Educación|SECRETARÍA DE EDUCACIÓN DEL ESTADO DE ZACATECAS|Secretaría de Educación del Estado de Zacatecas|32EBH0010L|000|32|FOCA070804MZSLSRA1|AURORA MARGARITA|FLORES|CASTRELLON|4|C|2024-05-07T12:00:00||"
})
headers = {
'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)