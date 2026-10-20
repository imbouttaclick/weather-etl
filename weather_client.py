import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=True)

def get_weather_forecast(city, lat, lon):
    api_key = os.getenv('WEATHER_API_KEY')
    
    base_url = os.getenv('WEATHER_API_BASE_URL', 'https://api.openweathermap.org/data/2.5/forecast')
    
    params = {
        'appid': api_key,
        'units': 'metric',
        'lang': 'ru'
    }
    
    if lat and lon:
        params.update({'lat': lat, 'lon': lon})
    else:
        params.update({'q': city})

    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Ошибка API погоды: {e}")
        return []

    daily_data = {}
    
    for item in data.get('list', []):
        date_str, time_str = item['dt_txt'].split(' ')
        
        if date_str not in daily_data:
            daily_data[date_str] = {
                'temp_min': item['main']['temp_min'],
                'temp_max': item['main']['temp_max'],
                'humidity_sum': 0,
                'count': 0,
                'wind_speed': item['wind']['speed'],
                'description': item['weather'][0]['description']
            }
            
        day = daily_data[date_str]
        day['temp_min'] = min(day['temp_min'], item['main']['temp_min'])
        day['temp_max'] = max(day['temp_max'], item['main']['temp_max'])
        day['humidity_sum'] += item['main']['humidity']
        day['count'] += 1
        day['wind_speed'] = max(day['wind_speed'], item['wind']['speed'])
        
        if time_str == '12:00:00':
            day['description'] = item['weather'][0]['description']

    results = []
    for d_str in sorted(daily_data.keys())[:4]:
        d = daily_data[d_str]
        results.append({
            'date': datetime.strptime(d_str, '%Y-%m-%d').date(),
            'temp_min': round(d['temp_min'], 1),
            'temp_max': round(d['temp_max'], 1),
            'humidity': d['humidity_sum'] // d['count'],
            'wind_speed': round(d['wind_speed'], 1),
            'description': d['description']
        })
    return results