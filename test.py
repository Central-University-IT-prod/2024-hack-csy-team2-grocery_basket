import requests
import json
from requests import post, get

print(get(f'http://127.0.0.1:5000/api/conditions/1').json())
