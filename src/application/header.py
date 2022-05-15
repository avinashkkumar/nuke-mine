import sys 
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from Database.database_query import (
    query_list,
    search,
    create,
)




# ***********************************************************************
# declaring the login page of the application
class login_page(QDialog):
    def __init__(self):
        super(login_page, self).__init__()
        loadUi("design/Login.ui",self)
        self.Login.clicked.connect(lambda: self.get_user_pass())



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



    def get_user_pass(self):
        uname = self.UserName.text()
        passw = self.Password.text()
        x = self.verify_user(uname, passw)
        if x == 0:
            print("you have logged in ")
            widget.setCurrentIndex(1)
            
        elif(x == 1):
            print("incorrect password")
        elif(x == 2):
            print("user not found")





# ***********************************************************************
# decleraing the home page the application 
class home_page(QDialog):
    def __init__(self):
        super(home_page, self).__init__()
        loadUi("design/Home_page.ui",self)
        self.add_user.clicked.connect(lambda: self.connect_add_user())
        self.add_items.clicked.connect(lambda: self.connect_add_item())

    def connect_add_user(self):
        widget.setCurrentIndex(2)
        
        user.firstname.setText("")
        user.lastname.setText("")
        user.phone.setText("")

    def connect_add_item(self):
        widget.setCurrentIndex(3)






# ***********************************************************************
# decleraing the add user page of the application
class add_user(QDialog):
    def __init__(self):
        super(add_user, self).__init__()
        loadUi("design/Add_user.ui",self)
        self.cancel.clicked.connect(lambda: self.connect_home())
        self.register.clicked.connect(lambda: self.create_user())
        self.firstname.setText("")
        self.lastname.setText("")
        self.phone.setText("")
    
    def connect_home(self):
        widget.setCurrentIndex(1)

    def create_user(self):
        first = self.firstname.text()
        last = self.lastname.text()
        phone = self.phone.text()
        print(first,last,phone)
        





# ***********************************************************************
# decleraing the add item page of the application
class add_item_page(QDialog):
    def __init__(self):
        super(add_item_page,self).__init__()
        loadUi("design/Add_Item.ui",self)
        self.cancel.clicked.connect(lambda: self.get_back_home())
        self.addInventory.clicked.connect(lambda: self.save_item())


    def get_back_home(self):
        widget.setCurrentIndex(1)

    def save_item(self):
        name = self.name.text()
        desc = self.description.toPlainText()
        price = self.price.value()
        print(name,desc,price)




# declaring the main application and main event loop here
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
login = login_page()
home = home_page()
user = add_user()
item = add_item_page()
widget.setMinimumHeight(500)
widget.setMinimumWidth(800)
widget.addWidget(login)
widget.addWidget(home)
widget.addWidget(user)
widget.addWidget(item)
widget.setCurrentIndex(3)
widget.show()
app.exec_()
