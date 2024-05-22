import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, \
    QMessageBox


class AddressClient(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('REST Client')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.inputField = QLineEdit(self)
        self.inputField.setPlaceholderText('Enter URL')
        layout.addWidget(self.inputField)

        self.fetchButton = QPushButton('Fetch', self)
        self.fetchButton.clicked.connect(self.fetchAddress)
        layout.addWidget(self.fetchButton)

        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Number', 'Street', 'Postcode', 'City'])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def fetchAddress(self):
        address_id = self.inputField.text()
        if address_id.isdigit() or True:
            url = address_id
            response = requests.get(url)
            if response.status_code == 200:
                address = response.json()
                self.displayAddress(address)
            else:
                QMessageBox.critical(self, 'Error', f'Error fetching: {response.status_code}')
        else:
            QMessageBox.warning(self, 'Invalid Input', 'Please enter a valid url.')

    def displayAddress(self, address):
        if type(address) is type(dict()):
            _address = address
            address = [_address]
        self.table.setRowCount(len(address))
        for i in range(len(address)):
            self.table.setItem(i, 0, QTableWidgetItem(str(address[i]['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(address[i]['number'])))
            self.table.setItem(i, 2, QTableWidgetItem(address[i]['street']))
            self.table.setItem(i, 3, QTableWidgetItem(address[i]['postcode']))
            self.table.setItem(i, 4, QTableWidgetItem(address[i]['city']['name']))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = AddressClient()
    client.show()
    sys.exit(app.exec_())
