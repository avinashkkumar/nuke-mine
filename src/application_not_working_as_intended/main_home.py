from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.append("/mnt/d/Working/nuke-mine/src/")
from application.design_files.Home_page import Ui_Form

from application.Database.database_query import (
    search,
    query_list
)

class home_page(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(home_page,self).__init__(*args, **kwargs)
        self.ui = Ui_Form()
        self.ui.setupUi(self)