from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database.models import Author
from madr.database.session import get_session
from madr.schemas.author import AuthorList, AuthorPublic, AuthorSchema

router = APIRouter(prefix='/authors', tags=['authors'])
T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=AuthorPublic)
def create_author(author: AuthorSchema, session: T_Session):
    db_author = session.scalar(
        select(Author).where((Author.name == author.name))
    )

    if db_author:
        if db_author.name == author.name:
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
def get_author_list(session: T_Session, skip: int = 0, limit: int = 100):
    authors = session.scalars(select(Author).offset(skip).limit(limit)).all()
    return {'authors': authors}
