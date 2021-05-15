import sys
import os
from PyQt5 import QtCore
from PyQt5.Qt import *


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        # 获取系统所有文件
        self.model01 = QFileSystemModel()
        # 进行筛选只显示文件夹，不显示文件和特色文件
        #self.model01.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
        #self.model01.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
        self.model01.setRootPath('')

        # 定义创建左边窗口
        self.treeView1 = QTreeView(self)
        self.treeView1.setModel(self.model01)
        for col in range(1, 4):
            self.treeView1.setColumnHidden(col, True)
        self.treeView1.doubleClicked.connect(self.initUI)

        # 定义创建右边窗口
        self.model02 = QStandardItemModel()
        self.treeView2 = QTreeView(self)
        self.treeView2.setModel(self.model02)

        # 将创建的窗口进行添加
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.treeView1)
        self.layout.addWidget(self.treeView2)
        self.setLayout(self.layout)

    def initUI(self, Qmodelidx):
        # 每次点击清空右边窗口数据
        self.model02.clear()
        # 定义一个数组存储路径下的所有文件
        PathData = []
        # 获取双击后的指定路径
        filePath = self.model01.filePath(Qmodelidx)
        # List窗口文件赋值
        PathDataName = self.model02.invisibleRootItem()
        # 拿到文件夹下的所有文件
        PathDataSet = os.listdir(filePath)
        # 进行将拿到的数据进行排序
        PathDataSet.sort()
        # 遍历判断拿到的文件是文件夹还是文件，Flase为文件，True为文件夹
        for Data in range(len(PathDataSet)):
            if os.path.isdir(filePath + '\\' + PathDataSet[Data]) == False:
                PathData.append(PathDataSet[Data])
            elif os.path.isdir(filePath + '\\' + PathDataSet[Data]) == True:
                print('2')
        # 将拿到的所有文件放到数组中进行右边窗口赋值。
        for got in range(len(PathData)):
            gosData = QStandardItem(PathData[got])
            PathDataName.setChild(got, gosData)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWidget()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())