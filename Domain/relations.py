from Domain.abstract_table import AbstractTable


class Relations(AbstractTable):
    def __init__(self):
        self.id = ''
        self.member_type = ''
        self.ref_way = ''
        self.ref_nod = ''
        self.role = ''

    def insert_into(self):
        pass

    def select(self):
        pass

    def update(self):
        pass

    def parse_string(self):
        pass
