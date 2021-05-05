from Domain.abstract_table import AbstractTable


class Tags(AbstractTable):
    def __init__(self, cursor=None):
        super().__init__(cursor)
        self.list = list()

    def insert_into(self, values):
        self.list.append(values)

    def execute_from_list(self):
        s = f"INSERT INTO" \
            f" Tags(id, key, value)" \
            f" VALUES (?, ?, ?)"
        self.sql_execute(s, self.list)
        self.list.clear()

    def parse_string(self, tag, tag_id):
        key = tag['k']
        value = tag['v']
        self.insert_into((tag_id, key, value))
        if len(self.list) % 10000 == 0:
            self.execute_from_list()

    @property
    def table_name(self):
        return 'Tags'
