from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import Text, create_engine, select, delete, update
import contextlib

class Base(DeclarativeBase):
    pass

class Book(Base):
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"Book(id={self.id}, title={self.title})"


class DBManager:
    def __init__(self, db_url: Optional[str] = None):
        if not db_url:
            self.engine = self.engine = create_engine('sqlite:///:memory:')
            Base.metadata.drop_all(self.engine)
            Base.metadata.create_all(self.engine)
        else:
            self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    @contextlib.contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_all_books(self, session) -> List[Book]:
        stmt = select(Book)
        result = session.execute(stmt)
        all_books = result.scalars()
        return all_books

    def add_book_with_title(self, session, title: str) -> Book:
        book = Book(title=title)
        session.add(book)
        session.commit()
        return book

    def delete_book(self, session, book_id: int) -> None:
        delete_stmt = delete(Book).where(Book.id == book_id)
        session.execute(delete_stmt)
        session.commit()

    def update_book(self, session, book_id: int, title: str) -> None:
        update_stmt = update(Book).where(Book.id == book_id).values(title=title)
        session.execute(update_stmt)
        session.commit()
        book = self.get_book_by_id(session, book_id)
        return book

    def get_book_by_id(self, session, book_id: int) -> Book:
        stmt = select(Book).where(Book.id == book_id)
        result = session.execute(stmt)
        book = result.scalars().first()
        return book

db = DBManager()
