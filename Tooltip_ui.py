# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Tooltip_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import os
import pandas as pd
import time
from program import program
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,QThread,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGroupBox, QHBoxLayout, QLabel, QSizePolicy,QMessageBox,
    QWidget)
from Worker import Worker

class Ui_Dialog_Tool(QDialog):
    def __init__(self, parent=None, path_Need_name = None, path_Roll_name = None, Need_file_encoding = None, Roll_file_encoding = None):
        super(Ui_Dialog_Tool, self).__init__(parent)
        self.parent = parent
        self.path = os.path.realpath(os.curdir) + '/参数配置文件'
        self.path_need = path_Need_name
        self.path_roll = path_Roll_name
        self.Need_encoding = Need_file_encoding
        self.Roll_encoding = Roll_file_encoding
        filelist = os.listdir(self.path)
        self.file_name_list = []
        for item in filelist:
            if(item.endswith('.xlsx')):
                self.file_name_list.append(item.split('.xlsx')[0])
        self.setupUi()

    def setupUi(self):
        self.setObjectName(u"Dialog")
        self.resize(455, 249)
        font = QFont()
        font.setFamilies([u"\u5b8b\u4f53"])
        font.setPointSize(14)
        self.setFont(font)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(150, 200, 161, 31))
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonY = self.buttonBox.button(QDialogButtonBox.Ok)
        self.buttonN = self.buttonBox.button(QDialogButtonBox.Cancel)
        self.groupBox = QGroupBox(self)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(30, 20, 391, 161))
        font1 = QFont()
        font1.setFamilies([u"\u5b8b\u4f53"])
        font1.setPointSize(14)
        font1.setBold(False)
        self.groupBox.setFont(font1)
        self.groupBox.setStyleSheet(u"background-color: rgb(239, 239, 239);\n"
"background-color: rgb(243, 243, 243);")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(80, 30, 271, 20))
        self.label.setFont(font)
        self.widget = QWidget(self.groupBox)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(50, 80, 321, 51))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(90, 70, 228, 19))
        self.label_2.setFont(font)
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(90, 110, 211, 20))
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignCenter)


        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.thread = Worker(self,Ui_Dialog_Tool.accept_th)
        self.thread.sinOut.connect(self.show_result)
        QMetaObject.connectSlotsByName(self)
    # setupUi

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Dialog", u"\u65b9\u6848\u9009\u62e9", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("Dialog", u"\u786e\u5b9a\u8981\u5f00\u59cb\u5207\u5272\u65b9\u6848\u751f\u6210\u5417\uff1f", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u5f53\u524d\u9009\u62e9\u53c2\u6570\u914d\u7f6e\u65b9\u6848\u4e3a\uff1a", None))
        if self.parent.Par_data == None:
            self.label_3.setText(self.file_name_list[0])
        else:
            self.label_3.setText(self.parent.scheme)
        self.buttonY.setText(QCoreApplication.translate("Dialog", u"\u786e\u5b9a", None))
        self.buttonN.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
    # retranslateUi
    def accept(self):
        if self.thread.isRunning():
            self.thread.stop()
        self.close()
        self.thread.start()
        self.parent.progress.start()

    def show_result(self,plan,prolist,list_rate,all_rate, main_len, roll_length, program_ok,idlist,leftcut):
        if len(prolist) == 0:
            if self.parent.progress.isVisible():
                self.parent.progress.stop()
            QMessageBox.warning(self, "提示", "没有需求文档或者原材料文档", QMessageBox.Ok)
        else:
            if program_ok == False:
                if self.parent.progress.isVisible():
                    self.parent.progress.stop()
                QMessageBox.warning(self, "错误提示", "程序运行发生错误", QMessageBox.Ok)
            else:
                self.parent.setresult(plan, prolist, list_rate, all_rate, main_len, roll_length,program_ok,idlist,leftcut)
                if self.parent.progress.isVisible():
                    self.parent.progress.stop()
        if self.thread.isRunning():
            self.thread.stop()

    def accept_th(self):
        if self.parent.Par_data != None:
            p = self.parent.Par_data
            print(p.REMAIN_MIN_WIDTH, p.THICKNESS, p.POSITIVE_ERROR_PERCENT, p.NEGATIVE_ERROR_PERCENT, p.LEFT_FUR, p.RIGHT_FUR, p.LEFT_CUT, p.RIGHT_CUT, p.LEFT_STOCK, p.RIGHT_STOCK, p.MIN_LENGTH, self.path_need, self.path_roll, self.Need_encoding, self.Roll_encoding, p.length_difference, p.mode)
            if self.path_need != None and self.path_roll != None:
                plan, prolist, list_rate, all_rate, main_len, roll_length,program_ok,idlist,leftcut = program(p.REMAIN_MIN_WIDTH, p.THICKNESS, p.POSITIVE_ERROR_PERCENT, p.NEGATIVE_ERROR_PERCENT, p.LEFT_FUR, p.RIGHT_FUR, p.LEFT_CUT, p.RIGHT_CUT, p.LEFT_STOCK, p.RIGHT_STOCK, p.MIN_LENGTH, self.path_need, self.path_roll, self.Need_encoding, self.Roll_encoding, p.length_difference, p.mode)
                # self.parent.setresult(self.plan, self.prolist, self.list_rate, self.all_rate, self.main_len)
                # self.close()
                return plan,prolist,list_rate,all_rate, main_len, roll_length,program_ok,idlist,leftcut
            else:
                plan = {}
                prolist = []
                list_rate = []
                all_rate = 0.0
                main_len = 0
                roll_length = []
                program_ok = True
                idlist=[]
                leftcut=0
                return plan,prolist,list_rate,all_rate, main_len, roll_length,program_ok,idlist,leftcut
                # QMessageBox.warning(self, "提示", "没有需求文档或者原材料文档", QMessageBox.Ok)
        else:
            self.new_path = self.path + '/' + self.file_name_list[0] + '.xlsx'
            para_file = pd.read_excel(self.new_path)
            para_list = para_file['值'].values.tolist()
            print(para_list)
            if self.path_need != None and self.path_roll != None:
                plan,prolist,list_rate,all_rate, main_len, roll_length, program_ok,idlist,leftcut = program(int(para_list[0]), str(para_list[1]), float(para_list[2]), float(para_list[3]), int(para_list[4]), int(para_list[5]), int(para_list[6]), int(para_list[7]), int(para_list[8]), int(para_list[9]), int(para_list[10]), str(self.path_need), str(self.path_roll), self.Need_encoding, self.Roll_encoding, int(para_list[11]), str(para_list[12]))
                # self.parent.setresult(self.plan, self.prolist, self.list_rate, self.all_rate, self.main_len)
                # self.close()
                return plan,prolist,list_rate,all_rate, main_len, roll_length, program_ok,idlist,leftcut
            else:
                plan = {}
                prolist = []
                list_rate = []
                all_rate = 0.0
                main_len = 0
                roll_length = []
                program_ok = True
                idlist=[]
                leftcut=0
                return plan,prolist,list_rate,all_rate, main_len, roll_length,program_ok,idlist,leftcut
                # QMessageBox.warning(self, "提示", "没有需求文档或者原材料文档", QMessageBox.Ok)