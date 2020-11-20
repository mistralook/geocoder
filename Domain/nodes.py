from Domain.abstract_table import AbstractTable


class Nodes(AbstractTable):
    def __init__(self):
        self.id = ''
        self.lat = ''
        self.lon = ''

    def insert_into(self, column, values):
        sql = f"INSERT INTO {column} VALUES(?, ?)", values
        return self.sql_execute(sql)

    def update(self, table, ):
        pass

    def parse_string(self):
        pass

    @property
    def table_name(self):
        return 'Nodes'
