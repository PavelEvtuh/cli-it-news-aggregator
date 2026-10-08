from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class Article(BaseModel):
    """Модель статьи Hacker News для валидации и сериализации."""

    model_config = ConfigDict(extra="ignore")

    title: str
    url: HttpUrl
    author: str
    created_at: datetime
