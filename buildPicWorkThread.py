# encoding: utf-8

"""
@author: ouwj
@file: buildPicWorkThread.py
@time: 2016/11/3 22:00
"""

from PyQt4 import QtCore
from buildPicWithPic import *
from buildPicWidget import *


class buildPicWorkThread(QtCore.QThread):
    # 声明一个信号，同时返回一个list，同理什么都能返回啦
    progressBarSignal = QtCore.pyqtSignal(int)
    infoTextSignal = QtCore.pyqtSignal(str)
    disableBtnSignal = QtCore.pyqtSignal()
    finalSignal = QtCore.pyqtSignal()

    # 构造函数里增加形参
    def __init__(self, src_filename, dst_filedir, parent=None):
        super(buildPicWorkThread, self).__init__(parent)
        self.src_filename = src_filename
        self.dst_filedir = dst_filedir

    # 重写 run() 函数，在里面干大事。
    def run(self):
        self.disableBtnSignal.emit()
        builder = BuildPicWithPic()
        print 'src picture loading...'
        self.progressBarSignal.emit(10)
        self.infoTextSignal.emit('src picture loading...')
        src_pic_path = unicode(self.src_filename.toUtf8(), 'utf-8', 'ignore')
        src_arr = builder.load_picture(src_pic_path, new_w=3000, new_h=4000)
        print 'preprocessing...'
        self.progressBarSignal.emit(40)
        self.infoTextSignal.emit('preprocessing...')
        dst_pic_dir = unicode(self.dst_filedir.toUtf8(), 'utf-8', 'ignore')
        builder.preprocess_dir(dst_pic_dir)
        dst_arrs = []
        print 'dst picture loading...'
        self.progressBarSignal.emit(60)
        self.infoTextSignal.emit('dst picture loading...')
        pic_paths = os.listdir(builder.TMP_DIR)
        for pic_path in pic_paths:
            dst_arr = builder.load_picture(builder.TMP_DIR + '\\' + pic_path)
            dst_arrs.append(dst_arr)
        print 'picture building...'
        self.progressBarSignal.emit(80)
        self.infoTextSignal.emit('picture building...')
        result_arr = builder.build_picture(src_arr, dst_arrs)
        alpha = 0.8
        beta = 1 - alpha
        result_arr = alpha * result_arr + beta * src_arr
        print 'picture saving...'
        self.progressBarSignal.emit(100)
        self.infoTextSignal.emit('picture saving...')
        result_arr = result_arr.astype('uint8')
        result_pic = Image.fromarray(result_arr)
        result_pic.save('result.jpg', 'jpeg')
        self.finalSignal.emit()
