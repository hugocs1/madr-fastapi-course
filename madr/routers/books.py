from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database.models import Book
from madr.database.session import get_session
from madr.schemas.book import (
    BookList,
    BookPublic,
    BookSchema,
    BookPatch,
)
from madr.schemas.message import Message

router = APIRouter(prefix='/books', tags=['books'])
T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookPublic)
def create_book(book: BookSchema, session: T_Session):
    db_book = session.scalar(select(Book).where((Book.title == book.title)))

    if db_book and db_book.title == book.title:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Book already exists',
        )

    db_book = Book(title=book.title, year=book.year, author_id=book.author_id)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


@router.get('/', response_model=BookList)
def get_book_list(
    session: T_Session,
    title: str = Query(None),
    year: str = Query(None),
    skip: int = 0,
    limit: int = 20,
):
    books = select(Book)

    if title:
        books = books.filter(Book.title.icontains(title))

    if year:
        books = books.filter(Book.year == year)

    books = session.scalars(books.offset(skip).limit(limit))

    return {'books': books}


def get_book_by_id_or_404(book_id, session):
    book = session.scalars(select(Book).where((Book.id == book_id))).first()

    if not book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Book not found',
        )

    return book


@router.get('/{book_id}', response_model=BookPublic)
def get_book(book_id: int, session: T_Session):
    return get_book_by_id_or_404(book_id, session)


@router.patch('/{book_id}', response_model=BookPublic)
def patch_book(book_id: int, session: T_Session, book: BookPatch):
    db_book = get_book_by_id_or_404(book_id, session)

    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


@router.delete('/{book_id}', response_model=Message)
def delete_book(book_id: int, session: T_Session):
    book = get_book_by_id_or_404(book_id, session)

    session.delete(book)
    session.commit()

    return {'message': 'Book deleted'}
