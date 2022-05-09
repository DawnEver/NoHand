# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("没人举手是吧")
        MainWindow.resize(800, 606)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(74, 120, 651, 200))
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 200))
        font = QtGui.QFont()
        font.setFamily("Source Han Serif SC")
        font.setPointSize(120)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit.setText("???")
        self.lineEdit.setFont(font)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(140, 380, 511, 151))
        font = QtGui.QFont()
        font.setFamily("Source Han Serif SC")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setText("开始滚动/暂停")
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.pushButton.clicked.connect(self.update)
        
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import random
import time
with open("totalList.txt",'r',encoding='UTF-8') as f:
    totalList=f.readlines()
totalListLen=len(totalList)-1

with open("luckyList.txt",'r',encoding='UTF-8') as f:
    luckyList=f.readlines()
luckyListLen=len(luckyList)-1

#配置
import json
with open("settings.json","r",encoding='UTF-8')as f:
    m=json.load(f,strict=False)
    order=m['order']#1为顺序循环选取luckyList.txt中的名单,0为随机抽取luckyList.txt中的名单
    delay=m['delay']

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)  
        self.setupUi(self)

        self.lineEdit.setReadOnly(True)
        self.lineEdit.setStyleSheet("background-color:rgba(254,254,254,150);border-width:1;border-style:inset")
        self.pushButton.setStyleSheet("background-color:rgba(244,244,244,255);border-width:1")
        self.pushButton.pressed.connect(self.start)
        self.pushButton.released.connect(self.stop)
        self.mythread=MyThread()
        self.mythread.signal.connect(self.callback)
        self.i=0
        
        
    def start(self):
            self.mythread.flag=True
            self.mythread.start()
            
    def stop(self):
            self.mythread.flag=False
            time.sleep(delay)
            
            if order==1:
                if self.i==luckyListLen:
                    self.i=0
                self.i+=1
            else:
                self.i=random.randint(0,luckyListLen)

            self.lineEdit.setText(luckyList[self.i])

            QApplication.processEvents()
        
    def callback(self,i):
        self.lineEdit.setText(totalList[i])
        QApplication.processEvents()

class MyThread(QThread):
    signal =pyqtSignal(int)
    
    def __init__(self):
        super(MyThread,self).__init__()
        self.flag = True

    def run(self):
        while self.flag:
            self.t=random.randint(0,totalListLen)
            self.signal.emit(int(self.t))
            time.sleep(delay)
    
if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)  
    app.setStyle("macintosh")
    
    MainWindow = QMainWindow()  
    ui = MyMainWindow()
    
    palette=QPalette()
    pix=QPixmap("./background.png")
    pix=pix.scaled(ui.width(),ui.height())
    palette.setBrush(QPalette.Background,QBrush(pix))
    ui.setPalette(palette)
    
    ui.show()
    sys.exit(app.exec_())  
