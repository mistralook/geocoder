from Domain.abstract_table import AbstractTable
from utils import make_criteria


class Relations(AbstractTable):
    def __init__(self):
        self.id = ''
        self.member_type = ''
        self.ref_way = ''
        self.ref_nod = ''
        self.role = ''

    def insert_into(self, values):
        sql = f"""INSERT INTO Relations (id, member_type, ref, role) 
                  VALUES ('{values[0]}', '{values[1]}', '{values[2]}', '{values[3]}')"""
        print(sql)
        return self.sql_execute(sql)

    def update(self, table, setter: tuple, *args, **kwargs):
        criteria = make_criteria(**kwargs)
        sql = f"""UPDATE {table} 
                  SET {setter[0]} = {setter[1]} WHERE {criteria}"""
        return self.sql_execute(sql)

    def parse_string(self, relation_id, member_type, ref, role):
        self.insert_into((relation_id, member_type, ref, role))

    @property
    def table_name(self):
        return 'Relations'
