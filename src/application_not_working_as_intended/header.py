import sys
from PyQt5 import (
    QtCore,
    QtGui,
    QtWidgets,
)

from Database.database_query import (
    search,
    query_list,
)

from main_login import login_page
from main_home import home_page


    


app = QtWidgets.QApplication(sys.argv)
if app is not None:
    widget = QtWidgets.QStackedWidget()
    login = login_page()
    home = home_page()
    widget.addWidget(login)
    widget.setMinimumWidth(900)
    widget.setMinimumHeight(500)
    widget.show()
    app.exec_()