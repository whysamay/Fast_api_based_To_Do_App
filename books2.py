#this is focused on creating Book API Endpoints.
#Continued Education includes
#GET, POST, PUT, DELETE request methods
#new info
#data validation, exception handling, status codes, 
# swagger configuration, python requests object
#create - post, read - get, update - put, delete - delete
from fastapi import FastAPI, Path, Query, HTTPException
from fastapi import Body
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating, published_data):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_data = published_data


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS
 


@app.get("/books/{books_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
          if book.id == book_id:
               return book
    raise HTTPException(status_code=404, detail="Book not found")
    

# @app.post("/create-book")
# async def create_book(book_request = Body()):
#         BOOKS.append(book_request)

#Now we validate values like so it stays in some range
#Pydantic and Data Validation

#pydantic is used for data modeling, data parsing and has efficient error handling
#commonly used as a resource for data validation and how to handle data
#coming to our fast api application
from pydantic import BaseModel, Field
#we will create diff request model for data validation
#field data validation on each variable
#baseModel is from pydantic

import typing
class BookRequest(BaseModel):
    #we want id to be incremented
    id: typing.Optional[int] = Field(description='ID is not needed on Create', default=None)
    #so our schema shows thisssss
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_lenght=100)
    rating: int = Field(gt = 0, lt = 6) #1-5 limit
    published_data: int = Field(gt = 1999, lt=2031)
    #we use model config to prefill the values
    #To create a more descriptive request within our Swagger documentation
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                "published_data": 2029
            }
        }
    }

#QUERY parametere validation
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_books_by_rating(book_rating: int = Query(gt=0, lt=6)):
     books_to_return = []
     for book in BOOKS:
        if book.rating == book_rating:
             books_to_return.append(book)
     return books_to_return


# @app.get("/books/published/{published_date}")
# async def get_books_by_published_date(published_date: int):
#      books_to_return = []
#      for book in BOOKS:
#           if book.published_data == published_date:
#                books_to_return.append(book)
#      return books_to_return

@app.get("/books/published/", status_code=status.HTTP_200_OK)
async def get_books_by_published_date(published_date: int = Query(gt=1999, lt=2031)):
     books_to_return = []
     for book in BOOKS:
          if book.published_data == published_date:
               books_to_return.append(book)
     return books_to_return
               

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
#book_reuqest should be type of BookRequest
async def create_book(book_request: BookRequest):
        new_book = Book(**book_request.model_dump()) 
        #**book_request.model_dump() if above doesnt work
        # ** operator will pass the key value 
        # from bookRequyest() into the Book() contructor
        #print(type(new_book)) to see type
        new_book = find_book_id(new_book)
        BOOKS.append(new_book)
        return new_book
        

#we will convert pydantic request into a book

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

#even if we pass something like with id that doesnt exist, even then we will
#get the status code 200 hence we will be using exceptions here in future
@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
     book_changed = False
     for i in range(len(BOOKS)):
          if BOOKS[i].id == book.id:
               BOOKS[i] = book
               book_changed = True
               break
     if not book_changed:
          raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
     book_changed = False
     for i in range(len(BOOKS)):
          if BOOKS[i].id == book_id:
               BOOKS.pop(i)
               book_changed = True
               break
     if not book_changed:
          raise HTTPException(status_code=404, detail="Item not found")




#PATH PARAMETERE validation
#using Path
#for query, we will use Query

#now we will add https exceptions
#HTTP Status Codes help the client (a user, browser, or any system) 
# #understand what happened when #they sent a request to the server.

#These codes are international standards defined by protocols like 
# #HTTP, and they indicate whether a request was successful, redirected, 
# #caused a client error, or failed on the server.

#They are essential for debugging, automation, and ensuring 
# #a smooth client-server communication — both humans and machines can 
# #interpret what happened just by reading the status code

#1xx → Information Response: Request Processing.

#2xx → Success: Request Successfully complete
# 200: OK →
#Standard Response for a Successful Request. Commonly used 
#for successful Get requests when data is being returned.

# 201: Created →
#The request has been successful, creating a new resource. 
# #Used when a POST creates an entity.

# 204: No Content →
#The request has been successful, did not create an entity 
#nor return anything. Commonly used with PUT requests.

#3xx → Redirection: Further action must be complete

#4xx → Client Errors: An error was caused by the client.
# 400: Bad Request

    #The request cannot be processed due to client error.

    #Often used for invalid request methods or malformed syntax.

# 401: Unauthorized

    #Authentication is required and has failed or not been provided.

    #The client lacks valid credentials for the resource.

# 404: Not Found

    #The requested resource cannot be found on the server.

# 422: Unprocessable Entity

    #The request was well-formed but contains semantic errors.

    #Often used in APIs when input validation fails

#5xx → Server Errors: An error occurred on the server.

# 500: Internal Server Error

    #A generic error message.

    #An unexpected condition occurred on the server. 