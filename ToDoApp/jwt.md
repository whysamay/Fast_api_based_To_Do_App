### Notes on JSON Web Token (JWT) Overview for PyCharm

Below are concise notes based on the provided transcript, tailored for use in PyCharm (e.g., for a FastAPI project like your ToDoApp). These notes summarize key concepts about JSON Web Tokens (JWT) and include practical insights for implementation in Python using libraries like `PyJWT`. You can save these notes as a `.md` file in PyCharm for reference while working on your project.

---

## JSON Web Token (JWT) Overview

### 1. **What is JWT?**
- **Definition**: JSON Web Token (JWT) is a self-contained, secure method to transmit data between parties using a JSON object.
- **Purpose**: Used for **authorization** (not authentication) in APIs, enabling a client-server relationship without repeated logins.
- **Key Feature**: Digitally signed to ensure data integrity, allowing servers to detect tampering.
- **Structure**: Consists of three parts: **Header**, **Payload**, and **Signature**, separated by dots (e.g., `xxxxx.yyyyy.zzzzz`).

### 2. **JWT Components**
- **Header**:
  - Contains:
    - `alg`: Algorithm for signing (e.g., `HS256`).
    - `typ`: Token type (`JWT`).
  - Encoded in Base64 to form the first part of the JWT.
- **Payload**:
  - Contains user data and metadata via **claims**:
    - **Registered Claims** (recommended, not mandatory):
      - `iss` (issuer): Identifies the token issuer.
      - `sub` (subject): Unique identifier for the user (e.g., user ID).
      - `exp` (expiration): Timestamp for token expiry (critical for security).
    - **Public Claims**: Custom claims registered in a public namespace.
    - **Private Claims**: Custom claims specific to the application (e.g., `name`, `email`, `admin`).
  - Encoded in Base64 to form the second part.
- **Signature**:
  - Created by hashing the encoded header, payload, and a **secret key** using the algorithm specified in the header.
  - Ensures token integrity; stored securely on the server, not accessible to clients.
  - Forms the third part of the JWT.

### 3. **How JWT Works**
- **Process**:
  1. User logs in; server generates a JWT and sends it to the client.
  2. Client includes the JWT in the `Authorization` header (using `Bearer` schema) for subsequent requests.
  3. Server validates the JWT on each request to authorize access.
- **Security**:
  - Always set an expiration (`exp`) to prevent indefinite token validity.
  - Example: Set `exp` to 1 hour of inactivity to invalidate the token.
  - Never store sensitive data in the payload, as it’s Base64-encoded (not encrypted).
  - Protect the secret key; if compromised, attackers can forge tokens.

### 4. **Practical Use Case**
- **Scenario**: Multiple applications (e.g., a cryptocurrency market and a digital wallet) sharing a single user session.
- **Solution**: Use JWT with a shared secret key across apps to enable seamless authorization without repeated logins.
- **Example**: User logs into the market app, receives a JWT, and uses it to access the wallet app without re-authenticating.
- **Architecture**: Ideal for microservices, where APIs are stateless but need user context via token decoding.

### 5. **Implementing JWT in PyCharm (FastAPI)**
- **Library**: Use `PyJWT` for encoding/decoding JWTs.
- **Installation**:
  ```bash
  pip install pyjwt
  ```
- **Example Code** (add to `routers/auth.py` in your ToDoApp):
  ```python
  from fastapi import APIRouter, Depends, HTTPException
  from passlib.context import CryptContext
  import jwt
  from datetime import datetime, timedelta
  from fastapi.security import OAuth2PasswordBearer

  router = APIRouter()
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
  SECRET_KEY = "learn_online"  # Replace with a secure key
  ALGORITHM = "HS256"

  def create_jwt_token(data: dict):
      to_encode = data.copy()
      expire = datetime.utcnow() + timedelta(hours=1)
      to_encode.update({"exp": expire})
      return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  @router.post("/token")
  async def login(username: str, password: str):
      # Replace with actual user validation
      if pwd_context.verify(password, hashed_password):  # Assume hashed_password from DB
          token_data = {"sub": username}
          return {"access_token": create_jwt_token(token_data), "token_type": "bearer"}
      raise HTTPException(status_code=401, detail="Invalid credentials")

  def verify_jwt_token(token: str = Depends(oauth2_scheme)):
      try:
          payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
          return payload
      except jwt.PyJWTError:
          raise HTTPException(status_code=401, detail="Invalid token")
  ```
- **Integration**:
  - Use `verify_jwt_token` in protected routes (e.g., in `todos.py`):
    ```python
    @router.get("/todos")
    def read_all(token: dict = Depends(verify_jwt_token), db: Session = Depends(get_db)):
        return db.query(Todos).filter(Todos.owner_id == token["sub"]).all()
    ```

### 6. **Testing JWT**
- **Tool**: Use `https://jwt.io` to encode/decode JWTs for debugging.
- **Validation**: If the secret key or token is altered, the server detects an invalid signature, ensuring security.

### 7. **Best Practices**
- Always set an `exp` claim (e.g., 1 hour) to limit token validity.
- Store the secret key securely (e.g., in environment variables using `python-dotenv`).
- Avoid sensitive data in the payload (e.g., passwords).
- Use HTTPS to prevent token interception.
- In microservices, share the same secret key across services for seamless authorization.

### 8. **Connection to Your ToDoApp**
- **Context**: Your FastAPI project uses `passlib` for password hashing and likely `PyJWT` for JWT handling in `auth.py`.
- **Fixing the Database Error**:
  - The current error (`no such column: todo.owner_id`) indicates the `todo` table lacks an `owner_id` column, but your `Todos` model expects it (likely tied to JWT’s `sub` claim for user-specific todos).
  - Update the database schema:
    ```bash
    del todoapp.db
    ```
    Ensure `models.py` includes:
    ```python
    from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
    from database import Base

    class Users(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True, index=True)
        username = Column(String, unique=True)
        hashed_password = Column(String)

    class Todos(Base):
        __tablename__ = "todo"
        id = Column(Integer, primary_key=True, index=True)
        title = Column(String)
        description = Column(String)
        priority = Column(Integer)
        complete = Column(Boolean, default=False)
        owner_id = Column(Integer, ForeignKey("users.id"))
    ```
    Recreate the database:
    ```python
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from models import Base

    engine = create_engine("sqlite:///todoapp.db")
    Base.metadata.create_all(bind=engine)
    ```
- **JWT Integration**: Ensure `auth.py` generates JWTs with `sub` as the user ID, and `todos.py` filters todos by `owner_id` matching `sub`.

### 9. **PyCharm Tips**
- **File**: Save these notes as `jwt_notes.md` in your project folder (`E:\Fast-API-Proj\ToDoApp`).
- **Debugging**:
  - Use PyCharm’s debugger to step through `auth.py` and `todos.py`.
  - Set breakpoints in `create_jwt_token` and `verify_jwt_token` to inspect token creation/validation.
- **Environment Variables**:
  - Create a `.env` file for the secret key:
    ```env
    SECRET_KEY=your_secure_secret_key
    ```
  - Load it in `auth.py`:
    ```python
    from dotenv import load_dotenv
    import os
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY")
    ```
- **Run Configuration**:
  - Create a PyCharm run configuration for `uvicorn main:app --reload`.
  - Ensure the virtual environment (`venv`) is selected in the Python interpreter settings.

---

### Save in PyCharm
1. In PyCharm, create a new file: `File > New > File > jwt_notes.md`.
2. Copy-paste the above notes.
3. Use the markdown preview (`View > Open in Browser`) to view formatted notes.
4. Reference these notes while implementing JWT in `auth.py` and fixing the database schema.

### Next Steps for Your ToDoApp
- **Fix the Database**:
  - Share `models.py`, `todos.py`, and `database.py` to confirm the schema and setup.
  - Recreate the database or use Alembic to add `owner_id`.
- **Implement JWT**:
  - Add the above JWT code to `auth.py`.
  - Update `todos.py` to filter by `owner_id` based on the JWT `sub` claim.
- **Test**:
  - Run `uvicorn main:app --reload`.
  - Test the `/token` endpoint with a tool like Postman to get a JWT.
  - Use the JWT in the `Authorization` header (`Bearer <token>`) for todo routes.

Let me know if you need help with the database fix or JWT implementation! Please share the requested files (`models.py`, `todos.py`, `database.py`) to address the `owner_id` error.