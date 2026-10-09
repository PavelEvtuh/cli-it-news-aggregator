import json
import csv
import click
import logging
from pathlib import Path
from fetcher import fetch_news
from logger_setup import setup_logging
from settings import settings

# Настраиваем логирование ОДИН РАЗ при старте
setup_logging()
logger = logging.getLogger(__name__)


@click.command()
@click.option('--tag', type=str, default='', help='Фильтр по тегу в заголовке или URL')
@click.option('--limit', type=int, default=None, help='Количество статей (по умолчанию из .env)')
@click.option('--output', type=click.Path(writable=True, path_type=str),
              default=None, help='Путь для сохранения (по умолчанию из .env)')
@click.option('--format', 'fmt', type=click.Choice(['json', 'csv']), default='json',
              help='Формат вывода: json или csv')
def fetch(tag: str, limit: int | None, output: str | None, fmt: str):
    """CLI-агрегатор IT-новостей с Hacker News."""
    # Используем настройки из .env, если параметры не переданы
    effective_output = output or f"{settings.output_dir}/news.{fmt}"
    
    results = fetch_news(tag=tag, limit=limit)
    
    if not results:
        click.secho("❌ Статьи не найдены. Попробуйте другой тег или увеличьте лимит.", fg="red")
        logger.warning("Поиск не дал результатов (tag='%s', limit=%s)", tag, limit)
        return

    # Сохранение в зависимости от формата
    output_path = Path(effective_output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if fmt == 'csv':
        _save_csv(results, output_path)
    else:
        _save_json(results, output_path)

    # Пользовательский вывод (не логи!)
    click.secho(f"✅ Найдено {len(results)} статей:\n", fg="green")
    for i, article in enumerate(results, 1):
        click.echo(f"{i}. 📰 {article.title}")
        click.echo(f"   🔗 {article.url}")
        click.echo(f"   👤 {article.author} | {article.created_at:%d.%m.%Y %H:%M}")
        click.echo("-" * 60)
    click.secho(f"\n💾 Сохранено в: {output_path}", fg="cyan")
    logger.info("Результаты сохранены в %s (формат: %s)", output_path, fmt)


def _save_json(articles, path: Path):
    """Сохраняет статьи в JSON."""
    serialized = [a.model_dump(mode='json') for a in articles]
    path.write_text(json.dumps(serialized, indent=2, ensure_ascii=False), encoding='utf-8')


def _save_csv(articles, path: Path):
    """Сохраняет статьи в CSV с поддержкой кириллицы для Excel."""
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url', 'author', 'created_at'])
        writer.writeheader()
        for a in articles:
            writer.writerow({
                'title': a.title,
                'url': str(a.url),
                'author': a.author,
                'created_at': a.created_at.strftime('%d.%m.%Y %H:%M')
            })
    logger.debug("CSV сохранен: %d строк", len(articles))


if __name__ == '__main__':
    fetch()