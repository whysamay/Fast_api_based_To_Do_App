# FastAPI Authentication and Authorization Notes

## Core Concepts

1.  **Authentication (AuthN):**
    *   Verifying *who* a user is.
    *   Achieved through username/password login and issuance of an access token.

2.  **Authorization (AuthZ):**
    *   Determining *what* an authenticated user is allowed to do.
    *   Foundation laid by `get_current_user`, which provides authenticated user details for endpoints to make authorization decisions.

3.  **JWT (JSON Web Tokens):**
    *   Standard for securely transmitting information (user details, expiration) as a JSON object.
    *   Signed with a `SECRET_KEY` using an `ALGORITHM` (e.g., HS256).
    *   Client sends the JWT (access token) in the `Authorization: Bearer <token>` header for protected requests.
    *   Server verifies signature and expiration.

4.  **Password Hashing:**
    *   Passwords are *never* stored in plain text.
    *   `passlib.context.CryptContext` (e.g., with `bcrypt`) is used to:
        *   Hash passwords during registration.
        *   Verify submitted passwords against stored hashes during login.

5.  **Separation of Concerns:**
    *   Dividing tasks into distinct, manageable components (e.g., token extraction vs. token validation).
    *   Enhances reusability, testability, and maintainability.

## Key FastAPI & Related Components

### 1. `OAuth2PasswordBearer`

*   **Purpose:**
    1.  **Token Extractor:** Automatically looks for and extracts the token string from the `Authorization: Bearer <token>` header in incoming requests.
    2.  **API Documentation Aid:** The `tokenUrl` parameter (e.g., `tokenUrl='auth/token'`) informs API documentation tools (like Swagger UI) where clients should go to obtain an access token.
    3.  **Basic Error Handling:** Handles missing or malformed `Authorization` headers by typically raising HTTP 401/403 errors.
*   **Usage:**
    ```python
    from fastapi.security import OAuth2PasswordBearer
    oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
    # Used with Depends() in functions that need the token:
    # async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]): ...
    ```
*   **Does NOT:** Validate token content, signature, or expiration. This is done separately.

### 2. `typing.Annotated`

*   **Purpose:** Adds metadata to Python type hints, allowing frameworks like FastAPI to understand how to process parameters.
*   **Syntax:** `Annotated[<Actual_Type>, <Metadata1>, <Metadata2>, ...]`
*   **Usage with FastAPI `Depends`:**
    ```python
    from typing import Annotated
    from fastapi import Depends
    from sqlalchemy.orm import Session
    # from .dependencies import get_db, oauth2_bearer # Assuming these are defined

    # Example 1: For DB session
    db_dependency = Annotated[Session, Depends(get_db)]

    # Example 2: For token string
    # async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]): ...
    ```
*   **Benefits:**
    *   **Clarity:** Explicitly separates type from how it's obtained/validated.
    *   **Multiple Metadata:** Can combine `Depends` with other metadata (e.g., `Query`, `Body`, `Path` for parameter location/validation).
    *   **Type Checker Friendly:** Standard Python typing feature.

### 3. `OAuth2PasswordRequestForm`

*   **Purpose:** A pre-defined Pydantic model by FastAPI representing the data structure for the **OAuth 2.0 Password Grant flow**. Used at the `/token` endpoint.
*   **Expected Data:** Clients POST data as `application/x-www-form-urlencoded` to the `/token` endpoint.
*   **Fields:**
    *   `username: str` (required)
    *   `password: str` (required)
    *   `scope: str` (optional, space-separated list of requested permissions)
    *   `grant_type: str` (optional, should be "password" for this flow)
    *   `client_id: str` (optional)
    *   `client_secret: str` (optional)
*   **Usage in `/token` endpoint:**
    ```python
    from fastapi.security import OAuth2PasswordRequestForm
    # from .models import Token # Your Pydantic model for the token response

    # @router.post("/token", response_model=Token)
    # async def login_for_access_token(
    #     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    #     # ... other dependencies like db_session
    # ):
    #     # form_data.username and form_data.password are now available
    #     # Authenticate user, create token...
    #     pass
    ```
*   **Functionality:** FastAPI (via `Depends()`) automatically parses the form data, validates it against the model, and provides a populated `OAuth2PasswordRequestForm` instance to your endpoint function.

## Core Authentication Functions (Conceptual)

### 1. `get_db` (Database Dependency)

*   **Purpose:** Provides a database session to path operation functions and ensures it's closed after the request.
*   **Implementation:** Typically a generator function using `try...finally` to manage session lifecycle.
    ```python
    # from .database import SessionLocal
    # def get_db():
    #     db = SessionLocal()
    #     try:
    #         yield db
    #     finally:
    #         db.close()
    ```

### 2. `authenticate_user(username, password, db)`

*   **Purpose:** Verifies a user's credentials against the database.
*   **Steps:**
    1.  Fetch user by `username` from `db`.
    2.  If user exists, verify `password` against `user.hashed_password` using `bcrypt_context.verify()`.
    3.  Return user object if valid, `False` or `None` otherwise.

### 3. `create_access_token(username, user_id, expires_delta)`

*   **Purpose:** Generates a JWT.
*   **Steps:**
    1.  Create a payload dictionary (e.g., `{'sub': username, 'id': user_id}`).
    2.  Calculate expiration time (`datetime.now(timezone.utc) + expires_delta`).
    3.  Add `exp` (expiration) claim to payload.
    4.  Encode payload using `jose.jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)`.
    5.  Return the encoded JWT string.

### 4. `get_current_user(token: Annotated[str, Depends(oauth2_bearer)])`

*   **Purpose:** The "bouncer." Validates an incoming token and retrieves the authenticated user's information. This is a crucial dependency for protected endpoints.
*   **Steps:**
    1.  Receives the `token` string (extracted by `oauth2_bearer`).
    2.  **Decode & Validate:** Use `jose.jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])`.
        *   Handles `JWTError` (e.g., invalid signature, expired token, malformed token) by raising `HTTPException(status.HTTP_401_UNAUTHORIZED)`.
    3.  **Extract Claims:** Get `username` (from `sub` claim) and `user_id` (from `id` claim) from the decoded payload.
    4.  **Verify Claims Presence:** Ensure `username` and `user_id` are present in the payload. If not, raise `HTTPException(status.HTTP_401_UNAUTHORIZED)`.
    5.  **(Optional but Recommended):** Check if the user (e.g., by `user_id`) still exists in the database and is active. Raise 401 if not.
    6.  Return user information (e.g., `{'username': username, 'id': user_id}`).
*   **Usage:** Endpoints requiring authentication will take this as a dependency.
    ```python
    # user_dependency = Annotated[dict, Depends(get_current_user)]
    # @router.get("/users/me")
    # async def read_users_me(current_user: user_dependency):
    #     # current_user now contains {'username': '...', 'id': ...}
    #     ...
    ```

## Workflow Summary

1.  **User Registration (`POST /auth/`):**
    *   Client sends user details (username, password, etc.).
    *   Password is hashed.
    *   User is saved to the database.

2.  **User Login (`POST /auth/token`):**
    *   Client sends `username` and `password` as `x-www-form-urlencoded` data.
    *   `OAuth2PasswordRequestForm` (with `Depends()`) parses this into `form_data`.
    *   `authenticate_user(form_data.username, form_data.password, db)` verifies credentials.
    *   If valid, `create_access_token(...)` generates a JWT.
    *   JWT is returned to the client (e.g., `{"access_token": "...", "token_type": "bearer"}`).

3.  **Accessing Protected Resource (e.g., `GET /users/me`):**
    *   Client includes the JWT in the `Authorization: Bearer <token>` header.
    *   The endpoint depends on `get_current_user`.
    *   `oauth2_bearer` (within `get_current_user`'s dependencies) extracts the token string.
    *   `get_current_user` decodes, validates the token, and checks claims.
    *   If valid, `get_current_user` returns user details to the endpoint function.
    *   The endpoint function executes, now knowing the identity of the authenticated user.

## Configuration Constants

*   `SECRET_KEY`: A long, random, secret string for signing JWTs. **Keep this secure!**
*   `ALGORITHM`: The algorithm used for JWT signing (e.g., `'HS256'`).

---