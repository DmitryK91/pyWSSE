import sys
from REST import Header, Request
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("design.ui", self)

        self.cbType.addItems(self.paramList())
        self.cbType.currentTextChanged.connect(self.onCurrentTextChanged)
        self.teData.setEnabled(self.cbType.currentText == 'PUT')

        self.teResult.setVisible(False)
        self.scrollArea.setVisible(False)

        self.btnSend.clicked.connect(self.send)

    def send(self):
        """Send request"""

        self.scrollArea.setVisible(True)
        self.teResult.setVisible(True)
        self.teResult.clear()

        try:
            header = Header(self.leUserName.text(), self.lePassword.text())
            result = Request(self.cbType.currentText(),
                             header,
                             self.leUri.text(),
                             self.teData.toPlainText())
        except Exception as ex:
            result = ex

        self.teResult.append(str(result))

    def paramList(self):
        """Request types combo box"""

        G = 'GET'
        P = 'PUT'

        allParams = [G, P]
        return allParams

    def onCurrentTextChanged(self, text):
        self.teData.setEnabled(str(text) == 'PUT')


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = AppWindow()
        ex.show()
        sys.exit(app.exec_())
    except Exception as ex:
        print(str(ex))
        sys.exit()
