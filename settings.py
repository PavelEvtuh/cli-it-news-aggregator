from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Конфигурация приложения. Загружает данные из .env и переменных окружения."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    hn_api_url: str = "https://hn.algolia.com/api/v1/search_by_date"
    default_limit: int = 5
    output_dir: str = "output"
    log_level: str = "INFO"


settings = Settings()