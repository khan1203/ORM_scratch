import pytest
from pathlib import Path

from roob.common_handlers import CommonHandlers
from tests.utils.test_framework import TestFramework
from tests.utils.temp_file_builder import TempFileBuilder

@pytest.fixture
def app() -> TestFramework:
    cwd = Path(__file__).resolve().parent
    app = TestFramework(template_dir=f"{cwd}/templates")
    
    return app


@pytest.fixture
def client(app: TestFramework):
    return app.test_session()

@pytest.fixture
def temp_file_builder(tmpdir_factory) -> TempFileBuilder:
    return TempFileBuilder(tmpdir_factory, root_dir="static")