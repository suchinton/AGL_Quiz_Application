from PyQt5.QtWidgets import QApplication, QSlider, QLCDNumber, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QBitmap, QPainter, QColor
from PyQt5 import uic
import json

import kuksa_client as kc

import os

current_dir = os.path.dirname(os.path.abspath(__file__))

Form, Base = uic.loadUiType(os.path.join(current_dir, "Main.ui"))

import sys

class MainWindow(Base, Form):
    def __init__(self):
        super().__init__()
        uic.loadUi('Main.ui', self)
        self.show()

        config = {
        "ip": 'localhost',
        "port": 55555,
        "protocol": "grpc",
        "insecure": True,
        }

        self.SpeedSlider = self.findChild(QSlider, 'SpeedSlider')
        self.lcdNumber = self.findChild(QLCDNumber, 'lcdNumber')
        
        self.ProfilePic = self.findChild(QLabel, 'ProfilePic')
        self.SwitchPP = self.findChild(QPushButton, 'SwitchPP')

        self.SpeedSlider.valueChanged.connect(self.changeValue)
        self.SwitchPP.clicked.connect(self.changePP)

        self.ProfilePic.setPixmap(self.roundEdges(self.ProfilePic.pixmap()))

        try:
            self.client = kc.KuksaClientThread(config)
            self.client.start()
        except Exception as e:
            print(f"Error: {e}")

    def changeValue(self, value):
        speed = int(value)
        try:
            self.client.setValue('Vehicle.Speed',str(speed),'value')
            print(f"Feeding Vehicle.Speed to {speed}")
            response = json.loads(self.client.getValue('Vehicle.Speed'))
            vs_val = int(response['value']['value'])
            self.lcdNumber.display(vs_val)
        except:
            print("Error!! kuksa_client not configured properly.")

    def changePP(self):
        PP1 = self.roundEdges(QPixmap(":/images/images/BG1.jpg"))
        PP2 = self.roundEdges(QPixmap(":/images/images/BG2.png"))

        if self.ProfilePic.pixmap().toImage() == PP1.toImage():
            self.ProfilePic.setPixmap(PP2)
        else:
            self.ProfilePic.setPixmap(PP1)

    def roundEdges(self, pixmap):
        mask = QBitmap(pixmap.size())
        mask.fill()
        painter = QPainter(mask)
        painter.setBrush(QColor(0, 0, 0))
        painter.setPen(QColor(0, 0, 0))
        painter.drawRoundedRect(0, 0, pixmap.width(), pixmap.height(), 100, 100)
        painter.end()
        pixmap.setMask(mask)
        return pixmap

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Suchinton App")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())