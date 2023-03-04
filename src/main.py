from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info
from uuid import uuid4
from typing import List
from .db import db

### Strawberry Schema

@strawberry.type
class Book:
    id: strawberry.ID
    title: str

@strawberry.input
class BookInput:
    title: str

@strawberry.type
class MutationResult:
    result: str

@strawberry.type
class BookMutationResult:
    book: Book

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(info: Info, book: BookInput) -> BookMutationResult:
        with db.session_scope() as session:
            db_book = db.add_book_with_title(session, title=book.title)
            book = Book(id=db_book.id, title=db_book.title)
            return BookMutationResult(book=book)

    @strawberry.mutation
    def delete_book(info: Info, book_id: strawberry.ID) -> MutationResult:
        with db.session_scope() as session:
            db.delete_book(session, book_id=int(book_id))
        return MutationResult(result="success")

    @strawberry.mutation
    def edit_book(info: Info, book_id: strawberry.ID, book: BookInput) -> BookMutationResult:
        with db.session_scope() as session:
            db_book = db.update_book(session, book_id=int(book_id), title=book.title)
            book = Book(id=db_book.id, title=db_book.title)
            return BookMutationResult(book=book)

@strawberry.type
class Query:
    @strawberry.field
    def books() -> List[Book]:
        with db.session_scope() as session:
            db_books = db.get_all_books(session)
            return [Book(id=db_book.id, title=db_book.title) for db_book in db_books]

    @strawberry.field
    def get_book_by_id(info: Info, book_id: strawberry.ID) -> Book:
        with db.session_scope() as session:
            db_book = db.get_book_by_id(session, book_id=int(book_id))
            return Book(id=db_book.id, title=db_book.title)

schema = strawberry.Schema(query=Query, mutation=Mutation)

### FastAPI

app = FastAPI(docs_url=None, redoc_url=None)

@app.on_event("startup")
async def startup_event():
    print("Starting up...")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    GraphQLRouter(
    schema,
    graphiql=True,
    debug=True,
), prefix="/graphql")

