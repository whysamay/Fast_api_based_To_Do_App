from fastapi import FastAPI

app = FastAPI()

@app.get("/api-endpoint") 
#decorator, we define the endpoint/path
#that will call this function
async def first_api(): #async is not needed in fastapi
    return {"message": "hello"}

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

#order matters so have less para first
#path parameters
@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/mybook")
async def read_all_books():
    return {"myboook": 'mybook'}

# @app.get("/books/{dynamic_param}")
# async def read_all_books(dynamic_param: str):
#     return {'dynamic_param': dynamic_param }

#title%20four = title four  (%20 is space)
#casefold -> smaller letters
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

#QUERY parameters are request parameters that have been attached after a "?"
#Query parameters have name=value pairs

#example
# 127.0.0.1:800/books/?catergory=science
#
#Simply Using Query Parameter
@app.get("/books/by-category/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

#added after lfec 17
@app.get("/books/by-author/") #having issue as one endpoint with two query parameter
async def get_all_books_by_query(author_name: str):
    books_to_return = []
    for i in range(len(BOOKS)):
        if BOOKS[i].get("author").casefold() == author_name.casefold():
                books_to_return.append(BOOKS[i].get('title'))
    return books_to_return

#query parameter w path parameter
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == book_author.casefold() and book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


#Post is used to create data
#post can have a body that has additional info that GET does not have
# example title:L title seven author: etc 
#this info is added to the database
from fastapi import Body

#create http data
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

#double quotation mark is neccesary for passing reqyest
# @app.get("/books/{book_title}")
# async def read_book(book_title: str, newBody = Body()):
#     for book in BOOKS:
#         if book.get('title').casefold() == book_title.casefold():
#             return book
# #request with GET cannot have a body

#PUT REQUEST METHOD
#used to update data
#PUT can have a body that GET does not have
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book 

#DELETE
#used to delete data
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

# assigment to fetch all books from a specific author
@app.get("/books/get_all_books/{author_name}")
async def get_all_books(author_name: str):
    books_to_return = []
    for i in range(len(BOOKS)):
        if BOOKS[i].get("author").casefold() == author_name.casefold():
                books_to_return.append(BOOKS[i].get('title'))
    return books_to_return

# @app.get("/books/by-author/") #having issue as one endpoint with two query parameter
# async def get_all_books_by_query(author_name: str):
#     books_to_return = []
#     for i in range(len(BOOKS)):
#         if BOOKS[i].get("author").casefold() == author_name.casefold():
#                 books_to_return.append(BOOKS[i].get('title'))
#     return books_to_return
#this is happening because order matters so commeting previous query
# so move it down the query category and above query and path functiin


#so MAIN THING IS ORDER MATTERS
#if query=cat and pat=autgor is above query = auth, it will give 422 error because order matters 
#smaller api endpoint should be first
#PUT or POST-> USE DOUBLE QUOTES