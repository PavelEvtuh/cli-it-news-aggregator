import logging
from datetime import datetime
from typing import List

import httpx
from pydantic import ValidationError

from models import Article
from settings import settings

logger = logging.getLogger(__name__)


def fetch_news(tag: str = "", limit: int | None = None) -> List[Article]:
    """Получает статьи с HN API, фильтрует и валидирует через Pydantic."""
    effective_limit = limit if limit is not None else settings.default_limit
    url = f"{settings.hn_api_url}?hitsPerPage={effective_limit * 3}"

    logger.info("Запрос к HN API: %s", url)

    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict):
            raise ValueError("Ответ API не является JSON-объектом")

        hits = data.get("hits", [])
        logger.debug("Получено %d сырых записей от API", len(hits))

        # Фильтрация: статья = есть url И нет comment_text
        articles = [hit for hit in hits if "url" in hit and "comment_text" not in hit]

        # Фильтрация по тегу в заголовке/URL (если тег задан)
        if tag:
            tag_lower = tag.lower()
            articles = [
                a for a in articles 
                if tag_lower in a.get("title", "").lower() or tag_lower in a.get("url", "").lower()
            ]
            logger.info("Найдено %d статей по тегу '%s'", len(articles), tag)

        # Валидация через Pydantic
        validated_articles: List[Article] = []
        for art_dict in articles[:effective_limit]:
            try:
                # Преобразуем created_at_i в created_at для модели
                if "created_at_i" in art_dict:
                    art_dict["created_at"] = datetime.fromtimestamp(art_dict["created_at_i"]).isoformat() + "Z"
                
                validated_articles.append(Article(**art_dict))
            except ValidationError as e:
                logger.warning("Пропущена невалидная статья: %s", e)

        logger.info("Валидацию прошло %d статей", len(validated_articles))
        return validated_articles

    except httpx.RequestError as e:
        logger.error("Ошибка сети при запросе к HN API: %s", e)
        return []
    except httpx.HTTPStatusError as e:
        logger.error("HTTP ошибка %s: %s", e.response.status_code, e.response.text)
        return []
    except ValueError as e:
        logger.error("Ошибка данных от API: %s", e)
        return []