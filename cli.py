from app.dependencies import (
    book_service_builder,
    author_service_builder,
    location_service_builder,
    genre_service_builder,
    state_service_builder
)
import typer
from app.database import session

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

author_app = typer.Typer()
app.add_typer(author_app, name="Authors")

state_app = typer.Typer()
app.add_typer(state_app, name="States")


# ------- BOOKS
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
def update_book(
    title: str,
    author: str = "",
    new_title: str = typer.Option(None, "--new-title"),
    new_author: str = typer.Option(None, "--new-author"),
    genre: str = typer.Option(None, "--genre"),
    state: str = typer.Option(None, "--state"),
    location: str = typer.Option(None, "--location"),
    published: str = typer.Option(None, "--published"),
):
    kwargs = {}
    if new_title:  kwargs["book_title"] = new_title
    if new_author: kwargs["author_name"] = new_author  # Service löst auf
    if genre:      kwargs["genre_name"] = genre
    if state:      kwargs["state_name"] = state
    if location:   kwargs["location_name"] = location

    if published:  
        try:
            parsed_date = datetime.fromisoformat(published)
        except ValueError:
            rprint(":x: invalid date format, please use YYYY-MM-DD")
            return
        
        kwargs["published"] = parsed_date
    try:
        with session() as s:
            service = book_service_builder(s)
            service.update(title, author, **kwargs)

            s.commit()
            rprint(f":white_check_mark: Book '{title}' successfully updated")

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
def search_book(title):
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


# ------- AUTHOR
@author_app.command("add")
def add_author(name: str):
    try:
        with session() as s:
            service = author_service_builder(s)
            service.new(name)
            s.commit()
            rprint(f":white_check_mark: The author '{name}' has been added successfully.")
    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")

@author_app.command("update")
def update_author(name: str, new_name: str):
    try:
        with session() as s:
            service = author_service_builder(s)
            service.update(name, author_name=new_name)
            s.commit()
            rprint(f":white_check_mark: Author '{name}' successfully updated")
    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")
    
@author_app.command("delete")
def delete_author(name: str):
    try:
        with session() as s:
            service = author_service_builder(s)
            service.delete(name)
            s.commit()
            rprint(f":white_check_mark: The author '{name}' was deleted")
    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")
    
@author_app.command("search")
def search_author(name: str):
    try:
        with session() as s:
            service = author_service_builder(s)

            author = service.get(name)

            if author:
                rprint(f":lower_left_fountain_pen: Name: '{author.author_name}'")
            else:
                rprint(":prohibited: Can't find this author!")

    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")

@author_app.command("all")
def list_authors():
    try:
        console = Console()
        with session() as s:
            service = author_service_builder(s)
            console.print("[grey15]-[grey15]" * 30)
            for author in service.list_all():
                rprint(f"Author:    {author.author_name}")

    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")


# ------- LOCATION
@location_app.command("add")
def add_location(shelf: str):
    try:
        with session() as s:
            service = location_service_builder(s)
            location = service.new(shelf)
            s.commit()
            rprint(f":white_check_mark: The location '{location.shelf}' has been added successfully.")
    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")
 
@location_app.command("update")
def update_location(shelf: str, new_shelf: str):
    try:
        with session() as s:
            service = location_service_builder(s)
            service.update(shelf, shelf=new_shelf)
            s.commit()
            rprint(f":white_check_mark: Location '{shelf}' successfully updated to '{new_shelf}'")
    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")
 
@location_app.command("delete")
def delete_location(shelf: str):
    try:
        with session() as s:
            service = location_service_builder(s)
            service.delete(shelf)
            s.commit()
            rprint(f":white_check_mark: The location '{shelf}' was deleted")
    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")
 
@location_app.command("search")
def search_location(shelf: str):
    try:
        with session() as s:
            service = location_service_builder(s)
            location = service.get(shelf)
            if location:
                rprint(f":card_index_dividers: Shelf: '{location.shelf}'")
            else:
                rprint(":prohibited: Can't find this location!")
    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")


# ------- GENRE
@genre_app.command("add")
def add_genre(name: str):
    try:
        with session() as s:
            service = genre_service_builder(s)
            genre = service.new(name)
            s.commit()
            rprint(f":white_check_mark: The genre '{genre.genre_name}' has been added successfully.")
    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")

@genre_app.command("update")
def update_genre(name: str, new_name: str):
    try:
        with session() as s:
            service = genre_service_builder(s)
            service.update(name, genre_name=new_name)
            s.commit()
            rprint(f":white_check_mark: Genre '{name}' successfully updated to '{new_name}'")
    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")
 
@genre_app.command("delete")
def delete_genre(name: str):
    try:
        with session() as s:
            service = genre_service_builder(s)
            service.delete(name)
            s.commit()
            rprint(f":white_check_mark: The genre '{name}' was deleted")
    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")
 
@genre_app.command("search")
def search_genre(name: str):
    try:
        with session() as s:
            service = genre_service_builder(s)
            genre = service.get(name)
            if genre:
                rprint(f":books: Genre: '{genre.genre_name}'")
            else:
                rprint(":prohibited: Can't find this genre!")
    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")


# ------- STATES
@state_app.command("add")
def add_state(name: str):
    try:
        with session() as s:
            service = state_service_builder(s)
            state = service.new(name)
            s.commit()
            rprint(f":white_check_mark: The state '{state.state_name}' has been added successfully.")
    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")
 
@state_app.command("update")
def update_state(name: str, new_name: str):
    try:
        with session() as s:
            service = state_service_builder(s)
            service.update(name, state_name=new_name)
            s.commit()
            rprint(f":white_check_mark: State '{name}' successfully updated to '{new_name}'")
    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")
 
@state_app.command("delete")
def delete_state(name: str):
    try:
        with session() as s:
            service = state_service_builder(s)
            service.delete(name)
            s.commit()
            rprint(f":white_check_mark: The state '{name}' was deleted")
    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")
 
@state_app.command("search")
def search_state(name: str):
    try:
        with session() as s:
            service = state_service_builder(s)
            state = service.get(name)
            if state:
                rprint(f":label: State: '{state.state_name}'")
            else:
                rprint(":prohibited: Can't find this state!")
    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")
 
@state_app.command("all")
def list_states():
    try:
        console = Console()
        with session() as s:
            service = state_service_builder(s)
            console.print("[grey15]-[grey15]" * 30)
            for state in service.list_all():
                rprint(f"State:     {state.state_name}")
            console.print("[grey15]-[grey15]" * 30)
    except ValueError as e:
        rprint(f":x: One of the argument is faulty: {e}")
    except Exception as e:
        rprint(f":x: An unexpected Error has ocurred: {e}")


if __name__ == "__main__":
    app()