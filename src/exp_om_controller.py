from PyQt4.QtCore import * #@UnusedWildImport
from PyQt4.QtGui import * #@UnusedWildImport
from PyQt4.QtSql import *  # @UnusedWildImport
from qgis.core import *
from qgis.gui import QgsMessageBar  # @UnresolvedImport
from qgis.utils import iface  # @UnresolvedImport
from utils import * #@UnusedWildImport
from functools import partial
from datetime import datetime
import time


def openExpOm(dialog, parcela, featureid = None):

    global _dialog, _iface, _parcela, current_path, current_date
    global MSG_DURATION

    # Check if it is the first time we execute this module
    #if isFirstTime():
    
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
    setDialog(dialog)
    widgetsToGlobal()	
    
    # Initial configuration
    initConfig()

    # Open form as modeless dialog
    _dialog.show()
    

def widgetsToGlobal():
    
    global refcat, lblInfo, txtId, txtNumExp, cboTipus, dateEntrada, dateLlicencia
    global rbFisica, rbJuridica, lblSol, cboSol, cboSolCif, cboRep, txtSolDades, txtAdresa, txtCp, txtPoblacio, txtRefcat20, cboEmp
    global cboRedactor, cboDirector, cboExecutor, txtRedactor, txtDirector, txtExecutor, dateVisat
    global txtPress, cboClavPlu

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
    _dialog.findChild(QPushButton, "btnRefresh").clicked.connect(refresh)    
    _dialog.findChild(QPushButton, "btnSave").clicked.connect(save)    
    _dialog.findChild(QPushButton, "btnClose").clicked.connect(close)
    
    # General and Tab 'Dades Expedient'
    txtId.editingFinished.connect(idChanged)    
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
        #layerType = layer.type()
        #print layer.name()
        if layer.name() == 'persona':
            layerFisica = layer
        if layer.name() == 'juridica':
            layerJuridica = layer
        if layer.name() == 'tecnic':
            layerTecnic = layer
                    

# Save data from Tab 'Dades Expedient' and 'Projecte' into Database
def saveDadesExpedient():
 
    # Check if we have set 'id'
    if not txtNumExp.text():
        msgBox = QMessageBox()
        msgBox.setText(u"Cal especificar un identificador d'expedient")
        msgBox.exec_()
        return False
    
    # Get dates
    dEntrada = getDate("dateEntrada", "data_ent")
    dLlicencia = getDate("dateLlicencia", "data_llic")
    dVisat = getDate("dateVisat", "visat_data")
    
    # Create SQLbody
    sql = "INSERT INTO data.exp_om (num_exp, data_ent, data_llic, tipus_id, tipus_solic_id, solic_persona_id, solic_juridica_id, repre_id"
    sql+= ", parcela_id, immoble_id, num_hab, notif_adreca, notif_poblacio, notif_cp"
    sql+= ", redactor_id, director_id, executor_id, constructor, visat_num, visat_data, observacions)"
    sql+= " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"     
    query = QSqlQuery()   
    query.prepare(sql)   
    
    # Bind values
    query.addBindValue(getStringValue("txtNumExp")) 
    query.addBindValue(dEntrada["value"]) 
    query.addBindValue(dLlicencia["value"]) 
    query.addBindValue(getSelectedItem("cboTipus"))
    # NIF or CIF?
    if rbFisica.isChecked():
        query.addBindValue('persona') 
        query.addBindValue(getSelectedItem("cboSol")) 
        query.addBindValue(None)
    else:
        query.addBindValue('juridica') 
        query.addBindValue(None)
        query.addBindValue(getSelectedItem("cboSolCif")) 
    query.addBindValue(getSelectedItem("cboRep")) 
    query.addBindValue(getStringValue("refcat")) 
    query.addBindValue(getStringValue("txtRefcat20")) 
    query.addBindValue(getStringValue("txtNumHab"))
    query.addBindValue(getStringValue("txtNotifAdreca"))
    query.addBindValue(getStringValue("txtNotifPoblacio"))
    query.addBindValue(getStringValue("txtNotifCp"))
    query.addBindValue(getSelectedItem("cboRedactor"))
    query.addBindValue(getSelectedItem("cboDirector"))
    query.addBindValue(getSelectedItem("cboExecutor"))
    query.addBindValue(getStringValue("txtConstructor"))
    query.addBindValue(getStringValue("txtVisatNum"))
    query.addBindValue(dVisat["value"])
    query.addBindValue(getStringValue("txtObs"))

    # Execute SQL
    result = query.exec_()
    if result is False:
        showWarning(query.lastError().text(), 100)
    
    return result

    
# Save data from Tab 'Liquidació' into Database
def saveLiquidacio():
 
    # Get id from Database
    sql = "SELECT last_value FROM data.exp_om_id_seq"
    query = QSqlQuery(sql)    
    if (query.next()):    
        expId = query.value(0)
    
    selItem = getSelectedItem2('cboClavPlu')
    clavPlu = selItem[-3:-1]
    if not isNumber(clavPlu):
        clavPlu = None
   
    # Create SQL
    sql= "INSERT INTO data.press_om (om_id, pressupost, placa, plu, res, ende, car, mov, fig, leg, par, pro, clav_uni, clav_plu, clav_mes, gar_res, gar_ser)"
    sql+= " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"           
    query = QSqlQuery()   
    query.prepare(sql)   
    
    # Bind values
    query.addBindValue(expId) 
    query.addBindValue(getStringValue("txtPress")) 
    query.addBindValue(isChecked("chkPlaca")) 
    query.addBindValue(isChecked("chkPlu")) 
    query.addBindValue(isChecked("chkRes")) 
    query.addBindValue(isChecked("chkEnd")) 
    query.addBindValue(getStringValue("txtCarM")) 
    query.addBindValue(getStringValue("txtMovM")) 
    query.addBindValue(getStringValue("txtFigM")) 
    query.addBindValue(isChecked("chkLeg")) 
    query.addBindValue(getStringValue("txtParM")) 
    query.addBindValue(isChecked("chkPro")) 
    query.addBindValue(getStringValue("txtClavUniN")) 
    query.addBindValue(clavPlu) 
    query.addBindValue(getStringValue("txtClavMesN")) 
    query.addBindValue(isChecked("chkGarRes")) 
    query.addBindValue(isChecked("chkGarSer")) 
    
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
    