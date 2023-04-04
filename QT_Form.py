import os
import sys
import pandas as pd
from PySide6 import QtCore, QtWidgets, QtGui
from QT_MAINUI import Ui_MainWindow
from login import Login_MainWindow
from progress import CircleLoadingAnimation
import logo
import json
import hashlib
import pickle
import base64

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Login_MainWindow()
        # self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.Par_data = None
        self.scheme = None
        self.name = None
        self.progress = CircleLoadingAnimation(self)
        config_path = os.path.realpath(os.curdir) + '/config.txt'
        if os.path.isfile(config_path):
            strjson=open(config_path,"rb").read()
            #字符串转换为json对象
            ciphertext_str = base64.b64decode(strjson)
            self.data=pickle.loads(ciphertext_str)
        else:
            pd = hashlib.md5()  #创建md5对象
            pd.update(b'sectech') #生成加密串，其中password是要加密的字符串
            #加密

            self.data = {
                'admin': {'account':'sectech','password':pd.hexdigest()},
                'user': [],
                'mac': []
            }
            bytejson=pickle.dumps(self.data)
            obj = base64.b64encode(bytejson)
            open(config_path,"wb").write(obj)
        
    def setresult(self,plan,prolist,list_rate,all_rate,main_len, roll_length,program_ok,idlist,leftcut):
        self.ui.setALL(plan,prolist,list_rate,all_rate,main_len, roll_length,program_ok,idlist,leftcut)
    
    def setMainwindow(self,isadmin):
        if isadmin == True:
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self,isadmin)
        elif isadmin == False:
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self,isadmin)
    
    def login_out(self):
        self.ui = Login_MainWindow()
        # self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(":/icon/logo.png")))
    mainWin = MainWindow()
    mainWin.show()
    path = os.path.realpath(os.curdir) + '/参数配置文件'
    if not os.path.exists(path):
        os.makedirs(path)
    filelist = os.listdir(path)
    if len(filelist) == 0:
        new_path = path + '/' + '默认方案.xlsx'
        dict = {'最小余材宽度':50, "厚度参数":0.285, "交货数量上限":0.12, "交货数量下限":0.1, "毛边卷最小边丝":15, "毛边卷最大边丝":20, "切边卷最小边丝":10, "切边卷最大边丝":20, "库存最小边丝":0, "库存最大边丝":20, "成品最短米数":500, "成品不同宽度间最小长度差":600, "优先标识":"宽度优先"}
        df = pd.DataFrame(pd.Series(dict), columns=['值'])
        df = df.reset_index().rename(columns={'index':'参数名'})
        df.to_excel(new_path,sheet_name="Parameters")
    sys.exit(app.exec_())  
