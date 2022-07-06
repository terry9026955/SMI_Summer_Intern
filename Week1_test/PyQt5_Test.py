import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QGridLayout, QLineEdit)
from PyQt5.QtGui import QFont

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My PyQt5 program window')
        self.setGeometry(200, 300, 800, 400)

        #Qlabel (印文字)
        self.mylabel = QLabel("Test!~", self)   #第一個參數放顯示之文本內容，第二個放父class
        self.mylabel.move(50, 50)
        self.mylabel.setFont(QFont('Arial', 18))

        #QPushButton (按鈕功能)
        self.mybutton = QPushButton("Press", self) #預設顯示字串
        self.mybutton.move(400,50)
        self.mybutton.clicked.connect(self.onButtonClick)
        #self.mybutton.setFont(QFont("Arial", 18))

        #QLineEdit (文字輸入框)
        gridLayout = QGridLayout()  #獲取可用空間並將其劃分為行和列，然後將每個視窗控制元件放入指定的單元格中
        self.setLayout(gridLayout)  #類似在視窗網格中放置控制元件

        #帳號部分
        self.mylabel2 = QLabel("Name", self)
        gridLayout.addWidget(self.mylabel2, 0, 0)   #參數: Qwidget(指定元件), in row(列), in column(行)
        self.mylineedit = QLineEdit(self)           #文字輸入框
        gridLayout.addWidget(self.mylineedit, 0, 1)

        #密碼部分
        self.mylabel3 = QLabel("Passward", self)
        gridLayout.addWidget(self.mylabel3, 1, 0)   
        self.mylineedit2 = QLineEdit(self)    
        self.mylineedit2.setEchoMode(QLineEdit.Password)
        gridLayout.addWidget(self.mylineedit2, 1, 1)




        


    def onButtonClick(self):
        self.mybutton.setText("Yes") #點擊後顯示字串

      

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())


#Reference: https://shengyu7697.github.io/python-pyqt-tutorial/




