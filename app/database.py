from model import Base
import sqlalchemy as sa 
from sqlalchemy.orm import sessionmaker

from pathlib import Path


db_file_name = "books.db"

if not Path(db_file_name).is_file():
    engine = sa.create_engine(f"sqlite:///{db_file_name}")
    Base.metadata.create_all(engine)
else:
    engine = sa.create_engine(f"sqlite:///{db_file_name}")

session = sessionmaker(bind=engine)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
