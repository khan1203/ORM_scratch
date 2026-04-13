from pathlib import Path

from core.middlewares import TokenMiddleware
from core.models.book import Book

from roob import Roob
from roob.middlewares import (
    ErrorHandlerMiddleware,
    ExecutionTimeMiddleware,
    ReqResLoggingMiddleware
)

from roob.orm.db_factory import DatabaseFactory, Dialect

cwd = Path(__file__).resolve().parent
app = Roob(
    template_dir=f"{cwd}/templates",
    static_dir=f"{cwd}/static"
)
app.add_middleware(TokenMiddleware)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(ExecutionTimeMiddleware)
app.add_middleware(ReqResLoggingMiddleware)

db = DatabaseFactory(dialect=Dialect.SQLITE).get_connection("./myapp.db")
db.create(Book)