from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development
        "https://your-frontend-domain.vercel.app",  # Replace with your frontend URL
        os.getenv("FRONTEND_URL", "http://localhost:3000")  # Environment variable
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
# creates the db from models and database
# nly runs when todo doesnt exist


@app.get('/')
def root():
    return {'message': 'Todo Hub API is running!'}


@app.get('/healthy')
def health_check():
    return {'status': 'Healthy'}

# Include API routers
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

# we are making api endpoint from auth and todos
