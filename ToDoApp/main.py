from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users

app = FastAPI()

Base.metadata.create_all(bind=engine)
# creates the db from models and database
# nly runs when todo doesnt exist


@app.get('/healthy')
def health_check():
    return {'status': 'Healthy'}

# Include API routers
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

# we are making api endpoint from auth and todos
