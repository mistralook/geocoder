from Domain.abstract_table import AbstractTable
from utils import make_criteria


class Nodes(AbstractTable):
    def __init__(self):
        self.id = ''
        self.lat = ''
        self.lon = ''

    def insert_into(self, values):
        sql = f"INSERT INTO Nodes VALUES ({', '.join(values)})"
        print(sql)
        return self.sql_execute(sql)

    def update(self, table, setter: tuple, *args, **kwargs):
        criteria = make_criteria(**kwargs)
        sql = f"""UPDATE {table} 
                  SET {setter[0]} = {setter[1]} WHERE {criteria}"""
        return self.sql_execute(sql)

    def parse_string(self, node):
        id = node['id']
        lat = node['lat']
        lon = node['lon']
        print(id, lat, lon)
        self.insert_into((id, lat, lon))

    @property
    def table_name(self):
        return 'Nodes'
