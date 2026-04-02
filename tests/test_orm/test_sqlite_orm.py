import os
import sqlite3

from roob.orm.sqlite_orm import Database
from tests.test_orm.conftest import Author, Book


class TestSqliteORM:
    def setup_class(self):
        self.db = Database("./test.db")

    def teardown_class(self):
        os.remove("./test.db")

    def test_db_conn(self):
        assert isinstance(self.db.connection, sqlite3.Connection)

    def test_define_tables(self):
        assert Author.name.type == str
        assert Author.name.sql_type == "TEXT"

        assert Book.author.table == Author
        assert Author.age.sql_type == "INTEGER"

    def test_create_table(self):
        self.db.create(Author)
        self.db.create(Book)
        db_tables = self.db.tables
        assert "author" in db_tables
        assert "book" in db_tables

    def test_table_creation_sql(self):
        assert Author._get_create_sql() == "CREATE TABLE IF NOT EXISTS author (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER);"
        assert Book._get_create_sql() == "CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, published INTEGER, author_id INTEGER);"