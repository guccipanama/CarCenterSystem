import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, \
    QTableWidgetItem, QMessageBox, QComboBox, QGroupBox, QFormLayout, QAbstractScrollArea, QDialog, QLabel
from PyQt5.QtCore import Qt
import urllib3
import time
import re
import json

address = "https://localhost"
port = 8443


class LoginAttemptTracker:
    def __init__(self, max_attempts=3, lock_time=60):
        self.max_attempts = max_attempts
        self.lock_time = lock_time
        self.attempts = 0
        self.locked_until = None

    def reset(self):
        self.attempts = 0
        self.locked_until = None

    def is_locked(self):
        if self.locked_until and time.time() < self.locked_until:
            return True
        return False

    def register_failed_attempt(self):
        self.attempts += 1
        if self.attempts >= self.max_attempts:
            self.locked_until = time.time() + self.lock_time

    def can_attempt(self):
        if self.is_locked():
            return False
        return True


class Validator:
    def __init__(self):
        pass

    def isValidCars(self, carId, carName, carCost, centerId):
        carIdRegex = r'[0-9]+'
        carNameRegex = r'([A-Za-z0-9]+( [A-Za-z0-9]+)+)'
        carCostRegex = r'[0-9]+'
        centerIdRegex = r'[0-9]+'
        if re.match(carIdRegex, carId) is None:
            return False
        if re.match(carNameRegex, carName) is None:
            return False
        if re.match(carCostRegex, carCost) is None:
            return False
        if re.match(centerIdRegex, centerId) is None:
            return False
        return True

    def isValidCenter(self, centerId, centerAddress, centerCity):
        centerIdRegex = r'[0-9]+'
        centerAddressRegex = r'([ул.а-яА-я]+([, 0-9]+)+)'
        centerCityRegex = r'([г. а-яА-я]+([-а-яА-я])+)'
        if re.match(centerIdRegex, centerId) is None:
            return False
        if re.match(centerAddressRegex, centerAddress) is None:
            return False
        if re.match(centerCityRegex, centerCity) is None:
            return False
        return True

    def isValidCustomers(self, customerId, customerName, customerBirthdate, customerPassport):
        customerIdRegex = r'[0-9]+'
        customerNameRegex = r'([а-яА-я]+[ а-яА-я]+[а-яА-я])+'
        customerBirthdateRegex = r'([0-9]+[-0-9]+)+'
        customerPassportRegex = r'[0-9]+'
        if re.match(customerIdRegex, customerId) is None:
            return False
        if re.match(customerNameRegex, customerName) is None:
            return False
        if re.match(customerBirthdateRegex, customerBirthdate) is None:
            return False
        if re.match(customerPassportRegex, customerPassport) is None:
            return False
        return True

    def isValidOrders(self, orderId, orderDate, carId, customerId):
        orderIdRegex = r'[0-9]+'
        orderDateRegex = r'([0-9]+[-0-9]+)+'
        carIdRegex = r'[0-9]'
        customerIdRegex = r'[0-9]'
        if re.match(orderIdRegex, orderId) is None:
            return False
        if re.match(orderDateRegex, orderDate) is None:
            return False
        if re.match(carIdRegex, carId) is None:
            return False
        if re.match(customerIdRegex, customerId) is None:
            return False
        return True


class Login(QDialog):
    def __init__(self, session, parent=None):
        super(Login, self).__init__(parent)
        self.setWindowTitle('Login')
        self.session = session
        self.tracker = LoginAttemptTracker(max_attempts=3, lock_time=60)
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.textPass.setEchoMode(QLineEdit.Password)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        if self.tracker.can_attempt():
            self.session.auth = (self.textName.text(), self.textPass.text())
            auth = self.session.post(address + ":" + str(port), verify=False)

            if auth.status_code == 401:
                self.tracker.register_failed_attempt()
                QMessageBox.warning(self, 'Error', 'Bad user or password')
            else:
                print(self.session)
                self.tracker.reset()
                self.accept()
        else:
            QMessageBox.warning(self, 'You are locked out',
                                f"Please try again after {int(self.tracker.locked_until - time.time())} seconds.")


class InsertCarDialog(QDialog):
    def __init__(self, session, parent=None):
        super(InsertCarDialog, self).__init__(parent)
        self.setWindowTitle('Insert')
        self.setGeometry(150, 150, 400, 200)
        self.session = session

        layout = QVBoxLayout(self)
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(layout4)

        self.carIdLabel = QLabel('carId', self)
        self.carIdLabel.setFixedWidth(50)
        self.carId = QLineEdit(self)
        layout1.addWidget(self.carIdLabel)
        layout1.addWidget(self.carId)

        self.carNameLabel = QLabel('carName', self)
        self.carNameLabel.setFixedWidth(50)
        self.carName = QLineEdit(self)
        layout2.addWidget(self.carNameLabel)
        layout2.addWidget(self.carName)

        self.carCostLabel = QLabel('carCost', self)
        self.carCostLabel.setFixedWidth(50)
        self.carCost = QLineEdit(self)
        layout3.addWidget(self.carCostLabel)
        layout3.addWidget(self.carCost)

        self.centerLabel = QLabel('centerId', self)
        self.centerLabel.setFixedWidth(50)
        self.center = QLineEdit(self)
        layout4.addWidget(self.centerLabel)
        layout4.addWidget(self.center)

        self.buttonInsert = QPushButton('Insert', self)
        self.buttonInsert.clicked.connect(self.handleInsert)
        layout.addWidget(self.buttonInsert)

        self.setLayout(layout)

        address_id = address + ":" + str(port) + "/api/cars"
        response = self.session.get(address_id, verify=False)
        if response.status_code == 200:
            data = response.json()
            self.carId.setText(str(int(data[-1]['carId']) + 1))
            self.carName.setText(str(data[-1]['carName']))
            self.carCost.setText(str(data[-1]['carCost']))
            self.center.setText(str(data[-1]['center']["centerId"]))
        elif response.status_code == 403:
            self.accept()
            QMessageBox.critical(self, 'Error', 'You have no permission to perform that operation')

    def handleInsert(self):
        validator = Validator()
        check = validator.isValidCars(self.carId.text(), self.carName.text(), self.carCost.text(), self.center.text())
        if not check:
            QMessageBox.critical(self, 'Error', 'Enter correct data')
        else:
            address_id = address + ":" + str(port) + "/add/car"
            arguments = {'carId': self.carId.text(),
                         'carName': self.carName.text(),
                         'carCost': self.carCost.text(),
                         'center': {
                             'centerId': self.center.text()
                            }
                         }
            arguments = json.dumps(arguments)
            headers = {'Content-type': 'application/json'}
            response = self.session.post(address_id, data=arguments, headers=headers, verify=False)
            if response.status_code == 200:
                QMessageBox.information(self, "Success!", "Success!")
            else:
                QMessageBox.critical(self, 'Error', 'You have no permission to perform that operation')
            self.accept()


class InsertCenterDialog(QDialog):
    def __init__(self, session, parent=None):
        super(InsertCenterDialog, self).__init__(parent)
        self.setWindowTitle('Insert')
        self.setGeometry(150, 150, 400, 150)
        self.session = session

        layout = QVBoxLayout(self)
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)

        self.centerIdLabel = QLabel('centerId', self)
        self.centerIdLabel.setFixedWidth(50)
        self.centerId = QLineEdit(self)
        layout1.addWidget(self.centerIdLabel)
        layout1.addWidget(self.centerId)

        self.centerAddressLabel = QLabel('centerAddress', self)
        self.centerAddressLabel.setFixedWidth(50)
        self.centerAddress = QLineEdit(self)
        layout2.addWidget(self.centerAddressLabel)
        layout2.addWidget(self.centerAddress)

        self.centerCityLabel = QLabel('centerCity', self)
        self.centerCityLabel.setFixedWidth(50)
        self.centerCity = QLineEdit(self)
        layout3.addWidget(self.centerCityLabel)
        layout3.addWidget(self.centerCity)

        self.buttonInsert = QPushButton('Insert', self)
        self.buttonInsert.clicked.connect(self.handleInsert)
        layout.addWidget(self.buttonInsert)

        self.setLayout(layout)

        address_id = address + ":" + str(port) + "/api/centers"
        response = self.session.get(address_id, verify=False)
        if response.status_code == 200:
            data = response.json()
            self.centerId.setText(str(int(data[-1]['centerId']) + 1))
            self.centerAddress.setText(str(data[-1]['centerAddress']))
            self.centerCity.setText(str(data[-1]['centerCity']))
        elif response.status_code == 403:
            QMessageBox.critical(self, 'Error', 'You have no permission to perform that operation')
            self.accept()

    def handleInsert(self):
        validator = Validator()
        check = validator.isValidCenter(self.centerId.text(), self.centerAddress.text(), self.centerCity.text())
        if not check:
            QMessageBox.critical(self, 'Error', 'Enter correct data')
        else:
            address_id = address + ":" + str(port) + "/add/center"
            arguments = {'centerId': self.centerId.text(),
                         'centerAddress': self.centerAddress.text(),
                         'centerCity': self.centerCity.text()}
            arguments = json.dumps(arguments)
            headers = {'Content-type': 'application/json'}
            response = self.session.post(address_id, data=arguments, headers=headers, verify=False)
            if response.status_code == 200:
                QMessageBox.information(self, "Success!", "Success!")
            else:
                QMessageBox.critical(self, 'Error', 'You have no permission to perform that operation')
            self.accept()


class InsertCustomerDialog(QDialog):
    def __init__(self, session, parent=None):
        super(InsertCustomerDialog, self).__init__(parent)
        self.setWindowTitle('Insert')
        self.setGeometry(150, 150, 400, 200)
        self.session = session

        layout = QVBoxLayout(self)
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(layout4)

        self.customerIdLabel = QLabel('customerId', self)
        self.customerIdLabel.setFixedWidth(90)
        self.customerId = QLineEdit(self)
        layout1.addWidget(self.customerIdLabel)
        layout1.addWidget(self.customerId)

        self.customerNameLabel = QLabel('customerName', self)
        self.customerNameLabel.setFixedWidth(90)
        self.customerName = QLineEdit(self)
        layout2.addWidget(self.customerNameLabel)
        layout2.addWidget(self.customerName)

        self.customerBirthdateLabel = QLabel('customerBirthdate', self)
        self.customerBirthdateLabel.setFixedWidth(90)
        self.customerBirthdate = QLineEdit(self)
        layout3.addWidget(self.customerBirthdateLabel)
        layout3.addWidget(self.customerBirthdate)

        self.customerPassportLabel = QLabel('customerPassport', self)
        self.customerPassportLabel.setFixedWidth(90)
        self.customerPassport = QLineEdit(self)
        layout4.addWidget(self.customerPassportLabel)
        layout4.addWidget(self.customerPassport)

        self.buttonInsert = QPushButton('Insert', self)
        self.buttonInsert.clicked.connect(self.handleInsert)
        layout.addWidget(self.buttonInsert)

        self.setLayout(layout)

        address_id = address + ":" + str(port) + "/api/customers"
        response = self.session.get(address_id, verify=False)
        if response.status_code == 200:
            data = response.json()
            self.customerId.setText(str(int(data[-1]['customerId']) + 1))
            self.customerName.setText(str(data[-1]['customerName']))
            self.customerBirthdate.setText(str(data[-1]['customerBirthdate']))
            self.customerPassport.setText(str(data[-1]['customerPassport']))

        elif response.status_code == 403:
            QMessageBox.critical(self, 'Error', 'You have no permission to perform that operation')

    def handleInsert(self):
        validator = Validator()
        check = validator.isValidCustomers(self.customerId.text(), self.customerName.text(),
                                           self.customerBirthdate.text(), self.customerPassport.text())
        if not check:
            QMessageBox.critical(self, 'Error', 'Enter correct data')
        else:
            address_id = address + ":" + str(port) + "/add/customer"
            arguments = {'customerId': self.customerId.text(),
                         'customerName': self.customerName.text(),
                         'customerBirthdate': self.customerBirthdate.text(),
                         'customerPassport': self.customerPassport.text()}
            arguments = json.dumps(arguments)
            headers = {'Content-type': 'application/json'}
            response = self.session.post(address_id, data=arguments, headers=headers, verify=False)
            if response.status_code == 200:
                QMessageBox.information(self, "Success!", "Success!")
            else:
                QMessageBox.critical(self, 'Error', 'You have no permission to perform that operation')
            self.accept()


class InsertOrderDialog(QDialog):
    def __init__(self, session, parent=None):
        super(InsertOrderDialog, self).__init__(parent)
        self.setWindowTitle('Insert')
        self.setGeometry(150, 150, 400, 200)
        self.session = session

        layout = QVBoxLayout(self)
        layout1 = QHBoxLayout(self)
        layout2 = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)
        layout4 = QHBoxLayout(self)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(layout4)

        self.orderIdLabel = QLabel('orderId', self)
        self.orderIdLabel.setFixedWidth(55)
        self.orderId = QLineEdit(self)
        layout1.addWidget(self.orderIdLabel)
        layout1.addWidget(self.orderId)

        self.orderDateLabel = QLabel('orderDate', self)
        self.orderDateLabel.setFixedWidth(55)
        self.orderDate = QLineEdit(self)
        layout2.addWidget(self.orderDateLabel)
        layout2.addWidget(self.orderDate)

        self.carLabel = QLabel('carId', self)
        self.carLabel.setFixedWidth(55)
        self.car = QLineEdit(self)
        layout3.addWidget(self.carLabel)
        layout3.addWidget(self.car)

        self.customerLabel = QLabel('customerId', self)
        self.customerLabel.setFixedWidth(55)
        self.customer = QLineEdit(self)
        layout4.addWidget(self.customerLabel)
        layout4.addWidget(self.customer)

        self.buttonInsert = QPushButton('Insert', self)
        self.buttonInsert.clicked.connect(self.handleInsert)
        layout.addWidget(self.buttonInsert)

        address_id = address + ":" + str(port) + "/api/orders"
        response = self.session.get(address_id, verify=False)
        if response.status_code == 200:
            data = response.json()
            self.orderId.setText(str(int(data[-1]['orderId']) + 1))
            self.orderDate.setText(str(data[-1]['orderDate']))
            self.car.setText(str(data[-1]['car']['carId']))
            self.customer.setText(str(data[-1]['customer']['customerId']))
        elif response.status_code == 403:
            QMessageBox.critical(self, 'Error', 'You have no permission to perform that operation')
            self.accept()

    def handleInsert(self):
        validator = Validator()
        check = validator.isValidOrders(self.orderId.text(), self.orderDate.text(), self.car.text(),
                                        self.customer.text())
        if not check:
            QMessageBox.critical(self, 'Error', 'Enter correct data')
        else:
            address_id = address + ":" + str(port) + "/add/customer"
            arguments = {'orderId': self.orderId.text(),
                         'orderDate': self.orderDate.text(),
                         'car': {
                             'carId': self.car.text()
                            },
                         'customer': {
                             'customerId': self.customer.text()
                            }
                         }
            arguments = json.dumps(arguments)
            headers = {'Content-type': 'application/json'}
            response = self.session.post(address_id, data=arguments, headers=headers, verify=False)
            if response.status_code == 200:
                QMessageBox.information(self, "Success!", "Success!")
            else:
                QMessageBox.critical(self, 'Error', 'You have no permission to perform that operation')
            self.accept()



class AddressClient(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)
        self.session = requests.Session()
        login = Login(self.session)
        if login.exec_() == QDialog.Accepted:
            self.setWindowTitle('Car Center System')
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

        self.idInputField = QLineEdit()
        self.idInputField.setPlaceholderText('')

        layout.addRow(self.idInputField, self.comboBox)

        self.topLayout.setLayout(layout)

    def createBottomLayout(self):

        self.bottomLayout = QGroupBox("Output")
        layout = QHBoxLayout()

        self.table = QTableWidget(self)
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
                insert = InsertCarDialog(self.session)
            case "Center":
                insert = InsertCenterDialog(self.session)
            case "Customer":
                insert = InsertCustomerDialog(self.session)
            case "Orders":
                insert = InsertOrderDialog(self.session)
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
        address_id = address + ":" + str(port) + get_request
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
                address_id = address + ":" + str(port) + delete_request
                delete_response = self.session.delete(address_id, verify=False)
                if delete_response.status_code == 200:
                    QMessageBox.information(self, "Success!", "Success!")
                    self.idInputField.setText("")
                else:
                    QMessageBox.critical(self, 'Error', 'You have no permission to perform that operation')
            else:
                QMessageBox.information(self, "Cancel!", "Cancel!")

    def select(self, request: str, displayFunc):
        address_id = address + ":" + str(port) + request
        if address_id.isdigit() or True:
            url = address_id
            response = self.session.get(url, verify=False)
            if response.status_code == 200:
                data = response.json()
                displayFunc(data)
            else:
                QMessageBox.critical(self, 'Error', 'You have no permission to perform that operation')
        else:
            QMessageBox.warning(self, 'Invalid Input', 'Please enter a valid url.')

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = AddressClient()
    client.show()
    sys.exit(app.exec_())
