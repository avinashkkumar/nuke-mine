from PyQt5 import QtCore, QtGui, QtWidgets
# impoirting the sys module to add the path to the parent module 
import sys
# this appends the path to the parent directory of the parent module and no the parent module is acessable 
sys.path.append("/mnt/d/Working/nuke-mine/src/")
from design_files.Login import Ui_Form
from design_files import Home_page

from Database.database_query import (
    search,
    query_list
)

class login_page(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(login_page,self).__init__(*args, **kwargs)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.Login.clicked.connect(lambda: self.get_user_pass())
    

    def verify_user(self,uname,passw):
        sql = "SELECT * FROM admin WHERE username='" + uname + "';" 
        user = search(sql)
        try:
            password = user.get("password")
            if passw == password:
                return 0
            else:
                return 1
        except:
            return 2
        
    def change_screen(self):
        widget = self.nativeParentWidget()
        widget.setCurrentIndex(5)
        print(widget.currentIndex())
        

    def get_user_pass(self):
        uname = self.ui.UserName.text()
        passw = self.ui.Password.text()
        x = self.verify_user(uname, passw)
        if x == 0:
            print("you have logged in ")
            self.change_screen()
            
        elif(x == 1):
            print("incorrect password")
        elif(x == 2):
            print("user not found")