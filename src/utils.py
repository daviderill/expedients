from PyQt4.QtCore import * #@UnusedWildImport
from PyQt4.QtGui import * #@UnusedWildImport
from PyQt4.QtSql import *  # @UnusedWildImport
from qgis.gui import QgsMessageBar  # @UnresolvedImport
from qgis.utils import iface  # @UnresolvedImport
import logging
import os.path


#
# Utility funcions
#
def isFirstTime():
    
    global first
    if not 'first' in globals():
        first = True
    else:
        first = False
    return first


def setDialog(p_dialog):
    
    global _dialog
    _dialog = p_dialog
    
    
def setComboModel(widgetName, vector):

    elem = _dialog.findChild(QComboBox, widgetName)
    completer = QCompleter()
    completer.setCompletionColumn(0)
    completer.setMaxVisibleItems(10)
    completer.setCaseSensitivity(Qt.CaseInsensitive)
    model = QStringListModel()
    model.setStringList(vector)
    completer.setModel(model)
    elem.setModel(model)
    elem.setCompleter(completer)


def queryToList(sql):
    
    vector = []
    vector.append('')
    query = QSqlQuery(sql)    
    while (query.next()):
        value = query.value(0)   
        vector.append(unicode(value))          
    return vector 


def getQueryValue(query, index):

    value = ""
    if not query.isNull(index):
        value = query.value(index)
    return value


def setSelectedItem(widgetName, text):

    elem = _dialog.findChild(QComboBox, widgetName)
    if elem:
        if text is not None:
            index = elem.findText(text)
            elem.setCurrentIndex(index);
        else:
            elem.setCurrentIndex(0);


def getSelectedItem(widgetName):
    
    elem = _dialog.findChild(QComboBox, widgetName)
    if not elem.currentText():
        elem_text = None
    else:
        elem_text = elem.currentText()
    return elem_text


def getSelectedItem2(widgetName):
    
    elem = _dialog.findChild(QComboBox, widgetName)
    if not elem.currentText():
        elem_text = "null"
    else:
        elem_text = "'"+elem.currentText().replace("'", "''")+"'"
    return elem_text


def getFloat(widgetName):
    
    widget = _dialog.findChild(QLineEdit, widgetName)
    value = 0.0
    if widget:
        if widget.text():
            value = float(widget.text().replace(",", "."))
    return value


def setNumeric(widgetName, number):
    
    if not isNumber(number):
        setText(widgetName, number)
        return
    
    elem = _dialog.findChild(QLineEdit, widgetName)
    number = float(number)
    if elem:    
        if number <> '':
            value = format(number, '.2f')
            elem.setText(str(value))
        else:
            elem.setText(None)
    else:
        elem = _dialog.findChild(QTextEdit, widgetName)    
        if number <> '':
            value = format(number, '.2f')
            elem.setText(str(value))
        else:
            elem.setText(None)
            

def getText(widgetName):
    
    elem = _dialog.findChild(QLineEdit, widgetName)
    if elem:
        if (not elem.text() or elem.text().lower() == "null"):
            elem_text = None
        else:
            elem_text = elem.text()
    else:
        elem = _dialog.findChild(QTextEdit, widgetName)
        if elem:
            if (not elem.toPlainText() or elem.toPlainText().lower() == "null"):
                elem_text = None  
            else:
                elem_text = elem.toPlainText()
        else:
            elem_text = None
    return elem_text


def getDate(widgetName, fieldName):

    try:    
        date_widget = _dialog.findChild(QDateEdit, widgetName)
        if not date_widget:
            return
        
        dateAux = date_widget.date()
        aux = dateAux.toString("yyyy-MM-dd") 
        if aux:   
            value = aux
            text = fieldName+"='"+value+"'"  
        else:
            value = "null"
            text = fieldName+"=null"
    except (TypeError, ValueError):
        value = "null"
        text = "" 
        
    return dict(value = value, text = text)


def isNull(widgetName):
    
    elem = _dialog.findChild(QLineEdit, widgetName)
    empty = True
    if elem:
        if elem.text():
            empty = False
    return empty


def isNumber(elem):
    
    try:
        float(elem)
        return True
    except (TypeError, ValueError):
        return False


def isChecked(widgetName):
    
    widget = _dialog.findChild(QCheckBox, widgetName)
    value = False
    if widget:    
        value = widget.isChecked()
    return value


def setChecked(widgetName, value):
    
    elem = _dialog.findChild(QCheckBox, widgetName)
    if elem:    
        elem.setChecked(value)
            

def setText(widgetName, text):
    
    elem = _dialog.findChild(QLineEdit, widgetName)
    if elem:    
        elem.setText(str(text))
    else:
        elem = _dialog.findChild(QTextEdit, widgetName)    
        if elem:    
            elem.setText(str(text))
        else:
            elem = _dialog.findChild(QLabel, widgetName)    
            if elem:    
                elem.setText(str(text))            
          
          
def setDate(widgetName, value):
    
    elem = _dialog.findChild(QDateEdit, widgetName)
    if elem:    
        elem.setDate(value)
    else:
        elem = _dialog.findChild(QDateTimeEdit, widgetName)    
        if elem:    
            elem.setDate(value)

            
def setVisible(widgetName, isVisible):

    elem = _dialog.findChild(QWidget, widgetName)
    if elem:    
        elem.setVisible(isVisible)


# User interaction functions
def showInfo(text, duration = None):
    
    if duration is None:
        iface.messageBar().pushMessage("", text, QgsMessageBar.INFO, 5)  
    else:
        iface.messageBar().pushMessage("", text, QgsMessageBar.INFO, duration)
    
      
def showWarning(text, duration = None):
    
    if duration is None:
        iface.messageBar().pushMessage("", text, QgsMessageBar.WARNING, 5)
    else:
        iface.messageBar().pushMessage("", text, QgsMessageBar.WARNING, duration)


def askQuestion(text, infText = None):

    msgBox = QMessageBox()
    msgBox.setText(text);
    if infText is not None:
        msgBox.setInformativeText(infText);
    msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msgBox.setDefaultButton(QMessageBox.No)
    return msgBox.exec_()  
    

def setLogger(name, folder, filename):
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # create file handler
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = folder + "/" + filename 
    fh = logging.FileHandler(filepath)
    fh.setLevel(logging.INFO)
    
    # create console handler
    #ch = logging.StreamHandler()
    #ch.setLevel(logging.INFO)
    
    # create formatter and add it to the handlers
    formatter_fh = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #formatter_ch = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter_fh)
    #ch.setFormatter(formatter_ch)
    
    # add the handlers to logger
    if (len(logger.handlers) > 0):  
        removeHandlers(logger) 
    logger.addHandler(fh)
    #logger.addHandler(ch)   
    
    return logger

    
def removeHandlers(logger):    
    
    #logger.info('Total: %d'%len(logger.handlers))    
    for h in logger.handlers:
        #logger.info('removing handler %s'%str(h))
        logger.removeHandler(h)     
        
        
