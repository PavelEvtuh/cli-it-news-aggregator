import logging
import sys
from pathlib import Path

from settings import settings


def setup_logging() -> None:
    """Настраивает логирование: файл + консоль."""
    # Создаём директорию для логов
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Получаем уровень логирования из настроек
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Формат сообщений
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 1. Логгер в файл (все уровни DEBUG+)
    file_handler = logging.FileHandler(filename=log_dir / "app.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # 2. Логгер в консоль (только WARNING+, чтобы не спамить пользователю)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)

    # Настраиваем корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
