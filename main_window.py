from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, \
    QTableWidgetItem, QMessageBox, QComboBox, QGroupBox, QFormLayout, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import urllib3
import json
from insert import InsertCarDialog, InsertCenterDialog, InsertCustomerDialog, InsertOrderDialog


class MainWindow(QWidget):
    def __init__(self, session):
        super().__init__()
        self.initUI(session)

    def initUI(self, session):
        urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)
        self.session = session
        config = json.load(open(file="config.json", mode="r", encoding="UTF-8"))
        self.address, self.port = config["address"], config["port"]

        self.setWindowTitle('Car Center System')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setGeometry(100, 100, 600, 400)

        self.createTopLayout()
        self.createBottomLayout()

        mainLayout = QVBoxLayout()

        mainLayout.addWidget(self.topLayout)
        mainLayout.addWidget(self.bottomLayout)

        self.setLayout(mainLayout)

    def createTopLayout(self):
        self.topLayout = QGroupBox("Tables")
        layout = QFormLayout()

        self.comboBox = QComboBox()
        self.comboBox.addItems(["Car", "Center", "Customer", "Orders"])

        self.idInputField = QLineEdit(self)
        self.idInputField.setPlaceholderText('')

        layout.addRow(self.idInputField, self.comboBox)

        self.topLayout.setLayout(layout)

    def createBottomLayout(self):

        self.bottomLayout = QGroupBox("Output")
        layout = QHBoxLayout()

        self.table = QTableWidget(self)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.cellClicked.connect(self.onCellClicked)
        layout.addWidget(self.table)

        layout1 = QVBoxLayout()
        layout.addLayout(layout1)

        self.selectButton = QPushButton('Select', self)
        self.selectButton.setFixedHeight(20)
        self.selectButton.clicked.connect(self.decideSelectTable)
        layout1.addWidget(self.selectButton)

        self.insertButton = QPushButton('Insert', self)
        self.insertButton.setFixedHeight(20)
        self.insertButton.clicked.connect(self.decideInsertTable)
        layout1.addWidget(self.insertButton)

        self.deleteButton = QPushButton('Delete', self)
        self.deleteButton.setFixedHeight(20)
        self.deleteButton.clicked.connect(self.decideDeleteTable)
        layout1.addWidget(self.deleteButton)

        layout1.setAlignment(Qt.AlignTop)
        self.bottomLayout.setLayout(layout)

    def onCellClicked(self, row, column):
        elem = [self.table.item(row, j).text() for j in range(self.table.columnCount())]
        self.idInputField.setText(str(elem[0]))

    def decideSelectTable(self):
        match self.comboBox.currentText():
            case "Car":
                request = "/api/cars"
                if self.idInputField.text() != "":
                    request = request + "/" + self.idInputField.text()
                self.select(request, self.displayCars)
            case "Center":
                request = "/api/centers"
                if self.idInputField.text() != "":
                    request = request + "/" + self.idInputField.text()
                self.select(request, self.displayCenters)
            case "Customer":
                request = "/api/customers"
                if self.idInputField.text() != "":
                    request = request + "/" + self.idInputField.text()
                self.select(request, self.displayCustomers)
            case "Orders":
                request = "/api/orders"
                if self.idInputField.text() != "":
                    request = request + "/" + self.idInputField.text()
                self.select(request, self.displayOrders)

    def decideInsertTable(self):
        match self.comboBox.currentText():
            case "Car":
                insert = InsertCarDialog(self.session, self.idInputField.text())
            case "Center":
                insert = InsertCenterDialog(self.session, self.idInputField.text())
            case "Customer":
                insert = InsertCustomerDialog(self.session, self.idInputField.text())
            case "Orders":
                insert = InsertOrderDialog(self.session, self.idInputField.text())
        if not insert.exec():
            QMessageBox.information(self, "Cancel!", "Cancel!")

    def decideDeleteTable(self):
        if self.idInputField.text() == "":
            QMessageBox.warning(self, 'Error', 'Enter ID of an element to delete!')
        else:
            match self.comboBox.currentText():
                case "Car":
                    self.deleteWindow("/delete/car/" + self.idInputField.text(), "/api/cars/" + self.idInputField.text())
                case "Center":
                    self.deleteWindow("/delete/center/" + self.idInputField.text(), "/api/centers/" + self.idInputField.text())
                case "Customer":
                    self.deleteWindow("/delete/customer/" + self.idInputField.text(), "/api/customers/" + self.idInputField.text())
                case "Orders":
                    self.deleteWindow("/delete/order/" + self.idInputField.text(), "/api/orders/" + self.idInputField.text())

    def deleteWindow(self, delete_request, get_request):
        address_id = self.address + ":" + str(self.port) + get_request
        get_response = self.session.get(address_id, verify=False)
        print(get_response.status_code)
        if get_response.status_code == 403:
            QMessageBox.critical(self, 'Error', 'You have no permission to perform that operation')
        elif get_response.status_code == 500:
            QMessageBox.warning(self, 'Error', 'Haven\'t found an element with such an ID!')
        else:
            reply = QMessageBox.question(self, 'Warning',
                                         'Are you sure you want to delete the following item?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                address_id = self.address + ":" + str(self.port) + delete_request
                delete_response = self.session.delete(address_id, verify=False)
                if delete_response.status_code == 200:
                    QMessageBox.information(self, "Success!", "Success!")
                    self.idInputField.setText("")
                else:
                    QMessageBox.critical(self, 'Error', 'You have no permission to perform that operation')
            else:
                QMessageBox.information(self, "Cancel!", "Cancel!")

    def select(self, request: str, displayFunc):
        response = self.session.get(self.address + ":" + str(self.port) + request, verify=False)
        if response.status_code == 200:
            data = response.json()
            displayFunc(data)
        elif response.status_code == 500:
            QMessageBox.critical(self, 'Haven\'t found an element with such an ID!')
        else:
            QMessageBox.critical(self, 'Error', 'You have no permission to perform that operation')

    def displayCars(self, data):
        if type(data) is type(dict()):
            _data = data
            data = [_data]
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Cost', 'Center'])
        self.table.setRowCount(len(data))
        for i in range(len(data)):
            self.table.setItem(i, 0, QTableWidgetItem(str(data[i]['carId'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(data[i]['carName'])))
            self.table.setItem(i, 2, QTableWidgetItem(str(data[i]['carCost'])))
            self.table.setItem(i, 3, QTableWidgetItem(str(data[i]['center']["centerAddress"])))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def displayCenters(self, data):
        if type(data) is type(dict()):
            _data = data
            data = [_data]
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', 'Address', 'City'])
        self.table.setRowCount(len(data))
        for i in range(len(data)):
            self.table.setItem(i, 0, QTableWidgetItem(str(data[i]['centerId'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(data[i]['centerAddress'])))
            self.table.setItem(i, 2, QTableWidgetItem(str(data[i]['centerCity'])))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def displayCustomers(self, data):
        if type(data) is type(dict()):
            _data = data
            data = [_data]
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Birthdate', 'Passport'])
        self.table.setRowCount(len(data))
        for i in range(len(data)):
            self.table.setItem(i, 0, QTableWidgetItem(str(data[i]['customerId'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(data[i]['customerName'])))
            self.table.setItem(i, 2, QTableWidgetItem(str(data[i]['customerBirthdate'])))
            self.table.setItem(i, 3, QTableWidgetItem(str(data[i]['customerPassport'])))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def displayOrders(self, data):
        if type(data) is type(dict()):
            _data = data
            data = [_data]
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Date', 'Car', 'Center', 'Customer'])
        self.table.setRowCount(len(data))
        for i in range(len(data)):
            self.table.setItem(i, 0, QTableWidgetItem(str(data[i]['orderId'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(data[i]['orderDate'])))
            self.table.setItem(i, 2, QTableWidgetItem(str(data[i]['car']['carName'])))
            self.table.setItem(i, 3, QTableWidgetItem(str(data[i]['car']['center']['centerAddress'])))
            self.table.setItem(i, 4, QTableWidgetItem(str(data[i]['customer']['customerName'])))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def exit_app(self):
        QApplication.quit()