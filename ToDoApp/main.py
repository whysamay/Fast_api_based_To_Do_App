import sys
import os
from pathlib import Path

# Add the current directory to Python path for local development
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Try relative imports first (for Railway), fall back to absolute (for local)
try:
    from .models import Base
    from .database import engine
    from .routers import auth, todos, admin, users
except ImportError:
    # Fall back to absolute imports for local development
    from models import Base
    from database import engine
    from routers import auth, todos, admin, users

app = FastAPI()

# Get frontend URL from environment variable
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development
        "https://*.vercel.app",   # Vercel domains
        "https://*.netlify.app",  # Netlify domains (if you use it)
        FRONTEND_URL,             # Environment variable
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
