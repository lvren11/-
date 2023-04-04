import random
import sys
 
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QGridLayout
import resource.res as res
 
 
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
 
        self.text = QtWidgets.QLabel("Hello World")
 
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        # 按钮布局
        self.btn_layout = QGridLayout()
        # 创建三个按钮
        self.button_last_step = QtWidgets.QPushButton()
        # 按钮图标
        self.button_last_step.setIcon(QPixmap(":/icon/ic_last_step"))
        self.btn_layout.addWidget(self.button_last_step, 0, 0)
 
        self.button_start = QtWidgets.QPushButton()
        self.button_start.setIcon(QPixmap(":/icon/ic_start"))
        self.btn_layout.addWidget(self.button_start, 0, 1)
 
        self.button_next_step = QtWidgets.QPushButton()
        self.button_next_step.setIcon(QPixmap(":/icon/ic_next_step"))
        self.btn_layout.addWidget(self.button_next_step, 0, 2)
        # 添加按钮布局到窗口布局中
        self.layout.addLayout(self.btn_layout)
 
 
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(400, 300)
    widget.show()
    sys.exit(app.exec())