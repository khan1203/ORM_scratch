from abc import abstractmethod, ABC
from typing import Any


class SQLType(ABC):
    def __init__(self, python_type: type, cast_fn=None):
        self.python_type = python_type
        self.cast_fn = cast_fn or self.python_type

    def to_python_type(self, column_value: Any) -> Any:
        return self.cast_fn(column_value)

    @property
    @abstractmethod
    def value(self) -> str:
        raise NotImplementedError


class INTEGER(SQLType):
    def __init__(self):
        super().__init__(python_type=int)

    @property
    def value(self) -> str:
        return 'INTEGER'


class BOOLEAN(SQLType):
    def __init__(self):
        super().__init__(python_type=bool)

    @property
    def value(self) -> str:
        return 'INTEGER'


class FLOAT(SQLType):
    def __init__(self):
        super().__init__(python_type=float)

    @property
    def value(self) -> str:
        return 'REAL'


class STRING(SQLType):
    def __init__(self):
        super().__init__(python_type=str)

    @property
    def value(self) -> str:
        return 'TEXT'


class BYTES(SQLType):
    def __init__(self):
        super().__init__(python_type=bytes)

    @property
    def value(self) -> str:
        return 'BLOB'


SQL_TYPE_MAP = {
    int: INTEGER(),
    float: FLOAT(),
    str: STRING(),
    bytes: BYTES(),
    bool: BOOLEAN(),
}