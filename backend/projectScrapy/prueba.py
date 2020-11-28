import os
import requests
import json
from datetime import datetime

if __name__ == "__main__":
    start_time = datetime.now()
    auth = {
        'email': 'admin@email.com',
        'password': 'password1'
    }
    token = requests.post('http://localhost:5000/api/auth/signin/', json=auth)
    token = json.loads(token.text)
    pages = ['computrabajo', 'mipleo', 'workana']
    for page in pages:
        os.system('scrapy crawl ' + page)
        j = open('items.json', 'r', encoding='utf-8')
        jsonItem = j.read().replace(',\n]', ']')
        h = {'Authorization': 'Bearer ' + token['userSession']['access_token'],
            'Scrapy': 'scrapy'
        }
        r = requests.post('http://localhost:5000/api/jobs/a/' + page, json = jsonItem, headers=h)
        print(r.status_code, page)
    end_time = datetime.now()
    print(end_time - start_time)