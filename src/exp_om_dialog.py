# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from ui_exp_om import Ui_Dialog


class ExpOmDialog(QtGui.QDialog):
    
    def __init__(self):
        
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        #self.setupUi(self)
        
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()   
        self.ui.setupUi(self) 
