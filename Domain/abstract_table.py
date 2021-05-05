import sqlite3
from abc import ABC, abstractmethod


class AbstractTable(ABC):
    def __init__(self, connect):
        self.connect = connect

    @classmethod
    def create_with_connect(cls, connect):
        return cls(connect)

    @staticmethod
    def create_connect(sql_db):
        conn = sqlite3.connect(sql_db)
        return conn

    @abstractmethod
    def insert_into(self, *args, **kwargs):
        pass

    @abstractmethod
    def parse_string(self, *args):
        pass

    @property
    @abstractmethod
    def table_name(self):
        pass

    def sql_execute(self, sql_request, values):
        c = self.connect.cursor()
        c.executemany(sql_request, values)
        result = c.fetchall()
        return result
