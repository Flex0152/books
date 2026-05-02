from model import Base
import sqlalchemy as sa 
from sqlalchemy.orm import sessionmaker


engine = sa.create_engine("sqlite:///books.db")
session = sessionmaker(bind=engine)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
