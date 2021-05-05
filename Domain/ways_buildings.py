from Domain.abstract_table import AbstractTable


class WayBuildings(AbstractTable):
    def __init__(self, cursor=None):
        super().__init__(cursor)
        self.list = list()

    def insert_into(self, values):
        self.list.append(values)

    def execute_from_list(self):
        s = f"INSERT INTO" \
            f" WayBuildings(building, street, housenumber," \
            f" lat, lon, fullness)" \
            f" VALUES (?, ?, ?, ?, ?, ?)"
        self.sql_execute(s, self.list)
        self.list.clear()

    def parse_string(self, last_nodes, nodes_dict, building_info):
        fullness = False
        if building_info['addr:street'] and \
                building_info['addr:housenumber'] != 'None':
            fullness = True
        information = list(building_info.values())
        coords = list()
        for node in last_nodes:
            coords.append(nodes_dict[node])
        lat_lon = self.get_coords(coords)
        self.insert_into((*information, *lat_lon, fullness))
        if len(self.list) % 10000 == 0:
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

    # def parse_string(self, last_nodes, building_info):
    #     fullness = False
    #     if building_info['addr:street'] and \
    #             building_info['addr:housenumber'] != 'None':
    #         fullness = True
    #     information = list(building_info.values())
    #     lat_lon = self.get_coords(last_nodes)
    #     self.insert_into((*information, *lat_lon, fullness))
    #     if len(self.list) % 10000 == 0:
    #         self.execute_from_list()
    #
    # def get_coords(self, last_nodes):
    #     coords_list = list()
    #     for node in last_nodes:
    #         s = f"SELECT lat, lon FROM Nodes WHERE id=(?)"
    #         self.sql_execute(s, node)
    #     node_count = 0
    #     coords = [0, 0]
    #     for coord in coords_list[:-1]:
    #         node_count += 1
    #         coords[0] += float(coord[0])
    #         coords[1] += float(coord[1])
    #     coords[0] /= node_count
    #     coords[1] /= node_count
    #     return coords

    @property
    def table_name(self):
        return 'WayBuildings'
