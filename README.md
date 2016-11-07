# buildPicWithPic
auto build big picture with small pictures.


依赖库：
	pyqt4
	PIL
	numpy

main.py是程序入口，运行可看到图形界面。
buildPicWithPic.py是算法文件，实现了small pictures构成big picture的算法。
buildPicWidget.py是图形界面文件，实现了main的图形界面。
buildPicWorkThread.py是界面子线程文件，用以后台运行算法。

建议，small pictures的数量最好超过500张