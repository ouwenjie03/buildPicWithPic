# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'buildPicWidget.ui'
#
# Created: Thu Nov 03 11:35:16 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from buildPicWithPic import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_mainWindow(QtGui.QMainWindow):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName(_fromUtf8("mainWindow"))
        mainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.picLabel_src = QtGui.QLabel(self.centralwidget)
        self.picLabel_src.setGeometry(QtCore.QRect(50, 20, 300, 400))
        self.picLabel_src.setObjectName(_fromUtf8("graphicsView_src"))
        self.picLabel_dst = QtGui.QLabel(self.centralwidget)
        self.picLabel_dst.setGeometry(QtCore.QRect(450, 20, 300, 400))
        self.picLabel_dst.setObjectName(_fromUtf8("graphicsView_dst"))
        self.src_button = QtGui.QPushButton(self.centralwidget)
        self.src_button.setGeometry(QtCore.QRect(50, 510, 111, 41))
        self.src_button.setObjectName(_fromUtf8("src_button"))
        self.dir_button = QtGui.QPushButton(self.centralwidget)
        self.dir_button.setGeometry(QtCore.QRect(240, 510, 111, 41))
        self.dir_button.setObjectName(_fromUtf8("dir_button"))
        self.dir_button.setDisabled(True)
        self.run_button = QtGui.QPushButton(self.centralwidget)
        self.run_button.setGeometry(QtCore.QRect(450, 510, 111, 41))
        self.run_button.setObjectName(_fromUtf8("run_button"))
        self.run_button.setDisabled(True)
        self.save_button = QtGui.QPushButton(self.centralwidget)
        self.save_button.setGeometry(QtCore.QRect(640, 510, 111, 41))
        self.save_button.setObjectName(_fromUtf8("save_button"))
        self.save_button.setDisabled(True)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(50, 470, 701, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.textView = QtGui.QLabel(self.centralwidget)
        self.textView.setGeometry(QtCore.QRect(50, 440, 691, 21))
        self.textView.setObjectName(_fromUtf8("label"))
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(mainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)

        # my click function
        self.src_button.clicked.connect(self.on_openfile_clicked)
        self.dir_button.clicked.connect(self.on_opendir_clicked)
        self.run_button.clicked.connect(self.on_run_clicked)

        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(_translate("mainWindow", "图片墙工具", None))
        self.src_button.setText(_translate("mainWindow", "选择源图片", None))
        self.dir_button.setText(_translate("mainWindow", "选择小图片文件夹", None))
        self.run_button.setText(_translate("mainWindow", "处理", None))
        self.save_button.setText(_translate("mainWindow", "保存", None))
        self.textView.setText(_translate("mainWindow", "info", None))

    def on_openfile_clicked(self):
        dlg = QtGui.QFileDialog(self)
        self.src_filename = dlg.getOpenFileName(self, 'open picture', '', 'Image files (*.jpg *.gif *.png)')
        if self.src_filename == "":
            return
        pic_src = QtGui.QPixmap(self.src_filename)
        pic_src = pic_src.scaledToHeight(400)
        pic_src = pic_src.scaledToWidth(300)
        self.picLabel_src.setPixmap(pic_src)
        print self.src_filename
        self.textView.setText(_translate("mainWindow", "打开图片"+self.src_filename, None))
        self.dir_button.setEnabled(True)

    def on_opendir_clicked(self):
        dlg = QtGui.QFileDialog(self)
        self.dst_filedir = dlg.getExistingDirectory()
        if self.dst_filedir == "":
            return
        print self.dst_filedir
        self.textView.setText(_translate("mainWindow", "加载文件夹"+self.dst_filedir, None))
        self.run_button.setEnabled(True)

    def on_run_clicked(self):
        from buildPicWorkThread import buildPicWorkThread
        self.bpthread = buildPicWorkThread(self.src_filename, self.dst_filedir)
        self.bpthread.progressBarSignal.connect(self.setProgressBar)
        self.bpthread.infoTextSignal.connect(self.setInfoText)
        self.bpthread.finalSignal.connect(self.show_result_picture)
        self.bpthread.disableBtnSignal.connect(self.set_btn_disable)
        print 'before start'
        self.bpthread.start()

    def show_result_picture(self):
        self.src_button.setEnabled(True)
        self.save_button.setEnabled(True)
        pic_tmp = QtGui.QPixmap('result.jpg')
        pic_tmp = pic_tmp.scaledToHeight(400)
        pic_tmp = pic_tmp.scaledToWidth(300)
        self.picLabel_dst.setPixmap(pic_tmp)
        self.save_button.setEnabled(True)

    def set_btn_disable(self):
        self.src_button.setDisabled(True)
        self.dir_button.setDisabled(True)
        self.run_button.setDisabled(True)
        self.save_button.setDisabled(True)

    def setProgressBar(self, value):
        self.progressBar.setProperty("value", value)

    def setInfoText(self, value):
        self.textView.setText(_translate("mainWindow", value, None))



