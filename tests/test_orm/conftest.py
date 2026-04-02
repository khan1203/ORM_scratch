from roob.orm.sqlite_orm import Table, PrimaryKey, Column, ForeignKey


class Author(Table):
    id = PrimaryKey()
    name = Column(str)
    age = Column(int)


class Book(Table):
    id = PrimaryKey()
    title = Column(str)
    published = Column(bool)
    author = ForeignKey(Author)