import sys
from REST import Header, Request
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class AppWindow(QMainWindow):
    def __init__(self):
        super(AppWindow, self).__init__()
        uic.loadUi("design.ui", self)

        self.cbServer.addItems(self.serverList)

        self.cbType.addItems(self.paramList)
        self.cbType.currentTextChanged.connect(self.onCurrentTextChanged)

        self.expand(False)

        self.btnSend.clicked.connect(self.send)

        self.btnExpand.clicked.connect(
            lambda: self.expand(not self.teResult.isVisible()))

    paramList = ['GET', 'PUT']

    serverList = {
        'QA': '10.21.17.211',
        'Dev': '217.74.37.156',
        'Prod': '10.21.17.210'
    }

    def getServer(self):
        server = self.serverList.get(self.cbServer.currentText())
        if not server:
            server = self.cbServer.currentText()
        return server

    def send(self):
        """Send request"""

        self.expand(True)
        self.teResult.clear()

        uri = (self.leDomen.text() + self.getServer()
               + self.leVersion.text() + self.leAPI.text())

        try:
            header = Header(self.leUserName.text(), self.lePassword.text())
            self.SetText(Request(self.cbType.currentText(),
                                 header, uri, self.teData.toPlainText()))
        except Exception as ex:
            self.teResult.append(str(ex))

    def SetText(self, result):
        if result[0] == '200':
            code = ('<div style="font-size:large; color:green">'
                    + result[0] + '</div>')
        else:
            code = ('<div style="font-size:large; color:red">'
                    + result[0] + '</div>')

        self.teResult.append(code)
        self.teResult.append(result[1])

    def onCurrentTextChanged(self, text):
        self.teData.setEnabled(str(text) == 'PUT')

    def expand(self, exp):
        self.teResult.setVisible(exp)
        if exp:
            self.btnExpand.setArrowType(QtCore.Qt.RightArrow)
        else:
            self.btnExpand.setArrowType(QtCore.Qt.LeftArrow)


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = AppWindow()
        ex.show()
        sys.exit(app.exec_())
    except Exception as ex:
        print(str(ex))
        sys.exit()
