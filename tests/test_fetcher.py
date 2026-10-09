import pytest
import respx
from httpx import Response
from fetcher import fetch_news


@respx.mock
def test_fetch_news_success():
    """Проверяет получение статей при успешном ответе API."""
    # 1. Готовим фейковый ответ от API
    fake_response = {
        "hits": [
            {
                "title": "Test Article",
                "url": "https://example.com",
                "author": "test_user",
                "created_at_i": 1728489600, # Unix timestamp
                "objectID": "123"
            }
        ]
    }
    
    # 2. Подменяем реальный запрос на наш фейк
    route = respx.get(url__startswith="https://hn.algolia.com").mock(
        return_value=Response(200, json=fake_response)
    )
    
    # 3. Запускаем функцию
    results = fetch_news(limit=1)
    
    # 4. Проверяем результат
    assert len(results) == 1
    assert results[0].title == "Test Article"
    assert route.called # Убеждаемся, что запрос действительно был сделан


@respx.mock
def test_fetch_news_empty_response():
    """Проверяет обработку пустого ответа от API."""
    respx.get(url__startswith="https://hn.algolia.com").mock(
        return_value=Response(200, json={"hits": []})
    )
    
    results = fetch_news(limit=1)
    assert len(results) == 0