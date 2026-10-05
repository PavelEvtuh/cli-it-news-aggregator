from pydantic import BaseModel, HttpUrl, ConfigDict, ValidationError
from datetime import datetime


class Article(BaseModel):
    model_config = ConfigDict(extra='ignore')
    
    title: str
    url: HttpUrl
    author: str
    created_at: datetime

if __name__ == "__main__":
    # Скопируй ОДИН объект hits из браузера: 
    # https://hn.algolia.com/api/v1/search_by_date?hitsPerPage=5
    test_data = {
        "title": "Figma restricts MCP access to whitelisted clients, excluding Pi",      # вставь реальный заголовок
        "url": "https://twitter.com/GayaniFigma/status/2105295629941350454",        # вставь реальную ссылку
        "author": "matchLevel",     # вставь реального автора
        "created_at": "2026-10-01T19:28:39Z"   # вставь реальное число (unix timestamp)
    }
    
    try:
        article = Article(**test_data)
        print(f"✅ Модель работает!")
        print(f"   Заголовок: {article.title}")
        print(f"   Дата: {article.created_at}")
        print(f"   URL: {article.url}")
    except ValidationError as e:
        print(f"❌ Ошибка валидации:")
        print(e)