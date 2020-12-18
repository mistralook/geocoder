from Domain.abstract_table import AbstractTable
from utils import make_criteria


class Nodes(AbstractTable):
    def __init__(self):
        self.id = ''
        self.lat = ''
        self.lon = ''
        self.list = list()
        self.index = 0

    def insert_into(self, values):
        self.list.append(values)
        if len(self.list) % 100000 == 0:
            s = f"INSERT INTO Nodes VALUES (?, ?, ?)"
            self.sql_execute(s, self.list[self.index:])
            self.index += 100000

    def update(self, table, setter: tuple, *args, **kwargs):
        criteria = make_criteria(**kwargs)
        sql = f"UPDATE {table}" \
              f" SET {setter[0]} = {setter[1]}" \
              f" WHERE {criteria}"
        return self.sql_execute(sql)

    def parse_string(self, node):
        id = node['id']
        lat = node['lat']
        lon = node['lon']
        self.insert_into((id, lat, lon))

    @property
    def table_name(self):
        return 'Nodes'
