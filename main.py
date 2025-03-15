from fastapi import FastAPI,HTTPException
from contextlib import asynccontextmanager
import os
import json

from schemas import *

db = {
    "libraries": [],  # stores library objects
    "books": [],  # stores book objects

    "book_serial_id_counter": 0,  # id counter for book
    "library_serial_id_counter": 0  # id counter for library
}

def save_db():
    with open('database/db.json','w') as f:
        json.dump(db,f,indent=4)

def load_db():
    global db
    if os.path.exists('database/db.json'):
        with open('database/db.json','r') as f:
            db = json.load(f)

@asynccontextmanager
async def lifespan(app:FastAPI):
    load_db()
    yield
    save_db()

app = FastAPI(lifespan=lifespan)

@app.post("/books/",response_model=CreateBookResponse)
def create_book(book:CreateBookRequest):

    if any(b['name'] == book.name for b in db['books']):
        print("duplicate name")
        raise HTTPException(status_code=400,detail="Duplicate book name")
    print(db)
    book_id = db['book_serial_id_counter']
    new_book = Book(id=book_id,name=book.name,writer=book.writer)
    db['books'].append(new_book.dict())
    db['book_serial_id_counter'] += 1
    return {"id":book_id,"message":"Book created successfully."}

@app.get("/books/",response_model=ListBooksResponse)
def list_books():
    return {"books":db['books']}


@app.delete("/books/{book_id}",response_model=DeleteBookResponse)
def delete_book(book_id:int):
    for i,book in enumerate(db['books']):
        if book['id'] == book_id:
            db['books'].pop(i)
            return {"status":True,"message":"Deletion successful"}
        
    raise HTTPException(status_code=404, detail="Book ID not found")


# Create these apis as project and complete the update method for books

@app.put("/books/{book_id}", response_model=UpdateBookResponse)
def update_book(book_id: int, book: UpdateBookRequest):
    for b in db['books']:
        if b['id'] == book_id:
            b['name'] = book.name
            b['writer'] = book.writer
            return {"status": True, "message": "Book updated successfully"}
    raise HTTPException(status_code=404, detail="Book ID not found")

@app.post("/libraries/", response_model=Library)
def create_library(library: CreateLibraryRequest):
    if any(l['name'] == library.name for l in db['libraries']):
        raise HTTPException(status_code=400, detail="Duplicate library name")
    library_id = db['library_serial_id_counter']
    new_library = Library(id=library_id, name=library.name)
    db['libraries'].append(new_library.dict())
    db['library_serial_id_counter'] += 1
    return new_library

@app.put("/libraries/{library_id}", response_model=Library)
def update_library(library_id: int, library: UpdateLibraryRequest):
    for l in db['libraries']:
        if l['id'] == library_id:
            l['name'] = library.name
            return l
    raise HTTPException(status_code=404, detail="Library ID not found")

@app.delete("/libraries/{library_id}", response_model=DeleteLibraryResponse)
def delete_library(library_id: int):
    for i, library in enumerate(db['libraries']):
        if library['id'] == library_id:
            db['libraries'].pop(i)
            return {"status": True, "message": "Deletion successful"}
    raise HTTPException(status_code=404, detail="Library ID not found")

@app.get("/libraries/{library_id}/books", response_model=ListBooksResponse)
def list_books_in_library(library_id: int):
    for library in db['libraries']:
        if library['id'] == library_id:
            return {"books": library['books']}
    raise HTTPException(status_code=404, detail="Library ID not found")

@app.get("/libraries/", response_model=ListLibrariesResponse)
def list_libraries():
    return {"libraries": db['libraries']}

@app.post("/libraries/{library_id}/books", response_model=Book)
def insert_book(library_id: int, book: CreateBookRequest):
    for library in db['libraries']:
        if library['id'] == library_id:
            book_id = db['book_serial_id_counter']
            new_book = Book(id=book_id, name=book.name, writer=book.writer)
            library['books'].append(new_book.dict())
            db['books'].append(new_book.dict())
            db['book_serial_id_counter'] += 1
            return new_book
    raise HTTPException(status_code=404, detail="Library ID not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app,host="127.0.0.1",port=8000)
