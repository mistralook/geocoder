from Domain.abstract_table import AbstractTable
from utils import make_criteria


class RelationTags(AbstractTable):
    def __init__(self):
        self.id = ''
        self.id_relation = ''
        self.id_tag = ''
        self.list = list()
        self.index = 0

    def insert_into(self, values):
        # sql = f"INSERT INTO RelationTags (id_relation, id_tag)" \
        #       f" VALUES ('{values[0]}', '{values[1]}')"
        # return self.sql_execute(sql)
        self.list.append(values)
        if len(self.list) % 10 == 0:
            s = f"INSERT INTO RelationTags(id_relation, id_tag)" \
                f" VALUES (?, ?)"
            self.sql_execute(s, self.list[self.index:])
            self.index += 10

    def update(self, table, setter: tuple, *args, **kwargs):
        criteria = make_criteria(**kwargs)
        sql = f"UPDATE {table}" \
              f" SET {setter[0]} = {setter[1]}" \
              f" WHERE {criteria}"
        return self.sql_execute(sql)

    def parse_string(self, relation_id, tag_id):
        self.insert_into((relation_id, tag_id))

    @property
    def table_name(self):
        return 'RelationTags'
