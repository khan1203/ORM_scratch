# Roob

Roob is a small, educational WSGI-compatible Python web framework built from scratch to help you understand how web frameworks work. It's intentionally lightweight and opinionated for learning and experimentation.

## Features
- **WSGI Compatible**: The framework exposes a callable application usable with any WSGI server.
- **Routing**: Supports both automatic (path pattern) and explicit route registration.
- **Handlers**: Function-based and class-based handlers are supported.
- **Middlewares**: Compose request/response processing via middleware classes. Includes `ErrorHandlerMiddleware` and helpers.
- **Templating**: Provides a templating system accessible via the `template()` helper on the app.
- **Static Files**: Static files (CSS/JS/images) can be served from a `static/` directory.
- **Error Handling**: Built-in `ResponseError` and optional middleware to convert exceptions into JSON responses.
- **HTTP Method Control**: Route definitions can restrict allowed HTTP methods.
- **Published**: The package is available on PyPI for easy installation.

## Installation
- **From PyPI**: `pip install Roob`

## Quick Start

- **Create a minimal app**

```python
from Roob.framework import Roob
app = Roob()

@app.route('/')
def index(request):
    return app.templates_env.get_template('dashboard.html').render()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8080, app)
    print('Serving on http://0.0.0.0:8080')
    server.serve_forever()
```

## Function-based handler

```python
from Roob.framework import Roob
from Roob.models.responses import JSONResponse

app = Roob()

@app.route('/hello')
def hello(request):
    return JSONResponse({"message": "Hello from Roob"})
```

## Class-based Handler
Roob support both automatic and manually registered Class Based handlers

### Self registered Class-based Handler
The function names should matched with HTTP request method.
```python
@app.route('/items')
class ItemHandler:
    def __init__(self):
        self.service = ItemService()

    # get all products
    def get(self, request):
        items: list[dict] = self.service.get_items()
        return JSONResponse(items)

    # create a product
    def post(self, request):
        items: dict = self.service.create_items()
        return JSONResponse(items)
```
Notes:
- Self registered Class-based handlers are registered as classes. The framework will instantiate the class and call the method matching the HTTP method name (e.g., `get`, `post`).


### Manually registerd Class-based Handler
If you need both custom handlers in a class then you can register routes manually

```python
from Roob.framework import Roob
from Roob.models.responses import JSONResponse

app = Roob()

class ItemHandlerCustomRouting:
    def get_by_id(self, request, item_id=None):
        return JSONResponse({"item_id": item_id})

    def get_by_category(self, request, category=None):
        # JSONResponse also supports list of classes
        items: list[Item] = items_service.get_by_category()
        return JSONResponse(items)

handler = ItemHandlerCustomRouting()
app.add_route('/items/{item_id:d}', handler.get_by_id)
app.add_route('/items/{category}', handler.get_by_category)
```

## Routing & Path Variables
- Paths can include variables using the `{name}` syntax. The framework will parse them and pass as kwargs to your handler.
- Example: `app.add_route('/users/{user_id}', handler)` — handler will receive `user_id` as a keyword argument.

## Middlewares & Error Handling
- **Built-in middlewares**: `ErrorHandlerMiddleware`, `ReqResLoggingMiddleware`, and `ExecutionTimeMiddleware` are provided in `Roob.middlewares` package.
- **ResponseError**: Raise `Roob.exceptions.ResponseError` (or its subclasses) from handlers to return structured JSON error responses. The `ErrorHandlerMiddleware` converts `ResponseError` into an appropriate JSON response with the specified HTTP status.

Example — adding middleware and a simple error:

```python
from Roob.framework import Roob
from Roob.middlewares import ErrorHandlerMiddleware
from Roob.exceptions import ResponseError

app = Roob()
app.add_middleware(ErrorHandlerMiddleware)

@app.route('/fail')
def fail(request):
    raise ResponseError('This is a custom error', 400)
```

- **Response JSON**
```json
{
    "message": "This is a custom error"
}
```

## Templating
- The app provides a templating system. Templates are loaded from the `templates` directory by default. Use `app.template(template_name, context)` to generate view from a template dynamically.

Example:
Register the template if you have a customer template directory

```python
from Roob.framework import Roob
from Roob.models.responses import HTMLResponse

app = Roob(template_dir=f"{cwd}/templates")

@app.route('/dashboard')
def dashboard(request) -> Response:
    name = "Hello User"
    title = "Dashboard View"
    html_content = app.template(
        "dashboard.html", 
        context={"name": name, "title": title}
    )
    return HTMLResponse(html_content)
```

**Static Files**
- Static assets under the `static` directory are served automatically. Place CSS/JS/images in `static/` and reference them from your templates.

**WSGI Compatibility**
- The `Roob` instance is a valid WSGI application. You can run it with any WSGI server (uWSGI, Gunicorn, or `wsgiref` during development).

You can run the demo application with Gunicorn service using
```
make run
```

**Tests & Examples**
- See the `tests/` and `core/` directories in this repository for usage examples and test coverage.

**Contributing**
- This project is intended for learning. Contributions that improve docs, add examples, or clarify internals are welcome.

**License**
- See the `LICENSE` file in this repository.