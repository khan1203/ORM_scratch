import sqlite3


class Column:
    def __init__(self, column_type):
        self.type = column_type
    @property
    def sql_type(self):
        type_map = {
            int: "INTEGER",
            float: "REAL",
            str: "TEXT",
            bytes: "BLOB",
            bool: "INTEGER",  # 0 or 1
        }
        return type_map[self.type]
class PrimaryKey(Column):
    def __init__(self, column_type=int, auto_increment=True):
        self.auto_increment = auto_increment
        super().__init__(column_type)
class TableMeta(type):
    def __new__(cls, name, bases, attrs):
        columns = {}  # Collect fields in declaration order
        for key, value in attrs.items():
            if isinstance(value, Column):
                columns[key] = value
        table_cls = super().__new__(cls, name, bases, attrs)
        table_cls._columns = columns
        return table_cls


class Table(metaclass=TableMeta):
    def __init__(self, **kwargs):
        self._data = {
            "id": None,
        }
        for key, value in kwargs.items():
            self._data[key] = value
        self.id = self._data["id"]

    def __getattribute__(self, key):
        # A python magic method that gets invoked when an instance field is accessed.
        # such as any defined author.name attribute or dynamic attribute like author.id

        # whenever any field is called we first try to return it from our data dictionary
        # or directly from the instance

        # can't use self._data as it will call __getattribute__ again and again leading to an infinite recursion call
        _data = super().__getattribute__("_data")
        if key in _data:
            return _data[key]

        return super().__getattribute__(key)

    @classmethod
    def _get_create_sql(cls):
        CREATE_TABLE_SQL = "CREATE TABLE IF NOT EXISTS {name} ({fields});"
        fields = []
        for name, field in cls._columns.items():
            if isinstance(field, PrimaryKey):
                sql = f"{name} {field.sql_type} PRIMARY KEY"
                if field.auto_increment:
                    sql += " AUTOINCREMENT"
                fields.append(sql)
            elif isinstance(field, ForeignKey):
                fields.append(f"{name}_id INTEGER")
            elif isinstance(field, Column):
                fields.append(f"{name} {field.sql_type}")
        table_name = cls.__name__.lower()
        fields = ", ".join(fields)
        return CREATE_TABLE_SQL.format(name=table_name, fields=fields)

    def _get_insert_sql(self) -> tuple[str, list]:
        # "INSERT INTO author (age, name) VALUES (?, ?);"
        INSERT_SQL = "INSERT INTO {name} ({fields}) VALUES ({placeholders});"

        fields = []
        placeholders = []
        values = []
        for name, field in self._columns.items():
            if isinstance(field, ForeignKey):
                fields.append(name + "_id")
                field_value: Table = getattr(self, name)
                values.append(field_value.id)
                placeholders.append("?")
            elif isinstance(field, Column):
                fields.append(name)
                values.append(getattr(self, name))
                placeholders.append("?")

        fields = ", ".join(fields)
        placeholders = ", ".join(placeholders)
        table_name = self.__class__.__name__.lower()
        query = INSERT_SQL.format(
            name=table_name,
            fields=fields,
            placeholders=placeholders,
        )
        return query, values




class ForeignKey(Column):
    def __init__(self, table: type[Table], column_type=int):
        self.table = table
        super().__init__(column_type)
class Database:
    def __init__(self, path):
        self.path = path
        self.connection = sqlite3.Connection(self.path)
    @property
    def tables(self):
        result_set = self.connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        return [rs[0] for rs in result_set]
    def create(self, table: type[Table]):
        raw_sql = table._get_create_sql()
        self.connection.execute(raw_sql)

    def save(self, table_instance: Table):
        sql, values = table_instance._get_insert_sql()
        cursor = self.connection.execute(sql, values)
        table_instance._data["id"] = cursor.lastrowid
        self.connection.commit()