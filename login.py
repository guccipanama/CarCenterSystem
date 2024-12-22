import requests
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QDialog
from PyQt5 import QtGui
import time
import json
from login_attempt_tracker import LoginAttemptTracker
from main_window import MainWindow


class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setWindowTitle('Login')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
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
        print("1")
        if self.tracker.can_attempt():
            config = json.load(open(file="config.json", mode="r", encoding="UTF-8"))
            address, port = config["address"], config["port"]

            self.session = requests.Session()
            self.session.auth = (self.textName.text(), self.textPass.text())
            auth = self.session.post(address + ":" + str(port), verify=False)

            if auth.status_code == 401:
                self.tracker.register_failed_attempt()
                QMessageBox.warning(self, 'Error', 'Bad user or password')
            else:
                print(self.session)
                self.tracker.reset()
                self.window = MainWindow(self.session)
                self.window.show()
                self.close()
        else:
            QMessageBox.warning(self, 'You are locked out',
                                f"Please try again after {int(self.tracker.locked_until - time.time())} seconds.")

    def exit_app(self):
        QApplication.quit()