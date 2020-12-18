import sqlite3 as sqlite

from Domain.abstract_table import AbstractTable
from utils import make_criteria
sql_db = 'parsed_data.db'


class WayBuildings(AbstractTable):
    def __init__(self):
        self.id = ''
        self.id_node = ''
        self.id_tag = ''
        self.list = list()
        self.node_list = list()

    def insert_into(self, values):
        self.list.append(values)

    def execute_from_list(self):
        s = f"INSERT INTO" \
            f" WayBuildings(id_way, lat, lon)" \
            f" VALUES (?, ?, ?)"
        self.sql_execute(s, self.list)
        self.list.clear()

    def update(self, table, setter: tuple, *args, **kwargs):
        criteria = make_criteria(**kwargs)
        sql = f"UPDATE {table}" \
              f" SET {setter[0]} = {setter[1]}" \
              f" WHERE {criteria}"
        return self.sql_execute(sql)

    def parse_string(self, way_id, last_nodes, nodes_dict):
        coords = list()
        for node in last_nodes:
            coords.append(nodes_dict[node])
        a = self.get_coords(coords)
        self.insert_into((way_id, *a))
        if len(self.list) % 1000 == 0:
            self.execute_from_list()

    @staticmethod
    def get_coords(coords_list):
        node_count = 0
        coords = [0, 0]
        for coord in coords_list[:-1]:
            node_count += 1
            coords[0] += float(coord[0])
            coords[1] += float(coord[1])
        coords[0] /= node_count
        coords[1] /= node_count
        return coords

    @property
    def table_name(self):
        return 'WayBuildings'
