import xml.parsers.expat as xml_parser
import sqlite3 as sql
from Domain import Nodes, Tags, NodesTags, \
    WaysNodes, WaysTags, Relations, RelationTags, WayBuildings

# osm_db = 'NORMAL-DB.osm'
# osm_db = 'way_base.osm'
# osm_db = 'node_base.osm'
# osm_db = 'relation_base.osm'
# osm_db = 'way_building_base.osm'
# osm_db = 'mixed_base.osm'
osm_db = 'london.osm'
# osm_db = 'test.osm'
sql_db = 'parsed_data.db'


class Parser:
    def __init__(self):
        self.current_table = ''
        self.current_id = ''
        self.nodes = Nodes()
        self.tags = Tags()
        self.nodes_tags = NodesTags()
        self.ways_nodes = WaysNodes()
        self.ways_tags = WaysTags()
        self.ways_buildings = WayBuildings()
        self.relations = Relations()
        self.relation_tags = RelationTags()
        self.parent_element = ()
        self.tag_id = 1
        self.last_nodes = []
        self.temp = []
        self.nodes_dict = dict()

    def parse_string(self, string, name):
        if name == "relation":
            self.parent_element = (string['id'], 'relation')

        if name == "member":
            if string['role'] != '':
                self.relations.parse_string(self.parent_element[0],
                                            string['type'],
                                            string['ref'],
                                            string['role'])
            else:
                self.relations.parse_string(self.parent_element[0],
                                            string['type'],
                                            string['ref'],
                                            '')

        if name == "way":
            self.temp = []
            self.parent_element = (string['id'], 'way')

        if name == "nd":
            self.ways_nodes.parse_string(self.parent_element[0],
                                         string['ref'])
            self.temp.append(string['ref'])
            self.last_nodes = self.temp

        if name == "node":
            if '/' in string:
                # self.nodes.parse_string(string)
                self.nodes_dict[string['id']] = (string['lat'], string['lon'])
            elif '/' not in string:
                self.parent_element = (string['id'], 'node')
                # self.nodes.parse_string(string)
                self.nodes_dict[string['id']] = (string['lat'], string['lon'])
        if name == "tag":
            if self.parent_element[1] == 'node':
                pass
            else:
                self.tags.parse_string(string, self.tag_id)
            if self.parent_element[1] == 'way':
                if string['k'] == 'building':
                    self.ways_buildings.parse_string(
                        self.parent_element[0],
                        self.last_nodes, self.nodes_dict)
                self.ways_tags.parse_string(self.parent_element[0],
                                            self.tag_id)
                self.tag_id += 1
            if self.parent_element[1] == 'relation':
                self.relation_tags.parse_string(self.parent_element[0],
                                                self.tag_id)
                self.tag_id += 1

    def parse_db(self, name, attr):
        self.parse_string(attr, name)

    def run(self):
        with sql.connect(sql_db) as con:
            c = con.cursor()
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
                'CREATE TABLE IF NOT EXISTS Nodes '
                '("id" PRIMARY KEY, "lat", "lon");')
            c.execute(
                'CREATE INDEX in_node_id ON Nodes(id);'
            )
            c.execute(
                'CREATE TABLE IF NOT EXISTS Tags '
                '("id" INTEGER, "key", "value");')
            c.execute(
                'CREATE TABLE IF NOT EXISTS WayBuildings '
                '("id" INTEGER PRIMARY KEY, "id_way", "lat", "lon");')

        parser = xml_parser.ParserCreate()
        parser.StartElementHandler = self.parse_db
        with open(osm_db, 'rb') as db:
            parser.ParseFile(db)
        self.ways_buildings.execute_from_list()
        self.relations.execute_from_list()


def main():
    ps = Parser()
    ps.run()


if __name__ == '__main__':
    main()
