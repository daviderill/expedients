﻿# -*- coding: utf-8 -*-
from PyQt4.QtCore import *    # @UnusedWildImport
from PyQt4.QtGui import *     # @UnusedWildImport
from qgis.core import *       # @UnusedWildImport
from qgis.utils import iface  # @UnresolvedImport
from datetime import datetime
import time
from utils import *           # @UnusedWildImport
from exp_om_dialog import ExpOmDialog
import exp_om_controller
from main_dao import MainDao


def formOpen(dialog,layerid,featureid):

    global _dialog, _iface, current_path, current_date, MSG_DURATION

    # Get dialog and his widgets
    _dialog = dialog
    setDialog(dialog)
    widgetsToGlobal()
    
    # Check if it is the first time we execute this module
    if isFirstTime():

        # Get current path and save reference to the QGIS interface
        current_path = os.path.dirname(os.path.abspath(__file__))
        date_aux = time.strftime("%d/%m/%Y")
        current_date = datetime.strptime(date_aux, "%d/%m/%Y")
        _iface = iface
        MSG_DURATION = 10

        # Connect to Database (only once, when loading map)
        if not loadSettings():
            return False
        #showInfo("Attempting to connect to DB")
        if not connectDb():
            return False
    
    # Initial configuration
    initConfig()


def loadSettings():
    
    global settings 

    # Load local settings of the plugin
    setting_file = os.path.join(current_path, 'config', 'expedients.config')
    if not os.path.isfile(setting_file):
        showWarning("Config file not found at: "+setting_file)
        return False
    
    settings = QSettings(setting_file, QSettings.IniFormat)
    return True
        

def connectDb():

    global mainDao
    
    # Get database parameters from configuration file
    try:
        host = str(settings.value('database/host'))
        port = int(settings.value('database/port', '5432'))
        db = str(settings.value('database/db'))
        user = str(settings.value('database/user'))
        pwd = str(settings.value('database/pwd'))
    except Exception as ex:
        showWarning('Error %s' % ex)
        return False        
         
    # Set database connection   
    mainDao = MainDao()
    mainDao.setParams(host, port, db, user, pwd)
    status = mainDao.initDb()
    if status is False:
        showWarning("Error connecting to Database")
    
    return status


def widgetsToGlobal():
    
    global refcat, tblExp, cboEmp
    refcat = _dialog.findChild(QLineEdit, "refcat")
    tblExp = _dialog.findChild(QTableView, "tblExp")
    cboEmp = _dialog.findChild(QComboBox, "cboEmp")  

    
def initConfig():
       
    # Load 'immobles' from selected 'parcela'
    loadImmobles()
    
    # Get 'Expedients' from selected 'parcela' and filter conditions
    filter_ = "parcela_id = '"+refcat.text()+"'"
    getExpedients(filter_)
    
    # Wire up our own signals
    setSignals()    
    
    # Other default configuration
    boldGroupBoxes()
    _dialog.hideButtonBox()    

    # Refresh map
    _iface.mapCanvas().refresh()

    # TODO TEST
    #dlg = ExpOmDialog()
    #if not dlg:
    #    showInfo("UI form not loaded")
    #    return
    #exp_om_controller.openExpOm(dlg, '7220201CF8672S', 122)
    
    
# Set Group Boxes title font to bold    
def boldGroupBoxes():   
    
    _dialog.findChild(QGroupBox, "gb1").setStyleSheet("QGroupBox { font-weight: bold; } ")
    _dialog.findChild(QGroupBox, "gb2").setStyleSheet("QGroupBox { font-weight: bold; } ")
    _dialog.findChild(QGroupBox, "gb3").setStyleSheet("QGroupBox { font-weight: bold; } ")
        
     
# Wire up our own signals    
def setSignals():
   
    _dialog.findChild(QPushButton, "btnCreate").clicked.connect(create)
    _dialog.findChild(QPushButton, "btnUpdate").clicked.connect(update)
    _dialog.findChild(QPushButton, "btnDelete").clicked.connect(delete)
    _dialog.findChild(QPushButton, "btnRefresh").clicked.connect(refresh)
    _dialog.findChild(QPushButton, "btnClose").clicked.connect(close)
    cboEmp.currentIndexChanged.connect(empChanged)


# Get 'Expedients' from selected 'parcela' and filter conditions
def getExpedients(filter_):

    global model
    
    # Define model
    model = QSqlTableModel();
    model.setTable("data.exp_om")
    model.setFilter(filter_)
    model.setSort(0, Qt.AscendingOrder)
    model.setEditStrategy(QSqlTableModel.OnRowChange)
    model.select()
    model.setHeaderData(0, Qt.Horizontal, "Id")
    model.setHeaderData(1, Qt.Horizontal, "Num. Exp.")
    model.setHeaderData(2, Qt.Horizontal, "D. Entrada")
    model.setHeaderData(23, Qt.Horizontal, "D. AutoLiq.")
    model.setHeaderData(16, Qt.Horizontal, "Immoble")
    model.dataChanged.connect(dataChanged)

    # Set this model to the view
    tblExp.setModel(model)
    tblExp.horizontalHeader().moveSection(23, 1)
    hideColumns(tblExp)
    verticalHeader = tblExp.verticalHeader()
    verticalHeader.setResizeMode(QHeaderView.ResizeToContents)
    tblExp.resizeColumnsToContents()
    tblExp.setCurrentIndex(model.index(0, 0))    
       
   
def hideColumns(tblExp):
    for i in range (3, 16):
        tblExp.hideColumn(i)
    for i in range (17, 23):
        tblExp.hideColumn(i)
    for i in range (24, 27):
        tblExp.hideColumn(i)

        
def dataChanged():
    ok = model.submitAll()
    if not ok:
        showWarning(u"Error d'actualització de la taula")


def loadImmobles():

    sql = "SELECT refcat20 || ' - ' || COALESCE(adreca_t, '') FROM data.ibi WHERE refcat14 = '"+refcat.text()+"' ORDER BY adreca_t"
    listImmobles = queryToList(sql)
    setComboModel("cboEmp", listImmobles)



# Slots

def empChanged():
    
    elem = getSelectedItem("cboEmp")
    if elem is not None:
        elem = elem[:23].strip()
        filter_ = "parcela_id = '"+refcat.text()+"' and immoble_id = '"+elem+"'"
    else:
        filter_ = "parcela_id = '"+refcat.text()+"'"
    getExpedients(filter_)

  
def create():
    
    dlg = ExpOmDialog()
    if not dlg:
        showWarning("No s'ha pogut carregar el formulari")
        return
    exp_om_controller.openExpOm(dlg, refcat.text())


def update(modelIndex):
     
    dlg = ExpOmDialog()
    if not dlg:
        showWarning("No s'ha pogut carregar el formulari")            
        return
    
    # Get selected rows, but we only process first one
    selectedList = tblExp.selectionModel().selectedRows()    
    if len(selectedList) == 0:
        showWarning("No ha seleccionat cap registre per modificar")
        return
    row = selectedList[0].row()               
    expOmId = model.record(row).value("id")
    
    # Open 'expOm' form
    exp_om_controller.openExpOm(dlg, refcat.text(), expOmId)        


def delete():

    # Get selected rows
    selectedList = tblExp.selectionModel().selectedRows()    
    if len(selectedList) == 0:
        showWarning("No ha seleccionat cap registre per eliminar")
        return
    
    msg = "Ha seleccionat les autoliquidacions:\n"
    listId = ''
    for i in range(0, len(selectedList)):
        row = selectedList[i].row()
        om_id = model.record(row).value("id")
        msg+= str(om_id)+", "
        listId = listId + str(om_id) + ", "
    msg = msg[:-2]
    listId = listId[:-2]
    infMsg = u"Està segur que desitja eliminar-los?"
    ret = askQuestion(msg, infMsg)
    if (ret == QMessageBox.Yes):
        sql = "DELETE FROM data.exp_om WHERE id IN ("+listId+")"
        query = QSqlQuery()
        query.exec_(sql)
        refresh()


def refresh():
    # Refresh table and map
    tblExp.model().select()
    _iface.mapCanvas().refresh()

    
def close():
    _dialog.parent().setVisible(False) 
    
    