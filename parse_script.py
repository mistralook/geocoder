import xml.parsers.expat as xml_parser
import sqlite3 as sql
from Domain import Nodes, Tags, WaysNodes, WaysTags, Relations, \
    RelationTags, WayBuildings, AbstractTable


class Parser:
    def __init__(self, sql_db='parser_data.db'):
        self.current_table = ''
        self.current_id = ''
        self.sql_db = sql_db
        self.conn = AbstractTable.create_connect(self.sql_db)
        self.tags = Tags.create_with_connect(self.conn)
        self.nodes = Nodes.create_with_connect(self.conn)
        self.ways_nodes = WaysNodes.create_with_connect(self.conn)
        self.ways_tags = WaysTags.create_with_connect(self.conn)
        self.ways_buildings = WayBuildings.create_with_connect(self.conn)
        self.relations = Relations.create_with_connect(self.conn)
        self.relation_tags = RelationTags.create_with_connect(self.conn)
        self.parent_element = ()
        self.tag_id = 1
        self.last_nodes = []
        self.nodes_dict = dict()
        self.addr_for_way = dict()
        self.building_info = {'building': 'None',
                              'addr:street': 'None',
                              'addr:housenumber': 'None'}
        self.is_building = False
        self.was_housenumber = False

    def parse_string(self, string, name):
        if name == "relation":
            if self.is_building or self.was_housenumber:
                self.ways_buildings.parse_string(self.last_nodes,
                                                 self.nodes_dict,
                                                 self.building_info)
            self.is_building = False
            self.was_housenumber = False
            self.parent_element = (string['id'], 'relation')

        if name == "member":
            self.relations.parse_string(self.parent_element[0],
                                        string['type'],
                                        string['ref'],
                                        string['role'])

        if name == "way":
            if self.is_building or self.was_housenumber:
                self.ways_buildings.parse_string(self.last_nodes,
                                                 self.nodes_dict,
                                                 self.building_info)
            self.building_info = {'building': 'None',
                                  'addr:street': 'None',
                                  'addr:housenumber': 'None'}
            self.is_building = False
            self.was_housenumber = False
            self.last_nodes.clear()
            self.parent_element = (string['id'], 'way')

        if name == "nd":
            self.ways_nodes.parse_string(self.parent_element[0],
                                         string['ref'])
            self.last_nodes.append(string['ref'])

        if name == "node":
            if '/' in string:
                # self.nodes.parse_string(string['id'],
                #                         string['lat'],
                #                         string['lon'])
                self.nodes_dict[string['id']] = (
                    string['lat'], string['lon'])

            elif '/' not in string:
                self.parent_element = (string['id'], 'node')
                # self.nodes.parse_string(string['id'],
                #                         string['lat'],
                #                         string['lon'])
                self.nodes_dict[string['id']] = (
                    string['lat'], string['lon'])

        if name == "tag":
            if self.parent_element[1] != 'node':
                self.tags.parse_string(string, self.tag_id)

            if self.parent_element[1] == 'way':
                if string['k'] == 'building':
                    self.building_info['building'] = string['v']
                    self.is_building = True

                if string['k'] == 'addr:street':
                    self.building_info['addr:street'] = string['v']

                if string['k'] == 'addr:housenumber':
                    self.building_info['addr:housenumber'] = string['v']
                    self.was_housenumber = True

                self.ways_tags.parse_string(self.parent_element[0],
                                            self.tag_id)
                self.tag_id += 1
            if self.parent_element[1] == 'relation':
                self.relation_tags.parse_string(self.parent_element[0],
                                                self.tag_id)
                self.tag_id += 1

    def parse_db(self, name, attr):
        self.parse_string(attr, name)

    def run(self, osm_db):
        with sql.connect(self.sql_db) as con:
            c = con.cursor()
            c.execute(
                'CREATE TABLE IF NOT EXISTS Nodes '
                '("id", "lat", "lon");')
            c.execute(
                'CREATE INDEX in_node_id ON Nodes(id);'
            )
            c.execute(
                'CREATE TABLE IF NOT EXISTS Relations '
                '("id" INTEGER PRIMARY KEY AUTOINCREMENT , "id_relation", '
                '"member_type", "ref", "role");')
            c.execute(
                'CREATE TABLE IF NOT EXISTS RelationTags '
                '("id" INTEGER PRIMARY KEY, "id_relation", "id_tag");')
            c.execute(
                'CREATE TABLE IF NOT EXISTS WayTags '
                '("id" INTEGER PRIMARY KEY, "id_way", "id_tag");')
            c.execute(
                'CREATE TABLE IF NOT EXISTS WayNodes '
                '("id" INTEGER PRIMARY KEY, "id_way", "id_node");')
            c.execute(
                'CREATE TABLE IF NOT EXISTS Tags '
                '("id" INTEGER, "key", "value");')
            c.execute(
                'CREATE TABLE IF NOT EXISTS WayBuildings '
                '("id" INTEGER PRIMARY KEY,'
                ' "building", "street", "housenumber",'
                ' "lat", "lon", "fullness" );')

        parser = xml_parser.ParserCreate()
        parser.StartElementHandler = self.parse_db
        with open(osm_db, 'rb') as db:
            parser.ParseFile(db)
        self.nodes.execute_from_list()
        self.ways_buildings.execute_from_list()
        self.ways_nodes.execute_from_list()
        self.ways_tags.execute_from_list()
        self.relations.execute_from_list()
        self.relation_tags.execute_from_list()
        self.tags.execute_from_list()
        self.conn.commit()
        self.conn.close()


def main():
    osm_db = 'london.osm'
    sql_db = 'parsed_data.db'
    ps = Parser(sql_db)
    ps.run(osm_db)


if __name__ == '__main__':
    main()
