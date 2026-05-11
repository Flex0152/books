from sqlalchemy import ForeignKey, UniqueConstraint

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from datetime import datetime
from typing import List


class Base(DeclarativeBase):
    pass

class Books(Base):
    __tablename__ = "Books"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_title: Mapped[str]
    published: Mapped[datetime]

    author_id: Mapped[int] = mapped_column(ForeignKey("Authors.id"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("Genres.id"))
    location_id: Mapped[int] = mapped_column(ForeignKey("Locations.id"))
    state_id: Mapped[int] = mapped_column(ForeignKey("States.id"))

    genre: Mapped["Genres"] = relationship(
        back_populates="books")
    
    location: Mapped["Locations"] = relationship(
        back_populates="books")

    author: Mapped["Authors"] = relationship(
            back_populates="books")
    
    state: Mapped["States"] = relationship(
        back_populates="books"
    )
    
    __table_args__ = (
        # Ein Author, ein Title. Versch. Author, gleicher Title
        UniqueConstraint("author_id", "book_title", name="uq_author_title"),
    )

    def __repr__(self):
        return f"<id: {self.id} - Title: {self.book_title} - Author: {self.author_id}>"


class States(Base):
    __tablename__ = "States"
    id: Mapped[int] = mapped_column(primary_key=True)
    state_name: Mapped[str] = mapped_column(unique=True)

    books: Mapped[List["Books"]] = relationship(
        back_populates="state"
    )

    def __repr__(self):
        return f"<id: {self.id} - name: {self.state_name}>"


class Locations(Base):
    __tablename__ = "Locations"
    id: Mapped[int] = mapped_column(primary_key=True)
    shelf: Mapped[str] = mapped_column(unique=True)

    books: Mapped[List["Books"]] = relationship(back_populates="location")

    def __repr__(self):
        return f"<id: {self.id} - shelf: {self.shelf}>"


class Authors(Base):
    __tablename__ = "Authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    author_name: Mapped[str] = mapped_column(unique=True)

    books: Mapped[List["Books"]] = relationship(
            back_populates="author", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<id: {self.id} - author: {self.author_name}>"


class Genres(Base):
    __tablename__ = "Genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    genre_name: Mapped[str] = mapped_column(unique=True)

    books: Mapped[List["Books"]] = relationship(back_populates="genre")

    def __repr__(self):
        return f"<id: {self.id} - Genre: {self.genre_name}>"
