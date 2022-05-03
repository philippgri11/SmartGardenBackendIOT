import sqlite3 as sql

con = sql.connect('database.db')

def updateRule(rule_id, rule_stuff):
    return True

def addRule(rule_stuff):
    return 1

def deleteRule(rule_id):
    return True

def createTables():
    with con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS Zones(
                ZONE_ID int NOT NULL PRIMARY KEY,
                NAME VARCHAR(256)
            );
            CREATE TABLE IF NOT EXISTS Rules(
                RULE_ID int NOT NULL PRIMARY KEY,
                VON INTEGER NOT NULL,
                BIS INTEGER NOT NULL,
                DAYS VARCHAR(7) NOT NULL,
                WETTER INT,
                ZONE_ID INT NOT NULL,
                FOREIGN KEY(ZONE_ID) REFERENCES ZONE(ZONE_ID)
            );
        """)

if __name__ == '__main__':
    pass