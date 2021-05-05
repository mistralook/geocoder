from Domain.abstract_table import AbstractTable


class Nodes(AbstractTable):
    def __init__(self, cursor=None):
        super().__init__(cursor)
        self.list = list()

    def insert_into(self, values):
        self.list.append(values)

    def execute_from_list(self):
        s = f"INSERT INTO" \
            f" Nodes(id, lat, lon)" \
            f" VALUES (?, ?, ?)"
        self.sql_execute(s, self.list)
        self.list.clear()

    def parse_string(self, node_id, lat, lon):
        self.insert_into((node_id, lat, lon))
        if len(self.list) % 10000 == 0:
            self.execute_from_list()

    @property
    def table_name(self):
        return 'Nodes'
