from dependencies import (
    book_service_builder,
    author_service_builder,
    location_service_builder,
)
import typer
from database import session

from rich import print as rprint
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
            rprint(f":white_check_mark: The book {book.book_title} has been added successfully.")

    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")

    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")


@books_app.command("delete")
def delete_book(title: str):
    print(f"Deleted a Book: {title}")



@location_app.command("add")
def add_location(name: str):
    print(f"deleted a location: {name}")


if __name__ == "__main__":
    app()