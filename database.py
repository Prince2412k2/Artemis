from sqlmodel import SQLModel, create_engine, Session

URL = "sqlite:///database.db"
engine = create_engine(URL, echo=True)


def get_db():
    with Session(engine) as session:
        yield session
