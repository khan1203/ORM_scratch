from roob.orm.column import PrimaryKey, Column
from roob.orm.table import Table


class Author(Table):
    id = PrimaryKey()
    name = Column(str)
    age = Column(int)


class Book(Table):
    id = PrimaryKey()
    name = Column(str)
    author = Column(str)