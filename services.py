from repos import (
    BooksRepo,
    GenresRepo,
    LocationsRepo,
    AuthorsRepo, 
    StatesRepo
)
from model import Genres, Locations, Authors, Books
from database import session as db
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

    def new(self, name: str):
        new_genre = self.get(name)
        if new_genre:
            raise ValueError(f"Genre {new_genre} already exists!")

        genre = self.genre_repo.create_genre(
            self._normalized(name))
        
        return genre
    
    def delete(self, name: str):
        genre = self.get(name)

        if not genre:
            raise ValueError(f"Genre {name} not found!")
        
        self.genre_repo.delete_genre_by_id(genre.id)
        
        return genre

    def update(self, name: str, **kwargs) -> Genres | None:
        genre = self.get(name)
        if not genre:
            raise ValueError(f"Genre {name} nicht gefunden!")
        
        updated_genre = self.genre_repo.update_genre_by_id(genre.id, **kwargs)
        if updated_genre:
            
            return updated_genre
        else:
            return None
        
class LocationService:
    def __init__(self, session: Session, location_repo: LocationsRepo):
        self.session = session
        self.location_repo = location_repo

    def _normalized(self, name: str) -> str:
        return name.strip()#.lower()

    def get(self, name: str) -> Locations | None:
        return self.location_repo.get_location_by_name(
            self._normalized(name))

    def new(self, name: str):
        new_location = self.get(name)
        if new_location:
            raise ValueError(f"location {new_location} already exists!")

        location = self.location_repo.create_location(
            self._normalized(name))
        
        return location
    
    def delete(self, name: str):
        location = self.get(name)

        if not location:
            raise ValueError(f"location {name} not found!")
        
        self.location_repo.delete_location_by_id(location.id)
        
        return location

    def update(self, name: str, **kwargs) -> Locations | None:
        location = self.get(name)
        if not location:
            raise ValueError(f"location {name} nicht gefunden!")
        
        updated_location = self.location_repo.update_location_by_id(location.id, **kwargs)
        if updated_location:
            
            return updated_location
        else:
            return None

class AuthorService:
    def __init__(self, session: Session, author_repo: AuthorsRepo):
        self.session = session
        self.author_repo = author_repo

    def _normalized(self, name: str) -> str:
        return name.strip().lower()

    def get(self, name: str) -> Authors | None:
        return self.author_repo.get_author_by_name(
            self._normalized(name))

    def new(self, name: str):
        new_author = self.get(name)
        if new_author:
            raise ValueError(f"author {new_author} already exists!")

        author = self.author_repo.create_author(
            self._normalized(name))
        
        return author
    
    def delete(self, name: str):
        author = self.get(name)

        if not author:
            raise ValueError(f"author {name} not found!")
        
        self.author_repo.delete_author_by_id(author.id)
        
        return author

    def update(self, name: str, **kwargs) -> Authors | None:
        author = self.get(name)
        if not author:
            raise ValueError(f"author {name} nicht gefunden!")
        
        updated_author = self.author_repo.update_author_by_id(author.id, **kwargs)
        if updated_author:
            
            return updated_author
        else:
            return None


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
    
    def delete(self, title: str, author: str = ""):
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

        self.book_repo.delete_book(book)
        


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

        book = service.create_book(
            "Test 2. Teil",
            "Felix",
            "Tester",
            "in Action",
            "irgendwo",
            datetime(2026,1,1)
        )

        book = service.create_book(
            "Test 1. Teil",
            "Felix",
            "Tester",
            "not started",
            "irgendwo",
            datetime(2026,1,1)
        )

        session.commit()