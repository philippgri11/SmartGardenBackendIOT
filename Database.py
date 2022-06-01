import datetime
import os
import sqlite3 as sql
import time

from model.Rule import Rule

_module_directory = os.path.dirname(os.path.abspath(__file__))
con = sql.connect(os.path.join(_module_directory, 'smartGarden.sqlite'), check_same_thread=False)
c = con.cursor()

def updateRule(rule_id, rule_stuff):
    return True


def addRule(rule_stuff):
    return 1


def deleteRule(rule_id):
    return True


def executeSelect(query, args):
    c.execute(query, args)
    inhalt = (c.fetchall())
    return inhalt

def updateZoneTitel(zoneID, titel):
    con.execute("""
    UPDATE ZONES
    SET NAME=?
    WHERE ZONE_ID=?
    """, (titel, zoneID))
    con.commit()

def updateStatus(zoneID, status):
    con.execute("""
    UPDATE ZONES
    SET STATUS=?
    WHERE ZONE_ID=?
    """, (status, zoneID))
    con.commit()

def getZones():
    inhalt = executeSelect("""
        SELECT *
        FROM Zones""",())
    return inhalt

def getGPIOByRuleID(ruleID):
    inhalt = executeSelect("""
            select GPIO FROM Zones JOIN Rules R on Zones.ZONE_ID = R.ZONE_ID WHERE RULE_ID = ? """, (ruleID, ))
    return inhalt[0][0]

def getRules(zoneId):
    inhalt = executeSelect("""
        SELECT *
        FROM Rules
        WHERE ZONE_ID=?""", (zoneId,))
    return inhalt

def getRuleByRuleId(ruleID):
    inhalt = executeSelect("""
        SELECT *
        FROM Rules
        WHERE RULE_ID=?""", (ruleID,))
    return inhalt

def deleteRuleByRuleId(ruleID):
    con.execute("""
        DELETE
        FROM Rules
        WHERE RULE_ID=?""", (ruleID,))
    con.commit()


def getZoneTitel(zoneId):
    return executeSelect("""
        SELECT NAME
        FROM Zones
        WHERE ZONE_ID=?""", (zoneId,))


def saveRule(vonminutes,vonHours,bisMinutes,bisHours,wochentag,wetter,id):
    con.execute("""
    UPDATE Rules
    SET VONMIN = ?, VONHOUR  = ?, BISMIN  = ?, BISHOUR  = ?, DAYS  = ?, WETTER = ?
    where RULE_ID = ?
    """, (vonminutes,vonHours,bisMinutes,bisHours,wochentag,wetter,id,))
    con.commit()

def getLastRuleID():
    return executeSelect("""SELECT MAX(RULE_ID) FROM RULES""",())[0][0]

def createNewRule(VONMIN, VONHOUR, BISMIN, BISHOUR, DAYS, WETTER, ZONE_ID):
    con.execute("""
    INSERT INTO Rules (VONMIN, VONHOUR, BISMIN, BISHOUR, DAYS, WETTER, ZONE_ID)
    VALUES (?,?,?,?,?,?,?)
    """, (VONMIN, VONHOUR, BISMIN, BISHOUR, DAYS, WETTER, ZONE_ID,))
    con.commit()

if __name__ == '__main__':
    deleteRuleByRuleId(8)
  #  print(getRules(1))