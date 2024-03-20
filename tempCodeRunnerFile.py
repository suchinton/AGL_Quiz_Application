from PyQt5.QtWidgets import QApplication, QSlider, QLCDNumber, QPushButton, QLabel, QPlainTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import uic

import kuksa_client as kc

import os
from AppRes_rc import *

current_dir = os.path.dirname(os.path.abspath(__file__))

Form, Base = uic.loadUiType(os.path.join(current_dir, "Main.ui"))

import sys
import platform

python_version = f"python{'.'.join(platform.python_version_tuple()[:2])}"

def check_paths(*paths):
    ans = {path: os.path.exists(path) for path in paths}
    # reverse the keys and values
    return {v: k for k, v in ans.items()}

CA_PATHS = check_paths(
    "/etc/kuksa-val/CA.pem",
    f"/usr/lib/{python_version}/site-packages/self.client/kuksa_server_certificates/CA.pem",
    os.path.abspath(os.path.join(os.path.dirname(
        __file__), "./cert/CA.pem"))
)

GRPC_TOKEN_PATHS = check_paths( 
    os.path.abspath(os.path.join(os.path.dirname(__file__),
                                 "./token/grpc/actuate-provide-all.token"))
)

class Worker(QThread):
    error_occurred = pyqtSignal(str)

    def __init__(self, client, speed):
        super().__init__()
        self.client = client
        self.speed = speed

    def run(self):
        try:
            self.client.setValue('Vehicle.Speed', str(self.speed), 'value')
        except Exception as e:
            self.error_occurred.emit(str(e))

class MainWindow(Base, Form):
    def __init__(self):
        super().__init__()
        uic.loadUi('Main.ui', self)
        self.show()

        config = {
        "ip": 'localhost',
        "port": 55555,
        "protocol": "grpc",
        "insecure": False,
        "tls_server_name": "Server",
        "cacert": CA_PATHS.get(True),
        "token": GRPC_TOKEN_PATHS.get(True),
        }

        self.SpeedSlider = self.findChild(QSlider, 'SpeedSlider')
        self.lcdNumber = self.findChild(QLCDNumber, 'lcdNumber')
        
        self.ProfilePic = self.findChild(QLabel, 'ProfilePic')
        self.SwitchPP = self.findChild(QPushButton, 'SwitchPP')
        self.OutputBox = self.findChild(QPlainTextEdit, 'OutputBox')
        self.OutputBox.appendPlainText("Output Box")

        self.SpeedSlider.valueChanged.connect(self.changeValue)
        self.SwitchPP.clicked.connect(self.changePP)

        try:
            self.client = kc.KuksaClientThread(config)
            self.client.start()
        except Exception as e:
            #print(f"Error: {e}")
            
            self.OutputBox.appendPlainText(e).setStyleSheet("color: red")

    def changeValue(self, value):
        speed = int(value)
        self.worker = Worker(self.client, speed)
        self.worker.error_occurred.connect(self.handle_error)
        self.worker.start()

    def handle_error(self, error_message):
        print("Error!! self.client not configured properly.")
        self.lcdNumber.display(int(self.client.getValue('Vehicle.Speed','value')))
        self.OutputBox.appendPlainText(error_message)


    def changePP(self):
        PP1 = QPixmap(":/images/images/BG1.jpg")
        PP2 = QPixmap(":/images/images/BG2.png")

        if self.ProfilePic.pixmap().toImage() == PP1.toImage():
            self.ProfilePic.setPixmap(PP2)
        else:
            self.ProfilePic.setPixmap(PP1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Suchinton App")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())