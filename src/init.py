from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from utils import *
from datetime import datetime
import time
import os.path
import psycopg2
import psycopg2.extras
import sys


def formOpen(dialog,layerid,featureid):

    global _dialog, _iface, current_path
    global MSG_DURATION
    
    # Set global variables    
    _dialog = dialog
    setDialog(dialog)    
    MSG_DURATION = 5
    widgetsToGlobal()
    
    # Check if it is the first time we execute this module
    #if isFirstTime():
          
    current_path = os.path.dirname(os.path.abspath(__file__))

    # Save reference to the QGIS interface
    _iface = iface
    getLayers()

    # Connect to Database (only once, when loading map)
    showInfo("Attempting to connect to DB")
    connectDb()

    # Load data from domain tables 
    loadData()
    
    
    # Fill combo boxes and completers with data stored in memory
    setComboModel(cboTipus, listTipus)
    setComboModel(cboSol, listNif)
    setComboModel(cboSolCif, listCif)
    setComboModel(cboRedactor, listTecnic)
    setComboModel(cboDirector, listTecnic)
    setComboModel(cboExecutor, listTecnic)
    
    # Get 'immobles' from selected 'parcela'
    loadImmobles()
    
    # Wire up our own signals
    setSignals()    
    
    # Other default configuration
    getTipusSol()
    boldGroupBoxes()


# Connect to Database (only once, when loading map)
def connectDb():

    global conn, cursor
    try:
        conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=gis_cubelles user=gisadmin password=8u9ijn")        
        #conn = psycopg2.connect("host=192.168.10.7 port=5432 dbname=gisdb user=gisadmin password=cubelles")        
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        setCursor(cursor)        
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e    
        sys.exit(1)
        

def widgetsToGlobal():
    
    global refcat, lblInfo, txtId, txtNumExp, cboTipus, rbFisica, rbJuridica, lblSol, cboSol, cboSolCif, cboRep, txtSolDades, txtAdresa, txtCp, txtPoblacio, cboEmp
    global cboRedactor, cboDirector, cboExecutor, txtRedactor, txtDirector, txtExecutor
        
    refcat = _dialog.findChild(QLineEdit, "refcat")        
    lblInfo = _dialog.findChild(QLabel, "lblInfo")        
    txtId = _dialog.findChild(QLineEdit, "txtId")        
    txtNumExp = _dialog.findChild(QLineEdit, "txtNumExp")        
    cboTipus = _dialog.findChild(QComboBox, "cboTipus")  
    rbFisica = _dialog.findChild(QRadioButton, "rbFisica")  
    rbJuridica = _dialog.findChild(QRadioButton, "rbJuridica")  
    lblSol = _dialog.findChild(QLabel, "lblSol")   
    cboSol = _dialog.findChild(QComboBox, "cboSol")   
    cboSolCif = _dialog.findChild(QComboBox, "cboSolCif")   
    cboRep = _dialog.findChild(QComboBox, "cboRep")   
    txtSolDades = _dialog.findChild(QLineEdit, "txtSolDades")        
    txtAdresa = _dialog.findChild(QLineEdit, "txtAdresa")        
    txtCp = _dialog.findChild(QLineEdit, "txtCp")       
    txtPoblacio = _dialog.findChild(QLineEdit, "txtPoblacio")          
    cboEmp = _dialog.findChild(QComboBox, "cboEmp")   
    
    # Tab 'Projecte'
    cboRedactor = _dialog.findChild(QComboBox, "cboRedactor")   
    cboDirector = _dialog.findChild(QComboBox, "cboDirector")   
    cboExecutor = _dialog.findChild(QComboBox, "cboExecutor")   
    txtRedactor = _dialog.findChild(QLineEdit, "txtRedactor")   
    txtDirector = _dialog.findChild(QLineEdit, "txtDirector")   
    txtExecutor = _dialog.findChild(QLineEdit, "txtExecutor")   
    
    
# Set Group Boxes title font to bold    
def boldGroupBoxes():   
    
    _dialog.findChild(QGroupBox, "gb1Expedient").setStyleSheet("QGroupBox { font-weight: bold; } ")
    _dialog.findChild(QGroupBox, "gb2Interessat").setStyleSheet("QGroupBox { font-weight: bold; } ")
    _dialog.findChild(QGroupBox, "gb3Emplasament").setStyleSheet("QGroupBox { font-weight: bold; } ")
    _dialog.findChild(QGroupBox, "gbProjecte").setStyleSheet("QGroupBox { font-weight: bold; } ")
    _dialog.findChild(QGroupBox, "gb5").setStyleSheet("QGroupBox { font-weight: bold; } ")
    _dialog.findChild(QGroupBox, "gbUrb").setStyleSheet("QGroupBox { font-weight: bold; } ")
    _dialog.findChild(QGroupBox, "gbClav").setStyleSheet("QGroupBox { font-weight: bold; } ")
    _dialog.findChild(QGroupBox, "gbTot").setStyleSheet("QGroupBox { font-weight: bold; } ")
    _dialog.findChild(QGroupBox, "gbGar").setStyleSheet("QGroupBox { font-weight: bold; } ")
        
     
# Wire up our own signals    
def setSignals():
  
    _dialog.findChild(QPushButton, "btnFisica").clicked.connect(manageFisica)    
    _dialog.findChild(QPushButton, "btnJuridica").clicked.connect(manageJuridica)    
    _dialog.findChild(QPushButton, "btnTecnic").clicked.connect(manageTecnic)    
    _dialog.findChild(QPushButton, "btnRefresh").clicked.connect(refresh)    
    _dialog.findChild(QPushButton, "btnSave").clicked.connect(save)    
    _dialog.findChild(QPushButton, "btnClose").clicked.connect(close)
    rbFisica.clicked.connect(getTipusSol)    
    rbJuridica.clicked.connect(getTipusSol)    
    cboSol.currentIndexChanged.connect(solChanged)
    cboSolCif.currentIndexChanged.connect(solChanged)
    
    cboRedactor.currentIndexChanged.connect(redactorChanged)
    cboDirector.currentIndexChanged.connect(directorChanged)
    cboExecutor.currentIndexChanged.connect(executorChanged)
    
        
# Load combos from domain tables (only first time)
def loadData():

    global listTipus, listNif, listCif, listTecnic
    
    sql = "SELECT id FROM data.tipus_om ORDER BY id"
    listTipus = sqlToList(sql)
    sql = "SELECT id FROM data.persona ORDER BY id"
    listNif = sqlToList(sql)
    sql = "SELECT id FROM data.juridica ORDER BY id"
    listCif = sqlToList(sql)
    sql = "SELECT id FROM data.tecnic ORDER BY id"
    listTecnic = sqlToList(sql)
        
        
def loadImmobles():

    global listEmp
    
    sql = "SELECT id FROM data.immoble WHERE refcat = '"+refcat.text()+"' ORDER BY id"
    listEmp = sqlToList(sql)
    setComboModel(cboEmp, listEmp)    

    
def getLayers():
    
    global layers, layerFisica, layerJuridica, layerTecnic
    
    layers = _iface.legendInterface().layers()
    
    # Iterate over all layers
    for layer in layers:
        #layerType = layer.type()
        #print layer.name()
        if layer.name() == 'persona':
            layerFisica = layer
        if layer.name() == 'juridica':
            layerJuridica = layer
        if layer.name() == 'tecnic':
            layerTecnic = layer
        # Check if they are vector
        #if layerType == QgsMapLayer.VectorLayer:
            #self.layersList.append(layer)
            #self.dlg.ui.cboStreetLayer.addItem(layer.name())
            #self.dlg.ui.cboPortalLayer.addItem(layer.name()) 
                    

# Save data from Tab 'Dades Expedient' into Database
def saveDadesExpedient(update):
 
    numExp = _dialog.findChild(QLineEdit, "txtNumExp")    
    if not numExp.text():
        msgBox = QMessageBox()
        msgBox.setText(u"Cal especificar un número d'expedient")
        msgBox.exec_()
        print "Cal especificar un número d'expedient"
        return
    
    # Get dates
    dEntrada = getDate("dateEntrada", "data_ent")
    dLlicencia = getDate("dateLlicencia", "data_llic")

    # Create SQL
    sql = "INSERT INTO data.exp_om (num_exp, data_ent, data_llic, tipus_id, parcela_id, num_hab)"
    sql+= " VALUES ("+getStringValue2("txtNumExp")+", '"+dEntrada["value"]+"', '"+dLlicencia["value"]+"', "+getSelectedItem2("cboTipus")
    sql+= ", "+getStringValue2("refcat")+", "+getStringValue2("txtNumHab")+")"                        
    print sql
    cursor.execute(sql)        
    conn.commit()   
          

def clearNotificacions():       
    txtSolDades.setText('')
    txtAdresa.setText('')
    txtCp.setText('')
    txtPoblacio.setText('')
           

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
        


# Slots (Events)

def getTipusSol():
    
    if rbFisica.isChecked():
        cboSol.setVisible(True)
        cboSolCif.setVisible(False)
        lblSol.setText(u"NIF sol·licitant")
    else:
        cboSolCif.setVisible(True)
        cboSol.setVisible(False)
        lblSol.setText(u"CIF sol·licitant")
    clearNotificacions()
    
            
# Called when 'Solicitant' is updated
def solChanged():
    
    if rbFisica.isChecked():
        table = 'persona'
        solId = getSelectedItem2("cboSol")
    else:
        table = 'juridica'
        solId = getSelectedItem2("cboSolCif")
        
    sql = "SELECT COALESCE(nom, '') || ' ' || COALESCE(cognom_1, '') || ' ' || COALESCE(cognom_2, '') AS nom_complet, adreca, cp, poblacio "
    sql+= "FROM data."+table+" WHERE id = "+solId
    #print sql
    cursor.execute(sql)
    row = cursor.fetchone()
    if row:
        txtSolDades.setText(row[0])
        txtAdresa.setText(row[1])
        txtCp.setText(row[2])
        txtPoblacio.setText(row[3])
    else:
        clearNotificacions()
        
        
def redactorChanged():
    tecnicChanged('cboRedactor', txtRedactor)
        
def directorChanged():
    tecnicChanged('cboDirector', txtDirector)
        
def executorChanged():
    tecnicChanged('cboExecutor', txtExecutor)
        
        
def tecnicChanged(cboName, txtWidget):
    
    sql = "SELECT COALESCE(nom, '') || ' ' || COALESCE(cognom_1, '') || ' ' || COALESCE(cognom_2, '') AS nom_complet "
    sql+= "FROM data.tecnic WHERE id = "+getSelectedItem2(cboName)
    print sql
    cursor.execute(sql)
    row = cursor.fetchone()
    if row:
        txtWidget.setText(row[0])
    else:
        txtWidget.setText('')
        
                    
def manageFisica():
    iface.showAttributeTable(layerFisica)
                    
def manageJuridica():
    iface.showAttributeTable(layerJuridica)
                    
def manageTecnic():
    iface.showAttributeTable(layerTecnic)
    
    
def refresh():
    #print "refresh"
    loadData()
    setComboModel(cboTipus, listTipus)
    setComboModel(cboSol, listNif)
         
         
def save():
    print "save"
    saveDadesExpedient(True)
    _dialog.accept()        
    
    
def close():
    print "close"
    #_dialog.reject() 
    #_dialog.parent().close() 
    _dialog.parent().setVisible(False)
    
    