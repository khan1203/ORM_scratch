from webob.request import Request
from webob.response import Response

from core import app
from core.decorators import login_required
from core.service.book_service import BookService
from roob.constants import HttpStatus
from roob.models.responses import JSONResponse, HTMLResponse

service = BookService()


@app.route('/books/all', allowed_methods=["GET"])
def get_all_books(request: Request) -> Response:
    books: list[dict] = service.get_all()
    html_content = app.template("books.html", context={"books": books})
    return HTMLResponse(html_content)


@app.route('/books', allowed_methods=["POST"])
@login_required
def create_book(request: Request) -> Response:
    book_created = service.create(request.json)
    return JSONResponse(book_created, status=HttpStatus.CREATED)


@app.route('/books/{book_id:d}', allowed_methods=["DELETE"])
@login_required
def delete_book(request: Request, book_id: int) -> Response:
    service.delete(book_id)
    return JSONResponse({
        "message": f"Book associated with {book_id} was deleted"
    })