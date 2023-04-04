# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'update_ped.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import hashlib
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QGroupBox, QLabel,QMessageBox,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Dialog_UPAD(QDialog):
    def __init__(self, parent=None):
        super(Ui_Dialog_UPAD, self).__init__(parent)
        self.parent = parent
        # self.path = os.path.realpath(os.curdir) + '/参数配置文件/'
        self.setupUi()

    def setupUi(self):
        self.setObjectName(u"Dialog")
        self.resize(488, 364)
        font = QFont()
        font.setFamilies([u"\u5b8b\u4f53"])
        font.setPointSize(14)
        self.setFont(font)
        self.groupBox = QGroupBox(self)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(30, 20, 431, 261))
        self.groupBox.setFont(font)
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.layoutWidget = QWidget(self.groupBox)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(70, 40, 111, 201))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.verticalLayout.addWidget(self.label_3)

        self.layoutWidget1 = QWidget(self.groupBox)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(210, 20, 181, 241))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(1, 0, 1, 0)
        self.lineEdit = QLineEdit(self.layoutWidget1)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setFont(font)

        self.verticalLayout_2.addWidget(self.lineEdit)

        self.lineEdit_2 = QLineEdit(self.layoutWidget1)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setFont(font)

        self.verticalLayout_2.addWidget(self.lineEdit_2)

        self.lineEdit_3 = QLineEdit(self.layoutWidget1)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setFont(font)

        self.verticalLayout_2.addWidget(self.lineEdit_3)

        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(30, 300, 121, 41))
        self.pushButton.clicked.connect(self.update)
        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(340, 300, 121, 41))
        self.pushButton_2.clicked.connect(self.reset)
        self.load_ui()
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)
    # setupUi

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Dialog", u"\u5bc6\u7801\u4fee\u6539", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"\u8bbe\u7f6e", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u5e10\u53f7\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u65b0\u5bc6\u7801\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u91cd\u590d\u5bc6\u7801\uff1a", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"\u4fee\u6539", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"\u91cd\u7f6e", None))
    # retranslateUi

    def load_ui(self):
        self.lineEdit.setText(self.parent.admin['account'])

    def update(self):
        md = hashlib.md5(str(self.lineEdit_2.text()).encode('utf-8'))
        if self.lineEdit_2.text() == self.lineEdit_3.text():
            self.parent.admin['account'] = str(self.lineEdit.text())
            str2 = ''
            for i in range(106-len(str(self.lineEdit.text()).encode('utf-8'))):
                str2 = str2 + ' '
            self.parent.parent.ui.setAction_3.setText(str2)
            str111 = '欢迎' + str(self.lineEdit.text()) + '登录' 
            self.parent.parent.ui.setAction_4.setText(str111)
            self.parent.admin['password'] = md.hexdigest()
            self.close()
        else:
            QMessageBox.critical(self, '错误', '密码不一致',QMessageBox.Yes, QMessageBox.No)

    def reset(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()

