# -*- coding: utf-8 -*-
from PyQt4.QtCore import * #@UnusedWildImport
from PyQt4.QtGui import * #@UnusedWildImport
from PyQt4.QtSql import * #@UnusedWildImport


class MainDao():
    
    HOST = "127.0.0.1"
    PORT = 5432
    DB = "gis_cubelles"
    USER = "gisadmin"
    PWD = "8u9ijn"

    def __init__(self): 
        pass

    def initDb(self):

        self.db = QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName(self.HOST)
        self.db.setPort(self.PORT)
        self.db.setDatabaseName(self.DB)
        self.db.setUserName(self.USER)
        self.db.setPassword(self.PWD)
        self.status = self.db.open()
        return self.status

    def getDb(self):
        return self.db
    
    def close(self):
        self.db.close()

