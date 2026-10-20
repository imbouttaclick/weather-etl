# Weather ETL Lab

Автоматическое определение локации пользователя (IP Geolocation), получение прогноза погоды на 4 дня (OpenWeatherMap), сохранение в SQLite и выгрузка отчета в Markdown.

## Установка и запуск

1. Клонируйте репозиторий и перейдите в папку проекта.
2. Создайте виртуальное окружение и активируйте его:
   `python -m venv venv`
   `source venv/bin/activate` (для Mac/Linux) или `venv\Scripts\activate` (для Windows)
3. Установите зависимости:
   `pip install -r requirements.txt`
4. Скопируйте файл конфигурации:
   `cp .env.example .env`
5. Зарегистрируйтесь на `openweathermap.org`, получите бесплатный API ключ и впишите его в файл `.env`.
6. Запустите скрипт:
   `python main.py`

## Структура проекта
* `main.py` — основной файл, управляющий ETL процессом.
* `geo_locator.py` — определение координат.
* `weather_client.py` — получение и агрегация погоды.
* `db_models.py` — схема базы данных SQLite.
* `exporter.py` — выгрузка обработанных данных.