import sys
from PyQt5.QtWidgets import QApplication
from login import Login

app = QApplication(sys.argv)
client = Login()

if __name__ == '__main__':
    client.show()
    sys.exit(app.exec_())
