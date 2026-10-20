import os
from db_models import WeatherForecast

def export_to_markdown(session, city):
    output_file = os.getenv('OUTPUT_FILE', 'weather_report.md')
    # сортировка по дате
    forecasts = session.query(WeatherForecast).filter_by(city=city).order_by(WeatherForecast.forecast_date).all()
    
    if not forecasts:
        print("Нет данных для выгрузки.")
        return

    start_date = forecasts[0].forecast_date
    end_date = forecasts[-1].forecast_date

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Прогноз погоды\n\n")
        f.write(f"Автоматически определённая локация: {city}  \n")
        f.write(f"Период: {start_date} – {end_date}  \n\n")
        f.write("| Дата       | Мин. темп. (°C) | Макс. темп. (°C) | Описание              | Влажность (%) | Ветер (м/с) |\n")
        f.write("|------------|-----------------|------------------|-----------------------|---------------|-------------|\n")
        
        for fc in forecasts:
            f.write(f"| {fc.forecast_date} | {fc.temp_min:<15} | {fc.temp_max:<16} | {fc.description.capitalize():<21} | {fc.humidity:<13} | {fc.wind_speed:<11} |\n")
            
    print(f"Отчет сохранен в {output_file}")