from Domain.abstract_table import AbstractTable
from utils import make_criteria


class Tags(AbstractTable):
    def __init__(self):
        self.id = ''
        self.key = ''
        self.value = ''
        self.list = list()
        self.index = 0

    def insert_into(self, values):
        # sql = f"INSERT INTO Tags (id, key, value)" \
        #       f" VALUES ('{values[0]}', '{values[1]}', '{values[2]}')"
        # return self.sql_execute(sql)
        self.list.append(values)
        if len(self.list) % 10000 == 0:
            s = f"INSERT INTO Tags(id, key, value) VALUES (?, ?, ?)"
            self.sql_execute(s, self.list[self.index:])
            self.index += 10000

    def update(self, table, setter: tuple, *args, **kwargs):
        criteria = make_criteria(**kwargs)
        sql = f"UPDATE {table}" \
              f" SET {setter[0]} = {setter[1]}" \
              f" WHERE {criteria}"
        return self.sql_execute(sql)

    def parse_string(self, tag, tag_id):
        key = tag['k']
        value = tag['v']
        self.insert_into((tag_id, key, value))

    @property
    def table_name(self):
        return 'Tags'
