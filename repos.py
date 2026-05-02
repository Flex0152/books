from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from model import Books, Locations, Authors, Genres, States
from database import session as dbSession


class BooksRepo:
    def __init__(self, session: Session):
        self.session = session

    def create_book(
        self,
        title: str, 
        published: datetime,
        author: Authors,
        genre: Genres,
        location: Locations,
        state: States
    ) -> Books:
        
        book = Books(
            book_title=title,
            published=published,
            author=author,
            genre=genre,
            location=location,
            state=state
        )

        self.session.add(book)

        return book
    
    def get_book_by_id(self, id: int) -> Books | None:
        return self.session.get(Books, id)
    
    def get_book_by_title_and_author(
            self,
            title: str, 
            author_name: str) -> Books | None:
        author = self.session.query(Authors).filter_by(
            author_name=author_name).first()
        if author:
            book = self.session.query(Books).filter_by(
                book_title=title, author_id=author.id).first()
            return book
        else:
            return None
    
    def get_book_by_title(self, name: str) -> Books | None:
        stmt = select(Books).filter_by(Book_Title=name)
        return session.execute(stmt).scalar()
    
    def delete_book_by_id(self, id: int) -> None: 
        book = self.get_book_by_id(id)
        if book:
            self.session.delete(book)
        
    def update_book_by_id(self, id: int, **kwargs) -> Books | None:
        book = self.get_book_by_id(id)
        if not book:
            return None
        
        for attr in kwargs:
            if hasattr(book, attr) and kwargs[attr] is not None:
                setattr(book, attr, kwargs[attr])

        return book
    

class LocationsRepo:
    def __init__(self, session: Session):
        self.session = session

    def create_location(self, shelf: str) -> Locations:
        location = Locations(
            shelf=shelf)
        self.session.add(location)
        return location
    
    def get_location_by_id(self, id: int) -> Locations | None:
        return self.session.get(Locations, id)
    
    def get_location_by_name(self, name: str) -> Locations | None:
        stmt = select(Locations).filter_by(shelf=name)
        return self.session.execute(stmt).scalar()
    
    def get_or_create(self, name: str) -> Locations:
        location = self.get_location_by_name(name)
        if not location:
            location = self.create_location(name)
        return location
    
    def delete_location_by_id(self, id: int) -> None:
        location = self.get_location_by_id(id)
        if location:
            self.session.delete(location)

    def update_location_by_id(self, id: int, **kwargs) -> Locations | None:
        location = self.get_location_by_id(id)
        if not location:
            return None
        
        for attr in kwargs:
            if hasattr(location, attr) and kwargs[attr] is not None:
                setattr(location, attr, kwargs[attr])

        return location
    

class AuthorsRepo:
    def __init__(self, session: Session):
        self.session = session

    def create_author(self, author_name: str) -> Authors:
        author = Authors(author_name=author_name)
        self.session.add(author)
        return author

    def get_author_by_id(self, id: int) -> Authors | None:
        return self.session.get(Authors, id)

    def get_author_by_name(self, name: str) -> Authors | None:
        stmt = select(Authors).filter_by(author_name=name)
        return self.session.execute(stmt).scalar()
    
    def get_or_create(self, name: str) -> Authors:
        author = self.get_author_by_name(name)
        if not author:
            author = self.create_author(name)
        return author
    
    def delete_author_by_id(self, id: int) -> None:
        author = self.get_author_by_id(id)
        if author:
            return self.session.delete(author)
    
    def update_author_by_id(self, id: int, **kwargs) -> Authors | None:
        author = self.get_author_by_id(id)
        if not author:
            return None
        
        for attr in kwargs:
            if hasattr(author, attr) and kwargs[attr] is not None:
                setattr(author, attr, kwargs[attr])

        return author
    
    
class GenresRepo:
    def __init__(self, session: Session):
        self.session = session

    def create_genre(self, genre_name: str) -> Genres:
        genre = Genres(genre_name=genre_name)
        self.session.add(genre)
        return genre

    def get_genre_by_id(self, id: int) -> Genres | None:
        return self.session.get(Genres, id)

    def get_genre_by_name(self, name: str) -> Genres | None:
        stmt = select(Genres).filter_by(genre_name=name)
        return self.session.execute(stmt).scalar()
    
    def get_or_create(self, name: str) -> Genres:
        genre = self.get_genre_by_name(name)
        if not genre:
            genre = self.create_genre(name)
        return genre
    
    def delete_genre_by_id(self, id: int) -> None:
        genre = self.get_genre_by_id(id)
        if genre:
            return self.session.delete(genre)
    
    def update_genre_by_id(self, id: int, **kwargs) -> Genres | None:
        genre = self.get_genre_by_id(id)
        if not genre:
            return None
        
        for attr in kwargs:
            if hasattr(genre, attr) and kwargs[attr] is not None:
                setattr(genre, attr, kwargs[attr])

        return genre

    
class StatesRepo:
    def __init__(self, session: Session):
        self.session = session

    def create_state(self, state_name: str) -> States:
        state = States(state_name=state_name)
        self.session.add(state)
        return state

    def get_state_by_id(self, id: int) -> States | None:
        return self.session.get(States, id)

    def get_state_by_name(self, name: str) -> States | None:
        stmt = select(States).filter_by(state_name=name)
        return self.session.execute(stmt).scalar()
    
    def get_or_create(self, name: str) -> States:
        state = self.get_state_by_name(name)
        if not state:
            state = self.create_state(name)
        return state
    
    def delete_state_by_id(self, id: int) -> None:
        state = self.get_state_by_id(id)
        if state:
            return self.session.delete(state)
    
    def update_state_by_id(self, id: int, **kwargs) -> States | None:
        state = self.get_state_by_id(id)
        if not state:
            return None
        
        for attr in kwargs:
            if hasattr(state, attr) and kwargs[attr] is not None:
                setattr(state, attr, kwargs[attr])

        return state


if __name__ == "__main__":
    with dbSession() as session:
        b = BooksRepo(session)
        author = Authors(author_name="Thomas Mann")
        genre = Genres(genre_name="Fantasy")
        location = Locations(shelf="schrank")
        state = States(state_name="in action")
        b.create_book(
            "tester", 
            datetime(1900,2,2),
            author,
            genre,
            location,
            state)
        session.commit()
