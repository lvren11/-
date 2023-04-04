# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Parameter_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import os
import pandas as pd

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,QAction,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem, QAbstractItemView,QMenu,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,QMessageBox,
    QWidget)
from save_tool import  Ui_Dialog_Save
from parameters import Parameters

class Ui_Dialog_Para(QDialog):
    def __init__(self, parent=None):
        super(Ui_Dialog_Para, self).__init__(parent)
        self.parent = parent
        self.selected_item_text = None
        # path表示路径
        self.path = os.path.realpath(os.curdir) + '/参数配置文件'
        filelist = os.listdir(self.path)
        self.file_name_list = []
        for item in filelist:
            if(item.endswith('.xlsx')):
                self.file_name_list.append(item.split('.xlsx')[0])
        self.setupUi()

    def setupUi(self):
        self.setObjectName(u"Dialog")
        self.resize(877, 532)
        self.setMaximumSize(QSize(877, 532))
        self.setMinimumSize(QSize(877, 532))
        font = QFont()
        font.setFamilies([u"\u5b8b\u4f53"])
        font.setPointSize(14)
        self.setFont(font)
        self.listWidget = QListWidget(self)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(21, 21, 171, 371))
        font1 = QFont()
        font1.setFamilies([u"\u5b8b\u4f53"])
        font1.setPointSize(11)
        self.listWidget.setFont(font1)
        self.label_2 = QLabel(self)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 450, 171, 20))
        self.label_2.setAlignment(Qt.AlignCenter)
        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(320, 470, 141, 41))
        #保存
        self.pushButton.clicked.connect(self.save_scheme)
        self.groupBox = QGroupBox(self)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(210, 20, 641, 371))
        self.groupBox.setFont(font)
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.layoutWidget = QWidget(self.groupBox)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(327, 48, 121, 251))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.layoutWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)

        self.verticalLayout_3.addWidget(self.label_7)

        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)

        self.verticalLayout_3.addWidget(self.label_5)

        self.label_9 = QLabel(self.layoutWidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font1)

        self.verticalLayout_3.addWidget(self.label_9)

        self.label_11 = QLabel(self.layoutWidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font1)

        self.verticalLayout_3.addWidget(self.label_11)

        self.label_13 = QLabel(self.layoutWidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font1)

        self.verticalLayout_3.addWidget(self.label_13)

        self.label_27 = QLabel(self.layoutWidget)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFont(font1)

        self.verticalLayout_3.addWidget(self.label_27)

        self.lineEdit_2 = QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(154, 58, 120, 21))
        self.lineEdit_2.setFont(font1)
        self.lineEdit_8 = QLineEdit(self.groupBox)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setGeometry(QRect(154, 184, 120, 21))
        self.lineEdit_8.setFont(font1)
        self.lineEdit_4 = QLineEdit(self.groupBox)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setGeometry(QRect(154, 100, 120, 21))
        self.lineEdit_4.setFont(font1)
        self.lineEdit_9 = QLineEdit(self.groupBox)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        self.lineEdit_9.setGeometry(QRect(154, 142, 120, 21))
        self.lineEdit_9.setFont(font1)
        self.lineEdit_26 = QLineEdit(self.groupBox)
        self.lineEdit_26.setObjectName(u"lineEdit_26")
        self.lineEdit_26.setGeometry(QRect(270, 310, 120, 21))
        self.lineEdit_26.setFont(font1)
        self.lineEdit_24 = QLineEdit(self.groupBox)
        self.lineEdit_24.setObjectName(u"lineEdit_24")
        self.lineEdit_24.setGeometry(QRect(154, 268, 120, 21))
        self.lineEdit_24.setFont(font1)
        self.lineEdit_11 = QLineEdit(self.groupBox)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
        self.lineEdit_11.setGeometry(QRect(154, 226, 120, 21))
        self.lineEdit_11.setFont(font1)
        self.label_28 = QLabel(self.groupBox)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setGeometry(QRect(30, 310, 231, 16))
        self.label_28.setFont(font1)
        self.widget = QWidget(self.groupBox)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(30, 48, 114, 251))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)

        self.verticalLayout.addWidget(self.label_4)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)

        self.verticalLayout.addWidget(self.label_6)

        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font1)

        self.verticalLayout.addWidget(self.label_8)

        self.label_10 = QLabel(self.widget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font1)

        self.verticalLayout.addWidget(self.label_10)

        self.label_12 = QLabel(self.widget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font1)

        self.verticalLayout.addWidget(self.label_12)

        self.label_26 = QLabel(self.widget)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font1)

        self.verticalLayout.addWidget(self.label_26)

        self.widget1 = QWidget(self.groupBox)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(455, 44, 120, 261))
        self.verticalLayout_2 = QVBoxLayout(self.widget1)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_3 = QLineEdit(self.widget1)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setFont(font1)

        self.verticalLayout_2.addWidget(self.lineEdit_3)

        self.lineEdit_5 = QLineEdit(self.widget1)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setFont(font1)

        self.verticalLayout_2.addWidget(self.lineEdit_5)

        self.lineEdit_7 = QLineEdit(self.widget1)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setFont(font1)

        self.verticalLayout_2.addWidget(self.lineEdit_7)

        self.lineEdit_10 = QLineEdit(self.widget1)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setFont(font1)

        self.verticalLayout_2.addWidget(self.lineEdit_10)

        self.lineEdit_12 = QLineEdit(self.widget1)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        self.lineEdit_12.setFont(font1)

        self.verticalLayout_2.addWidget(self.lineEdit_12)

        self.comboBox = QComboBox(self.widget1)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setFont(font1)

        self.verticalLayout_2.addWidget(self.comboBox)

        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(570, 470, 151, 41))
                #加载出保存方案窗口
        self.pushButton_2.clicked.connect(self.use_scheme)
        self.layoutWidget1 = QWidget(self)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(30, 410, 821, 31))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget1)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.label_3 = QLabel(self.layoutWidget1)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.lineEdit = QLineEdit(self.layoutWidget1)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.load_list()
        self.retranslateUi()

        QMetaObject.connectSlotsByName(self)
    # setupUi

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Dialog", u"\u53c2\u6570\u914d\u7f6e", None))
        #设置被选中的方案
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u65b9\u6848\u4e00", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"\u4fdd\u5b58\u65b9\u6848", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"\u53c2\u6570\u786e\u5b9a", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"\u6700\u5c0f\u4f59\u6750\u5bbd\u5ea6\u003a", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"\u4ea4\u8d27\u6570\u91cf\u4e0a\u9650\u003a", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"\u6bdb\u8fb9\u5377\u6700\u5c0f\u8fb9\u4e1d\u003a", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"\u5207\u8fb9\u5377\u6700\u5c0f\u8fb9\u4e1d\u003a", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"\u5e93\u5b58\u6700\u5c0f\u8fb9\u4e1d\u003a", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"\u6210\u54c1\u6700\u77ed\u7c73\u6570\u003a", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"\u539a\u5ea6\u53c2\u6570\u003a", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"\u4ea4\u8d27\u6570\u91cf\u4e0b\u9650\u003a", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"\u6bdb\u8fb9\u5377\u6700\u5927\u8fb9\u4e1d\u003a", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"\u5207\u8fb9\u5377\u6700\u5927\u8fb9\u4e1d\u003a", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"\u5e93\u5b58\u6700\u5927\u8fb9\u4e1d\u003a", None))
        self.label_27.setText(QCoreApplication.translate("Dialog", u"\u4f18\u5148\u6807\u8bc6\u003a", None))
        self.label_28.setText(QCoreApplication.translate("Dialog", u"\u6210\u54c1\u4e0d\u540c\u5bbd\u5ea6\u95f4\u6700\u5c0f\u957f\u5ea6\u5dee\u003a", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"\u5bbd\u5ea6\u4f18\u5148", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"\u957f\u5ea6\u4f18\u5148", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"\u4f7f\u7528\u5f53\u524d\u65b9\u6848", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u5f53\u524d\u53c2\u6570\u914d\u7f6e\u65b9\u6848", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u5f53\u524d\u578b\u53f7\u540d\u79f0\u003a", None))
    # retranslateUi

    def load_list(self):
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        self.listWidget.addItems(self.file_name_list)
        self.listWidget.itemActivated.connect(self.itemActivated_event)

        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested[QPoint].connect(self.rightMenuShow)
        

    def rightMenuShow(self, point):
        def CreateNewItem():
            # # 创建一个没有名字的item

            item = QListWidgetItem("")
            # 使得item是可以编辑的.
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.listWidget.addItem(item)
            # 创建后就可以编辑item,用户自己起名字.
            self.listWidget.editItem(item)
            self.listWidget.itemChanged.connect(lambda: ChangeItem(item))

        def ChangeItem(item):
            self.listWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.file_name_list.append(item.text())
            new_path = self.path + '/' + str(item.text()) + '.xlsx'
            dict = {'最小余材宽度':0, "厚度参数":0, "交货数量上限":0, "交货数量下限":0, "毛边卷最小边丝":0, "毛边卷最大边丝":0, "切边卷最小边丝":0, "切边卷最大边丝":0, "库存最小边丝":0, "库存最大边丝":0, "成品最短米数":0, "成品不同宽度间最小长度差":0, "优先标识":"宽度优先"}
            df = pd.DataFrame(pd.Series(dict), columns=['值'])
            df = df.reset_index().rename(columns={'index':'参数名'})
            df.to_excel(new_path,sheet_name="Parameters")

        def DeleteItem():
            remove_path = self.path + '/' + str(self.listWidget.currentItem().text()) + '.xlsx'
            a = self.listWidget.takeItem(self.listWidget.currentRow())
            os.remove(remove_path)
 
        popMenu = QMenu()
        popMenu.addAction(QAction(u'添加方案', self, triggered=CreateNewItem))
        popMenu.addAction(QAction(u'删除方案', self, triggered=DeleteItem))
 
        popMenu.exec_(QCursor.pos())


    def itemActivated_event(self, item):
        #print(item.text())
        self.selected_item_text = item.text()
        self.selected_item_index = self.listWidget.currentRow()
        self.label_2.setText(item.text())

        if self.selected_item_text != None:
            self.new_path = self.path + '/' + self.selected_item_text + '.xlsx'
            para_file = pd.read_excel(self.new_path)
            para_list = para_file['值'].values.tolist()
            self.lineEdit_2.setText(str(para_list[0]))
            self.lineEdit_3.setText(str(para_list[1]))
            self.lineEdit_4.setText(str(para_list[2]))
            self.lineEdit_5.setText(str(para_list[3]))
            self.lineEdit_9.setText(str(para_list[4]))
            self.lineEdit_7.setText(str(para_list[5]))
            self.lineEdit_8.setText(str(para_list[6]))
            self.lineEdit_10.setText(str(para_list[7]))
            self.lineEdit_11.setText(str(para_list[8]))
            self.lineEdit_12.setText(str(para_list[9]))
            self.lineEdit_24.setText(str(para_list[10]))
            self.lineEdit_26.setText(str(para_list[11]))
            if str(para_list[12]) == "宽度优先":
                self.comboBox.setCurrentIndex(0)
            else:
                self.comboBox.setCurrentIndex(1)
            self.lineEdit.setText(self.selected_item_text)
        else:
            QMessageBox.warning(self, "提示", "没有选中列表的参数方案", QMessageBox.Ok)

    def save_scheme(self):
        REMAIN_MIN_WIDTH = int(float(self.lineEdit_2.text()))
        THICKNESS = float(self.lineEdit_3.text())
        POSITIVE_ERROR_PERCENT = float(self.lineEdit_4.text())
        NEGATIVE_ERROR_PERCENT = float(self.lineEdit_5.text())
        LEFT_FUR = int(float(self.lineEdit_9.text()))
        RIGHT_FUR = int(float(self.lineEdit_7.text()))
        LEFT_CUT = int(float(self.lineEdit_8.text()))
        RIGHT_CUT = int(float(self.lineEdit_10.text()))
        LEFT_STOCK = int(float(self.lineEdit_11.text()))
        RIGHT_STOCK = int(float(self.lineEdit_12.text()))
        MIN_LENGTH = int(float(self.lineEdit_24.text()))
        length_difference = int(float(self.lineEdit_26.text()))
        mode = str(self.comboBox.currentText())
        scheme_name = str(self.lineEdit.text())

        Parameter_data = Parameters(REMAIN_MIN_WIDTH, THICKNESS, POSITIVE_ERROR_PERCENT, NEGATIVE_ERROR_PERCENT, LEFT_FUR, RIGHT_FUR, LEFT_CUT, RIGHT_CUT, LEFT_STOCK, RIGHT_STOCK, MIN_LENGTH, length_difference, mode, scheme_name)
        save_ui = Ui_Dialog_Save(self, Parameter_data)
        save_ui.exec()

    def use_scheme(self):
        REMAIN_MIN_WIDTH = int(float(self.lineEdit_2.text()))
        THICKNESS = float(self.lineEdit_3.text())
        POSITIVE_ERROR_PERCENT = float(self.lineEdit_4.text())
        NEGATIVE_ERROR_PERCENT = float(self.lineEdit_5.text())
        LEFT_FUR = int(float(self.lineEdit_9.text()))
        RIGHT_FUR = int(float(self.lineEdit_7.text()))
        LEFT_CUT = int(float(self.lineEdit_8.text()))
        RIGHT_CUT = int(float(self.lineEdit_10.text()))
        LEFT_STOCK = int(float(self.lineEdit_11.text()))
        RIGHT_STOCK = int(float(self.lineEdit_12.text()))
        MIN_LENGTH = int(float(self.lineEdit_24.text()))
        length_difference = int(float(self.lineEdit_26.text()))
        mode = str(self.comboBox.currentText())
        scheme_name = str(self.lineEdit.text())
        self.parent.scheme = scheme_name
        Parameter_data = Parameters(REMAIN_MIN_WIDTH, THICKNESS, POSITIVE_ERROR_PERCENT, NEGATIVE_ERROR_PERCENT, LEFT_FUR, RIGHT_FUR, LEFT_CUT, RIGHT_CUT, LEFT_STOCK, RIGHT_STOCK, MIN_LENGTH, length_difference, mode, scheme_name)
        self.parent.Par_data = Parameter_data
        if (self.selected_item_text in self.file_name_list) and self.selected_item_text != scheme_name:
            remove_file_path = self.path + '/' + self.selected_item_text +'.xlsx'
            os.remove(remove_file_path)
        file_path = self.path + '/' + scheme_name + '.xlsx'
        dict = {'最小余材宽度':REMAIN_MIN_WIDTH, "厚度参数":THICKNESS, "交货数量上限":POSITIVE_ERROR_PERCENT, "交货数量下限":NEGATIVE_ERROR_PERCENT, "毛边卷最小边丝":LEFT_FUR, "毛边卷最大边丝":RIGHT_FUR, "切边卷最小边丝":LEFT_CUT, "切边卷最大边丝":RIGHT_CUT, "库存最小边丝":LEFT_STOCK, "库存最大边丝":RIGHT_STOCK, "成品最短米数":MIN_LENGTH, "成品不同宽度间最小长度差":length_difference, "优先标识":mode}
        df = pd.DataFrame(pd.Series(dict), columns=['值'])
        df = df.reset_index().rename(columns={'index':'参数名'})
        df.to_excel(file_path,sheet_name="Parameters")
        self.close()
