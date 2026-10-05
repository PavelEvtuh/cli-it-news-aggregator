# CLI Агрегатор IT-новостей

Консольная утилита для получения и фильтрации статей с Hacker News.

## Стек технологий
- **Python 3.10+**
- **httpx**: Современный HTTP-клиент
- **Click**: Декларативный CLI-интерфейс
- **Pydantic V2**: Валидация и типизация данных
- **pathlib**: Работа с файловой системой

## Установка и запуск

1. Клонируйте репозиторий:
   \\\ash
   git clone https://github.com/PavelEvtuh/cli-it-news-aggregator.git
   cd cli-it-news-aggregator
   \\\

2. Установите зависимости:
   \\\ash
   pip install -r requirements.txt
   \\\

3. Запустите утилиту:
   \\\ash
   python cli.py --tag python --limit 5
   python cli.py --output results.json
   \\\

## Особенности
- Фильтрация комментариев на стороне клиента
- Строгая валидация данных через Pydantic
- Цветной вывод в терминале с эмодзи
- Сохранение результатов в JSON с правильной кодировкой
