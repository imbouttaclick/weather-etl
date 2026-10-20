import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

def get_location():
    try:
        url = os.getenv('GEO_API_URL', 'http://ip-api.com/json/')
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if 'city' in data and 'lat' in data and 'lon' in data:
            return data['city'], data['lat'], data['lon']
    except requests.RequestException as e:
        print(f"Предупреждение гео-API: {e}")
    
    fallback_city = os.getenv('GEO_API_FALLBACK_CITY')
    fallback_lat = os.getenv('GEO_API_FALLBACK_LAT')
    fallback_lon = os.getenv('GEO_API_FALLBACK_LON')
    
    if fallback_lat and fallback_lon:
        city_name = fallback_city if fallback_city else "Неизвестная локация"
        print(f"Используем резервные координаты из .env: {city_name} ({fallback_lat}, {fallback_lon})")
        return city_name, float(fallback_lat), float(fallback_lon)
    
    elif fallback_city:
        print(f"Используем резервный город из .env: {fallback_city}")
        return fallback_city, None, None
    
    else:
        raise ValueError(
            "Критическая ошибка: Не удалось определить геолокацию через API, "
            "а в файле .env отсутствуют параметры GEO_API_FALLBACK_LAT/LON и GEO_API_FALLBACK_CITY."
        )