from typing import List

import httpx

from models import Article


def fetch_news(tag: str = "", limit: int = 5) -> List[Article]:
    """Получает статьи с HN API, фильтрует и валидирует через Pydantic."""
    url = f"https://hn.algolia.com/api/v1/search_by_date?hitsPerPage={limit * 3}"

    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict):
            raise ValueError("Ответ не является JSON-объектом")

        hits = data.get("hits", [])

        # Фильтрация: статья = есть url И нет comment_text
        articles = [hit for hit in hits if "url" in hit and "comment_text" not in hit]

        # Фильтрация по тегу в заголовке/URL (если тег задан)
        if tag:
            tag_lower = tag.lower()
            articles = [
                a for a in articles if tag_lower in a.get("title", "").lower() or tag_lower in a.get("url", "").lower()
            ]

        # Валидация через Pydantic
        validated_articles: List[Article] = []
        for art_dict in articles[:limit]:
            try:
                validated_articles.append(Article(**art_dict))
            except Exception as e:
                print(f"️ Пропущена статья из-за ошибки валидации: {e}")

        return validated_articles  # ✅ Только один return

    except httpx.RequestError as e:
        print(f"❌ Ошибка сети: {e}")
        return []
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP ошибка {e.response.status_code}: {e.response.text}")
        return []
    except ValueError as e:
        print(f"❌ Ошибка данных: {e}")
        return []


if __name__ == "__main__":
    # ✅ Вызываем функцию и сохраняем результат
    results = fetch_news(tag="", limit=3)

    print(f"Найдено валидных статей: {len(results)}\n")
    for article in results:
        print(f"📰 {article.title}")
        print(f"   🔗 {article.url}")
        print(f"   👤 {article.author}")
        print(f"   📅 {article.created_at}")
        print("-" * 60)
