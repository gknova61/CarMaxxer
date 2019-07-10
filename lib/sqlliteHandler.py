#!/usr/bin/env python3

"""sqlliteHandler.py: General lib for handling interaction with SQLLite 3 database"""

__author__      = "Keanu Kauhi-Correia"
__version__ = "1.0"
__maintainer__ = "Keanu Kauhi-Correia"
__email__ = "keanu.kkc@gmail.com "

import sqlite3
from sqlite3 import Error

conn = None
lastException = None

def createConnection(db_file):
    global conn
    """
    Source: http://www.sqlitetutorial.net/sqlite-python/creating-database/
    """
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        lastException = e
        return False

    return True


if __name__ == '__main__':
    createConnection("C:\\sqlite\db\pythonsqlite.db")

def createTable(tableName, rec, pkList):
    global conn
    global lastException

    try:
        primaryKeys = ','.join(pkList)
        tableKeys = ','.join(rec.keys())
        conn.execute('CREATE TABLE ' + tableName + '(' + tableKeys + ', PRIMARY KEY ('+ primaryKeys +'))')
    except Exception as e:
        lastException = e
        return False

    return True

def executeRawQuery(statementToExec):
    global conn
    global lastException

    data = None

    try:
        data = conn.execute(statementToExec)
        return data
    except Exception as e:
        lastException = e
        return False

def getRow(tableName, keyToSearch, valueToSearch):
    global conn
    global lastException

    data = None

    try:
        conn.cursor().execute('SELECT * FROM '+tableName+' WHERE `' + keyToSearch + '`=\'' + valueToSearch +'\';')
        data = conn.cursor().fetchall()
    except Exception as e:
        lastException = e
        return False

    return data

def postRow(tableName, rowToPost):
    global conn
    global lastException

    try:
        keys = ','.join(rowToPost.keys())
        question_marks = ','.join(list('?' * len(rowToPost)))
        values = tuple(rowToPost.values())
        conn.execute('INSERT INTO ' + tableName + ' (' + keys + ') VALUES (' + question_marks + ')', values)
    except Exception as e:
        lastException = e
        return False

    return True

def commitChanges():
    global conn
    global lastException

    try:
        conn.commit()
    except Exception as e:
        lastException = e
        return False

    return True

def closeConnection():
    global lastException

    try:
        conn.close()
    except Exception as e:
        lastException = e
        return False

    return True

def getLastException():
    global lastException

    return str(lastException)