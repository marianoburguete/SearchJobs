import os
import requests
import json

if __name__ == "__main__":
    # os.system('scrapy crawl computrabajo')
    # os.system('scrapy crawl mipleo')
    #os.system('scrapy crawl workana')

    j = open('items.json', 'r', encoding='utf-8')
    jsonItem = json.load(j)
    aaaa = json.dumps(jsonItem, ensure_ascii=False).encode('utf-8').decode()
    h = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MjEyODg2MDUsImlhdCI6MTYwMzI4ODYwNSwic3ViIjozLCJyb2xlIjoiZnVuY2lvbmFyaW8ifQ.99yssqEyh0d7-XLfmiW31AfjT8QEbox0f4_wp7QT5LY',
        'Scrapy': 'scrapy'
    }
    r = requests.post('http://localhost:5000/api/jobs/a/workana', json = aaaa, headers=h)
    print(r.status_code)