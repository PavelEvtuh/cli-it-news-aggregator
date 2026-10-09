from datetime import datetime
import pytest
from models import Article
from pydantic import ValidationError


def test_valid_article_creation():
    """Проверяет создание валидной статьи из словаря."""
    # 1. Подготовка данных (Arrange)
    data = {
        "title": "Test Title",
        "url": "https://example.com",
        "author": "test_author",
        "created_at": "2026-10-09T12:00:00Z"
    }
    
    # 2. Выполнение действия (Act)
    article = Article(**data)
    
    # 3. Проверка результата (Assert)
    assert article.title == "Test Title"
    assert str(article.url) == "https://example.com/"
    assert isinstance(article.created_at, datetime)


def test_invalid_url_raises_error():
    """Проверяет, что невалидный URL вызывает ошибку валидации."""
    data = {
        "title": "Test",
        "url": "not-a-valid-url", # ❌ Ошибка здесь
        "author": "test",
        "created_at": "2026-10-09T12:00:00Z"
    }
    
    # Мы ожидаем, что Pydantic выбросит ошибку
    with pytest.raises(ValidationError):
        Article(**data)