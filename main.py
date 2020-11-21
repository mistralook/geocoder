import xml.parsers.expat as xml_parser
import sqlite3 as sql
from Domain import Nodes, Tags, NodesTags, \
    WaysNodes, WaysTags, Relations, RelationTags

# osm_db = 'NORMAL-DB.osm'
# osm_db = 'way_test.osm'
# osm_db = 'node_test.osm'
# osm_db = 'relation_test.osm'
osm_db = 'mixed_test.osm'
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
        self.relations = Relations()
        self.relation_tags = RelationTags()
        self.parent_element = ()
        self.tag_id = 1

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
            self.parent_element = (string['id'], 'way')

        if name == "nd":
            self.ways_nodes.parse_string(self.parent_element[0],
                                         string['ref'])

        if name == "node":
            if '/' in string:
                self.nodes.parse_string(string)
            elif '/' not in string:
                self.parent_element = (string['id'], 'node')
                self.nodes.parse_string(string)

        if name == "tag":
            self.tags.parse_string(string, self.tag_id)
            if self.parent_element[1] == 'node':
                self.nodes_tags.parse_string(self.parent_element[0],
                                             self.tag_id)
                self.tag_id += 1
            if self.parent_element[1] == 'way':
                self.ways_tags.parse_string(self.parent_element[0],
                                            self.tag_id)
                self.tag_id += 1
            if self.parent_element[1] == 'relation':
                self.relation_tags.parse_string(self.parent_element[0],
                                                self.tag_id)
                self.tag_id += 1

    def parse_db(self, name, attr):
        self.parse_string(attr, name)


def main():
    ps = Parser()
    with sql.connect(sql_db) as con:
        c = con.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS Relations '
            '("id" INTEGER PRIMARY KEY , "id_relation", '
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
            'CREATE TABLE IF NOT EXISTS NodesTags '
            '("id" INTEGER PRIMARY KEY, "id_node", "id_tag");')
        c.execute(
            'CREATE TABLE IF NOT EXISTS Tags '
            '("id" INTEGER PRIMARY KEY, "key", "value");')

    parser = xml_parser.ParserCreate()
    parser.StartElementHandler = ps.parse_db
    with open(osm_db, 'rb') as db:
        parser.ParseFile(db)


if __name__ == '__main__':
    main()
