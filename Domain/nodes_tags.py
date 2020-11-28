from Domain.abstract_table import AbstractTable
from utils import make_criteria


class NodesTags(AbstractTable):
    def __init__(self):
        self.id = ''
        self.id_node = ''
        self.id_tag = ''

    def insert_into(self, values):
        sql = f"""INSERT INTO NodesTags (id_node, id_tag) 
                  VALUES ('{values[0]}', '{values[1]}')"""
        # print(sql)
        return self.sql_execute(sql)

    def update(self, table, setter: tuple, *args, **kwargs):
        criteria = make_criteria(**kwargs)
        sql = f"""UPDATE {table} 
                  SET {setter[0]} = {setter[1]} WHERE {criteria}"""
        return self.sql_execute(sql)

    def parse_string(self, node_id, tag_id):
        self.insert_into((node_id, tag_id))

    @property
    def table_name(self):
        return 'NodesTags'

