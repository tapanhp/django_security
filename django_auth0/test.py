import requests
import json

headers = {
    'content-type': 'application/x-www-form-urlencoded',
}

data = {
    'grant_type': 'client_credentials',
    'client_id': 'sbiluTSF1zAHV7WY9k5edttsf57LVq0W',
    'client_secret': 'ZFYRWZDVT7htmY7qwwh5Nfa-TtfJCr2NNWB6RVzqXFLv0e78seas0yGSQA7smi4U',
    'audience': 'https://django-auth0/api'
}

response = requests.post('', headers=headers, data=data)  # auth token url

with open("access_token.json", "w") as f:
    f.write(json.dumps(response.json()))
