from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )


@table_registry.mapped_as_dataclass
class Author:
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    books: Mapped[List['Book']] = relationship(
        init=False, back_populates='author'
    )

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )


@table_registry.mapped_as_dataclass
class Book:
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    year: Mapped[str]

    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))
    author: Mapped['Author'] = relationship(init=False, back_populates='books')

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
