import requests
import json
from requests import post
print(post(f'http://127.0.0.1:5000/api/foods',
           json={'name': 'Фрика',
                 'user_id': 1,
                 'storage_life': '2020-20-14',
                 'count': 111,
                 'category': 'berry',
                 'count_units': 11,
                 "purchase_date": '2020-11-14'}).json())