from PyQt6.QtWidgets import QApplication, QSlider, QLCDNumber, QPushButton, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6 import uic

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
    f"/usr/lib/{python_version}/site-packages/kuksa_client/kuksa_server_certificates/CA.pem",
    os.path.abspath(os.path.join(os.path.dirname(
        __file__), "./cert/CA.pem"))
)

GRPC_TOKEN_PATHS = check_paths( 
    os.path.abspath(os.path.join(os.path.dirname(__file__),
                                 "./token/grpc/actuate-provide-all.token"))
)

class MainWindow(Base, Form):
    def __init__(self):
        super().__init__()
        uic.loadUi('Main.ui', self)
        self.show()

        self.SpeedSlider = self.findChild(QSlider, 'SpeedSlider')
        self.lcdNumber = self.findChild(QLCDNumber, 'lcdNumber')
        
        self.ProfilePic = self.findChild(QLabel, 'ProfilePic')
        self.SwitchPP = self.findChild(QPushButton, 'SwitchPP')
        

        self.SpeedSlider.valueChanged.connect(self.changeValue)
        self.SwitchPP.clicked.connect(self.changePP)

    def changeValue(self, value):
        config = {
        "ip": 'localhost',
        "port": 55555,
        "protocol": "grpc",
        "insecure": False,
        "tls_server_name": "Server",
        "cacert": CA_PATHS.get(True),
        "token": GRPC_TOKEN_PATHS.get(True),
        }

        print(config)

        kuksa_client = kc.KuksaClientThread(config)
        kuksa_client.start()

        speed = int(self.SpeedSlider.value())
        try:
            kuksa_client.setValue('Vehicle.Speed',str(speed),'value')
            print(f"Feeding Vehicle.Speed to {speed}")
            self.lcdNumber.display(int(kuksa_client.getValue('Vehicle.Speed','value')))
        except:
            print("Error!! kuksa_client not configured properly.")

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