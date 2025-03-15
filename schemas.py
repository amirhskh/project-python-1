from pydantic import BaseModel
from typing import List, Optional

class Book(BaseModel):
    id: int
    name: str
    writer: str

class CreateBookRequest(BaseModel):
    name: str
    writer: str

class CreateBookResponse(BaseModel):
    id: int
    message: str

class ListBooksResponse(BaseModel):
    books: List[Book]

class DeleteBookResponse(BaseModel):
    status: bool
    message: str

class UpdateBookRequest(BaseModel):
    name: Optional[str]
    writer: Optional[str]

class UpdateBookResponse(BaseModel):
    status: bool
    message: str

class CreateLibraryRequest(BaseModel):
    name: str

class Library(BaseModel):
    id: int
    name: str
    books: List[Book] = []

class UpdateLibraryRequest(BaseModel):
    name: str

class DeleteLibraryResponse(BaseModel):
    status: bool
    message: str

class ListLibrariesResponse(BaseModel):
    libraries: List[Library]