"""
Module defines repository that works with sqlite3 DBMS
"""

import dataclasses
from itertools import count
from typing import Any
from typing import Type
from typing import Optional
import sqlite3

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SqliteRepository(AbstractRepository[T]):
    """
    Repository working with sqlite3 DBMS. Stores connection
    object.
    """

    @staticmethod
    def get_fields_as_string(type_name: Type[T]) -> str:
        """
        Returns class fields in form:
        field1,field2,field3...,fieldN
        (Used for SQL queries)
        """
        return ','.join(list(type_name.__annotations__))

    # Since it's impossible to get actual type of generic
    # from within instance 'class_used' argument is used
    # to get fields of corresponding dataclass
    def __init__(self, class_used: Type[T], db_name: str | None = None) -> None:
        self._table_name = class_used.__name__
        self._class_used = class_used
        if db_name is not None:
            self._db_name = db_name + '.db'
        else:
            self._db_name = class_used.__name__ + '.db'
        print(self._db_name)
        # since connect doesn't raise exception
        # no need to use try-except
        # self._conn: Optional[sqlite3.Connection] = sqlite3.connect(self._db_name)
        self._conn: Optional[sqlite3.Connection] = None

        cmd = f'create table if not exists {self._table_name}' \
              f'({SqliteRepository.get_fields_as_string(class_used)})'
        print(cmd)

        # get fields to create table
        cur = None
        try:
            self._conn = sqlite3.connect(self._db_name)
            cur = self._conn.cursor()
            cur.execute(cmd)

            # get maximum primary key value from table
            max_pk = cur.execute(f'select max(pk) from {self._table_name}').fetchone()
            print(max_pk)
            if max_pk[0] is None:
                self._counter = count(1)
            else:
                self._counter = count(max_pk[0] + 1)
        finally:
            if cur is not None:
                cur.close()
            if self._conn is not None:
                self._conn.close()
                self._conn = None

    def __del__(self) -> None:
        if self._conn is not None:
            self._conn.close()

    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        pk = next(self._counter)

        assert self._conn is not None

        cur = self._conn.cursor()
        q_marks = ','.join(['?']*len(self._class_used.__annotations__))
        print(q_marks)
        cmd = f'insert into {self._table_name} values({q_marks})'
        print(cmd)
        old_pk = obj.pk
        try:
            obj.pk = pk
            cur.execute(cmd, dataclasses.astuple(obj))
            self._conn.commit()
        except sqlite3.DatabaseError:
            obj.pk = old_pk
            raise
        finally:
            cur.close()

        # obj.pk = pk
        return pk

    def get(self, pk: int) -> T | None:
        assert self._conn is not None

        cur = self._conn.cursor()
        cmd = f'select * from {self._table_name} where pk={pk}'
        print(cmd)
        try:
            res = cur.execute(cmd).fetchone()
        finally:
            cur.close()

        if res is None:
            return None
        return self._class_used(*res)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        assert self._conn is not None

        cur = self._conn.cursor()
        try:
            return [self._class_used(*i) for i in cur.execute(
                f'select * from {self._table_name}').fetchall()]
        finally:
            cur.close()

    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')

        # col_set = ','.join([attr+'='+str(getattr(obj, attr)) for attr in
        # obj.__annotations__])
        col_set = repr(obj).split('(')[1].split(')')[0]
        # print(col_set)
        cmd = f'update {self._table_name} set {col_set} where pk={obj.pk}'
        # print(cmd)

        assert self._conn is not None

        cur = self._conn.cursor()
        try:
            cur.execute(cmd)
            self._conn.commit()
        finally:
            cur.close()

    def delete(self, pk: int) -> None:
        assert self._conn is not None

        cur = self._conn.cursor()
        cmd = f'delete from {self._table_name} where pk={pk}'
        # print(cmd)
        try:
            cur.execute(cmd)
            self._conn.commit()
        finally:
            cur.close()
