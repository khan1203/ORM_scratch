from roob.orm.table import Table
from roob.orm.column import PrimaryKey, Column, ForeignKey


class Author(Table):
    id = PrimaryKey()
    name = Column(str)
    age = Column(int)


class Book(Table):
    id = PrimaryKey()
    title = Column(str)
    published = Column(bool)
    author = ForeignKey(Author)