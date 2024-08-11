import requests
#from ss2 import key2  # Ensure key2 is defined in the ss2 module

# OpenWeatherMap API URL with your API key
api_address = f'https://api.openweathermap.org/data/2.5/weather?id=1267701&appid={"04c5779ab395db55356ebb3467424423"}'
json_data = requests.get(api_address).json()

def temp():
    temperature = round(json_data["main"]["temp"] - 273.15, 1)  # Corrected the spelling and conversion
    return temperature

def des():
    description = json_data["weather"][0]["description"]
    return description

print(temp())
print(des())
