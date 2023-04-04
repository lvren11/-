# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'save_tool.ui'
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
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QSizePolicy, QWidget)

class Ui_Dialog_Save(QDialog):

    def __init__(self, parent=None, Parameter_data = None):
        super(Ui_Dialog_Save, self).__init__(parent)
        self.parent = parent
        self.Parameter_data = Parameter_data
        self.path = os.path.realpath(os.curdir) + '/参数配置文件/'
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
        self.buttonBox.setGeometry(QRect(90, 200, 211, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonY = self.buttonBox.button(QDialogButtonBox.Ok)
        self.buttonN = self.buttonBox.button(QDialogButtonBox.Cancel)
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(70, 50, 331, 51))
        self.label_2 = QLabel(self)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(130, 120, 181, 31))
        self.label_2.setAlignment(Qt.AlignCenter)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        QMetaObject.connectSlotsByName(self)
    # setupUi

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Dialog", u"\u4fee\u6539\u4fdd\u5b58", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u786e\u8ba4\u5c06\u4fdd\u5b58\u5f53\u524d\u53c2\u6570\u914d\u7f6e\u65b9\u6848\u4e3a\uff1a", None))
        self.label_2.setText(self.Parameter_data.scheme_name)
        self.buttonY.setText(QCoreApplication.translate("Dialog", u"\u786e\u5b9a", None))
        self.buttonN.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
    # retranslateUi

    def accept(self):
        self.parent.parent.Par_data = self.Parameter_data
        # self.parent.parent.scheme = self.Parameter_data.scheme_name
        if self.parent.selected_item_text != self.Parameter_data.scheme_name:
            remove_file_path = self.path + self.parent.selected_item_text +'.xlsx'
            os.remove(remove_file_path)
            self.parent.file_name_list[int(self.parent.selected_item_index)] = self.Parameter_data.scheme_name
            self.parent.listWidget.clear()
            self.parent.listWidget.addItems(self.parent.file_name_list)
        file_path = self.path + self.Parameter_data.scheme_name +'.xlsx'
        dict = {'最小余材宽度':self.Parameter_data.REMAIN_MIN_WIDTH, "厚度参数":self.Parameter_data.THICKNESS, "交货数量上限":self.Parameter_data.POSITIVE_ERROR_PERCENT, "交货数量下限":self.Parameter_data.NEGATIVE_ERROR_PERCENT, "毛边卷最小边丝":self.Parameter_data.LEFT_FUR, "毛边卷最大边丝":self.Parameter_data.RIGHT_FUR, "切边卷最小边丝":self.Parameter_data.LEFT_CUT, "切边卷最大边丝":self.Parameter_data.RIGHT_CUT, "库存最小边丝":self.Parameter_data.LEFT_STOCK, "库存最大边丝":self.Parameter_data.RIGHT_STOCK, "成品最短米数":self.Parameter_data.MIN_LENGTH, "成品不同宽度间最小长度差":self.Parameter_data.length_difference, "优先标识":self.Parameter_data.mode}
        df = pd.DataFrame(pd.Series(dict), columns=['值'])
        df = df.reset_index().rename(columns={'index':'参数名'})
        df.to_excel(file_path,sheet_name="Parameters")
        self.close()


