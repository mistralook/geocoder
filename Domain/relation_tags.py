from Domain.abstract_table import AbstractTable


class RelationTags(AbstractTable):
    def __init__(self, cursor=None):
        super().__init__(cursor)
        self.list = list()

    def insert_into(self, values):
        self.list.append(values)

    def execute_from_list(self):
        s = f"INSERT INTO" \
            f" RelationTags(id_relation, id_tag)" \
            f" VALUES (?, ?)"
        self.sql_execute(s, self.list)
        self.list.clear()

    def parse_string(self, relation_id, tag_id):
        self.insert_into((relation_id, tag_id))
        if len(self.list) % 10000 == 0:
            self.execute_from_list()

    @property
    def table_name(self):
        return 'RelationTags'
