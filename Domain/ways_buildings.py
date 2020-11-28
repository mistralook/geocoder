import sqlite3 as sqlite

from Domain.abstract_table import AbstractTable
from utils import make_criteria
sql_db = 'parsed_data.db'


class WayBuildings(AbstractTable):
    def __init__(self):
        self.id = ''
        self.id_node = ''
        self.id_tag = ''

    def insert_into(self, values):
        sql = f"""INSERT INTO WayBuildings (id_way, coordinates) 
                  VALUES ('{values[0]}', '{values[1]}')"""
        return self.sql_execute(sql)

    def update(self, table, setter: tuple, *args, **kwargs):
        criteria = make_criteria(**kwargs)
        sql = f"""UPDATE {table} 
                  SET {setter[0]} = {setter[1]} WHERE {criteria}"""
        return self.sql_execute(sql)

    def parse_string(self, way_id, last_nodes):
        coords = self.get_coords(last_nodes)
        self.insert_into((way_id, coords))

    @staticmethod
    def get_coords(nodes):
        centroid = [0, 0]
        signed_area = 0
        with sqlite.connect(sql_db) as con:
            c = con.cursor()
            result = []
            for node in nodes[:-1]:
                s = f'SELECT lat, lon FROM Nodes WHERE id={int(node)}'
                c.execute(s)
                result.append(*c.fetchall())
            c.close()
        for i in range(len(result)):
            cur_lat, cur_lon = result[i]
            next_lat, next_lon = result[(i+1) % len(result)]
            a = cur_lat*next_lon - next_lat*cur_lon
            signed_area += a
            centroid[0] += (cur_lat + next_lat)*a
            centroid[1] += (cur_lon + next_lon)*a
        signed_area /= 2
        centroid[0] /= (6 * signed_area)
        centroid[1] /= (6 * signed_area)
        return centroid

    @property
    def table_name(self):
        return 'WayBuildings'

