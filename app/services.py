from app.repos import (
    BooksRepo,
    GenresRepo,
    LocationsRepo,
    AuthorsRepo, 
    StatesRepo
)
from app.model import Genres, Locations, Authors, Books, States
from app.database import session as db
from sqlalchemy.orm import Session

from datetime import datetime


class GenreService:
    def __init__(self, session: Session, genre_repo: GenresRepo):
        self.session = session
        self.genre_repo = genre_repo

    def _normalized(self, name: str) -> str:
        return name.strip().capitalize()

    def get(self, name: str) -> Genres | None:
        return self.genre_repo.get_genre_by_name(
            self._normalized(name))

    def new(self, name: str) -> Genres:
        new_genre = self.get(name)
        if new_genre:
            raise ValueError(f"Genre {new_genre} already exists!")

        genre = self.genre_repo.create_genre(
            self._normalized(name))
        
        return genre
    
    def delete(self, name: str) -> None:
        genre = self.get(name)
        if not genre:
            raise ValueError(f"Genre {name} not found!")
        
        self.genre_repo.delete_genre(genre)

    def update(self, name: str, **kwargs) -> Genres | None:
        genre = self.get(name)
        if not genre:
            raise ValueError(f"Genre {name} nicht gefunden!")
        
        return self.genre_repo.update_genre(genre, **kwargs)
        
class LocationService:
    def __init__(self, session: Session, location_repo: LocationsRepo):
        self.session = session
        self.location_repo = location_repo

    def _normalized(self, name: str) -> str:
        return name.strip()

    def get(self, name: str) -> Locations | None:
        return self.location_repo.get_location_by_name(
            self._normalized(name))
    
    def get_by_id(self, id: int) -> Locations | None:
        return self.location_repo.get_location_by_id(id)

    def new(self, name: str):
        new_location = self.get(name)
        if new_location:
            raise ValueError(f"location {new_location} already exists!")

        location = self.location_repo.create_location(
            self._normalized(name))
        
        return location
    
    def delete(self, name: str) -> None:
        location = self.get(name)       
        if not location:
            raise ValueError(f"location '{name}' not found!")
        self.location_repo.delete_location(location)

    def update(self, name: str, **kwargs) -> Locations | None:
        location = self.get(name)
        if not location:
            raise ValueError(f"location {name} nicht gefunden!")
        
        return self.location_repo.update_location(location, **kwargs)

class StateService:
    def __init__(self, session: Session, state_repo: StatesRepo):
        self.session = session
        self.state_repo = state_repo

    def _normalized(self, name: str) -> str:
        return name.strip()

    def get(self, name: str) -> States | None:
        return self.state_repo.get_state_by_name(
            self._normalized(name))
    
    def get_by_id(self, id: int) -> States | None:
        return self.state_repo.get_state_by_id(id)
    
    def list_all(self) -> list[States]:
        return self.state_repo.list_states()

    def new(self, name: str) -> States:
        new_state = self.get(name)
        if new_state:
            raise ValueError(f"state {new_state} already exists!")

        state = self.state_repo.create_state(
            self._normalized(name))
        
        return state
    
    def delete(self, name: str) -> States:
        state = self.get(name)       
        if not state:
            raise ValueError(f"state '{name}' not found!")
        return self.state_repo.delete_state(state)

    def update(self, name: str, **kwargs) -> States | None:
        state = self.get(name)
        if not state:
            raise ValueError(f"state {name} not found!")
        
        return self.state_repo.update_state(state, **kwargs)

class AuthorService:
    def __init__(self, session: Session, author_repo: AuthorsRepo):
        self.session = session
        self.author_repo = author_repo

    def _normalized(self, name: str) -> str:
        return name.strip()

    def get(self, name: str) -> Authors | None:
        return self.author_repo.get_author_by_name(
            self._normalized(name))
    
    def get_by_id(self, id: int) -> Authors | None:
        return self.author_repo.get_author_by_id(id)
    
    def list_all(self) -> list[Authors]:
        return self.author_repo.list_authors()

    def new(self, name: str) -> Authors:
        if self.get(name):
            raise ValueError(f"author '{name}' already exists!")

        author = self.author_repo.create_author(
            self._normalized(name))
        
        return author
    
    def delete(self, name: str) -> None:
        author = self.get(name)
        if not author:
            raise ValueError(f"author '{name}' not found!")
        self.author_repo.delete_author(author)

    def update(self, name: str, **kwargs) -> Authors | None:
        author = self.get(name)
        if not author:
            raise ValueError(f"author {name} not found!")

        return self.author_repo.update_author(author, **kwargs)


class BookService:
    def __init__(
        self,
        session: Session,
        book_repo: BooksRepo,
        author_repo: AuthorsRepo,
        genre_repo: GenresRepo,
        state_repo: StatesRepo,
        location_repo: LocationsRepo
    ):
        self.session = session
        self.book_repo = book_repo
        self.author_repo = author_repo
        self.genre_repo = genre_repo
        self.state_repo = state_repo
        self.location_repo = location_repo

    def create_book(
        self,
        title: str,
        author_name: str,
        genre_name: str,
        state_name: str,
        location_name: str,
        published: datetime
    ) -> Books:
        
        if not title or not title.strip():
            raise ValueError("Book title must not be empty")

        title = title.strip()

        existing_book = self.book_repo.get_book_by_title_and_author(
            title, author_name.strip())

        if existing_book:
            return existing_book

        author = self.author_repo.get_or_create(author_name.strip())
        genre = self.genre_repo.get_or_create(genre_name.strip())
        state = self.state_repo.get_or_create(state_name.strip())
        location = self.location_repo.get_or_create(location_name.strip())

        book = self.book_repo.create_book(
            title=title,
            published=published,
            author=author,
            genre=genre,
            state=state,
            location=location
        )

        return book
    
    def get(self, title: str) -> Books | None:
        return self.book_repo.get_book_by_title(title)
    
    def list_all(self) -> list[Books]:
        return self.book_repo.list_books()
    
    def _identify_book(self, title: str, author: str = ""):
        if author:
            book = self.book_repo.get_book_by_title_and_author(title, author)
        else:
            book_list = self.book_repo.list_books_by_title(title)
            if len(book_list) == 1:
                book = book_list[0]
            else:
                raise ValueError(f"The book '{title}' could not be identified. Please provide an author.")  

        if not book:
            raise ValueError(f"book '{title}' not found!")
        
        return book
    
    def delete(self, title: str, author: str = ""):
        book = self._identify_book(title, author)
        self.book_repo.delete_book(book)

    def update(self, title: str, author: str = "", **kwargs) -> Books:

        book = self._identify_book(title, author)

        resolved = {}

        if "author_name" in kwargs:
            resolved["author"] = self.author_repo.get_or_create(kwargs.pop("author_name").strip())

        if "genre_name" in kwargs:
            resolved["genre"] = self.genre_repo.get_or_create(kwargs.pop("genre_name").strip())

        if "state_name" in kwargs:
            resolved["state"] = self.state_repo.get_or_create(kwargs.pop("state_name").strip())

        if "location_name" in kwargs:
            resolved["location"] = self.location_repo.get_or_create(kwargs.pop("location_name").strip())

        self.book_repo.update_book(book, **resolved, **kwargs)
        return book
        


if __name__ == "__main__":

    with db() as session:

        service = BookService(
            session,
            BooksRepo(session),
            AuthorsRepo(session),
            GenresRepo(session),
            StatesRepo(session),
            LocationsRepo(session)
        )

        author_service = AuthorService(
            session,
            AuthorsRepo(session)
        )

        # author_service.new("Felix")
        # book = author_service.update("Felix", author_name="Felix W.")
        print(author_service.list_all())