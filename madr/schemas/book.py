from pydantic import BaseModel, ConfigDict


class BookSchema(BaseModel):
    title: str
    year: str
    author_id: int


class BookPublic(BaseModel):
    id: int
    title: str
    year: str
    author_id: int
    model_config = ConfigDict(from_attributes=True)


class BookList(BaseModel):
    books: list[BookPublic]


class BookPatch(BaseModel):
    title: str | None = None
    year: str | None = None
    author_id: int | None = None
