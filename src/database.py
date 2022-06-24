import json
import os
import sqlite3 as sql
import threading

from src.Rule import Rule

with open("src/environment.json") as f:
    d = json.load(f)
    databaseName = d["databaseName"]

# _module_directory = os.path.dirname(os.path.abspath(__file__)).removesuffix('/src')
# path= os.path.join(_module_directory, databaseName)
path = "/project/smartGarden.sqlite"
con = sql.connect(path, check_same_thread=False)
c = con.cursor()
lock = threading.Lock()

def getPath():
    return path

def executeSelect(query, args):
    try:
        lock.acquire(True)
        c.execute(query, args)
        inhalt = (c.fetchall())
    finally:
        lock.release()
    return inhalt



def updateStatus(status):
    try:
        lock.acquire(True)
        con.execute("""
        UPDATE RUHEMODUS
        SET STATUS=?
        """, (status,))
        con.commit()
    finally:
        lock.release()

def getStatusRuhemodus():
    inhalt = executeSelect("""
        SELECT status
        FROM RUHEMODUS
        """, ())
    return inhalt[0][0]
