import sys
from pathlib import Path

# Adding project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from wsgiref.simple_server import make_server

from core import app
from core.api import product_controller
from core.api import auth_controller
from core.view import home_controller
from core.view import book_controller

if __name__ == "__main__":
    host = "localhost"
    port = 8000
    with make_server(host, port, app=app) as server:
        print(f"Listening to http://{host}:{port}")
        server.serve_forever()
