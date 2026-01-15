import requests
import json

url = "http://localhost:5000/analyze"

test_cases = [
    {
        "name": "Likely Real",
        "text": "The local library is opening a new wing next month. Community members are invited to attend the ribbon-cutting ceremony. The project was funded by a grant from the city council."
    },
    {
        "name": "Likely Fake - Mixed",
        "text": "BREAKING: Scientists are SHOCKED! This 100% safe miracle cure heals ALL diseases instantly. Share before it's deleted! ACT NOW!"
    }
]

for case in test_cases:
    print(f"Testing: {case['name']}")
    response = requests.post(url, json={"text": case['text']})
    data = response.json()
    print(f"Score: {data.get('trust_score')}, Label: {data.get('label')}")
    print("-" * 20)
