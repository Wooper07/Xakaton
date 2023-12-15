import requests
import json
from geopy.geocoders import Nominatim
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def getData():
    # Создаем объект геокодера
    geolocator = Nominatim(user_agent="my_geocoder")
    Por = "City"
    # Название города для поиска координат
    city_name = f"Yuzhno Sakhalinsk {Por}"
    # Получаем координаты (широта и долгота)
    location = geolocator.geocode(city_name)

    if location:
        latitude, longitude = location.latitude, location.longitude
        print(f"Coordinates for {city_name}: Latitude {latitude}, Longitude {longitude}")
    else:
        print(f"Coordinates for {city_name} not found.")
    # URL-запрос для API airvisual с добавлением параметра country=Russia
    url = f'http://api.airvisual.com/v2/nearest_city?lat={latitude}&lon={longitude}&key=d05111d1-53ce-42ae-80db-a1cb25a356d7&country=Russia'
    res2 = requests.get(url)
    # Проверяем успешность запроса (статус код 200)
    if res2.status_code == 200:
        # Загружаем JSON-данные из ответа
        data = res2.json()
        # Проверяем, что страна в ответе соответствует "Russia"
        if data.get('data', {}).get('country') == 'Russia':
            # Красиво выводим JSON-данные
            formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
            # return (formatted_json)
        else:
            return (f"Data for {city_name} is not in Russia.")
    else:
        return(f"Error: {res2.status_code}")
 