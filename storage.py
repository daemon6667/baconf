#!/usr/bin/env python

# -*- codepage: utf-8 -*-

import sqlite3

db_tables = {
    "sessions": """
    create table sessions (session varchar(30) unique)
    """,
    "resources": """
    create table resources (
        id integer primary key autoincrement,
        namespace varchar(30) default "default",
        name varchar(30) default "",
        restype varchar(30),
        data text default "",
        enabled integer default 1,
        note text
    );
    """
}
db_indexes = [
    "create unique index if not exists resource_name on resources (namespace, restype, name);",
]

class Storage:
    m_db = ""
    m_connection = None
    def __init__(self, basename):
        self.m_db = basename
        self.connect()

    def connect(self):
        if not self.m_connection:
            self.m_connection = sqlite3.connect(self.m_db)
        return self.m_connection
    
    def initDb(self):
        cur = self.m_connection.cursor()
        for table in db_tables:
            print(db_tables[table])
            cur.execute(db_tables[table])
        for index in db_indexes:
            print(index)
            cur.execute(index);
        self.m_connection.commit()
    
    def insertSessionId(self, sess_id):
        cur = self.m_connection.cursor()
        try:
            cur.execute("insert into sessions values (?)", (sess_id, ))
        except sqlite3.IntegrityError:
            pass
        self.m_connection.commit()

    def saveResource(self, namespace, name, restype, data, enabled=True, note=""):
        cur = self.m_connection.cursor()
        cur.execute("insert into resources(namespace, name, restype, data, enabled, note) values (?,?,?,?,?,?)", (namespace, name, restype, data, enabled, note))
        self.m_connection.commit()

    def namespaces(self):
        result = []
        cur = self.m_connection.cursor()
        cur.execute("select namespace from resources group by namespace")
        result = [ x[0] for x in cur ]
        return result

    def listResources(self, namespace=None):
        cur = self.m_connection.cursor()
        cur.execute("select namespace, restype, name, enabled from resources order by namespace");
        result = []
        i = 0
        for namespace, restype, name, enabled in cur.fetchall():
            i += 1
            result.append({'recid': i, 'namespace': namespace, 'restype': restype, 'name': name, 'enabled': True if enabled else False})
        return result
    
if __name__ == "__main__":
    s = Storage('super.db')
#    s.saveResource("production", "localdevice", "Device", "some data", True, "Just a test")
#    s.saveResource("development", "freebsdclient", "Client", "some data", False, "just a test")
#    s.saveResource("development", "BackupJob", "Job", "some data", True, "just a test")
    s.namespaces()
    s.listResources()

