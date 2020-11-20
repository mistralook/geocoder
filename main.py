import xml.parsers.expat as xml_parser
import sqlite3 as sql
import json

# osm_db = 'NORMAL-DB.osm'
osm_db = 'prikol.osm'
sql_db = 'parsed_data.db'


class Parser:
    def __init__(self):
        self.current_table = ''
        self.current_id = ''

    def parse_node(self, attr):
        id = attr['id']
        lat = attr['lat']
        lon = attr['lon']
        self.current_id = id
        self.current_table = 'nodes'
        tags = dict()
        with sql.connect(sql_db) as conn:
            c = conn.cursor()
            tags = json.dumps(tags)
            values = (id, tags, lat, lon)
            c.execute(f'INSERT INTO nodes VALUES (?,?,?,?)', values)

    def parse_way(self, attr):
        id = attr['id']
        print(id, 'iD ')
        tags = dict()
        nodes = list()
        self.current_id = id
        self.current_table = 'ways'
        with sql.connect(sql_db) as conn:
            c = conn.cursor()
            tags = json.dumps(tags)
            nodes = json.dumps(nodes)
            values = (id, tags, nodes)
            c.execute(f'INSERT INTO ways VALUES (?,?,?)', values)

    def parse_relation(self, attr):
        pass

    def parse_tag(self, attr):
        with sql.connect(sql_db) as connection:
            c = connection.cursor()
            k = attr['k']
            v = attr['v']
            c.execute(
                f'''SELECT tags FROM {self.current_table} WHERE id=?''',
                (self.current_id,))
            tags = json.loads(*c.fetchone())
            tags[k] = v
            tags = json.dumps(tags)
            c.execute(
                f"""UPDATE {self.current_table} 
                    SET tags='{tags}' WHERE id='{self.current_id}'""")
            c.fetchall()
            c.close()

    def parse_nd(self, attr):
        with sql.connect(sql_db) as conn:
            c = conn.cursor()
            ref = attr['ref']
            print(ref)
            c.execute(
                f'''SELECT nodes FROM {self.current_table} WHERE id=?''',
                (self.current_id,))
            print(*c.fetchone())
            nodes = json.loads(*c.fetchone())
            nodes.append(ref)
            nodes = json.dumps(nodes)
            c.execute(f"""UPDATE {self.current_table} 
                        SET nodes='{nodes}' WHERE id='{self.current_id}'""")
            c.fetchall()
            c.close()

    def parse_db(self, name, attr):
        # if name == 'relation':
        #     ps.parse_relation(attr)
        if name == 'way':
            self.parse_way(attr)
        if name == 'nd':
            self.parse_nd(attr)
        # if name == 'node':
        #     self.parse_node(attr)
        if name == 'tag':
            self.parse_tag(attr)


def main():
    ps = Parser()
    with sql.connect(sql_db) as con:
        c = con.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS Relations '
            '("id" PRIMARY KEY, "member_type", "ref_way", '
            '"ref_node", "role");')
        c.execute(
            'CREATE TABLE IF NOT EXISTS RelationTags '
            '("id" PRIMARY KEY, "id_relation", "id_tag");')
        c.execute(
            'CREATE TABLE IF NOT EXISTS WayTags '
            '("id" PRIMARY KEY, "id_way", "id_tag");')
        c.execute(
            'CREATE TABLE IF NOT EXISTS WayNodes '
            '("id" PRIMARY KEY, "id_way", "id_node");')
        c.execute(
            'CREATE TABLE IF NOT EXISTS Nodes '
            '("id" PRIMARY KEY, "lat", "lon");')
        c.execute(
            'CREATE TABLE IF NOT EXISTS NodesTags '
            '("id" PRIMARY KEY, "id_node", "id_tag");')
        c.execute(
            'CREATE TABLE IF NOT EXISTS Tags '
            '("id" PRIMARY KEY, "key", "value");')

    parser = xml_parser.ParserCreate()
    parser.StartElementHandler = ps.parse_db
    with open(osm_db, 'rb') as db:
        parser.ParseFile(db)


if __name__ == '__main__':
    main()
