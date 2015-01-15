

def updateTotals():

    global row_total, row_cur
    row_cur = 0
    row_total = getTotal()    
    if (row_total > 0):
        row_cur = 1    
    enable_previous = (row_cur > 1)
    enable_next = (row_total > row_cur)      
    _dialog.findChild(QPushButton, "previous").setEnabled(enable_previous) 
    _dialog.findChild(QPushButton, "next").setEnabled(enable_next)     
    loadActivity()    
    

def previousRecord():

    global row_cur
    row_cur = row_cur - 1;        
    if (row_cur <= 1):
        _dialog.findChild(QPushButton, "previous").setEnabled(False)    
    _dialog.findChild(QPushButton, "next").setEnabled(True)        
    loadActivity()        


def nextRecord():

    global row_cur
    row_cur = row_cur + 1;    
    if (row_cur >= row_total):
        _dialog.findChild(QPushButton, "next").setEnabled(False)    
    _dialog.findChild(QPushButton, "previous").setEnabled(True)                
    loadActivity()        


def getTotal():

    #sql = "SELECT COUNT(*) FROM activitat WHERE emplacament_id = '"+id.text()+"'"    
    #cursor.execute(sql)
    #row = cursor.fetchone()    
    #row_total = row[0]
    row_total = 3
    return row_total    


# Load data related to current Activity from Database    
def loadActivity():

    global rows, iterator

    # Dades generals activitat
    sql = "SELECT id, nif, rao_social, nom_comercial, descripcio, nom_contacte, telefon, mail, superficie, actual"
    # Marc legal
    sql+= ", exp_relacionats, num_llicencia, data_llicencia, data_baixa, data_control_inicial, data_control_periodic, estat_legal_id, tipus_act_id, marc_legal_id, clas_legal_id, codi_legal, observacions_act, num_exp"    
    sql+= " FROM activitat WHERE emplacament_id = '"+id.text()+"' ORDER BY id DESC"
    sql+= " LIMIT 1 OFFSET "+str(row_cur-1)
    cursor.execute(sql)
    lblInfo.setText("Activitat "+str(row_cur)+" de "+str(row_total))    
    row = cursor.fetchone()        
    if row:    
        setWidgetsActivity(row)          


def setWidgetsActivity(row):

    setField(row, 0, "act_id")
    setField(row, 1, "nif")    
    setField(row, 2, "rao_social")
    setField(row, 3, "nom_comercial")
    setTextEdit(row, 4, "descripcio")
    setField(row, 5, "nom_contacte")
    setField(row, 6, "telefon")
    setField(row, 7, "mail")    
    setField(row, 8, "superficie")    
    #setField(row, 9, "actual")    
    setField(row, 10, "exp_relacionats")    
    #setField(row, 11, "num_llicencia")            
    setDate(row, 12, "data_llicencia")
    setDate(row, 13, "data_baixa")
    setDate(row, 14, "data_control_inicial")
    setDate(row, 15, "data_control_periodic")    
    setCombo(row, 16, "estat_legal_id")    
    setCombo(row, 17, "tipus_act_id")
    setCombo(row, 18, "marc_legal_id")
    setCombo(row, 19, "clas_legal_id")
    setField(row, 20, "codi_legal")
    setTextEdit(row, 21, "observacions_act")
    setField(row, 22, "num_exp")        

    chk_actual = _dialog.findChild(QCheckBox, "actual")    
    if row[9]==-1:
        chk_actual.setChecked(True);
    else:
        chk_actual.setChecked(False);    


def setTextEdit(row, index, field):
    
    aux = _dialog.findChild(QTextEdit, field)   
    if not aux:
        print "field not found: " + field    
        return    
    value = unicode(row[index])
    if value == 'None':    
        aux.setText("")         
    else:
        aux.setText(value)         


def setField(row, index, field):
    
    aux = _dialog.findChild(QLineEdit, field)   
    if not aux:
        print "field not found: " + field    
        return    
    value = unicode(row[index])
    if value == 'None':    
        aux.setText("")         
    else:
        aux.setText(value)             


def setCombo(row, index, field):
    
    aux = _dialog.findChild(QComboBox, field)   
    if not aux:
        print "combo not found: " + field    
        return    
    index = aux.findText(row[index])        
    aux.setCurrentIndex(index);        


def setDate(row, index, field):
    
    aux = _dialog.findChild(QLineEdit, field)   
    if not aux:
        print "date not found: " + field    
        return     
    value = unicode(row[index])    
    #print field + ": " + value      
    if value != 'null' and value != 'None' and value != '1900-01-01':   
        date_aux = datetime.strptime(row[index], "%Y-%m-%d")
        date_text = date_aux.strftime("%d/%m/%Y")
    else:
        date_text = ""                         
    aux.setText(date_text);    
    
    
def createActivity():

    lblInfo.setText("Creant expedient...")    
    #sql = "SELECT 1 + (SELECT id FROM activitat ORDER BY id DESC LIMIT 1)"
    #cursor.execute(sql)
    #row = cursor.fetchone()        
    #_dialog.findChild(QLineEdit, "act_id").setText(str(row[0]))


# Delete current activity
def deleteActivity():

    act_id = _dialog.findChild(QLineEdit, "act_id")    
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Eliminar activitat")    
    msgBox.setText(u"Està segur que desitja esborrar aquesta activitat?")
    msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msgBox.setDefaultButton(QMessageBox.Yes)
    resp = msgBox.exec_()
    if (resp == QMessageBox.Yes):
        sql = "DELETE FROM activitat WHERE id = "+act_id.text()    
        cursor.execute(sql)            
        conn.commit()        
        updateTotals()    


 