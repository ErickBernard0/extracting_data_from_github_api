
# PACOTES
import pandas as pd
import requests
import json
import dotenv

# PARÂMETROS
url_base = 'http://api.github.com/events'

# CÓDIGO
response = requests.get(url_base)

print(response.json())