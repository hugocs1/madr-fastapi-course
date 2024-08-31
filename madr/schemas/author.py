from pydantic import BaseModel, ConfigDict


class AuthorSchema(BaseModel):
    name: str


class AuthorPublic(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class AuthorList(BaseModel):
    authors: list[AuthorPublic]
