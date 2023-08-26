import requests

url = 'https://api.coindesk.com/v1/bpi/currentprice.json'

response = requests.get(url).json()

for curr in response['bpi']:
    print(f"{curr} {response['bpi'][curr]['rate']}")
