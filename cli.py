import json
import click
from pathlib import Path
from fetcher import fetch_news


@click.command()
@click.option('--tag', type=str, default='', help='Фильтр по тегу в заголовке или URL статьи')
@click.option('--limit', type=int, default=5, help='Количество статей для вывода (по умолчанию 5)')
@click.option(
    '--output', 
    type=click.Path(file_okay=True, dir_okay=False, writable=True, path_type=str),
    default='output/news.json',
    help='Путь для сохранения результатов (JSON)'
)
def fetch(tag, limit, output):
    """CLI-агрегатор IT-новостей с Hacker News."""
    results = fetch_news(tag=tag, limit=limit)
    print(f"DEBUG: fetcher вернул {len(results)} статей")
    if not results:
        click.secho("❌ Статьи не найдены. Попробуйте другой тег или увеличьте лимит.", fg="red")
        return
    
    # ✅ Сериализация Pydantic моделей в JSON-совместимые словари
    serialized = [article.model_dump(mode='json') for article in results]
    json_string = json.dumps(serialized, indent=2, ensure_ascii=False)
    
    # ✅ Безопасное создание директории и запись файла
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json_string, encoding='utf-8')
    
    # ✅ Вывод результатов в консоль
    click.secho(f"✅ Найдено {len(results)} статей:\n", fg="green")
    for i, article in enumerate(results, 1):
        click.echo(f"{i}. 📰 {article.title}")
        click.echo(f"   🔗 {article.url}")
        click.echo(f"   👤 {article.author} |  {article.created_at:%d.%m.%Y %H:%M}")
        click.echo("-" * 60)
    
    # ✅ Подтверждение сохранения
    click.secho(f"\n💾 Сохранено в: {output_path}", fg="cyan")


if __name__ == '__main__':
    fetch()