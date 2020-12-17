import os
import requests
import json
from datetime import datetime
import time
from datetime import timedelta

apiUrl = 'http://localhost:5000/api/'


if __name__ == "__main__":
    auth = {
        'email': '',
        'password': ''
    }

    minutes = 120

    while True:
        print('Ingrese los datos de una cuenta tipo administrador')
        print('Email: ')
        auth['email'] = input()
        print('Contraseña: ')
        auth['password'] = input()
        token = requests.post(apiUrl + 'auth/signin/', json=auth)
        if token.status_code == 200:
            break;
        else:
            print('Los datos ingresados no son válidos, vuelva a intentarlo')

    print('Ingrese cada cuantos minutos quiere que se corra el script')
    minutes = int(input())
    print(type(minutes))

    while True:
        start_time = datetime.now()
        token = requests.post(apiUrl + 'auth/signin/', json=auth)
        token = json.loads(token.text)
        pages = ['computrabajo', 'mipleo', 'workana']
        for page in pages:
            print('Realizando scraping en ' + page)
            os.system('scrapy crawl --nolog ' + page)
            j = open('items.json', 'r', encoding='utf-8')
            jsonItem = j.read().replace(',\n]', ']')
            h = {'Authorization': 'Bearer ' + token['userSession']['access_token'],
                'Scrapy': 'scrapy'
                }
            print('Ingresando los datos obtenidos en la base de datos')
            r = requests.post(apiUrl + 'jobs/a/' + page, json=jsonItem, headers=h)
            if r.status_code == 201:
                print('Datos obtenidos de ' + page + ' ingresados')
            else:
                print('Ocurrio un error ingresando los datos provenientes de ' + page)
        end_time = datetime.now()
        print('Escaneadas todas las paginas, tiempo transcurrido desde el inicio:',end_time - start_time)
        print('Se volvera a ejecutar un rastreo de datos el ', datetime.now() + timedelta(days=1))
        time.sleep(60 * minutes)