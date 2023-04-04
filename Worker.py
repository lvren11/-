from PySide6.QtCore import QThread,Signal

class Worker(QThread):
    sinOut = Signal(dict,list,list,float,int,list,bool,list,int)

    def __init__(self, parent=None, func = None):
        super(Worker, self).__init__(parent)
        #设置工作状态与初始num数值
        self.func = func
        self.parent = parent

    def run(self):
        self.plan, self.prolist, self.list_rate, self.all_rate, self.main_len, self.roll_length,self.program_ok ,self.idlist,self.leftcut= self.func(self.parent)
        self.sinOut.emit(self.plan, self.prolist, self.list_rate, self.all_rate, self.main_len, self.roll_length, self.program_ok,self.idlist,self.leftcut)
    
    def stop(self):
        self.terminate()


