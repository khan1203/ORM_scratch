import sqlite3
from typing import TypeVar

from roob.orm.sql_types import SQL_TYPE_MAP, SQLType
from roob.orm.exceptions import RecordNotFound


class Column:
    def __init__(self, column_type):
        self.type = column_type

    @property
    def sql_type(self) -> SQLType:
        return SQL_TYPE_MAP[self.type]


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

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self._data:
            self._data[key] = value

    @property
    def __dict__(self):
        return self._data

    @classmethod
    def _get_create_sql(cls):
        CREATE_TABLE_SQL = "CREATE TABLE IF NOT EXISTS {name} ({fields});"
        fields = []
        for name, field in cls._columns.items():
            if isinstance(field, PrimaryKey):
                sql = f"{name} {field.sql_type.value} PRIMARY KEY"
                if field.auto_increment:
                    sql += " AUTOINCREMENT"
                fields.append(sql)
            elif isinstance(field, ForeignKey):
                fields.append(f"{name}_id INTEGER")
            elif isinstance(field, Column):
                fields.append(f"{name} {field.sql_type.value}")

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

    @classmethod
    def _get_select_all_sql(cls):
        # SELECT id, name, age from author
        SELECT_ALL_SQL = 'SELECT {fields} FROM {name};'
        table_name = cls.__name__.lower()
        fields = []
        for field_name, field in cls._columns.items():
            if isinstance(field, ForeignKey):
                fields.append(field_name + "_id")
            elif isinstance(field, Column):
                fields.append(field_name)

        sql = SELECT_ALL_SQL.format(name=table_name, fields=", ".join(fields))
        return sql, fields

    @classmethod
    def _get_select_by_id_sql(cls, id: int):
        SELECT_BY_ID_SQL = "SELECT {fields} FROM {name} WHERE id = ?;"
        table_name = cls.__name__.lower()
        fields = []
        for field_name, field in cls._columns.items():
            if isinstance(field, ForeignKey):
                fields.append(field_name + "_id")
            elif isinstance(field, Column):
                fields.append(field_name)
        params = [id]
        sql = SELECT_BY_ID_SQL.format(name=table_name, fields=", ".join(fields))
        return sql, fields, params

    def _get_update_sql(self):
        # UPDATE author SET name = ?, age = ? WHERE id = ?;
        UPDATE_SQL_TEMPLATE = "UPDATE {name} SET {fields} WHERE id = ?;"
        table_name = self.__class__.__name__.lower()
        fields = []
        values = []

        for field_name, field in self._columns.items():
            if isinstance(field, PrimaryKey):
                continue

            if isinstance(field, ForeignKey):
                fields.append(field_name + "_id = ?")
                fk_instance: T = getattr(self, field_name)
                values.append(fk_instance.id)
            elif isinstance(field, Column):
                fields.append(field_name + " = ?")
                field_value = getattr(self, field_name)
                values.append(field_value)

        values.append(getattr(self, 'id'))

        sql = UPDATE_SQL_TEMPLATE.format(
            name=table_name,
            fields=", ".join(fields),
        )
        return sql, fields, values

    @classmethod
    def _get_delete_sql(cls, id: int):
        # DELETE FROM author WHERE id = 1;
        DELETE_SQL_TEMPLATE = "DELETE FROM {name} WHERE id = ?;"
        table_name = cls.__name__.lower()
        params = [id]
        sql = DELETE_SQL_TEMPLATE.format(name=table_name)
        return sql, params

class ForeignKey(Column):
    
    def __init__(self, table: type[Table], column_type=int):
        self.table = table
        super().__init__(column_type)


T = TypeVar("T", bound=Table)
class Database:
    def __init__(self, path):
        self.path = path
        self.connection = sqlite3.Connection(self.path)
    @property
    def tables(self):
        result_set = self.connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        return [rs[0] for rs in result_set]

    def create(self, table: type[T]):
        raw_sql = table._get_create_sql()
        self.connection.execute(raw_sql)

    def save(self, table_instance: T):
        sql, values = table_instance._get_insert_sql()
        cursor = self.connection.execute(sql, values)
        table_instance._data["id"] = cursor.lastrowid
        self.connection.commit()

    def get_all(self, table_type: type[T]) -> list[T]:
        sql, column_names = table_type._get_select_all_sql()
        rows = self.connection.execute(sql).fetchall()
        results = []
        for row in rows:
            # Map to Python type class
            instance = self._to_instance(
                table_type=table_type,
                column_names=column_names,
                row=row,
            )
            results.append(instance)
        return results

    def get_by_id(self, table_type: type[T], id: int) -> T:
        sql, column_names, params = table_type._get_select_by_id_sql(id)
        row = self.connection.execute(sql, params).fetchone()
        if not row:
            raise RecordNotFound(f"Table {table_type.__name__.lower()} with id {id} not found")

        return self._to_instance(
            table_type=table_type,
            column_names=column_names,
            row=row,
        )
    
    def update(self, table_to_update: T) -> None:
        update_sql, column_names, params = table_to_update._get_update_sql()
        self.connection.execute(update_sql, params)
        self.connection.commit()

    def delete(self, table_type: type[T], id: int) -> None:
        delete_sql, params = table_type._get_delete_sql(id)
        self.connection.execute(delete_sql, params)
        self.connection.commit()

    def _to_instance(self, table_type: type[T], column_names: list[str], row: tuple) -> T:
        kwargs = {}
        for column_name, col_value in zip(column_names, row):
            field_name = self._to_field_name(column_name)
            column: Column = table_type._columns[field_name]
            if isinstance(column, ForeignKey):
                fk_instance = self._get_fk_by_id(
                    parent_table_type=table_type,
                    fk_field_name=field_name,
                    fk_id=col_value
                )
                kwargs[field_name] = fk_instance
            else:
                sql_type: SQLType = column.sql_type
                kwargs[field_name] = sql_type.to_python_type(col_value)
        instance = table_type(**kwargs)
        return instance

    def _get_fk_by_id(
        self,
        parent_table_type: type[T],
        fk_field_name: str,
        fk_id: int
    ) -> T:
        fk: ForeignKey = parent_table_type._columns[fk_field_name]
        fk_instance = self.get_by_id(fk.table, id=fk_id)
        return fk_instance

    def _to_field_name(self, column_name: str) -> str:
        if column_name.endswith("_id"):
            return column_name[:-3]
        return column_name