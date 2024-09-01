from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database.models import Author
from madr.database.session import get_session
from madr.schemas.author import (
    AuthorList,
    AuthorPublic,
    AuthorSchema,
    AuthorUpdate,
)
from madr.schemas.message import Message

router = APIRouter(prefix='/authors', tags=['authors'])
T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=AuthorPublic)
def create_author(author: AuthorSchema, session: T_Session):
    db_author = session.scalar(
        select(Author).where((Author.name == author.name))
    )

    if db_author and db_author.name == author.name:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Author already exists',
        )

    db_author = Author(name=author.name)

    session.add(db_author)
    session.commit()
    session.refresh(db_author)

    return db_author


@router.get('/', response_model=AuthorList)
def get_author_list(
    session: T_Session,
    name: str = Query(None),
    skip: int = 0,
    limit: int = 20,
):
    authors = select(Author)

    if name:
        authors = authors.filter(Author.name.icontains(name))

    authors = session.scalars(authors.offset(skip).limit(limit))

    return {'authors': authors}


def get_author_by_id_or_404(author_id, session):
    author = session.scalars(
        select(Author).where((Author.id == author_id))
    ).first()

    if not author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author not found',
        )

    return author


@router.get('/{author_id}', response_model=AuthorPublic)
def get_author(author_id: int, session: T_Session):
    return get_author_by_id_or_404(author_id, session)


@router.patch('/{author_id}', response_model=AuthorPublic)
def patch_author(author_id: int, session: T_Session, author: AuthorUpdate):
    db_author = get_author_by_id_or_404(author_id, session)

    for key, value in author.model_dump(exclude_unset=True).items():
        setattr(db_author, key, value)

    session.add(db_author)
    session.commit()
    session.refresh(db_author)

    return db_author


@router.delete('/{author_id}', response_model=Message)
def delete_author(author_id: int, session: T_Session):
    author = get_author_by_id_or_404(author_id, session)

    session.delete(author)
    session.commit()

    return {'message': 'Author deleted'}
