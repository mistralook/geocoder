from Domain.abstract_table import AbstractTable
from utils import make_criteria


class Relations(AbstractTable):
    def __init__(self):
        self.id = ''
        self.member_type = ''
        self.ref_way = ''
        self.ref_nod = ''
        self.role = ''
        self.list = list()

    def insert_into(self, values):
        self.list.append(values)

    def execute_from_list(self):
        s = f"INSERT INTO" \
            f" Relations(id_relation, member_type, ref, role)" \
            f" VALUES (?, ?, ?, ?)"
        self.sql_execute(s, self.list)
        self.list.clear()

    def update(self, table, setter: tuple, *args, **kwargs):
        criteria = make_criteria(**kwargs)
        sql = f"UPDATE {table}" \
              f" SET {setter[0]} = {setter[1]}" \
              f" WHERE {criteria}"
        return self.sql_execute(sql)

    def parse_string(self, relation_id, member_type, ref, role):
        self.insert_into((relation_id, member_type, ref, role))
        if len(self.list) % 1000 == 0:
            self.execute_from_list()

    @property
    def table_name(self):
        return 'Relations'
