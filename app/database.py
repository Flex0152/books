from app.model import Base
import sqlalchemy as sa 
from sqlalchemy.orm import sessionmaker

from pathlib import Path


db_file_path = Path(__file__).parent.parent / "data" / "books.db"
db_file_path.parent.mkdir(parents=True, exist_ok=True)

if not db_file_path.is_file():
    engine = sa.create_engine(f"sqlite:///data/{db_file_path}")
    Base.metadata.create_all(engine)
else:
    engine = sa.create_engine(f"sqlite:///data/{db_file_path}")

session = sessionmaker(bind=engine)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
