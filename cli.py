from dependencies import (
    book_service_builder,
    author_service_builder,
    location_service_builder,
)
from typer import Typer


app = Typer()

books = Typer()
app.add_typer(books, name="Books")

genre = Typer()
app.add_typer(genre, name="Genres")

location = Typer()
app.add_typer(location, name="Locations")

@books.command("add")
def add_book(title: str):
    print(f"Added a new book: {title}")

@books.command("delete")
def delete_book(title: str):
    print(f"Deleted a Book: {title}")

@location.command("add")
def add_location(name: str):
    print(f"deleted a location: {name}")


if __name__ == "__main__":
    app()