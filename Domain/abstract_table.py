import sqlite3
from Domain import context_manager
from abc import ABC, abstractmethod
sql_db = 'parsed_data.db'


class AbstractTable(ABC):
    @abstractmethod
    def insert_into(self, *args, **kwargs):
        pass

    def select(self, *args, **kwargs):
        sql = f"SELECT {' '.join(args)}" \
              f" FROM {self.table_name}" \
              f" WHERE" \
              f" {' AND '.join('{}={}'.format(k, v) for k, v in kwargs)}"
        return self.sql_execute(sql)

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def parse_string(self, *args):
        pass

    @property
    @abstractmethod
    def table_name(self):
        pass

    # @staticmethod
    # def sql_execute(sql_request):
    #     with sqlite3.connect(sql_db) as conn:
    #         c = conn.cursor()
    #         c.execute(sql_request)
    #         result = c.fetchall()
    #         c.close()
    #     return result

    @staticmethod
    def sql_execute(sql_request, values):
        with context_manager.dbopen(sql_db) as c:
            # print(sql_request, values)
            c.executemany(sql_request, values)
            result = c.fetchall()
        return result
