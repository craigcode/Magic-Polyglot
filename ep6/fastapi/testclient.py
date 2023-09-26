import http.client
import json
import os
from configparser import ConfigParser


config = ConfigParser()
config.read(".config")
config = config["AUTH0"]

client_id = config["CLIENT_ID"]
client_secret = config["CLIENT_SECRET"]
api_audience = config["API_AUDIENCE"]


conn = http.client.HTTPSConnection("craigmartin.auth0.com")

payload = "{\"client_id\":\""+client_id+"\",\
    \"client_secret\":\""+client_secret+"\",\
    \"audience\":\""+api_audience+"\",\
    \"grant_type\":\"client_credentials\"}"


headers = { "content-type": "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

res = json.loads(data.decode("unicode_escape"))

try:
    token = res["access_token"]
    print("JWT="+token)
    print()
except:
    token = ""

server = "127.0.0.1"
port = 8000

conn = http.client.HTTPConnection(server, port)

headers = { "authorization": f"Bearer {token}" }

conn.request("GET", "/api/private", headers=headers)

res = conn.getresponse()
data = res.read()

print("payload="+data.decode("unicode_escape"))
