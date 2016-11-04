# encoding: utf-8

"""
@author: ouwj
@file: testQt.py
@time: 2016/11/3 10:39
"""

import sys
from PyQt4 import QtGui

app = QtGui.QApplication(sys.argv)
label = QtGui.QLabel("Hello Qt!")
label.show()

sys.exit(app.exec_())