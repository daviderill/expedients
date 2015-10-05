﻿from PyQt4.QtCore import *  # @UnusedWildImport
from PyQt4.QtGui import *  # @UnusedWildImport
from PyQt4.QtSql import *  # @UnusedWildImport
from qgis.core import *
from qgis.gui import QgsMessageBar  # @UnresolvedImport
from qgis.utils import iface  # @UnresolvedImport
from utils import *  # @UnusedWildImport
from datetime import datetime
import time
from exp_om_dialog import ExpOmDialog
from exp_om_controller import openExpOm
from main_dao import MainDao


def formOpen(dialog,layerid,featureid):

    global _dialog, _iface, current_path, current_date
    global MSG_DURATION
       
    # Check if it is the first time we execute this module
    #if True:		
    if isFirstTime():
          
        # Get current path and save reference to the QGIS interface		  
        current_path = os.path.dirname(os.path.abspath(__file__))
        date_aux = time.strftime("%d/%m/%Y")
        current_date = datetime.strptime(date_aux, "%d/%m/%Y")
        _iface = iface
        MSG_DURATION = 5		

        # Connect to Database (only once, when loading map)
        showInfo("Attempting to connect to DB")
        connectDb()

    # If not, close previous dialog	if already opened
    else:
        if _dialog.isVisible():
            _dialog.parent().setVisible(False)			

    # Get dialog and his widgets
    _dialog = dialog	
    widgetsToGlobal()

    # Get 'Expedients' from selected 'parcela' and filter conditions
    getExpedients()
    
    # Initial configuration
    initConfig()


def connectDb():

    global mainDao

    mainDao = MainDao()
    status = mainDao.initDb()
    if status is False:
        showWarning("Error connecting to Database")


def widgetsToGlobal():
    
    global refcat, cboEmp, tblExp

    refcat = _dialog.findChild(QLineEdit, "refcat")             
    cboEmp = _dialog.findChild(QComboBox, "cboEmp")    
    tblExp = _dialog.findChild(QTableView, "tblExp")   

    
def initConfig():    
    
    # Wire up our own signals
    setSignals()    
    
    # Other default configuration
    boldGroupBoxes()
    _dialog.hideButtonBox()    

    # Refresh map
    _iface.mapCanvas().refresh()	

    # TEST
    #dlg = ExpOmDialog()   
    #if not dlg:        
        #showInfo("UI form not loaded")            
        #return	
    #openExpOm(dlg)	
    
    
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
    #tblExp.doubleClicked.connect(update)	
    
        
# Get 'Expedients' from selected 'parcela' and filter conditions
def getExpedients():

    global model
    
    # Define model
    model = QSqlTableModel();
    model.setTable("data.exp_om")		
    model.setFilter("parcela_id = '"+refcat.text()+"'")	
    model.setSort(0, Qt.AscendingOrder)	

    model.setEditStrategy(QSqlTableModel.OnRowChange)   # OnManualSubmit
    model.select()

    model.setHeaderData(0, Qt.Horizontal, "Id");
    model.setHeaderData(1, Qt.Horizontal, "Num. Exp");
    model.dataChanged.connect(dataChanged)

    # Set this model to the view
    tblExp.setModel(model)
    hideColumns(tblExp)
    verticalHeader = tblExp.verticalHeader()
    verticalHeader.setResizeMode(QHeaderView.Fixed)
    verticalHeader.setDefaultSectionSize(20)
    tblExp.resizeColumnsToContents()

    # Load 'immobles' from selected 'parcela'
    loadImmobles()
       
   
def hideColumns(tblExp):
    for i in range (5, 16):	
        tblExp.hideColumn(i)	
    for i in range (18, 23):	
        tblExp.hideColumn(i)			

def dataChanged():
    ok = model.submitAll()
    if not ok:
        showWarning(u"Error d'actualització de la taula")


def loadImmobles():

    sql = "SELECT adreca FROM data.immoble WHERE refcat = '"+refcat.text()+"' ORDER BY id"
    #query = QSqlQuery(sql)	
    #fieldNo = query.record().indexOf("adreca")
    #while (query.next()):
    #    country = query.value(fieldNo)
    model = QSqlQueryModel();
    model.setQuery(sql);
    cboEmp.setModel(model)
 

# Utility functions
def showInfo(text, duration = None):
    
    if duration is None:
        _iface.messageBar().pushMessage("", text, QgsMessageBar.INFO, MSG_DURATION)  
    else:
        _iface.messageBar().pushMessage("", text, QgsMessageBar.INFO, duration)              
    
      
def showWarning(text, duration = None):
    
    if duration is None:
        _iface.messageBar().pushMessage("", text, QgsMessageBar.WARNING, MSG_DURATION)  
    else:
        _iface.messageBar().pushMessage("", text, QgsMessageBar.WARNING, duration)               


def askQuestion(text, infText = None):

    msgBox = QMessageBox()
    msgBox.setText(text);
    if infText is not None:
        msgBox.setInformativeText(infText);
    msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msgBox.setDefaultButton(QMessageBox.No)
    return msgBox.exec_()  
     
            
# Slots: Window buttons  
  
def create():
    
    dlg = ExpOmDialog()   
    if not dlg:        
        showWarning("No s'ha pogut carregar el formulari")            
        return	
    openExpOm(dlg, refcat.text())	
         
         
def update(modelIndex):
     
    #print str(modelIndex)	
    dlg = ExpOmDialog()   
    if not dlg:        
        showWarning("No s'ha pogut carregar el formulari")            
        return    
    
    # Get selected rows, but we only process first one
    selectedList = tblExp.selectionModel().selectedRows()    
    if len(selectedList) == 0:
        showWarning("No ha seleccionat cap registre per modificar")
        return
    row = selectedList[0].row()               #QModelIndex
    expOmId = model.record(row).value("id")          # @ReservedAssignment
    
    # Open 'expOm' form
    openExpOm(dlg, refcat.text(), expOmId)        


def delete():
   
    #selModel = tblExp.selectionModel()   #QItemSelectionModel
    #itemSel = selModel.selection()       #QItemSelection
    #indexes = itemSel.indexes()          #QModelIndexList

    # Get selected rows
    selectedList = tblExp.selectionModel().selectedRows()    
    if len(selectedList) == 0:
        showWarning("No ha seleccionat cap registre per eliminar")
        return
    
    msg = "Ha seleccionat els expedients:\n"	
    listId = ''
    for i in range(0, len(selectedList)):
        row = selectedList[i].row()               #QModelIndex
        id = model.record(row).value("id")		  # @ReservedAssignment
        num_exp = model.record(row).value("num_exp")
        msg = msg + num_exp + ", "		
        listId = listId + str(id) + ", "
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
    mainDao.close()	
    _dialog.parent().setVisible(False) 
    