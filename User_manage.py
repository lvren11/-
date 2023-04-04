# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Parameter_ui_new.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import os
import json
import pickle
import base64
from add_address import Ui_Dialog_ADD
from add_user import Ui_Dialog_ADDU
from update_pwd import Ui_Dialog_UP
from update_admin import Ui_Dialog_UPAD


from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QGroupBox, QLabel,QMessageBox,QListWidget, QListWidgetItem,QAbstractItemView,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog_User(QDialog):
    def __init__(self, parent=None):
        super(Ui_Dialog_User, self).__init__(parent)
        self.parent = parent
        self.admin = self.parent.data['admin']
        self.user = self.parent.data['user']
        self.mac = self.parent.data['mac']
        self.selected_item_text = None
        self.path = os.path.realpath(os.curdir) + '/config.txt'
        self.setupUi()

    def setupUi(self):
        self.setObjectName(u"Dialog")
        self.resize(878, 444)
        self.setMaximumSize(QSize(878, 444))
        self.setMinimumSize(QSize(878, 444))
        font = QFont()
        font.setFamilies([u"\u5b8b\u4f53"])
        font.setPointSize(14)
        self.setFont(font)
        self.groupBox = QGroupBox(self)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 30, 221, 371))
        self.groupBox.setFont(font)
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        font1 = QFont()
        font1.setFamilies([u"\u5b8b\u4f53"])
        font1.setPointSize(13)
        self.listWidget = QListWidget(self.groupBox)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(0, 20, 221, 351))
        self.listWidget.setFont(font1)
        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(250, 30, 171, 41))
        self.pushButton.clicked.connect(self.refreshuser)
        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(690, 30, 171, 41))
        self.pushButton_2.clicked.connect(self.refreshadd)
        self.pushButton_3 = QPushButton(self)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(250, 100, 171, 41))
        self.pushButton_3.clicked.connect(self.adduser)
        self.pushButton_4 = QPushButton(self)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(250, 170, 171, 41))
        self.pushButton_4.clicked.connect(self.removeuser)
        self.pushButton_5 = QPushButton(self)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(250, 240, 171, 41))
        self.pushButton_5.clicked.connect(self.updatepwd)
        self.pushButton_8 = QPushButton(self)
        self.pushButton_8.setObjectName(u"pushButton_5")
        self.pushButton_8.setGeometry(QRect(250, 310, 171, 41))
        self.pushButton_8.clicked.connect(self.updateadmin)
        self.pushButton_6 = QPushButton(self)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(690, 100, 171, 41))
        self.pushButton_6.clicked.connect(self.addaddre)
        self.pushButton_7 = QPushButton(self)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(690, 170, 171, 41))
        self.pushButton_7.clicked.connect(self.removeadd)
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 410, 121, 31))
        self.groupBox_2 = QGroupBox(self)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(450, 30, 221, 371))
        self.groupBox_2.setFont(font)
        self.groupBox_2.setAutoFillBackground(False)
        self.groupBox_2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.listWidget_2 = QListWidget(self.groupBox_2)
        self.listWidget_2.setObjectName(u"listWidget_2")
        self.listWidget_2.setGeometry(QRect(0, 20, 221, 351))
        self.listWidget_2.setFont(font1)
        self.retranslateUi()
        self.load_list()
        self.load_list_2()
        QMetaObject.connectSlotsByName(self)
    # setupUi

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Dialog", u"\u7528\u6237\u7ba1\u7406", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"\u5141\u8bb8\u767b\u5f55\u7684\u7528\u6237", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"\u5141\u8bb8\u767b\u5f55\u7684mac\u5730\u5740", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"\u5237\u65b0\u7528\u6237\u5217\u8868", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"\u5237\u65b0\u5730\u5740\u5217\u8868", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", u"\u6dfb\u52a0\u7528\u6237", None))
        self.pushButton_4.setText(QCoreApplication.translate("Dialog", u"\u5220\u9664\u7528\u6237", None))
        self.pushButton_5.setText(QCoreApplication.translate("Dialog", u"\u4fee\u6539\u5f53\u524d\u5bc6\u7801", None))
        self.pushButton_6.setText(QCoreApplication.translate("Dialog", u"\u6dfb\u52a0\u5730\u5740", None))
        self.pushButton_7.setText(QCoreApplication.translate("Dialog", u"\u5220\u9664\u5730\u5740", None))
        self.pushButton_8.setText(QCoreApplication.translate("Dialog", u"\u4fee\u6539\u7ba1\u7406\u5458\u4fe1\u606f", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u8bf7\u89c4\u8303\u64cd\u4f5c\uff01", None))
    # retranslateUi

    def load_list(self):
        self.account = []
        for i in range(len(self.user)):
            self.account.append(self.user[i]['account'])
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        self.listWidget.addItems(self.account)
        self.listWidget.itemActivated.connect(self.itemActivated_event)

    def itemActivated_event(self, item):
        #print(item.text())
        self.selected_item_text = item.text()

    def load_list_2(self):
        self.listWidget_2.setAlternatingRowColors(True)
        self.listWidget_2.setDragDropMode(QAbstractItemView.InternalMove)
        self.listWidget_2.addItems(self.mac)

    def refreshuser(self):
        self.listWidget.clear()
        new_data = {
            'admin': self.admin,
            'user': self.user,
            'mac': self.mac
        }
        bytejson=pickle.dumps(new_data)
        obj = base64.b64encode(bytejson)
        open(self.path,"wb").write(obj)

        strjson=open(self.path,"rb").read()
        ciphertext_str = base64.b64decode(strjson)
        #字符串转换为json对象
        data = pickle.loads(ciphertext_str)
        self.user = data['user']
        self.load_list()

    def refreshadd(self):
        self.listWidget_2.clear()
        new_data = {
            'admin': self.admin,
            'user': self.user,
            'mac': self.mac
        }
        bytejson=pickle.dumps(new_data)
        obj = base64.b64encode(bytejson)
        open(self.path,"wb").write(obj)

        strjson=open(self.path,"rb").read()
        ciphertext_str = base64.b64decode(strjson)
        #字符串转换为json对象
        data = pickle.loads(ciphertext_str)
        self.mac = data['mac']
        self.load_list_2()

    def adduser(self):
        add_ui = Ui_Dialog_ADDU(self)
        add_ui.exec()

    def removeuser(self):
        self.box = QMessageBox.question(self, '提示', '您确定要删除该用户吗？',
           QMessageBox.Yes, QMessageBox.No)
        if self.box == QMessageBox.Yes:
            count = self.listWidget.count()  # 得到QListWidget的总个数
            for i in range(count):
                item = self.listWidget.item(i)
                if item.isSelected():
                    if item.text() == '管理员':
                        QMessageBox.critical(self, '错误', '不能删除管理员',QMessageBox.Yes, QMessageBox.No)
                    else:
                        self.listWidget.removeItemWidget(self.listWidget.takeItem(i))
                        index = 0
                        for i in range(len(self.user)):
                            if self.user[i]['account'] == item.text():
                                index = i
                                break
                        self.user.pop(i)

    def updatepwd(self):
        if self.selected_item_text != None:
            count = self.listWidget.count()  # 得到QListWidget的总个数
            for i in range(count):
                item = self.listWidget.item(i)
                if item.isSelected():
                    if self.selected_item_text == item.text():
                        UP_ui = Ui_Dialog_UP(self)
                        UP_ui.exec()
                    else:
                        QMessageBox.critical(self, '错误', '没有双击选中修改密码的帐号',QMessageBox.Yes, QMessageBox.No)
                    break
        else:
            QMessageBox.critical(self, '错误', '没有双击选中修改密码的帐号',QMessageBox.Yes, QMessageBox.No)

    def addaddre(self):
        addad_ui = Ui_Dialog_ADD(self)
        addad_ui.exec()

    def removeadd(self):
        self.box = QMessageBox.question(self, '提示', '您确定要删除该地址吗？',
           QMessageBox.Yes, QMessageBox.No)
        if self.box == QMessageBox.Yes:
            count = self.listWidget_2.count()  # 得到QListWidget的总个数
            for i in range(count):
                item = self.listWidget_2.item(i)
                if item.isSelected():
                    self.listWidget_2.removeItemWidget(self.listWidget_2.takeItem(i))
                    self.mac.remove(item.text())

    def closeEvent(self, event):
        new_data = {
            'admin': self.admin,
            'user': self.user,
            'mac': self.mac
        }
        bytejson=pickle.dumps(new_data)
        obj = base64.b64encode(bytejson)
        open(self.path,"wb").write(obj)
    
    def updateadmin(self):
        UPAD_ui = Ui_Dialog_UPAD(self)
        UPAD_ui.exec()
