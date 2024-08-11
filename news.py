import requests

# Replace 'your_api_key' with your actual API key from News API
api_key = "da8f10bf8bb24d239a3ae495b767486d"
api_address = f"https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey={api_key}"
json_data = requests.get(api_address).json()

ar = []

def news():
    for i in range(3):
        ar.append("Number " + str(i+1) + ": " + json_data["articles"][i]["title"] + ".")
    return ar

arr = news()

print(arr)
