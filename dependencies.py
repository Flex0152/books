from services import (BookService,
    AuthorService,
    GenreService,
    LocationService)
from repos import (BooksRepo,
    AuthorsRepo,
    GenresRepo,
    StatesRepo,
    LocationsRepo)
from database import session as db
from datetime import datetime


def book_service_builder(session) -> BookService:
    book_service = BookService(
        session=session,
        book_repo=BooksRepo(session),
        author_repo=AuthorsRepo(session),
        genre_repo=GenresRepo(session),
        state_repo=StatesRepo(session),
        location_repo=LocationsRepo(session)
    )
    return book_service

def author_service_builder(session) -> AuthorService:
    author_service = AuthorService(
        session,
        author_repo=AuthorsRepo(session)
    )
    return author_service

def genre_service_builder(session) -> GenreService:
    genre_service = GenreService(
        session,
        genre_repo=GenresRepo(session)
    )
    return genre_service

def location_service_builder(session) -> LocationService:
    location_service = LocationService(
        session,
        location_repo=LocationsRepo(session)
    )
    return location_service


if __name__ == "__main__":
    with db() as session:
        service = book_service_builder(session)