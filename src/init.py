﻿from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from utils import *
from functools import partial
from datetime import datetime
import time
import os.path
import psycopg2
import psycopg2.extras
import sys


def formOpen(dialog,layerid,featureid):

    global _dialog, _iface, current_path, current_date
    global MSG_DURATION
    
    # Set global variables    
    _dialog = dialog
    setDialog(dialog)    
    MSG_DURATION = 5
    widgetsToGlobal()
    
    # Check if it is the first time we execute this module
    #if isFirstTime():
          
    current_path = os.path.dirname(os.path.abspath(__file__))
    date_aux = time.strftime("%d/%m/%Y")
    current_date = datetime.strptime(date_aux, "%d/%m/%Y")

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
    setComboModel(cboRep, listNif)
    setComboModel(cboRedactor, listTecnic)
    setComboModel(cboDirector, listTecnic)
    setComboModel(cboExecutor, listTecnic)
    
    # Fill date widgets with current Date
    dateEntrada.setDate(current_date)
    dateLlicencia.setDate(current_date)
    dateVisat.setDate(current_date)
        
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
    
    global refcat, lblInfo, txtId, txtNumExp, cboTipus, dateEntrada, dateLlicencia
    global rbFisica, rbJuridica, lblSol, cboSol, cboSolCif, cboRep, txtSolDades, txtAdresa, txtCp, txtPoblacio, txtRefcat20, cboEmp
    global cboRedactor, cboDirector, cboExecutor, txtRedactor, txtDirector, txtExecutor, dateVisat

    # Tab 'Dades Expedient'  
    refcat = _dialog.findChild(QLineEdit, "refcat")        
    lblInfo = _dialog.findChild(QLabel, "lblInfo")        
    txtId = _dialog.findChild(QLineEdit, "txtId")        
    txtNumExp = _dialog.findChild(QLineEdit, "txtNumExp")        
    cboTipus = _dialog.findChild(QComboBox, "cboTipus")  
    dateEntrada = _dialog.findChild(QDateEdit, "dateEntrada")  
    dateLlicencia = _dialog.findChild(QDateEdit, "dateLlicencia")  
    
    rbFisica = _dialog.findChild(QRadioButton, "rbFisica")  
    rbJuridica = _dialog.findChild(QRadioButton, "rbJuridica")  
    lblSol = _dialog.findChild(QLabel, "lblSol")   
    cboSol = _dialog.findChild(QComboBox, "cboSol")   
    cboSolCif = _dialog.findChild(QComboBox, "cboSolCif")   
    cboRep = _dialog.findChild(QComboBox, "cboRep")   
    txtSolDades = _dialog.findChild(QLineEdit, "txtSolDades")        
    txtAdresa = _dialog.findChild(QLineEdit, "txtNotifAdreca")        
    txtCp = _dialog.findChild(QLineEdit, "txtNotifCp")       
    txtPoblacio = _dialog.findChild(QLineEdit, "txtNotifPoblacio")          
    txtRefcat20 = _dialog.findChild(QLineEdit, "txtRefcat20")          
    cboEmp = _dialog.findChild(QComboBox, "cboEmp")   
    
    # Tab 'Projecte'
    cboRedactor = _dialog.findChild(QComboBox, "cboRedactor")   
    cboDirector = _dialog.findChild(QComboBox, "cboDirector")   
    cboExecutor = _dialog.findChild(QComboBox, "cboExecutor")   
    txtRedactor = _dialog.findChild(QLineEdit, "txtRedactor")   
    txtDirector = _dialog.findChild(QLineEdit, "txtDirector")   
    txtExecutor = _dialog.findChild(QLineEdit, "txtExecutor")   
    dateVisat = _dialog.findChild(QDateEdit, "dateVisat")  
    
    
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
  
    # General and Tab 'Dades Expedient'
    _dialog.findChild(QPushButton, "btnFisica").clicked.connect(manageFisica)    
    _dialog.findChild(QPushButton, "btnJuridica").clicked.connect(manageJuridica)    
    _dialog.findChild(QPushButton, "btnTecnic").clicked.connect(manageTecnic)    
    _dialog.findChild(QPushButton, "btnRefresh").clicked.connect(refresh)    
    _dialog.findChild(QPushButton, "btnSave").clicked.connect(save)    
    _dialog.findChild(QPushButton, "btnClose").clicked.connect(close)
    txtId.editingFinished.connect(idChanged)    
    rbFisica.clicked.connect(getTipusSol)    
    rbJuridica.clicked.connect(getTipusSol)    
    #cboSol.currentIndexChanged.connect(solChanged, 'persona')
    #cboSolCif.currentIndexChanged.connect(solChanged, 'juridica')
    #cboRep.currentIndexChanged.connect(solChanged, 'representant')
    cboSol.currentIndexChanged.connect(partial(solChanged, 'persona'))
    cboSolCif.currentIndexChanged.connect(partial(solChanged, 'juridica'))
    cboRep.currentIndexChanged.connect(partial(solChanged, 'representant'))
    cboEmp.currentIndexChanged.connect(empChanged)
    
    # Tab 'Projecte'
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
    
    listEmp = []
    cboEmp.addItem('')
    dAux = dict(refcat20 = '', emp = '')
    listEmp.append(dAux)    
    sql = "SELECT id, adreca FROM data.immoble WHERE refcat = '"+refcat.text()+"' ORDER BY id"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        cboEmp.addItem(unicode(row[1]))
        dAux = dict(refcat20 = row[0], emp = row[1])
        listEmp.append(dAux)

    
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
 
    # Check if we have set 'id'
    if not txtNumExp.text():
        msgBox = QMessageBox()
        msgBox.setText(u"Cal especificar un identificador d'expedient")
        msgBox.exec_()
        return
    
    # Get dates
    dEntrada = getDate("dateEntrada", "data_ent")
    dLlicencia = getDate("dateLlicencia", "data_llic")
    dVisat = getDate("dateVisat", "visat_data")

    # NIF or CIF?
    if rbFisica.isChecked():
        solic = "'persona', "+getSelectedItem2("cboSol")+", null"
    else:
        solic = "'juridica', null, "+getSelectedItem2("cboSolCif")
    
    # Create SQL
    sql_1 = "INSERT INTO data.exp_om (num_exp, data_ent, data_llic, tipus_id"
    sql_1+= ", tipus_solic_id, solic_persona_id, solic_juridica_id, repre_id"    
    sql_1+= ", parcela_id, immoble_id, num_hab, notif_adreca, notif_poblacio, notif_cp"
    sql_1+= ", redactor_id, director_id, executor_id, constructor, visat_num, visat_data"
    sql_2= " ) VALUES ("
    sql_2+= getStringValue2("txtNumExp")+", '"+dEntrada["value"]+"', '"+dLlicencia["value"]+"', "+getSelectedItem2("cboTipus")
    sql_2+= ", "+solic+ ", "+getSelectedItem2("cboRep")
    sql_2+= ", "+getStringValue2("refcat")+", "+getStringValue2("txtRefcat20")+", "+getStringValue2("txtNumHab")
    sql_2+= ", "+getStringValue2("txtNotifAdreca")+", "+getStringValue2("txtNotifPoblacio")+", "+getStringValue2("txtNotifCp")   
    sql_2+= ", "+getSelectedItem2("cboRedactor")+", "+getSelectedItem2("cboDirector")+", "+getSelectedItem2("cboExecutor")+", "+getStringValue2("txtConstructor")+", "+getStringValue2("txtVisatNum") +", '"+dVisat["value"]+"'"       
    sql_2+= ")"      
    sql= sql_1 + sql_2               
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
 
 
# Called when 'id' is updated
def idChanged():
    
    expId = txtId.text()
    if len(expId) <> 5:
        showInfo(u"El id ha de tenir exactament 5 caràcters amb el format: <any><xxx>")
        txtNumExp.setText("")        
        return
    numExp = expId[2:]+"/"+expId[:2]
    txtNumExp.setText(numExp)
    
            
# Called when 'Solicitant' is updated
def solChanged(aux):

    if aux == 'persona':
        table = 'persona'
        solId = getSelectedItem2("cboSol")
    elif aux == 'representant':
        table = 'persona'
        solId = getSelectedItem2("cboRep")
    else:
        table = 'juridica'
        solId = getSelectedItem2("cboSolCif")
        
    sql = "SELECT COALESCE(nom, '') || ' ' || COALESCE(cognom_1, '') || ' ' || COALESCE(cognom_2, '') AS nom_complet, adreca, cp, poblacio "
    sql+= "FROM data."+table+" WHERE id = "+solId
    cursor.execute(sql)
    row = cursor.fetchone()
    if row:
        txtSolDades.setText(row[0])
        txtAdresa.setText(row[1])
        txtCp.setText(row[2])
        txtPoblacio.setText(row[3])
    else:
        clearNotificacions()
        
        
# Called when 'Emplaçament' is updated
def empChanged():
    
    selIndex = cboEmp.currentIndex()
    refcat20 = listEmp[selIndex]["refcat20"]
    txtRefcat20.setText(refcat20)     
        
        
def redactorChanged():
    tecnicChanged('cboRedactor', txtRedactor)
        
def directorChanged():
    tecnicChanged('cboDirector', txtDirector)
        
def executorChanged():
    tecnicChanged('cboExecutor', txtExecutor)
        
        
def tecnicChanged(cboName, txtWidget):
    
    sql = "SELECT COALESCE(nom, '') || ' ' || COALESCE(cognom_1, '') || ' ' || COALESCE(cognom_2, '') AS nom_complet "
    sql+= "FROM data.tecnic WHERE id = "+getSelectedItem2(cboName)
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
    saveDadesExpedient(True)
    _dialog.accept()        
    
    
def close():
    print "close"
    #_dialog.reject() 
    #_dialog.parent().close() 
    _dialog.parent().setVisible(False)
    
    