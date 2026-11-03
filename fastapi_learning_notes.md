# FastAPI Learning Notes

## 1. What is FastAPI?

FastAPI is a Python framework for building APIs. It supports type hints,
request validation, automatic API documentation, and asynchronous
programming.

Common uses include: - Building REST APIs - Creating backend services
for web or mobile applications - Connecting frontend applications to
databases and business logic

## 2. Project setup with `uv`

`uv` is a Python project and dependency manager. In this project, use
`uv` to add packages and run the application.

Run the development server:

``` bash
uv run fastapi dev main.py
```

Useful URLs while the server is running:

-   Application: `http://127.0.0.1:8000/`
-   Interactive API documentation: `http://127.0.0.1:8000/docs`
-   Alternative documentation: `http://127.0.0.1:8000/redoc`

## 3. Creating a FastAPI application

``` python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI"}

@app.get("/about")
def about():
    return {"message": "Welcome to About"}
```

-   `FastAPI()` creates the application.
-   `@app.get("/")` registers a function to handle `GET /`.
-   `home()` runs when a matching request reaches that route.
-   Returning a Python dictionary produces a JSON response.

The decorator connects a URL path and HTTP method to an endpoint
function.

## 4. HTTP methods

  Method     Typical purpose
  ---------- ----------------------------------
  `GET`      Retrieve data
  `POST`     Create a resource or submit data
  `PUT`      Replace a resource
  `PATCH`    Partially update a resource
  `DELETE`   Delete a resource

These are common conventions. The exact behavior depends on how the
endpoint is implemented.

## 5. Path parameters

Path parameters are part of the URL.

``` python
@app.get("/books/{book_id}")
def get_book(book_id: int):
    return {"book_id": book_id}
```

For a request such as `GET /books/10`, FastAPI reads `10` from the URL,
converts it to an integer, and passes it to `get_book`.

Because `book_id` is annotated as `int`, FastAPI validates the value. An
invalid integer value normally produces a `422 Unprocessable Entity`
response.

## 6. Query parameters

Query parameters are written after `?` in a URL.

``` python
@app.get("/books")
def get_books(category: str = "all"):
    return {"category": category}
```

Examples:

-   `/books` uses the default value `"all"`.
-   `/books?category=python` passes `"python"`.

A parameter that is not part of the route path is generally interpreted
as a query parameter, unless it is declared as a request body or
dependency.

## 7. Request bodies with Pydantic

Pydantic models describe and validate the structure of incoming data.

``` python
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    price: float
    description: str | None = None

@app.post("/books")
def create_book(book: Book):
    return {
        "message": "Book added successfully",
        "book": book
    }
```

Example JSON request body:

``` json
{
  "title": "Learning Python",
  "author": "Alex",
  "price": 499.0,
  "description": "A beginner-friendly book"
}
```

Key points:

-   `BaseModel` defines a data model.
-   `book: Book` tells FastAPI to parse and validate the request body as
    a `Book`.
-   `title: str` means the field is required and must be a string.
-   `price: float` means the field must be convertible to a number.
-   `description: str | None = None` means the field may be omitted or
    set to `null`.

### Optional and nullable fields

These declarations have different meanings:

  -----------------------------------------------------------------------
  Declaration                         Meaning
  ----------------------------------- -----------------------------------
  `name: str`                         Required; must be a string

  `name: str = "Guest"`               May be omitted; defaults to
                                      `"Guest"`; cannot be `null`

  `name: str \| None`                 Required, but may be `null`

  `name: str \| None = None`          May be omitted and may be `null`
  -----------------------------------------------------------------------

For Python 3.10 and later, `str | None` is valid union type syntax. No
backslash is used in Python code; the backslash shown in this Markdown
table only escapes the pipe character for table formatting.

## 8. Response models

A response model describes and filters the data returned by an endpoint.

``` python
class BookResponse(BaseModel):
    title: str
    author: str

@app.post("/books/preview", response_model=BookResponse)
def preview_book(book: Book):
    return book
```

Although the input `Book` can include `price` and `description`, the
response model includes only `title` and `author`.

Use response models to make API responses consistent and avoid returning
fields that should not be exposed.

## 9. Status codes

You can use `status` constants instead of remembering numeric codes.

``` python
from fastapi import status

@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    return {"message": "Book added successfully", "book": book}
```

Common status codes:

  Code                          Meaning
  ----------------------------- -------------------------------------------------
  `200 OK`                      Request succeeded
  `201 Created`                 A resource was created
  `204 No Content`              Request succeeded with no response body
  `400 Bad Request`             Request is invalid
  `401 Unauthorized`            Authentication is required or failed
  `403 Forbidden`               The client is not allowed to perform the action
  `404 Not Found`               Resource was not found
  `422 Unprocessable Entity`    Request data failed validation
  `500 Internal Server Error`   Unexpected server error

## 10. PUT and PATCH

### PUT: replace a resource

``` python
@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    return {
        "message": "Book replaced",
        "book_id": book_id,
        "book": book
    }
```

This example demonstrates receiving the full replacement data. It does
not actually update a database.

### PATCH: update selected fields

``` python
class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    price: float | None = None

@app.patch("/books/{book_id}")
def part_upd_book(book_id: int, book: BookUpdate):
    changes = book.model_dump(exclude_unset=True)
    return {
        "message": "Book partially updated",
        "book_id": book_id,
        "changes": changes
    }
```

`model_dump(exclude_unset=True)` returns only fields explicitly included
in the request. This helps avoid overwriting existing values with
defaults for fields that the client did not send.

For example, if the request body is:

``` json
{
  "price": 250
}
```

then `changes` contains only:

``` json
{
  "price": 250.0
}
```

Important distinction:

-   `exclude_unset=True` excludes fields not supplied by the client.
-   `exclude_none=True` excludes fields whose value is `None`.
-   If a client explicitly sends a field as `null`, `exclude_unset=True`
    alone keeps that field in the result.

A real update endpoint must also retrieve the existing record, apply
changes, and save the result to persistent storage.

## 11. DELETE endpoint

``` python
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    return {
        "message": "Book deleted",
        "book_id": book_id
    }
```

This demonstrates a delete route and response. It does not delete a real
database record because no database operation is implemented.

## 12. Error handling with `HTTPException`

Use `HTTPException` when an endpoint needs to return an HTTP error.

``` python
from fastapi import HTTPException

@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id != 1:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return {
        "book_id": 1,
        "title": "Basic Python"
    }
```

-   `status_code=404` sets the HTTP status code.
-   `detail` provides an explanation in the error response.
-   Raising the exception stops normal execution of the endpoint and
    returns an error response.

Avoid defining the same HTTP method and path multiple times in the same
application. Use distinct paths or separate routers with clear prefixes.

## 13. APIRouter and project structure

`APIRouter` lets you group related endpoints in separate modules instead
of putting every route in `main.py`.

Example `books.py`:

``` python
from fastapi import APIRouter

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/")
def get_books():
    return {"books": ["Python", "Django"]}

@router.get("/{book_id}")
def get_book(book_id: int):
    return {"book_id": book_id}
```

Example `main.py`:

``` python
from fastapi import FastAPI
from books import router as bookrouter

app = FastAPI()
app.include_router(bookrouter)

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI"}
```

Important concepts:

-   `APIRouter()` creates a group of routes.
-   `prefix="/books"` adds `/books` to the beginning of routes
    registered on that router.
-   `tags=["Books"]` groups routes under the "Books" heading in the
    interactive API documentation. Tags do not change the URL.
-   `app.include_router(bookrouter)` registers the router's routes with
    the main application.
-   The router prefix applies to routes registered on that router, not
    to unrelated routes declared directly with `@app.get(...)`.

## 14. Dependency injection with `Depends`

Dependencies allow FastAPI to call reusable functions and provide their
results to endpoints.

Example `users.py`:

``` python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

def get_current_user():
    return {"username": "fakecurrentuser"}
```

Example usage in `main.py`:

``` python
from fastapi import FastAPI, Depends
from users import router as userrouter
from users import get_current_user

app = FastAPI()
app.include_router(userrouter)

@app.get("/profile")
def get_profile(user: dict = Depends(get_current_user)):
    return {"profile": user}
```

How it works:

1.  FastAPI receives a request for `/profile`.
2.  It sees `Depends(get_current_user)`.
3.  FastAPI calls `get_current_user`.
4.  The dependency's return value is passed into the `user` parameter.
5.  The endpoint returns the profile response.

Important points:

-   Use `Depends(get_current_user)`, without parentheses.
-   `Depends()` itself does not authenticate a user. The dependency must
    implement the required authentication or user lookup logic.
-   The example returns a fake user for learning purposes; it is not
    real authentication.
-   `user: dict` is a type annotation. FastAPI does not automatically
    validate an ordinary dependency's return value against that
    annotation.
-   Dependencies can be reused, can themselves have dependencies, and
    FastAPI normally caches the same dependency result within a request.

### Comparison with Django

Django commonly provides the authenticated user through `request.user`,
with authentication handled by its middleware and authentication system.
In FastAPI, dependencies are often used to extract and validate
credentials and retrieve the current user. The dependency function must
implement that work.

## 15. HTTP middleware

Middleware runs around request handling. It can inspect a request before
the endpoint executes and inspect or modify the response before it is
returned to the client.

Example `middleware.py`:

``` python
import time
from fastapi import Request

async def log_request(request: Request, call_next):
    start_time = time.time()

    print(f"Request: {request.method} {request.url.path}")

    response = await call_next(request)

    process_time = time.time() - start_time
    print(f"Processing time: {process_time:.4f} seconds")

    return response
```

Register it in `main.py`:

``` python
from fastapi import FastAPI
from middleware import log_request

app = FastAPI()
app.middleware("http")(log_request)
```

### Middleware request/response flow

1.  An HTTP request arrives.
2.  Middleware runs and can log the method and URL path.
3.  `await call_next(request)` passes the request onward through the
    application.
4.  FastAPI routing selects the matching endpoint, which executes.
5.  The endpoint produces a response.
6.  Middleware receives the response and can perform additional work.
7.  `return response` allows the response to continue back to the
    client.

### What are `request`, `call_next`, and `response`?

-   `request` receives the incoming HTTP request.
-   `call_next` is a callable supplied by the HTTP middleware mechanism.
-   `call_next(request)` passes the request onward and produces the
    resulting response.
-   `response` stores that response.
-   `await` waits for the asynchronous operation to finish before the
    middleware continues.

`call_next` is a conventional parameter name, not a Python keyword. It
can be given another parameter name, but `call_next` is clearer and
conventional.

The line:

``` python
app.middleware("http")(log_request)
```

registers `log_request` as HTTP middleware. `"http"` identifies the
middleware type; it is not a URL or an HTTP method.

Printing the request does not itself execute the endpoint. The request
must be passed onward, which is what `call_next(request)` does in this
middleware pattern.

## 16. Environment variables and `.env`

Environment variables keep configuration separate from application code.
They are useful for settings that vary between development and
production, such as database credentials, debug settings, and service
URLs.

Example `.env` file:

``` dotenv
APP_NAME=My Book API
DEBUG=True

DATABASE_HOST=localhost
DATABASE_USER=root
DATABASE_PASSWORD=change_me
DATABASE_NAME=books_db
```

This is example configuration. Replace placeholder values with your own
settings. Do not commit real secrets to source control.

### Install `pydantic-settings`

Because this project uses `uv`, run:

``` bash
uv add pydantic-settings
```

### Create `config.py`

``` python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "FastAPI App"
    debug: bool = False

    database_host: str
    database_user: str
    database_password: str
    database_name: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
```

Explanation:

-   `BaseSettings` loads configuration from environment variables and
    supported configuration sources.
-   `SettingsConfigDict(env_file=".env")` tells Pydantic Settings to
    read the `.env` file.
-   Field type annotations describe expected types.
-   Fields without defaults are required. If a required value is
    missing, settings creation raises a validation error.
-   `settings = Settings()` creates the settings object and
    loads/validates the values.
-   Values such as `DEBUG=True` are converted to the declared Boolean
    type.

Environment variable names are matched case-insensitively by default.
For example, `APP_NAME` maps to `app_name`.

### Use settings in `main.py`

``` python
from fastapi import FastAPI
from config import settings

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

@app.get("/")
def home():
    return {
        "app_name": settings.app_name,
        "debug": settings.debug
    }
```

This example demonstrates loading settings. Defining `DATABASE_HOST`,
`DATABASE_USER`, and related values does not connect to MySQL by itself.
A database driver and database integration code are needed for an actual
connection.

### `.env` versus `python-dotenv` and `os.getenv()`

An alternative is to use `python-dotenv` with `os.getenv()`:

``` python
import os
from dotenv import load_dotenv

load_dotenv()

db_name = os.getenv("DB_NAME")
debug = os.getenv("DEBUG", "False").lower() == "true"
```

Comparison:

-   `python-dotenv` loads `.env` values into the process environment.
-   `os.getenv()` retrieves an environment variable, normally as a
    string or `None`.
-   Manual conversion may be required for Boolean and numeric values.
-   `pydantic-settings` can read `.env` files directly, convert values
    to declared types, and validate required settings.

Both approaches are valid. For this learning project,
`pydantic-settings` keeps configuration organized and provides
convenient validation.

### Protect secrets with `.gitignore`

Add these entries to `.gitignore`:

``` gitignore
.env
.venv/
__pycache__/
*.py[cod]
```

Important: adding `.env` to `.gitignore` does not untrack a file that
was already committed. If a real credential was exposed, rotate or
change it.

## 17. Recommended project structure

The project files covered so far can be organized like this:

``` text
fastapi_project/
├── main.py
├── books.py
├── users.py
├── middleware.py
├── config.py
├── .env
├── .gitignore
├── pyproject.toml
└── uv.lock
```

Responsibilities:

  -----------------------------------------------------------------------
  File                                Responsibility
  ----------------------------------- -----------------------------------
  `main.py`                           Creates the FastAPI app, includes
                                      routers, registers middleware, and
                                      defines app-level routes

  `books.py`                          Groups book-related routes using
                                      `APIRouter`

  `users.py`                          Holds user-related routes or
                                      reusable user dependency functions

  `middleware.py`                     Defines HTTP middleware

  `config.py`                         Loads and validates application
                                      configuration

  `.env`                              Stores local configuration values;
                                      should not be committed if it
                                      contains secrets

  `.gitignore`                        Lists files and folders Git should
                                      ignore

  `pyproject.toml`                    Project metadata and declared
                                      dependencies managed by `uv`

  `uv.lock`                           Locks resolved dependency versions
                                      for reproducible installs
  -----------------------------------------------------------------------

## 18. Important limitations of the current examples

Many examples in these notes demonstrate FastAPI request handling, but
do not yet implement persistent database operations.

-   The create endpoint returns the submitted book but does not save it.
-   The PUT endpoint returns replacement data but does not update a
    stored record.
-   The PATCH endpoint shows which fields were submitted but does not
    update a stored record.
-   The DELETE endpoint returns a message but does not delete a stored
    record.
-   The sample `get_current_user` function returns a hardcoded example
    user; it is not a real authentication system.
-   The `.env` configuration provides database settings but does not
    create a MySQL connection.

These are intentional learning examples. Database integration,
authentication, and testing can be added as separate topics.

## 19. Quick revision checklist

Before moving on, make sure you can explain these concepts:

-   [ ] What `FastAPI()` creates
-   [ ] How route decorators connect methods and paths to functions
-   [ ] The difference between path and query parameters
-   [ ] How Pydantic validates request bodies
-   [ ] Required, optional, and nullable fields
-   [ ] How `response_model` shapes output
-   [ ] When to use GET, POST, PUT, PATCH, and DELETE
-   [ ] How status codes and `HTTPException` work
-   [ ] Why and how to use `APIRouter`
-   [ ] How `Depends()` supplies dependency results to endpoints
-   [ ] How HTTP middleware wraps request handling
-   [ ] What `call_next(request)` does
-   [ ] How `.env` and `pydantic-settings` manage configuration
-   [ ] Why `.env` should be excluded from Git when it contains secrets