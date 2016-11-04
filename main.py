# encoding: utf-8

"""
@author: ouwj
@file: main.py
@time: 2016/11/3 21:59
"""

import sys
from buildPicWidget import *


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui=Ui_mainWindow()# Ui_Dialog为.ui产生.py文件中窗体类名，经测试类名以Ui_为前缀，加上UI窗体对象名（此处为Dialog，见上图）
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()  ### Dialog是main.py的上部的Class的名字
    window.show()
    sys.exit(app.exec_())