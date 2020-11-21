from Domain.abstract_table import AbstractTable
from utils import make_criteria


class Tags(AbstractTable):
    def __init__(self):
        self.id = ''
        self.key = ''
        self.value = ''

    def insert_into(self, values):
        sql = f"""INSERT INTO Tags (id, key, value) 
                VALUES ('{values[0]}', '{values[1]}', '{values[2]}')"""
        print(sql)
        return self.sql_execute(sql)

    def update(self, table, setter: tuple, *args, **kwargs):
        criteria = make_criteria(**kwargs)
        sql = f"""UPDATE {table} 
                  SET {setter[0]} = {setter[1]} WHERE {criteria}"""
        return self.sql_execute(sql)

    def parse_string(self, tag, tag_id):
        key = tag['k']
        value = tag['v']
        self.insert_into((tag_id, key, value))

    @property
    def table_name(self):
        return 'Tags'
