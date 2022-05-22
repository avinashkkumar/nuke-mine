import sys 
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStyleFactory
from Database.database_query import (
    query_list,
    search,
    create,
    get_id,
)
from copy import deepcopy
from fpdf import FPDF, HTMLMixin
import os, webbrowser,json
from datetime import datetime

# ***********************************************************************
# some pdf class 
class PDF(FPDF, HTMLMixin):
    pass







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
        self.order.clicked.connect(lambda: self.connect_order_page())
        self.UserList.clicked.connect(lambda: self.connect_user_list())
        self.ItemList.clicked.connect(lambda: self.connect_Item_list())
        self.orderl.clicked.connect(lambda: self.orderList())

    def connect_add_user(self):
        widget.setCurrentIndex(2)
        
        user.firstname.setText("")
        user.lastname.setText("")
        user.phone.setText("")

    def connect_user_list(self):
        widget.setCurrentIndex(5)

    def connect_add_item(self):
        widget.setCurrentIndex(3)

    def connect_order_page(self):
        widget.setCurrentIndex(4)
    
    def connect_Item_list(self):
        widget.setCurrentIndex(6)

    def orderList(self):
        widget.setCurrentIndex(7)






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
        uid = get_id("cust")
        sql = "insert into cust values (" + str(uid) + "," + str(phone) + ",'" + first + "','" + last + "');"
        create(sql)
        self.connect_home()
        





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
        if price !="" and desc != "" and name != "":
            fid = get_id("food")
            sql = "insert into food values(" + str(fid) + ",'" + name + "','" + desc + "'," + str(price) + ");"
            create(sql)
            self.get_back_home()
            self.name.setText("")
            self.description.setText("")
            self.price.setValue(0)




class order_page(QDialog):
    def __init__(self):
        super(order_page, self).__init__()
        loadUi("design/order_page.ui",self)
        self.OrderList.setColumnWidth(0,350)
        self.OrderList.setColumnWidth(1,100)
        self.OrderList.setColumnWidth(2,100)
        self.OrderList.setColumnWidth(2,100)
        self.userDetail.clicked.connect(lambda: self.get_user())
        data = query_list("select * from food")
        data1 = []
        self.product_list(data)
        self.loadData(data1)
        self.CheckAvailablity.clicked.connect(lambda: self.check_available(data,data1))
        self.Cancel.clicked.connect(lambda: self.go_to_home())
        self.Order.clicked.connect(lambda: self.order_food(data1))
        self.TotalBill = 0
        self.Product.setDisabled(True)
        self.productQuantity.setDisabled(True)
        self.CheckAvailablity.setDisabled(True)
        
    

    def go_to_home(self):
        self.reset_ui()
        widget.setCurrentIndex(1)

    
    def check_available(self,data,data1):
        product = self.Product.currentData()
        y = None
        for x in data:
            if x["id"] == product:
                y = x
                y["quant"] = self.productQuantity.value()
                y["total"] = y["quant"] * x["price"]
                data1.append(deepcopy(y))
                self.loadData(data1)
                self.productQuantity.setValue(0)
            tot = self.calc_total(data1)
            self.finalTotal.setText("Total is : " + str(tot))

    def loadData(self,data):
        row = 0
        self.OrderList.setRowCount(len(data))
        for x in data:
            self.OrderList.setItem(row,0,QtWidgets.QTableWidgetItem(str(x["name"])))
            self.OrderList.setItem(row,1,QtWidgets.QTableWidgetItem(str(x["quant"])))
            self.OrderList.setItem(row,2,QtWidgets.QTableWidgetItem(str(x["price"])))
            self.OrderList.setItem(row,3,QtWidgets.QTableWidgetItem(str(x["total"])))
            row += 1
    


    def product_list(self,data):
        row = 0
        for x in data:
            self.Product.addItem(x["name"], x["id"])



    def get_user(self):
        phone = self.PhoneNo.text()
        sql = "select * from cust where phone=" + str(phone) + ";"
        res = search(sql)
        if bool(res):
            self.UserName.setText("User : " + res["f_name"] + " " + res["l_name"])
            self.Product.setDisabled(False)
            self.productQuantity.setDisabled(False)
            self.CheckAvailablity.setDisabled(False)
            self.PhoneNo.setDisabled(True)
            self.userDetail.setDisabled(True)
        else:
            self.UserName.setText("User Not Found")
    
    def calc_total(self,data):
        total = 0
        for x in data:
            total += int(x["total"])
        return total


    def order_food(self,dataa):
        phone = self.PhoneNo.text()
        sql = "select * from cust where phone=" + str(phone) + ";"
        res = search(sql)
        orid = get_id("ord")
        data = []
        sql = "insert into ord values(" + str(orid) + "," + str(self.calc_total(dataa)) + ",'" + str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")) + "'," +  str(res["id"]) + ");"
        create(sql)
        pdf = PDF()
        head = ["name","quant","price","total"]
        name = "avinash Kumar"
        total = self.calc_total(dataa)
        pdf.set_font_size(16)
        pdf.add_page()
        pdf.write_html(
            self.html_parse(head, dataa, name,total),
            table_line_separators=True
        )
        pdf.output(f'{orid}.pdf')
        webbrowser.open_new(f"{orid}.pdf")
        self.reset_ui()
        widget.setCurrentIndex(1)
    
    def html_parse(self,head,data,name, total):
        html = f''' 
        <center><h1>Culture Pune</h1></center>
        <span>Ordered by : {name}<span>
        <table border="1">
            <tr>
                <th width="50%">{head[0]}</th>
                <th width="15%">{head[1]}</th>
                <th width="15%">{head[2]}</th>
                <th width="20%">{head[3]}</th>
            </tr> '''

        for x in range(len(data)):
            inhtml = f'''
                <tr>
                    <td>{data[x]["name"]}</td>
                    <td>{data[x]["quant"]}</td>
                    <td>{data[x]["price"]}</td>
                    <td>{data[x]["total"]}</td>
                </tr>
            '''
            html += inhtml
        html += "</table>"
        html += f"<span>The total of the bill is : {total}</span>"
        html += f"<br><br><center>Thank you visit again</center>"
        return html

    def reset_ui(self):
        self.PhoneNo.setEnabled(True)
        self.PhoneNo.setText("")
        self.UserName.setText("User : ")
        self.userDetail.setEnabled(True)
        self.TotalBill = 0
        self.Product.setDisabled(True)
        self.productQuantity.setDisabled(True)
        self.CheckAvailablity.setDisabled(True)
        data1 = []
        self.loadData(data1)
        data = query_list("select * from food")
        for x in data:
            self.Product.addItem(x["name"], x["id"])

class user_list(QDialog):
    def __init__(self):
        super(user_list, self).__init__()
        loadUi("design/user_list.ui",self)
        self.UserList.setColumnWidth(0,100)
        self.UserList.setColumnWidth(1,250)
        self.UserList.setColumnWidth(2,250)
        self.UserList.setColumnWidth(3,200)
        data = query_list("select * from cust;")
        self.loadData(data)
        self.Home.clicked.connect(lambda: self.get_back_home())

    def loadData(self,data):
        row = 0
        self.UserList.setRowCount(len(data))
        for x in data:
            self.UserList.setItem(row,0,QtWidgets.QTableWidgetItem(str(x["id"])))
            self.UserList.setItem(row,1,QtWidgets.QTableWidgetItem(str(x["f_name"])))
            self.UserList.setItem(row,2,QtWidgets.QTableWidgetItem(str(x["l_name"])))
            self.UserList.setItem(row,3,QtWidgets.QTableWidgetItem(str(x["phone"])))
            row += 1
    
    def get_back_home(self):
        widget.setCurrentIndex(1)


class ItemList(QDialog):
    def __init__(self):
        super(ItemList, self).__init__()
        loadUi("design/item_list.ui",self)
        self.items.setColumnWidth(0,100)
        self.items.setColumnWidth(1,450)
        self.items.setColumnWidth(2,250)
        data = query_list("select * from food;")
        self.loadData(data)
        self.Home.clicked.connect(lambda: self.get_back_home())

    def loadData(self,data):
        row = 0
        self.items.setRowCount(len(data))
        for x in data:
            self.items.setItem(row,0,QtWidgets.QTableWidgetItem(str(x["id"])))
            self.items.setItem(row,1,QtWidgets.QTableWidgetItem(str(x["name"])))
            self.items.setItem(row,2,QtWidgets.QTableWidgetItem(str(x["price"])))
            row += 1
    
    def get_back_home(self):
        widget.setCurrentIndex(1)



class OrderList(QDialog):
    def __init__(self):
        super(OrderList, self).__init__()
        loadUi("design/order_list.ui",self)
        self.orl.setColumnWidth(0,100)
        self.orl.setColumnWidth(1,225)
        self.orl.setColumnWidth(2,225)
        self.orl.setColumnWidth(3,225)
        data = query_list("select * from ord;")
        self.loadData(data)
        self.Home.clicked.connect(lambda: self.get_back_home())

    def loadData(self,data):
        row = 0
        self.orl.setRowCount(len(data))
        for x in data:
            self.orl.setItem(row,0,QtWidgets.QTableWidgetItem(str(x["id"])))
            cust = search("select * from cust where id=" + str(x["ucust"]))
            self.orl.setItem(row,1,QtWidgets.QTableWidgetItem(cust["f_name"] + " " + cust["l_name"]))
            self.orl.setItem(row,2,QtWidgets.QTableWidgetItem(str(x["dt"])))
            self.orl.setItem(row,3,QtWidgets.QTableWidgetItem(str(x["total"])))
            row += 1
    
    def get_back_home(self):
        widget.setCurrentIndex(1)

        


# declaring the main application and main event loop here
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
login = login_page()
home = home_page()
user = add_user()
item = add_item_page()
order = order_page()
ul = user_list()
il = ItemList()
ol = OrderList()
widget.setMinimumHeight(500)
widget.setMinimumWidth(800)
widget.addWidget(login)
widget.addWidget(home)
widget.addWidget(user)
widget.addWidget(item)
widget.addWidget(order)
widget.addWidget(ul)
widget.addWidget(il)
widget.addWidget(ol)
widget.show()
app.exec_()
