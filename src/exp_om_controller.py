from PyQt4.QtCore import * #@UnusedWildImport
from PyQt4.QtGui import * #@UnusedWildImport
from PyQt4.QtSql import *  # @UnusedWildImport
from qgis.core import *
from qgis.gui import QgsMessageBar  # @UnresolvedImport
from qgis.utils import iface  # @UnresolvedImport
from functools import partial
from datetime import datetime
import time
import os
from utils import *  # @UnusedWildImport


def openExpOm(dialog, parcela, expOmId = None):

    global _dialog, _iface, _parcela, _expOmId, current_path, current_date
    global MSG_DURATION
   
    current_path = os.path.dirname(os.path.abspath(__file__))
    date_aux = time.strftime("%d/%m/%Y")
    current_date = datetime.strptime(date_aux, "%d/%m/%Y")

    # Save reference to the QGIS interface
    MSG_DURATION = 5	
    _iface = iface
    getLayers()

    # Load data from domain tables 
    loadData()

    # Get dialog and his widgets
    _parcela = parcela		
    _dialog = dialog	
    _expOmId = None            
    setDialog(dialog)
    widgetsToGlobal()	
    
    # Initial configuration
    initConfig()
    
    # Check if we are in mode 'Create' or 'Update'
    if expOmId is None:
        
        # Fill date widgets with current Date
        dateLiquidacio.setDate(current_date)        
        dateEntrada.setDate(current_date)
        dateLlicencia.setDate(current_date)
        dateVisat.setDate(current_date)   
        
        # Manage 'Tipus solicitatnt'
        getTipusSol() 
        
    else:
        _expOmId = expOmId
        getDadesExpedient()
        getLiquidacio()
        checkDocument()           
    

    # Open form as modeless dialog
    _dialog.show()
    

def widgetsToGlobal():
    
    global refcat, lblInfo, txtId, txtNumExp, cboTipus, txtEntrada, dateLiquidacio, dateEntrada, dateLlicencia
    global rbFisica, rbJuridica, lblSol, cboSol, cboSolCif, cboRep, txtSolDades, txtAdresa, txtCp, txtPoblacio, txtRefcat20, cboEmp
    global cboRedactor, cboDirector, cboExecutor, txtRedactor, txtDirector, txtExecutor, dateVisat, txtDoc
    global txtPress, cboClavPlu

    # Tab 'Dades Expedient'  
    refcat = _dialog.findChild(QLineEdit, "refcat")        
    lblInfo = _dialog.findChild(QLabel, "lblInfo")        
    txtId = _dialog.findChild(QLineEdit, "txtId")        
    txtNumExp = _dialog.findChild(QLineEdit, "txtNumExp")  
    txtEntrada = _dialog.findChild(QLineEdit, "txtEntrada")            
    cboTipus = _dialog.findChild(QComboBox, "cboTipus") 
    dateLiquidacio = _dialog.findChild(QDateEdit, "dateLiquidacio")      
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
    txtDoc = _dialog.findChild(QTextEdit, "txtDoc")   
    
    # Tab 'Liquidació'
    txtPress = _dialog.findChild(QLineEdit, "txtPress")    
    cboClavPlu = _dialog.findChild(QComboBox, "cboClavPlu") 


def initConfig():    
    
    refcat.setText(str(_parcela))

    # Fill combo boxes and completers with data stored in memory
    setComboModel(cboTipus, listTipus)
    setComboModel(cboSol, listNif)
    setComboModel(cboSolCif, listCif)
    setComboModel(cboRep, listNif)
    setComboModel(cboRedactor, listTecnic)
    setComboModel(cboDirector, listTecnic)
    setComboModel(cboExecutor, listTecnic)
    setComboModel(cboClavPlu, listClavPlu)
           
    # Get 'immobles' from selected 'parcela'
    loadImmobles()
    
    # Wire up our own signals
    setSignals()    
    
    # Other default configuration
    boldGroupBoxes()
    _dialog.findChild(QPushButton, "btnOpenDoc").setEnabled(False)         

        
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
  
    # Buttons
    _dialog.findChild(QPushButton, "btnFisica").clicked.connect(manageFisica)    
    _dialog.findChild(QPushButton, "btnJuridica").clicked.connect(manageJuridica)    
    _dialog.findChild(QPushButton, "btnTecnic").clicked.connect(manageTecnic)    
    _dialog.findChild(QPushButton, "btnDoc").clicked.connect(selectDocument)    
    _dialog.findChild(QPushButton, "btnOpenDoc").clicked.connect(openDocument)    
    _dialog.findChild(QPushButton, "btnRefresh").clicked.connect(refresh)    
    _dialog.findChild(QPushButton, "btnSave").clicked.connect(save)    
    _dialog.findChild(QPushButton, "btnClose").clicked.connect(close)
    
    # General and Tab 'Dades Expedient'
    #txtId.editingFinished.connect(idChanged)    
    rbFisica.clicked.connect(getTipusSol)    
    rbJuridica.clicked.connect(getTipusSol)    
    cboSol.currentIndexChanged.connect(partial(solChanged, 'persona'))
    cboSolCif.currentIndexChanged.connect(partial(solChanged, 'juridica'))
    cboRep.currentIndexChanged.connect(partial(solChanged, 'representant'))
    cboEmp.currentIndexChanged.connect(empChanged)
    
    # Tab 'Projecte'
    cboRedactor.currentIndexChanged.connect(redactorChanged)
    cboDirector.currentIndexChanged.connect(directorChanged)
    cboExecutor.currentIndexChanged.connect(executorChanged)
    
    # Tab 'Liquidació'
    txtPress.editingFinished.connect(pressChanged)    
    _dialog.findChild(QCheckBox, "chkPlaca").clicked.connect(partial(llicChanged, 'chkPlaca'))    
    _dialog.findChild(QCheckBox, "chkPlu").clicked.connect(partial(llicChanged, 'chkPlu'))    
    _dialog.findChild(QCheckBox, "chkRes").clicked.connect(partial(llicChanged, 'chkRes'))    
    _dialog.findChild(QCheckBox, "chkEnd").clicked.connect(partial(llicChanged, 'chkEnd'))   
    _dialog.findChild(QCheckBox, "chkCar").clicked.connect(partial(llicChanged, 'chkCar'))   
    _dialog.findChild(QCheckBox, "chkMov").clicked.connect(partial(llicChanged, 'chkMov'))   
    _dialog.findChild(QCheckBox, "chkFig").clicked.connect(partial(llicChanged, 'chkFig'))   
    _dialog.findChild(QCheckBox, "chkLeg").clicked.connect(partial(llicChanged, 'chkLeg'))   
    _dialog.findChild(QCheckBox, "chkPar").clicked.connect(partial(llicChanged, 'chkPar'))   
    _dialog.findChild(QCheckBox, "chkPro").clicked.connect(partial(llicChanged, 'chkPro'))   
    _dialog.findChild(QLineEdit, "txtCarM").editingFinished.connect(partial(llicChanged, 'chkCar'))   
    _dialog.findChild(QLineEdit, "txtMovM").editingFinished.connect(partial(llicChanged, 'chkMov'))   
    _dialog.findChild(QLineEdit, "txtFigM").editingFinished.connect(partial(llicChanged, 'chkFig'))   
    _dialog.findChild(QLineEdit, "txtParM").editingFinished.connect(partial(llicChanged, 'chkPar'))   
    _dialog.findChild(QCheckBox, "chkClavUni").clicked.connect(partial(clavChanged, 'chkClavUni'))   
    _dialog.findChild(QCheckBox, "chkClavPlu").clicked.connect(partial(clavChanged, 'chkClavPlu'))   
    _dialog.findChild(QCheckBox, "chkClavMes").clicked.connect(partial(clavChanged, 'chkClavMes'))   
    _dialog.findChild(QLineEdit, "txtClavUniN").editingFinished.connect(partial(clavChanged, 'chkClavUni'))   
    cboClavPlu.currentIndexChanged.connect(partial(clavChanged, 'chkClavPlu'))   
    _dialog.findChild(QLineEdit, "txtClavMesN").editingFinished.connect(partial(clavChanged, 'chkClavMes'))   
    _dialog.findChild(QCheckBox, "chkGarRes").clicked.connect(partial(garChanged, 'chkGarRes'))   
    _dialog.findChild(QCheckBox, "chkGarSer").clicked.connect(partial(garChanged, 'chkGarSer'))   
    
        
# Load combos from domain tables (only first time)
def loadData():

    global listTipus, listNif, listCif, listTecnic, listClavPlu
    
    sql = "SELECT id FROM data.tipus_om ORDER BY id"
    listTipus = queryToList(sql)
    sql = "SELECT id FROM data.persona ORDER BY id"
    listNif = queryToList(sql)
    sql = "SELECT id FROM data.juridica ORDER BY id"
    listCif = queryToList(sql)
    sql = "SELECT id FROM data.tecnic ORDER BY id"
    listTecnic = queryToList(sql)
    
    listClavPlu = []
    listClavPlu.append('')
    listClavPlu.append('2 a 5')
    listClavPlu.append('6 a 9')
    listClavPlu.append('10 a 13')
        
        
def loadImmobles():

    model = QSqlQueryModel();
    sql = "SELECT adreca FROM data.immoble WHERE refcat = '"+refcat.text()+"' ORDER BY id"
    model.setQuery(sql);
    cboEmp.setModel(model)

    
def getLayers():
    
    global layers, layerFisica, layerJuridica, layerTecnic
       
    # Iterate over all layers
    layers = _iface.legendInterface().layers()	
    for layer in layers:
        if layer.name() == 'persona':
            layerFisica = layer
        if layer.name() == 'juridica':
            layerJuridica = layer
        if layer.name() == 'tecnic':
            layerTecnic = layer
                    

def getDadesExpedient():

    sql = "SELECT num_exp, data_ent, data_llic, tipus_id, tipus_solic_id, solic_persona_id, solic_juridica_id, repre_id"
    sql+= ", parcela_id, immoble_id, num_hab, notif_adreca, notif_poblacio, notif_cp"
    sql+= ", redactor_id, director_id, executor_id, constructor, visat_num, visat_data, observacions, id, reg_ent, data_liq, documentacio "
    sql+= "FROM data.exp_om WHERE id = "+str(_expOmId)
    query = QSqlQuery(sql) 
       
    if (query.next()):    
        setText("txtId", getQueryValue(query, 21))        
        setText("txtEntrada", getQueryValue(query, 22))        
        dateLiquidacio.setDate(query.value(23))
        txtNumExp.setText(getQueryValue(query, 0))
        dateEntrada.setDate(query.value(1))
        dateLlicencia.setDate(query.value(2))
        setSelectedItem("cboTipus", getQueryValue(query, 3))
        if (query.value(4) == 'persona'):
            rbFisica.setChecked(True)
            cboSol.setVisible(True)
            cboSolCif.setVisible(False)            
            setSelectedItem("cboSol", getQueryValue(query, 5))
            setSelectedItem("cboSolCif", None)
        else:
            rbJuridica.setChecked(True)
            setSelectedItem("cboSol", None)
            setSelectedItem("cboSolCif", getQueryValue(query, 6))  
             
        setSelectedItem("cboRep", getQueryValue(query, 7))   
        setText("refcat", query.value(8))
        
        # TODO: Gestió immoble
        setText("txtRefcat20", getQueryValue(query, 9))
        
        setText("txtNumHab", getQueryValue(query, 10))
        setText("txtNotifAdreca", getQueryValue(query, 11))
        setText("txtNotifPoblacio", getQueryValue(query, 12))
        setText("txtNotifCp", getQueryValue(query, 13))
        setSelectedItem("cboRedactor", getQueryValue(query, 14))  
        setSelectedItem("cboDirector", getQueryValue(query, 15))  
        setSelectedItem("cboExecutor", getQueryValue(query, 16))  
        setText("txtConstructor", getQueryValue(query, 17))
        setText("txtVisatNum", getQueryValue(query, 18))
        dateVisat.setDate(query.value(19))
        setText("txtObs", getQueryValue(query, 20)) 
        setText("txtDoc", getQueryValue(query, 24)) 
                           
    else:
        showWarning(query.lastError().text(), 100)
    

# TODO Update: Get Dades Liquidacio
def getLiquidacio():
    pass


def checkId():
    
#     if not txtNumExp.text():
#         msgBox = QMessageBox()
#         msgBox.setText(u"Cal especificar un identificador d'expedient")
#         msgBox.exec_()
#         return False 
    return True


# Save data from Tab 'Dades Expedient' and 'Projecte' into Database
def saveDadesExpedient():
 
    # Check if we have set 'id'
    if not checkId():
        return    
    
    # Get dates
    dLiquidacio = getDate("dateLiquidacio", "data_liq")       
    dEntrada = getDate("dateEntrada", "data_ent")
    dLlicencia = getDate("dateLlicencia", "data_llic")
    dVisat = getDate("dateVisat", "visat_data")
    
    # Create SQL body
    if _expOmId is None:
        sql = "INSERT INTO data.exp_om (num_exp, data_ent, data_llic, tipus_id, tipus_solic_id, solic_persona_id, solic_juridica_id, repre_id"
        sql+= ", parcela_id, immoble_id, num_hab, notif_adreca, notif_poblacio, notif_cp"
        sql+= ", redactor_id, director_id, executor_id, constructor, visat_num, visat_data, observacions, reg_ent, data_liq, documentacio)"
        sql+= " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"           
    else:
        sql = "UPDATE data.exp_om SET"
        sql+= " num_exp=:0, data_ent=:1, data_llic=:2, tipus_id=:3, tipus_solic_id=:4, solic_persona_id=:5, solic_juridica_id=:6, repre_id=:7"
        sql+= ", parcela_id=:8, immoble_id=:9, num_hab=:10, notif_adreca=:11, notif_poblacio=:12, notif_cp=:13"     
        sql+= ", redactor_id=:14, director_id=:15, executor_id=:16, constructor=:17, visat_num=:18, visat_data=:19, observacions=:20"
        sql+= ", reg_ent=:21, data_liq=:22, documentacio=:23"
        sql+= " WHERE id=:id"       
    
    # Bind values
    query = QSqlQuery()    
    query.prepare(sql)           
    query.bindValue(":id", str(_expOmId))        
    query.bindValue(0, getStringValue("txtNumExp")) 
    query.bindValue(1, dEntrada["value"]) 
    query.bindValue(2, dLlicencia["value"]) 
    query.bindValue(3, getSelectedItem("cboTipus")) 

    # NIF or CIF?
    if rbFisica.isChecked():
        query.bindValue(4, 'persona') 
        query.bindValue(5, getSelectedItem("cboSol")) 
        query.bindValue(6, None)
    else:
        query.bindValue(4, 'juridica') 
        query.bindValue(5, None)
        query.bindValue(6, getSelectedItem("cboSolCif")) 
    
    query.bindValue(7, getSelectedItem("cboRep")) 
    query.bindValue(8, getStringValue("refcat")) 
    query.bindValue(9, getStringValue("txtRefcat20")) 
    query.bindValue(10, getStringValue("txtNumHab"))
    query.bindValue(11, getStringValue("txtNotifAdreca"))
    query.bindValue(12, getStringValue("txtNotifPoblacio"))
    query.bindValue(13, getStringValue("txtNotifCp"))
    query.bindValue(14, getSelectedItem("cboRedactor"))
    query.bindValue(15, getSelectedItem("cboDirector"))
    query.bindValue(16, getSelectedItem("cboExecutor"))
    query.bindValue(17, getStringValue("txtConstructor"))
    query.bindValue(18, getStringValue("txtVisatNum"))
    query.bindValue(19, dVisat["value"])
    query.bindValue(20, getStringValue("txtObs"))  
    query.bindValue(21, getStringValue("txtEntrada"))  
    query.bindValue(22, dLiquidacio["value"])  
    query.bindValue(23, getStringValue("txtDoc"))  

    # Execute SQL
    result = query.exec_()
    if result is False:
        showWarning(query.lastError().text(), 100)
        showWarning(query.lastQuery(), 100)        
    
    return result

    
# Save data from Tab 'Liquidació' into Database
def saveLiquidacio():
 
    clavPlu = None
    selItem = getSelectedItem('cboClavPlu')
    if selItem is not None:
        clavPlu = selItem[:2]
        if not isNumber(clavPlu):
            clavPlu = None        
   
    # Create SQL
    query = QSqlQuery()   
    if _expOmId is None:    
        # Get last id
        sql = "SELECT last_value FROM data.exp_om_id_seq"
        query = QSqlQuery(sql)    
        if (query.next()):    
            expId = query.value(0)
        sql= "INSERT INTO data.press_om (pressupost, placa, plu, res, ende, car, mov, fig, leg, par, pro, clav_uni, clav_mes, gar_res, gar_ser, clav_plu, om_id)"
        sql+= " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"         
        query.prepare(sql)   
        query.bindValue(16, expId)         
    else:   
        sql = "UPDATE data.press_om SET"
        sql+= " pressupost=:0, placa=:1, plu=:2, res=:3, ende=:4, car=:5, mov=:6, fig=:7, leg=:8, par=:9"
        sql+= ", pro=:10, clav_uni=:11, clav_mes=:12, gar_res=:13, gar_ser=:14, clav_plu=:15"
        sql+= " WHERE om_id=:om_id"                
        query.prepare(sql)                
        query.bindValue(":om_id", _expOmId) 
    
    # Bind values
    query.bindValue(0, getStringValue("txtPress")) 
    query.bindValue(1, isChecked("chkPlaca")) 
    query.bindValue(2, isChecked("chkPlu")) 
    query.bindValue(3, isChecked("chkRes")) 
    query.bindValue(4, isChecked("chkEnd")) 
    query.bindValue(5, getStringValue("txtCarM")) 
    query.bindValue(6, getStringValue("txtMovM")) 
    query.bindValue(7, getStringValue("txtFigM")) 
    query.bindValue(8, isChecked("chkLeg")) 
    query.bindValue(9, getStringValue("txtParM")) 
    query.bindValue(10, isChecked("chkPro")) 
    query.bindValue(11, getStringValue("txtClavUniN")) 
    query.bindValue(12, getStringValue("txtClavMesN")) 
    query.bindValue(13, isChecked("chkGarRes")) 
    query.bindValue(14, isChecked("chkGarSer")) 
    query.bindValue(15, clavPlu) 
    
    # Execute SQL
    result = query.exec_()
    if result is False:
        showWarning(query.lastError().text(), 100)
    else:
        showInfo("Expedient guardat correctament")
                  

def getPress():
    
    press = txtPress.text().replace(",", ".")
    txtPress.setText(press)
    if not isNumber(press):
        showWarning(u"Format numèric incorrecte")
        return 0.0
    return float(press)


def updateTotal():
    total = getFloat('txtIcio')+getFloat('txtPlaca')+getFloat('txtLlicTot')+getFloat('txtClavTot')
    setText('txtTotalLiq', total)  
      
    
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
        


# Slots: Tab 'Dades expedient'
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
 
 
def idChanged():
    
    expId = txtId.text()
    if len(expId) <> 5:
        showInfo(u"El id ha de tenir exactament 5 caràcters amb el format: <any><xxx>")
        txtNumExp.setText("")        
        return
    numExp = expId[2:]+"/"+expId[:2]
    txtNumExp.setText(numExp)
    
    
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
    query = QSqlQuery(sql)    
    if (query.next()):      
        txtSolDades.setText(query.value(0))
        txtAdresa.setText(query.value(1))
        txtCp.setText(query.value(2))
        txtPoblacio.setText(query.value(3))
    else:
        clearNotificacions()
        
       
def empChanged():

    sql = "SELECT id FROM data.immoble WHERE adreca = "+getSelectedItem2("cboEmp")+" ORDER BY id"
    query = QSqlQuery(sql)    
    if (query.next()):        
        txtRefcat20.setText(query.value(0))    
   
        
# Slots: Tab 'Projecte'        
def redactorChanged():
    tecnicChanged('cboRedactor', txtRedactor)
        
def directorChanged():
    tecnicChanged('cboDirector', txtDirector)
        
def executorChanged():
    tecnicChanged('cboExecutor', txtExecutor)
        
def tecnicChanged(cboName, txtWidget):
    
    sql = "SELECT COALESCE(nom, '') || ' ' || COALESCE(cognom_1, '') || ' ' || COALESCE(cognom_2, '') AS nom_complet "
    sql+= "FROM data.tecnic WHERE id = "+getSelectedItem2(cboName)
    query = QSqlQuery(sql)    
    if (query.next()):      
        txtWidget.setText(query.value(0))
    else:
        txtWidget.setText('')
    
    
# Slots: Tab 'Liquidació'
def pressChanged():
    
    press = getPress()
    icio = float(press) * 0.04
    setText("txtIcio", icio)
    llicChanged('chkPlu')
    llicChanged('chkRes')
    llicChanged('chkEnd')
    llicChanged('chkLeg')
    llicChanged('chkPro')
    garChanged('chkGarRes')
    garChanged('chkGarSer')
    updateTotal()
    

def llicChanged(widgetName):
    
    widget = _dialog.findChild(QCheckBox, widgetName)
    
    if widgetName == 'chkPlaca':
        value = ''
        if widget.isChecked():
            value = 12.9
        setText('txtPlaca', value)
        
    elif widgetName == 'chkPlu':
        value = ''
        if widget.isChecked():
            value = max(38.15, getPress() * 0.0096)
        setText('txtPlu', value)
        
    elif widgetName == 'chkRes':
        value = ''
        if widget.isChecked():
            value = max(38.15, getPress() * 0.0094)
        setText('txtRes', value)
        
    elif widgetName == 'chkEnd':
        value = ''
        if widget.isChecked():
            value = max(0, getPress() * 0.0367)
        setText('txtEnd', value)
        
    elif widgetName == 'chkCar':
        value = ''
        if widget.isChecked():
            value = getFloat('txtCarM') * 8.9
        setText('txtCar', value)
        
    elif widgetName == 'chkMov':
        value = ''
        if widget.isChecked():
            value = getFloat('txtMovM') * 0.26
        setText('txtMov', value)
        
    elif widgetName == 'chkFig':
        value = ''
        if widget.isChecked():
            value = max(725.4, getFloat('txtFigM') * 0.02)
        setText('txtFig', value)
        
    elif widgetName == 'chkLeg':
        value = ''
        if widget.isChecked():
            value = getFloat('txtPlu') + getFloat('txtCar') + getFloat('txtEnd')
        setText('txtLeg', value)
    
    elif widgetName == 'chkPar':
        value = ''
        if widget.isChecked():
            value = max(244, getFloat('txtParM') * 0.02)
        setText('txtPar', value)
    
    elif widgetName == 'chkPro':
        value = ''
        if widget.isChecked():
            value = 22.2
        setText('txtPro', value)
        
    total = getFloat('txtPlu')+getFloat('txtRes')+getFloat('txtEnd')+getFloat('txtCar')+getFloat('txtMov')+getFloat('txtFig')+getFloat('txtLeg')+getFloat('txtPar')+getFloat('txtPro')
    setText('txtLlicTot', total)
    updateTotal()    
    
    
def clavChanged(widgetName):
    
    widget = _dialog.findChild(QCheckBox, widgetName)
    
    if widgetName == 'chkClavUni':
        value = ''
        if widget.isChecked():
            value = getFloat('txtClavUniN') * 390.66
        setText('txtClavUni', value)
        
    elif widgetName == 'chkClavMes':
        value = ''
        if widget.isChecked():
            value = getFloat('txtClavMesN') * 65.025
        setText('txtClavMes', value)
        
    elif widgetName == 'chkClavPlu':
        value = ''
        if widget.isChecked():
            selIndex = cboClavPlu.currentIndex()
            if selIndex == 1:
                value = 650.76
            elif selIndex == 2:
                value = 910.86
            elif selIndex == 3:
                value = 1170.96
        setText('txtClavPlu', value)
        
    total = getFloat('txtClavUni')+getFloat('txtClavPlu')+getFloat('txtClavMes')
    setText('txtClavTot', total)   
    updateTotal()    
    
         
def garChanged(widgetName):
    
    widget = _dialog.findChild(QCheckBox, widgetName)
    
    if widgetName == 'chkGarRes':
        value = ''
        if widget.isChecked():
            value = max(1000, getPress() * 0.01)
        setText('txtGarRes', value)
        
    elif widgetName == 'chkGarSer':
        value = ''
        if widget.isChecked():
            value = max(600, getPress() * 0.01)
        setText('txtGarSer', value)
        
    updateTotal()        
        
    #total = getFloat('txtGarRes')+getFloat('txtGarSer')
    #setText('txtClavTot', total)        
            
            
# Slots: Window buttons    
def manageFisica():
    iface.showAttributeTable(layerFisica)
                    
def manageJuridica():
    iface.showAttributeTable(layerJuridica)
                    
def manageTecnic():
    iface.showAttributeTable(layerTecnic)
    
def selectDocument():
    os.chdir(os.getcwd())
    fileDialog = QFileDialog()
    fileDialog.setFileMode(QFileDialog.ExistingFile);
    filePath = fileDialog.getOpenFileName(None, "Select doc file")
    txtDoc.setText(filePath)
    checkDocument()
    
def openDocument():
    filePath = getStringValue("txtDoc")
    if filePath is not None:    
        if os.path.isfile(filePath):
            os.startfile(filePath)
        
def checkDocument():
    filePath = getStringValue("txtDoc")
    if filePath is not None:
        if os.path.isfile(filePath):
            _dialog.findChild(QPushButton, "btnOpenDoc").setEnabled(True)         
    
def refresh():
    loadData()
    setComboModel(cboTipus, listTipus)
    setComboModel(cboSol, listNif)       
         
def save():
    result = saveDadesExpedient()
    if result:
        saveLiquidacio()
        _dialog.accept()   
    
def close():
    _dialog.close()   
    