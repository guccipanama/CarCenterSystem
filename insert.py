from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QDialog, QLabel
from PyQt5 import QtGui
import json
from validator import Validator


class InsertCarDialog(QDialog):
    def __init__(self, session, elem_id, parent=None):
        super(InsertCarDialog, self).__init__(parent)
        self.setWindowTitle('Insert')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setGeometry(150, 150, 400, 200)
        self.session = session
        self.elem_id = elem_id
        config = json.load(open(file="config.json", mode="r", encoding="UTF-8"))
        self.address, self.port = config["address"], config["port"]

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
        address_id = self.address + ":" + str(self.port) + "/api/cars"
        if elem_id != '':
            address_id += '/' + str(elem_id)
        response = self.session.get(address_id, verify=False)
        if response.status_code == 200:
            data = response.json()
            if elem_id == '':
                data = data[-1]
            self.carId.setText(str(int(data['carId'])))
            self.carName.setText(str(data['carName']))
            self.carCost.setText(str(data['carCost']))
            self.center.setText(str(data['center']["centerId"]))
        elif response.status_code == 403:
            self.accept()
            QMessageBox.critical(self, 'Error', 'You have no permission to perform that operation')

    def handleInsert(self):
        validator = Validator()
        check = validator.isValidCars(self.carId.text(), self.carName.text(), self.carCost.text(), self.center.text())
        if not check:
            QMessageBox.critical(self, 'Error', 'Enter correct data')
        else:
            address_id = self.address + ":" + str(self.port) + "/add/car"
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
    def __init__(self, session, elem_id, parent=None):
        super(InsertCenterDialog, self).__init__(parent)
        self.setWindowTitle('Insert')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setGeometry(150, 150, 400, 150)
        self.session = session
        self.elem_id = elem_id
        config = json.load(open(file="config.json", mode="r", encoding="UTF-8"))
        self.address, self.port = config["address"], config["port"]

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

        address_id = self.address + ":" + str(self.port) + "/api/centers"
        if elem_id != '':
            address_id += '/' + str(elem_id)
        response = self.session.get(address_id, verify=False)
        if response.status_code == 200:
            data = response.json()
            if elem_id == '':
                data = data[-1]
            self.centerId.setText(str(int(data['centerId'])))
            self.centerAddress.setText(str(data['centerAddress']))
            self.centerCity.setText(str(data['centerCity']))
        elif response.status_code == 403:
            QMessageBox.critical(self, 'Error', 'You have no permission to perform that operation')
            self.accept()

    def handleInsert(self):
        validator = Validator()
        check = validator.isValidCenter(self.centerId.text(), self.centerAddress.text(), self.centerCity.text())
        if not check:
            QMessageBox.critical(self, 'Error', 'Enter correct data')
        else:
            address_id = self.address + ":" + str(self.port) + "/add/center"
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
    def __init__(self, session, elem_id, parent=None):
        super(InsertCustomerDialog, self).__init__(parent)
        self.setWindowTitle('Insert')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setGeometry(150, 150, 400, 200)
        self.session = session
        self.elem_id = elem_id
        config = json.load(open(file="config.json", mode="r", encoding="UTF-8"))
        self.address, self.port = config["address"], config["port"]

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

        address_id = self.address + ":" + str(self.port) + "/api/customers"
        if elem_id != '':
            address_id += '/' + str(elem_id)
        response = self.session.get(address_id, verify=False)
        if response.status_code == 200:
            data = response.json()
            if elem_id == '':
                data = data[-1]
            self.customerId.setText(str(int(data['customerId'])))
            self.customerName.setText(str(data['customerName']))
            self.customerBirthdate.setText(str(data['customerBirthdate']))
            self.customerPassport.setText(str(data['customerPassport']))

        elif response.status_code == 403:
            QMessageBox.critical(self, 'Error', 'You have no permission to perform that operation')

    def handleInsert(self):
        validator = Validator()
        check = validator.isValidCustomers(self.customerId.text(), self.customerName.text(),
                                           self.customerBirthdate.text(), self.customerPassport.text())
        if not check:
            QMessageBox.critical(self, 'Error', 'Enter correct data')
        else:
            address_id = self.address + ":" + str(self.port) + "/add/customer"
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
    def __init__(self, session, elem_id, parent=None):
        super(InsertOrderDialog, self).__init__(parent)
        self.setWindowTitle('Insert')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setGeometry(150, 150, 400, 200)
        self.session = session
        self.elem_id = elem_id
        config = json.load(open(file="config.json", mode="r", encoding="UTF-8"))
        self.address, self.port = config["address"], config["port"]

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

        address_id = self.address + ":" + str(self.port) + "/api/orders"
        if elem_id != '':
            address_id += '/' + str(elem_id)
        response = self.session.get(address_id, verify=False)
        if response.status_code == 200:
            data = response.json()
            if elem_id == '':
                data = data[-1]
            self.orderId.setText(str(int(data['orderId'])))
            self.orderDate.setText(str(data['orderDate']))
            self.car.setText(str(data['car']['carId']))
            self.customer.setText(str(data['customer']['customerId']))
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
            address_id = self.address + ":" + str(self.port) + "/add/order"
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
            print(arguments)
            if response.status_code == 200:
                QMessageBox.information(self, "Success!", "Success!")
            else:
                QMessageBox.critical(self, 'Error', 'You have no permission to perform that operation')
            self.accept()