from Domain.abstract_table import AbstractTable
from utils import make_criteria


class WaysTags(AbstractTable):
    def __init__(self):
        self.id = ''
        self.id_way = ''
        self.id_tag = ''
        self.list = list()
        self.index = 0

    def insert_into(self, values):
        #sql = f"INSERT INTO WayTags (id_way, id_tag)" \
        #      f" VALUES ('{values[0]}', '{values[1]}')"
        #return self.sql_execute(sql)

        self.list.append(values)
        if len(self.list) % 10000 == 0:
            s = f"INSERT INTO WayTags(id_way, id_tag) VALUES (?, ?)"
            self.sql_execute(s, self.list[self.index:])
            self.index += 10000

    def update(self, table, setter: tuple, *args, **kwargs):
        criteria = make_criteria(**kwargs)
        sql = f"UPDATE {table}" \
              f" SET {setter[0]} = {setter[1]}" \
              f" WHERE {criteria}"
        return self.sql_execute(sql)

    def parse_string(self, way_id, tag_id):
        self.insert_into((way_id, tag_id))

    @property
    def table_name(self):
        return 'WayTags'
