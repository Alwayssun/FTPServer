# -*- coding: utf-8 -*-

'''
Author:AlwaysSun
Time:2021-05-08
function:实现FTP客户端GUI界面
思路：分成两个类 一个负责ftp的处理（FTPClient） 另一个负责点击事件和文件系统的响应和更新（FTPUI）
特色代码：文件系统的实现（通过自建多叉树实现文件系统， 同时运用PYQT实现文件系统的显示）具体包括按照文件名 获取系统的默认图标 文件树的建立和显示的对应'''

__all__ = ['FTPUI','FTPClient']

from PyQt5.Qt import *
import sys
from clientUi import Ui_Dialog
from ftplib import FTP
from treelib import Tree
from PyQt5 import QtCore
from PyQt5.QtCore import  pyqtSignal
from PyQt5 import QtWidgets
import time,os,datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class FTPClient(QtWidgets.QLabel):
    """
    FTP 连接类
    """
    _signal = pyqtSignal(str)

    def __del__(self):
        """
        退出时执行ftp断开
        :return: 
        """
        print("connect close")
        self.ftp.close()
        #self._signal.emit('Del')

    def __init__(self, host:str, username:str, password:str, port = '21'):
        """
        初始化 FTP 输入主机 端口用户名密码 之后连接FTP服务器
        :param host: 主机
        :param username: 用户名
        :param password: 密码
        :param port: 端口
        """
        print("init")
        super(FTPClient, self).__init__()
        self.host = host
        self.port = int(port)
        self.username = username
        self.password = password
    def startConnect(self):
        """
        建立FTP连接
        :return: 
        """
        self.nowDirName = 'root'
        #建立文件树 和根节点
        self.tree = Tree()
        itemProject = QStandardItem('root')
        itemProject.setIcon(self.getIcon())
        self.tree.create_node('root','root',parent=None,data =itemProject)
        # 连接FTP 连接成功之后 创建root的子目录
        self.ftp_connect()
        self.createTree(self.ftp.nlst(),'root')
        #print('pwd',self.ftp.pwd())
        # 以下注释部分完成了 在ftp上文件系统内部的跳转 和列出文件系统
        #print('cwd0428',self.ftp.cwd('0428'))
        #print('nlst',self.ftp.nlst())
        #print('pwd',self.ftp.pwd())
        #print('cwd0428', self.ftp.cwd('Laser'))
        #print('nlst', self.ftp.nlst())
        #print('pwd', self.ftp.pwd())
        #self.createTree(self.ftp.nlst(), 'root/0428')
        self.tree.show()
        self._signal.emit("OK");  # 信号发送
        #print("EMIT OK")
        #print(self.tree.children('root'))
        #self.download_file('/readme.txt','G:/data_sun/readme.txt')
    def restartTree(self):
        print("刷新树")
        self.tree.remove_subtree('root')
        itemProject = QStandardItem('root')
        itemProject.setIcon(self.getIcon())
        self.tree.create_node('root', 'root', parent=None, data=itemProject)
        self.ftp.cwd('/')
        self.createTree(self.ftp.nlst(), 'root')


    def createTree(self, chiledList:list , parent:str)->bool:
        """
        通过输入的 子目录列表 和父目录的名称 进行建立文件树
        :param chiledList: 下一层目录所有的文件列表
        :param parent: 父路径名字
        :return: 是否创建了子树 0创建失败 1创建成功
        """
        if self.tree.subtree(parent).depth() == 0:#当前子树深度 为0  那么说明还没有刷新该节点
            print("叶节点,开始创建文件子树")
        else:
            print("不是叶节点")
            return 0
        #按照列表内部的数据 依此建树  树的名称均为 父路径 + / + 当前文件名称（主要为了实现唯一标识 不然不同文件夹下相同的文件名 就会出错）
        for i in chiledList:
            itemProject = QStandardItem((parent+'/'+i))
            #print((parent+'/'+i),(parent+'/'+i).split('.'))
            if len((parent+'/'+i).split('.')) == 1:#如果是文件夹 那么获取系统的文件夹的图标
                itemProject.setIcon(self.getIcon())
            else:
                itemProject.setIcon(self.getIcon('.'+(parent+'/'+i).split('.')[-1]))
            self.tree.create_node(parent+'/'+i.encode('utf-8').decode('utf-8'), parent+'/'+i.encode('utf-8').decode('utf-8'),parent=parent,data = itemProject)  # 根节点
        return 1
    def ftp_connect(self):
        """
        FTP的具体连接类
        :return: None
        """
        self.ftp = FTP()
        # ftp.set_debuglevel(2)
        #连接主机
        self.ftp.connect(self.host, self.port)
        #实现登录
        self.ftp.login(self.username, self.password)
        self.ftp.encoding = 'utf-8'
        print("log in success")

    def getIcon(self,extension='file'):
        """
        获取扩展名在操作系统下的默认图标
        :param extension: 文件扩展名 如果不写默认为是文件
        :return: 对应的图标
        """
        provider = QFileIconProvider()
        tmpFile = QTemporaryFile('./_aa'+extension);
        tmpFile.setAutoRemove(False);
        icon = provider.icon(QFileInfo('./_aa'+extension))
        if extension == 'file':
            # 首先生成一个临时文件 之后获取临时文件的图标返回
            fileInfo = QFileInfo("C:\\Users")
            fileIcon = QFileIconProvider()
            #print(fileInfo, fileIcon)
            icon = QIcon(fileIcon.icon(fileInfo))
            return icon
        return icon

    def download_file(self, remotepath:str, localpath:str):
        """
        从远程FTP服务器下载文件 到本地路径
        :param remotepath: 远端路径
        :param localpath: 本地路径
        :return: None
        """
        remotepath = remotepath.replace('//','/')
        localpath = localpath.replace('//','/')
        if os.path.isdir(remotepath) or len(remotepath.split('.')) == 1:#是文件夹
            self.download_dir(remotepath, localpath)
            return
        print("是文件")
        bufsize = 1024
        fp = open(localpath, 'wb')
        self.ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
        self.ftp.set_debuglevel(0)
        fp.close()
        print("下载远程文件：",remotepath,"\t到本地路径：",localpath,"成功")

    def download_dir(self,remotedir:str, localdir:str):
        """
        下载远程的文件夹到本地文件夹 
        例如 download_dir('/test','G:/ftpdata/test10') 或者download_dir('test','G:/ftpdata/test10')
        后面这个会新建一个test文档  之前那个新建/test会报错 因此就不会创建
        :param remotedir: 远程文件夹
        :param localdir: 本地文件夹
        :return: 
        """
        try:
            os.makedirs(localdir)  # 由于我之前的处理是 将文件夹直接加到了 本地连接的后面 所以需要先新建一个文件夹
        except OSError:
            print("本地文件已经存在，不进行新建")
            pass

        print("开始下载文件夹：从 ",remotedir," 到 ",localdir)
        os.chdir(localdir)
        self.walk(remotedir, localdir)
        print("文件夹下载结束")
    def get_dirs_files(self):
        """
        获取当前目录的文件夹和文件 
        :return: （当前目录下的文件，当前目录下的文件夹）
        """
        dir_res = []
        self.ftp.dir('.', dir_res.append)
        files = [f.split(None, 8)[-1] for f in dir_res if f.startswith('-')]
        dirs = [f.split(None, 8)[-1] for f in dir_res if f.startswith('d')]
        return (files, dirs)

    def walk(self, remotedir, localdir):
        """
        在文件夹内部递归 单个传递每一个文件 直到文件夹内部文件全部传递完毕
        :param remotedir: 远程文件夹
        :param localdir: 本地文件夹
        :return: 
        """
        print('Walking to', remotedir,os.getcwd())
        self.ftp.cwd(remotedir)
        try:
            os.mkdir(remotedir)
        except OSError:
            print("创建文件夹失败，文件夹可能已经存在")
            pass
        os.chdir(localdir)
        print("now dir", os.getcwd())
        ftp_curr_dir = self.ftp.pwd()

        print("local dir",localdir)
        files, dirs = self.get_dirs_files()
        print("FILES: ", files)
        print("DIRS: ", dirs)
        for f in files:
            print(remotedir, ':', f)
            outf = open(f, 'wb')
            try:
                self.ftp.retrbinary('RETR %s' % f, outf.write)
            finally:
                outf.close()
        for d in dirs:
            print("Dir:",d,ftp_curr_dir)
            os.chdir(localdir)
            #self.ftp.cwd(ftp_curr_dir)
            self.walk(d,os.path.join(localdir,d))
        self.ftp.cwd('..')#不加这句的话  只能递归一层 之后会出错

    def uploadFile(self, remotepath='./',localpath = './'):
        print("Upload",localpath,remotepath,os.path.isfile(localpath))
        if not os.path.isfile(localpath):
            return
        print('+++ upload %s to %s' % (localpath, remotepath))
        self.ftp.storbinary('STOR ' + remotepath, open(localpath, 'rb'))


    def upload_dir(self, remotedir='./', localdir='./'):
        '''
        实现文件的上传
        :param localdir: 
        :param remotedir: 
        :return: 
        '''
        if not os.path.isdir(localdir):
            return
        print("Upload dir",remotedir,localdir)
        try:
            self.ftp.cwd(remotedir)
        except:
            self.ftp.mkd(remotedir)
            self.ftp.cwd(remotedir)
            print("远程文件夹创建成功")
        for file in os.listdir(localdir):
            # src = os.path.join(localdir, file)
            src = localdir+'/'+file
            print(src)
            if os.path.isfile(src):
                print("is file")
                self.uploadFile(file,src)
            elif os.path.isdir(src):
                try:
                    self.ftp.mkd(file)
                except:
                    sys.stderr.write('the dir is exists %s' % file)
                self.upload_dir(file,src)
        self.ftp.cwd('..')

    def upload_file(self, remotepath:str, localpath:str):
        """
        上传本地文件到服务器
        :param remotepath:  远端路径
        :param localpath:  本地路径
        :return: None
        """
        while  '//' in remotepath:
            remotepath = remotepath.replace('//', '/')
        while '//' in localpath:
            localpath = localpath.replace('//', '/')
        print(remotepath,localpath)
        if os.path.isdir(remotepath) or len(remotepath.split('.')) == 1:#是文件夹
            self.upload_dir(remotepath, localpath)
            return

        bufsize = 1024
        fp = open(localpath, 'rb')
        self.ftp.storbinary('STOR ' + remotepath, fp, bufsize)
        self.ftp.set_debuglevel(0)
        fp.close()
        print("上传本地文件：", localpath, "\t到远程：",remotepath , "成功")

class FTPUI(QWidget,Ui_Dialog):
    """
    实现具体的UI界面
    """
    def __init__(self):
        """
        界面初始化
        """
        desktop = QApplication.desktop()
        width = desktop.width()
        height = desktop.height()
        super(FTPUI, self).__init__()
        #参数初始化 长宽均设置为屏幕的一半
        self.setupUi(self,width//2,height//2)
        self.host = ""
        self.port = ""
        self.userName = ""
        self.password = ""
        self.serverChoseFileName = ""
        self.clientChoseFileName = ""
        self.ftpStatue = False #ftp是否已经连接
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        #客户端边的 文件夹显示
        self.modelClientAllDirs = QFileSystemModel()#文件夹显示
        self.modelClientAllDirs.setFilter(QDir.Dirs | QDir.NoDotAndDotDot)#只显示文件夹
        self.modelClientAllDirs.setRootPath('C:/')
        self.treeView.setModel(self.modelClientAllDirs)
        self.treeView.setRootIndex(self.modelClientAllDirs.index(''))
        #客户端的  所有文件显示
        self.modelClientFiles = QFileSystemModel()  # 显示文件和文件夹
        self.treeView_3.setModel(self.modelClientFiles)

        #服务器端的 所有文件夹显示
        self.modelServerAllDirs = QStandardItemModel()
        self.serverModelAllDirsFilesInit()



        self.clientChoseFileName  = ''
        self.serverChoseFileName = ''
        self.lineEdit_5.setText('')
        self.lineEdit_6.setText('')



        # 最下方的状态显示
        self.stateModel = QStandardItemModel()
        self.stateModel.setHorizontalHeaderLabels(['时间', '本地文件','方向', '远程/服务器文件'])
        # #水平方向，表格大小拓展到适当的尺寸
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setShowGrid(False)
        self.tableView.setAlternatingRowColors(True)
        #self.tableView.setTextAlignment(1)
        self.tableView.setModel(self.stateModel)



        #槽函数 连接
        self.treeView.clicked.connect(self.clientSetFiles)
        self.treeView_2.clicked.connect(self.serverDirList)
        self.treeView_2.doubleClicked.connect(self.downloadFile)
        self.treeView_2.selectionModel().currentChanged.connect(self.onServerCurrentChanged)
        self.treeView_3.clicked.connect(self.clientFilesChoice)
        self.treeView_3.doubleClicked.connect(self.uploadFile)
        self.pushButton.clicked.connect(self.connectBtnClicked)
        self.pushButton_2.clicked.connect(self.rushTree)#刷新按键

    def rushTree(self):
        if self.ftpStatue:
            self.ftpClient.restartTree()
            self.modelServerAllDirs.clear()
            self.updateServerTree('root')
        else:
            QMessageBox.warning(self, "警告", "未连接任何的服务器")
    def getNowTime(self):
        return datetime.datetime.now().strftime('%H:%M:%S')
    def stateBarShow(self,remoteDir,localDir,direction):
        str = '--->' if direction == 'UP' else '<---'
        #self.stateBarOutput("本地文件 "+localDir+"\t"+str+"\t远程文件 "+remoteDir)
        timeR = QStandardItem(self.getNowTime())
        localR = QStandardItem(localDir)
        strR = QStandardItem(str)
        remoteR = QStandardItem(remoteDir)
        timeR.setTextAlignment(QtCore.Qt.AlignCenter)
        localR.setTextAlignment(QtCore.Qt.AlignCenter)
        strR.setTextAlignment(QtCore.Qt.AlignCenter)
        remoteR.setTextAlignment(QtCore.Qt.AlignCenter)
        self.stateModel.appendRow([timeR,localR,strR ,remoteR])

    # def stateBarOutput(self,str_my):
    #     """
    #     状态栏输出，先显示时间 之后显示内容
    #     :param str_my: 需要显示的内容
    #     :return: None
    #     """
    #     #self.textEdit.append(self.getNowTime() +":\t"+ str_my)
    #     QApplication.processEvents()
    def uploadFile(self,Qmodelidx):
        """
        双击客户端实现文件上传
        :param Qmodelidx: 
        :return: None
        """
        self.clientChoseFileName = self.modelClientFiles.filePath(Qmodelidx)
        #print("client double click", Qmodelidx)
        # filePath = Qmodelidx.data()
        # # print(filePath,Qmodelidx.index(),Qmodelidx.parent(),Qmodelidx.columnCount())
        # print(filePath, Qmodelidx.parent().data(), Qmodelidx.row(), Qmodelidx.column())
        # self.clientChoseFileName = filePath

        if not self.ftpStatue:
            QMessageBox.warning(self,"警告","未连接任何的服务器")
            print("未连接任何的服务器")
        else:
            if os.path.isfile(self.serverChoseFileName) or len(self.serverChoseFileName.split('.')) > 1:
                print("服务端选择的是文件")
                self.serverChoseFileName = self.getHeadStr(self.serverChoseFileName)  # 字符串如果是文件的话  选择文件的父路径
            else:
                print("服务端选择的是文件夹")
            print("start upload: from ", self.clientChoseFileName, ' to ',self.serverChoseFileName + '/' + self.clientChoseFileName.split('/')[-1])
            self.ftpClient.upload_file(self.serverChoseFileName+'/'+self.clientChoseFileName.split('/')[-1],  self.clientChoseFileName)
            self.stateBarShow(self.serverChoseFileName+'/'+self.clientChoseFileName.split('/')[-1],  self.clientChoseFileName,"UP")

    def downloadFile(self,Qmodelidx):
        """
        服务器双击实现下载
        :param Qmodelidx: 
        :return: 
        """
        #print("server double click", Qmodelidx)
        filePath = Qmodelidx.data()
        # print(filePath,Qmodelidx.index(),Qmodelidx.parent(),Qmodelidx.columnCount())
        #print(filePath, Qmodelidx.parent().data(), Qmodelidx.row(), Qmodelidx.column())
        self.serverChoseFileName = filePath[4:]
        #print(self.ftpClient)
        if not self.ftpStatue:
            QMessageBox.warning(self, "警告", "未连接任何的服务器")
            print("未连接任何的服务器")
        else:
            if os.path.isfile(self.clientChoseFileName):
                print("客户端选择的是文件")
                self.clientChoseFileName = self.getHeadStr(self.clientChoseFileName)  # 字符串如果是文件的话  选择文件的父路径
            else:
                print("客户端选择的是文件夹")

            print("start download: from ", self.serverChoseFileName, ' to ',self.clientChoseFileName + '/' + self.serverChoseFileName.split('/')[-1])
            self.ftpClient.download_file(self.serverChoseFileName,self.clientChoseFileName+'/'+self.serverChoseFileName.split('/')[-1])
            self.stateBarShow(self.serverChoseFileName,self.clientChoseFileName+'/'+self.serverChoseFileName.split('/')[-1], "DOWN")
        #self.download_file('/readme.txt','G:/data_sun/readme.txt')
    def getHeadStr(self,str:str) ->str :#'root/0428'
        """
        获取字符串以 \分割 除了尾部之外的字符串
        :param str: 输入的字符串
        :return: 分割结束 返回的字符串
        """
        strSplit = str.split('/')
        returnStr = ''
        if len(strSplit) <= 1:
            return ""
        for m in range(len(strSplit)-1):
            if m == len(strSplit)-2:
                returnStr += strSplit[m]
            else:
                returnStr += strSplit[m]+'/'
        #print('returnStr',returnStr)
        return returnStr

    def updateServerTree(self,rootName):
        """
        更新服务器部分的文件夹显示
        :return: None
        """
        #print("preOreder", self.ftpClient.tree.get_node('root'))

        self.preOrderTree(self.ftpClient.tree.get_node(rootName))

        #self.modelServerAllDirs.clear()
        self.modelServerAllDirs.setHorizontalHeaderLabels(['Name'])
        self.modelServerAllDirs.appendRow(self.ftpClient.tree.get_node(rootName).data)
        self.treeView_2.setModel(self.modelServerAllDirs)


    def preOrderTree(self,root):
        """
        前序遍历建树
        :param root: 当前入口节点
        :return: None
        """
        #print(self.ftpClient.tree.__getitem__(root))
        #print(self.ftpClient.tree.children(root.tag))
        if root == None:
            return
        elif len(self.ftpClient.tree.children(root.tag)) == 0:#没有子树
            return self.ftpClient.tree.__getitem__(root.tag).data
        else:
            for m in self.ftpClient.tree.children(root.tag):
                #print(m.data)
                a = self.preOrderTree(m)
                if a!=None:
                    root.data.appendRow(a)
                else:
                    root.data.appendRow(m.data)

    def serverModelAllDirsFilesInit(self):
        """
        初始化 服务器文件的显示
        :return: 
        """
        self.modelServerAllDirs.setHorizontalHeaderLabels(['Name'])
        self.treeView_2.setModel(self.modelServerAllDirs)
        self.treeView_2.setStyle(QStyleFactory.create('windows'))


    def getIcon(self,extension='file'):
        """
        获取输入后缀在系统中默认的图标
        :param extension: 后缀str
        :return: None
        """
        provider = QFileIconProvider()
        tmpFile = QTemporaryFile('./_aa'+extension);
        tmpFile.setAutoRemove(False);
        icon = provider.icon(QFileInfo('./_aa'+extension))
        if extension == 'file':
            fileInfo = QFileInfo("C:\\Users")
            fileIcon = QFileIconProvider()
            #print(fileInfo, fileIcon)
            icon = QIcon(fileIcon.icon(fileInfo))
            return icon
        return icon

    def clientFilesChoice(self,Qmodelidx):
        """
        客户端文件目录点击  选择的文件
        :param Qmodelidx: 
        :return: 
        """
        self.clientChoseFileName = self.modelClientFiles.filePath(Qmodelidx)
        if os.path.isfile(self.clientChoseFileName):
            print("客户端选择的是文件")
            self.clientChoseFileName = self.getHeadStr(self.clientChoseFileName)# 字符串如果是文件的话  选择文件的父路径
        else:
            print("客户端选择的是文件夹")
        self.lineEdit_5.setText(self.clientChoseFileName)

    def connectOk(self,str):
        """
        收到连接成功的ok信号 开始更新服务端的文件列表
        :param str: 接收的信号 
        :return: 
        """
        #print("connect5555",str)
        if str == "OK":
            #self.stateBarOutput("FTP服务器(%s)连接成功"%self.host)
            self.setWindowTitle(self.userName+'@'+self.host+':'+self.port+' '+self.windowTitle())
            self.ftpStatue = True
            self.updateServerTree('root')
            self.serverChoseFileName = '/'
            self.lineEdit_6.setText('/')
        elif str =="Del":
            #self.stateBarOutput("FTP服务器(%s)已断开" % self.host)
            self.setWindowTitle(self.windowTitle().split(' ')[-1])

    def connectBtnClicked(self):
        """
        快速连接按键按下 进行ftp的连接
        :return: None
        """
        self.host = self.lineEdit.text()
        self.port = self.lineEdit_4.text()
        self.userName = self.lineEdit_2.text()
        self.password = self.lineEdit_3.text()
        self.ftpClient = FTPClient(self.host,self.userName,self.password,self.port)
        self.ftpClient._signal.connect(self.connectOk)
        self.ftpClient.startConnect()

    def serverDirList(self,Qmodelidx):
        """
        服务器端选择目标文件
        :param Qmodelidx: 
        :return: 
        """
        #self.updateServerTree()
        filePath = Qmodelidx.data()
        #print(filePath,Qmodelidx.parent().data(),Qmodelidx.row(),Qmodelidx.column())
        self.serverChoseFileName = filePath[4:]
        if self.serverChoseFileName =='':
            self.serverChoseFileName = '/'
        if os.path.isfile(self.serverChoseFileName):
            self.serverChoseFileName = self.getHeadStr(self.serverChoseFileName)# 字符串如果是文件的话  选择文件的父路径
        self.lineEdit_6.setText(self.serverChoseFileName)
        if len(filePath.split('.')) == 1:#是文件的话才要 进行具体目录的获取
            print("切换目录",filePath)
            self.ftpClient.ftp.cwd('/')
            for m in filePath.split('/')[1:]:
                print(m,self.ftpClient.ftp.pwd())
                self.ftpClient.ftp.cwd(m)
            #self.ftpClient.ftp.cwd(filePath.split('/')[-1])
            if self.ftpClient.createTree(self.ftpClient.ftp.nlst(),filePath):
                self.ftpClient.tree.show()
                self.updateServerTree(filePath)

    def clientSetFiles(self,Qmodelidx):
        """
        显示 客户端的具体文件
        :param Qmodelidx: 
        :return: 
        """
        filePath = self.modelClientAllDirs.filePath(Qmodelidx)
        self.modelClientFiles.setRootPath(filePath)
        #self.modelClientFiles.setRootPath(filePath)

        self.clientChoseFileName = self.modelClientFiles.filePath(Qmodelidx)
        self.lineEdit_5.setText(self.clientChoseFileName)

        self.treeView_3.setRootIndex(self.modelClientFiles.index(filePath))


    def onServerCurrentChanged(self, current,previous):
        """
        服务器部分 点击的文件改变了
        :param current: 
        :param previous: 
        :return: 
        """
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FTPUI()
    ex.show()
    sys.exit(app.exec_())