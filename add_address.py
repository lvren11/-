# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'update_address.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_Dialog_ADD(QDialog):
    def __init__(self, parent=None):
        super(Ui_Dialog_ADD, self).__init__(parent)
        self.parent = parent
        # self.path = os.path.realpath(os.curdir) + '/参数配置文件/'
        self.setupUi()

    def setupUi(self):
        self.setObjectName(u"Dialog")
        self.resize(488, 233)
        font = QFont()
        font.setFamilies([u"\u5b8b\u4f53"])
        font.setPointSize(14)
        self.setFont(font)
        self.groupBox = QGroupBox(self)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(30, 20, 431, 121))
        self.groupBox.setFont(font)
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.widget = QWidget(self.groupBox)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 30, 401, 71))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setFont(font)

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(30, 170, 121, 41))
        self.pushButton.clicked.connect(self.update)
        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(340, 170, 121, 41))
        self.pushButton_2.clicked.connect(self.reset)
        self.retranslateUi()

        QMetaObject.connectSlotsByName(self)
    # setupUi

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Dialog", u"\u65b0\u589e\u5730\u5740", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"\u8bbe\u7f6e", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u65b0\u5730\u5740\uff1a", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"\u4fee\u6539", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"\u91cd\u7f6e", None))
    # retranslateUi

    def update(self):
        self.parent.mac.append(str(self.lineEdit.text()))
        self.parent.listWidget_2.addItem(str(self.lineEdit.text()))
        self.close()

    def reset(self):
        self.lineEdit.clear()