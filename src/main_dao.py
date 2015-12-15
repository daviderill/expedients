# -*- coding: utf-8 -*-
from PyQt4.QtSql import * #@UnusedWildImport


class MainDao():

    def __init__(self): 
        pass

    def initDb(self):
        self.db = QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName(self.host)
        self.db.setPort(self.port)
        self.db.setDatabaseName(self.dbname)
        self.db.setUserName(self.user)
        self.db.setPassword(self.password)
        self.status = self.db.open()
        return self.status

    def setParams(self, host, port, dbname, user, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password  

    def getDb(self):
        return self.db
    
    def close(self):
        self.db.close()
