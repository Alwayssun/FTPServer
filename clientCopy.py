# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clientUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog,width,heigth):
        Dialog.setObjectName("Dialog")
        Dialog.resize(width,heigth)
        Dialog.setWindowOpacity(1.0)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout.addWidget(self.lineEdit_3)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout.addWidget(self.lineEdit_4)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.toolButton = QtWidgets.QToolButton(Dialog)
        self.toolButton.setWhatsThis("")
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 8)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 8)
        self.horizontalLayout.setStretch(4, 1)
        self.horizontalLayout.setStretch(5, 8)
        self.horizontalLayout.setStretch(6, 1)
        self.horizontalLayout.setStretch(7, 1)
        self.horizontalLayout.setStretch(8, 3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.lineEdit_5 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.horizontalLayout_4.addWidget(self.lineEdit_5)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.lineEdit_6 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.horizontalLayout_4.addWidget(self.lineEdit_6)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.treeView = QtWidgets.QTreeView(Dialog)
        self.treeView.setObjectName("treeView")
        self.horizontalLayout_2.addWidget(self.treeView)
        self.treeView_2 = QtWidgets.QTreeView(Dialog)
        self.treeView_2.setObjectName("treeView_2")
        self.horizontalLayout_2.addWidget(self.treeView_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.treeView_3 = QtWidgets.QTreeView(Dialog)
        self.treeView_3.setObjectName("treeView_3")
        self.horizontalLayout_3.addWidget(self.treeView_3)
        self.treeView_4 = QtWidgets.QTreeView(Dialog)
        self.treeView_4.setObjectName("treeView_4")
        self.horizontalLayout_3.addWidget(self.treeView_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 3)
        self.verticalLayout_2.setStretch(2, 6)
        self.verticalLayout_2.setStretch(3, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "FTP文件传输客户端-孙郑义"))
        self.label.setText(_translate("Dialog", "主机(H):"))
        self.lineEdit.setText(_translate("Dialog", "192.168.0.102"))
        self.label_2.setText(_translate("Dialog", "用户名(U):"))
        self.lineEdit_2.setText(_translate("Dialog", "softwares_sun"))
        self.label_3.setText(_translate("Dialog", "密码"))
        self.lineEdit_3.setText(_translate("Dialog", "12345"))
        self.label_4.setText(_translate("Dialog", "端口"))
        self.lineEdit_4.setText(_translate("Dialog", "21"))
        self.pushButton.setText(_translate("Dialog", "快速连接"))
        self.toolButton.setText(_translate("Dialog", "..."))
        self.label_5.setText(_translate("Dialog", "本地站点"))
        self.label_6.setText(_translate("Dialog", "远程站点"))
