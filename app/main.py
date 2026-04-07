import requests


payload = {
    "text": "오늘 날씨 어떤가요?"
}


response = requests.post(
    url="http://localhost:8000/predict", 
    json=payload
)

print(response.json())