from pathlib import Path

from core.middlewares import TokenMiddleware
from roob import Roob
from roob.middlewares import (
    ErrorHandlerMiddleware,
    ExecutionTimeMiddleware,
    ReqResLoggingMiddleware
)
cwd = Path(__file__).resolve().parent
app = Roob(
    template_dir=f"{cwd}/templates",
    static_dir=f"{cwd}/static"
)
app.add_middleware(TokenMiddleware)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(ExecutionTimeMiddleware)
app.add_middleware(ReqResLoggingMiddleware)