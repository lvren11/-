# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_2.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import hashlib
from psutil import net_if_addrs
import logo
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,QScreen,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,QMessageBox,
    QStatusBar, QVBoxLayout, QWidget)

class Login_MainWindow(object):
    def setupUi(self, MainWindow):
        self.parent = MainWindow
        self.admin = None
        self.mac_address = self.get_mac_address()
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(579, 390)
        MainWindow.setMinimumSize(QSize(579, 390))
        MainWindow.setMaximumSize(QSize(579, 390))
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = MainWindow.frameGeometry()
        geo.moveCenter(center)
        MainWindow.move(geo.topLeft())
        font = QFont()
        font.setFamilies([u"\u5b8b\u4f53"])
        font.setPointSize(14)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(270, 30, 41, 41))
        self.label_5.setPixmap(QPixmap(":/icon/logo.png").scaled(self.label_5.size(), aspectMode=Qt.KeepAspectRatio))
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(100, 140, 131, 141))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_3)

        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_4)

        self.layoutWidget_2 = QWidget(self.centralwidget)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(250, 130, 211, 161))
        self.verticalLayout = QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(1, 0, 1, 0)
        self.comboBox = QComboBox(self.layoutWidget_2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout.addWidget(self.comboBox)

        self.lineEdit = QLineEdit(self.layoutWidget_2)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout.addWidget(self.lineEdit)

        self.lineEdit_2 = QLineEdit(self.layoutWidget_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setEchoMode(QLineEdit.Password)

        self.verticalLayout.addWidget(self.lineEdit_2)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(230, 300, 121, 31))
        self.pushButton.clicked.connect(self.login)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(170, 60, 261, 51))
        font1 = QFont()
        font1.setFamilies([u"\u5b8b\u4f53"])
        font1.setPointSize(18)
        self.label.setFont(font1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 579, 25))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u767b\u5f55", None))
        self.label_5.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u89d2\u8272\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5e10\u53f7\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u5bc6\u7801\uff1a", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u7ba1\u7406\u5458", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u666e\u901a\u7528\u6237", None))

        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u767b\u5f55", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u53d6\u5411\u7845\u94a2\u667a\u80fd\u914d\u6599\u7cfb\u7edf", None))
    # retranslateUi
    def get_mac_address(self):
        address_all = []
        for k, v in net_if_addrs().items():
            for item in v:
                address = item[1]
                if '-' in address and len(address)==17:
                    address_all.append(address)
        return address_all

    def login(self):
        md = hashlib.md5(str(self.lineEdit_2.text()).encode('utf-8'))
        if str(self.comboBox.currentText()) == '管理员':
            if str(self.lineEdit.text()) == self.parent.data['admin']['account']:
                    if md.hexdigest() == self.parent.data['admin']['password']:
                        self.parent.name = self.parent.data['admin']['account']
                        self.admin = True
                    else:
                        QMessageBox.critical(self.parent, "错误", "帐号或密码错误", QMessageBox.Ok)
            else:
                QMessageBox.critical(self.parent, "错误", "帐号或密码错误", QMessageBox.Ok)
        else:
            flag = False
            user_develop_set = set(self.mac_address)-(set(self.mac_address)-set(self.parent.data['mac']))
            if  user_develop_set and user_develop_set <= set(self.parent.data['mac']):
                flag = True
            account_sum = 0
            if flag == True:
                for i in range(len(self.parent.data['user'])):
                    if str(self.lineEdit.text()) == self.parent.data['user'][i]['account']:
                        if md.hexdigest() == self.parent.data['user'][i]['password']:
                            self.parent.name = self.parent.data['user'][i]['account']
                            self.admin = False
                        else:
                            QMessageBox.critical(self.parent, "错误", "帐号或密码错误", QMessageBox.Ok)
                    else:
                        account_sum = account_sum + 1
                if account_sum == len(self.parent.data['user']):
                    QMessageBox.critical(self.parent, "错误", "帐号或密码错误", QMessageBox.Ok)
            else:
                QMessageBox.critical(self.parent, "地址错误", "您的IP地址不在允许列表里", QMessageBox.Ok)
        self.parent.setMainwindow(self.admin)
