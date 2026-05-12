from dependencies import (
    book_service_builder,
    author_service_builder,
    location_service_builder,
)
import typer
from database import session

from rich import print as rprint
from rich.console import Console
from datetime import datetime


app = typer.Typer()

books_app = typer.Typer()
app.add_typer(books_app, name="Books")

genre_app = typer.Typer()
app.add_typer(genre_app, name="Genres")

location_app = typer.Typer()
app.add_typer(location_app, name="Locations")

@books_app.command("add")
def add_book(
    title: str,
    author: str,
    genre: str,
    state: str,
    location: str,
    published: str = typer.Option("1900-01-01", help="Format: YYYY-MM-DD")
) -> None:
    try:
        parsed_date = datetime.fromisoformat(published)
    except ValueError:
        rprint(":x: invalid date format, please use YYYY-MM-DD")
        return
    
    try:
        
        with session() as s:
            service = book_service_builder(s)

            book = service.create_book(
                title=title,
                author_name=author,
                genre_name=genre,
                state_name=state,
                location_name=location,
                published=parsed_date
            )

            s.commit()
            rprint(f":white_check_mark: The book '{book.book_title}' has been added successfully.")

    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")

    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")

@books_app.command("update")
def update_book(title: str, author: str = "", **kwargs):
    try:
        with session() as s:
            service = book_service_builder(s)
            service.update(title, author, **kwargs)

            s.commit()
            rprint(f"Book {title} successfully updated")

    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")

    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")    

@books_app.command("delete")
def delete_book(title: str, author: str = ""):
    try:
    
        with session() as s:
            service = book_service_builder(s)

            service.delete(title, author)

            s.commit()
            rprint(f":white_check_mark: The book '{title}' was deleted")

    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")

    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")

@books_app.command("search")
def fetch_book(title):
    try:
        with session() as s:
            service = book_service_builder(s)

            book = service.get(title)

            if book:
                rprint(f":book: Title: '{book.book_title}', Autor: '{book.author.author_name}', published: {book.published}")
            else:
                rprint(":prohibited: Can't find this book!")

    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")

    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")

@books_app.command("all")
def list_books():
    try:
        console = Console()
        with session() as s:
            service = book_service_builder(s)

            console.print("[grey15]-[grey15]" * 30)
            for book in service.list_all():
                rprint(f"Title:     {book.book_title}")
                rprint(f"Author:    {book.author.author_name}")
                rprint(f"Published: {book.published}")
                console.print("[grey15]-[grey15]" * 30)

    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")

    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")

@location_app.command("add")
def add_location(name: str):
    print(f"deleted a location: {name}")


if __name__ == "__main__":
    app()