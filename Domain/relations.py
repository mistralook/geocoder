from Domain.abstract_table import AbstractTable


class Relations(AbstractTable):
    def __init__(self, cursor=None):
        super().__init__(cursor)
        self.list = list()

    def insert_into(self, values):
        self.list.append(values)

    def execute_from_list(self):
        s = f"INSERT INTO" \
            f" Relations(id_relation, member_type, ref, role)" \
            f" VALUES (?, ?, ?, ?)"
        self.sql_execute(s, self.list)
        self.list.clear()

    def parse_string(self, relation_id, member_type, ref, role):
        self.insert_into((relation_id, member_type, ref, role))
        if len(self.list) % 10000 == 0:
            self.execute_from_list()

    @property
    def table_name(self):
        return 'Relations'
