import requests
import json

url = "http://localhost:5000/analyze"
payload = {
    "text": "SHOCKING: Scientists are SHOCKED by this 100% effective miracle cure that heals ALL diseases instantly! Share before this gets deleted! ACT NOW!"
}
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
print(json.dumps(response.json(), indent=4))
