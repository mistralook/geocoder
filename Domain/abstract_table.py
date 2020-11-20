import sqlite3

from abc import ABC, abstractmethod
from main import sql_db


class AbstractTable(ABC):
    @abstractmethod
    def insert_into(self, *args, **kwargs):
        pass

    def select(self, *args, **kwargs):
        sql = f"""SELECT {' '.join(args)} FROM {self.table_name} 
        WHERE {' AND '.join('{}={}'.format(k, v) for k, v in kwargs)}"""
        return self.sql_execute(sql)

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def parse_string(self):
        pass

    @property
    @abstractmethod
    def table_name(self):
        pass

    @staticmethod
    def sql_execute(sql_request):
        with sqlite3.connect(sql_db) as conn:
            c = conn.cursor()
            c.execute(sql_request)
            result = c.fetchall()
            c.close()
        return result
