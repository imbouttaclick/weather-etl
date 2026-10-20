from dotenv import load_dotenv
load_dotenv()

from db_models import get_session, WeatherForecast
from geo_locator import get_location
from weather_client import get_weather_forecast
from exporter import export_to_markdown

def main():
    print("1. Определение локации...")
    city, lat, lon = get_location()
    print(f"Локация: {city} ({lat}, {lon})")

    print("2. Получение прогноза из OpenWeatherMap...")
    forecast_data = get_weather_forecast(city, lat, lon)
    if not forecast_data:
        print("Прогноз не получен. Завершение работы.")
        return

    print("3. Сохранение данных в SQLite...")
    session = get_session()
    saved_count = 0
    
    for item in forecast_data:
        exists = session.query(WeatherForecast).filter_by(city=city, forecast_date=item['date']).first()
        if not exists:
            new_record = WeatherForecast(
                city=city,
                forecast_date=item['date'],
                temp_min=item['temp_min'],
                temp_max=item['temp_max'],
                humidity=item['humidity'],
                wind_speed=item['wind_speed'],
                description=item['description']
            )
            session.add(new_record)
            saved_count += 1
            
    session.commit()
    
    print("4. Выгрузка в Markdown...")
    export_to_markdown(session, city)
    print("Процесс завершен.")

if __name__ == '__main__':
    main()