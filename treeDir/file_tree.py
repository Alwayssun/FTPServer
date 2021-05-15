import sys
from PyQt5.QtWidgets import *
from PyQt5 import Qt, QtGui,QtCore
from PyQt5.QtCore import *
import os


class DirTree(QTreeView):
    def __init__(self, parent=None):
        super(DirTree, self).__init__(parent)
        #self.setupUi(self)
        self.setWindowTitle("File_Tree")
        #self.setGeometry(QtCore.QRect(200, 300, 800, 500))
        #self.actionfileopen.triggered.connect(self.Open_Folder)
        self.Open_Folder()

    def file_name(self,path):
        return os.listdir(path)

    def Open_Folder(self,path = 'G:\\data_sun\\ftp'):
        #path = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        self.verticalLayout_2 = QVBoxLayout(self)
        self.tree = QTreeWidget(self)
        self.verticalLayout_2.addWidget(self.tree)
        #self.tree.setGeometry(QtCore.QRect(200, 300, 800, 500))
        self.tree.setColumnCount(1)
        self.tree.setColumnWidth(0, 500)
        self.tree.setHeaderLabels(["EXPLORER"])
        self.tree.setIconSize(QtCore.QSize(25, 25))
        self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        #self.actionfileopen.triggered.connect(self.Open_Folder)

        dirs = self.file_name(path)
        print(dirs)

        fileInfo = QFileInfo(path)
        fileIcon = QFileIconProvider()
        print(fileInfo,fileIcon)
        icon = QtGui.QIcon(fileIcon.icon(fileInfo))
        root = QTreeWidgetItem(self.tree)
        root.setText(0, path.split('/')[-1])
        root.setIcon(0, QtGui.QIcon(icon))


        self.getFileType('.exe')
        child = QTreeWidgetItem(root)
        child.setText(0, 'hello')
        child.setIcon(0, QtGui.QIcon(self.getIcon()))
        QApplication.processEvents()

    def getIcon(self,extension='file'):
        provider = QFileIconProvider()
        tmpFile = QtCore.QTemporaryFile('./_aa'+extension);
        tmpFile.setAutoRemove(False);
        icon = provider.icon(QFileInfo('./_aa'+extension))
        if extension == 'file':
            fileInfo = QFileInfo("C:\\Users")
            fileIcon = QFileIconProvider()
            #print(fileInfo, fileIcon)
            icon = QtGui.QIcon(fileIcon.icon(fileInfo))
            return icon
        return icon

    def getFileType(self,extension):
        provider = QFileIconProvider()
        tmpFile = QtCore.QTemporaryFile('./_aa'+extension);
        tmpFile.setAutoRemove(False);
        icon = provider.icon(QFileInfo('./_aa'+extension))
        strType = provider.type(QFileInfo(tmpFile.fileName()));
        print(strType)
        return strType

    def CreateTree(self, dirs, root, path):
        for i in dirs:
            path_new = path + '\\' + i
            if os.path.isdir(path_new):
                fileInfo = Qt.QFileInfo(path_new)
                fileIcon = Qt.QFileIconProvider()
                icon = QtGui.QIcon(fileIcon.icon(fileInfo))
                child = QTreeWidgetItem(root)
                child.setText(0, i)
                child.setIcon(0, QtGui.QIcon(icon))
                dirs_new = self.file_name(path_new)
                self.CreateTree(dirs_new, child, path_new)
            else:
                fileInfo = Qt.QFileInfo(path_new)
                fileIcon = Qt.QFileIconProvider()
                icon = QtGui.QIcon(fileIcon.icon(fileInfo))
                child = QTreeWidgetItem(root)
                child.setText(0, i)
                child.setIcon(0, QtGui.QIcon(icon))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DirTree()
    win.show()
    sys.exit(app.exec_())